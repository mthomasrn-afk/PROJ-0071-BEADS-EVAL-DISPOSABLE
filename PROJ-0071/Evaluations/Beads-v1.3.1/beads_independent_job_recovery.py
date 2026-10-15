#!/usr/bin/env python3
"""CP09: synthetic cross-GitHub-job issue-level Beads recovery; NOT a product acceptance tool."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cp08_fixture", ROOT / "beads_h3_pcr_comparison.py")
cp08 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp08)
TASKS = ("S100", "S110", "S120", "S130", "S140")

def check_snapshot(raw, expected_sha, authority):
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise cp08.Blocked("BLOCKED_HANDOFF_DIGEST_MISMATCH")
    try:
        rows = [json.loads(s) for s in raw.decode("utf-8").splitlines() if s.strip()]
    except (UnicodeError, ValueError) as exc:
        raise cp08.Blocked("BLOCKED_HANDOFF_JSONL_INVALID") from exc
    expected_titles = {"CP08 synthetic " + t for t in TASKS}
    if len(rows) != len(TASKS) or {r.get("title") for r in rows} != expected_titles:
        raise cp08.Blocked("BLOCKED_HANDOFF_ISSUE_SET")
    if any(not isinstance(r.get("id"), str) or not r["id"] for r in rows):
        raise cp08.Blocked("BLOCKED_HANDOFF_MISSING_ID")
    mapping = {r["title"].split()[-1]: r["id"] for r in rows}
    if len(set(mapping.values())) != len(TASKS):
        raise cp08.Blocked("BLOCKED_HANDOFF_DUPLICATE_ID")
    by_task = {r["title"].split()[-1]: r for r in rows}
    for task, row in by_task.items():
        expected_deps = {mapping[t] for t in authority["pcr"][task]["deps"]}
        dependencies = row.get("dependencies", [])
        got_deps = {d.get("depends_on_id") for d in dependencies if d.get("type") in ("blocks", None)}
        if got_deps != expected_deps:
            raise cp08.Blocked("BLOCKED_HANDOFF_DEPENDENCIES_" + task)
        expected_closed = task in authority["h3"]["completed"]
        if (row.get("status") == "closed") != expected_closed:
            raise cp08.Blocked("BLOCKED_HANDOFF_ACCEPTED_STATE_" + task)
    return mapping

def phase_seed(archive, workspace, transport):
    cp08.seed(archive, workspace, "normal")
    bd, project, env = cp08.context(archive, workspace)
    data = cp08.cold.call(bd, project, env, "export").encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    authority = cp08.read_authority()
    mapping = check_snapshot(data, sha, authority)
    transport.write_bytes(data)
    result = {"phase": "SEED_JOB", "snapshot_sha256": sha, "issue_count": len(mapping),
              "source_sha256": hashlib.sha256(cp08.FROZEN.read_bytes()).hexdigest(),
              "job": os.environ.get("GITHUB_JOB", "UNKNOWN"),
              "run_id": os.environ.get("GITHUB_RUN_ID", "UNKNOWN"),
              "disposition": "CANDIDATE_ONLY", "qualified": False}
    print("CP09_RESULT " + json.dumps(result, sort_keys=True))
    return 0

def phase_restore(archive, workspace, transport, source_sha, handoff_sha):
    authority = cp08.read_authority()
    if source_sha != hashlib.sha256(cp08.FROZEN.read_bytes()).hexdigest():
        raise cp08.Blocked("BLOCKED_AUTHORITY_SOURCE_CHANGED")
    if not transport.is_file():
        raise cp08.Blocked("BLOCKED_HANDOFF_ABSENT")
    data = transport.read_bytes()
    mapping = check_snapshot(data, handoff_sha, authority)
    if workspace.exists():
        raise cp08.Blocked("BLOCKED_EXISTING_RESTORE_WORKSPACE")
    workspace.mkdir(parents=True)
    bd, project, env = cp08.context(archive, workspace)
    cp08.cold.call(bd, project, env, "init", "--stealth", "--skip-agents", "--skip-hooks", "--non-interactive")
    cp08.cold.call(bd, project, env, "import", str(transport))
    ready = cp08.cold.ready(cp08.cold.call(bd, project, env, "ready", "--json"))
    expected = {mapping["S120"], mapping["S140"]}
    if ready != expected:
        raise cp08.Blocked("BLOCKED_RESTORED_GRAPH_DIFFERS")
    if mapping["S130"] in ready or mapping["S100"] in ready or mapping["S110"] in ready:
        raise cp08.Blocked("BLOCKED_ACCEPTED_OR_PROMOTION_VIOLATION")
    print("CP09_RESULT " + json.dumps({
        "phase": "FRESH_JOB_RESTORE", "disposition": "PASS_BOUNDARY_ONLY",
        "first_incomplete": "S120", "baseline_first_incomplete": cp08.without_beads(authority)["first_incomplete"],
        "beads_ready": ["S120", "S140"], "completed_preserved": authority["h3"]["completed"],
        "promotion_blocked": True, "matched_handoff_digest": True, "source_sha256": source_sha,
        "handoff_sha256": handoff_sha, "job": os.environ.get("GITHUB_JOB", "UNKNOWN"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "UNKNOWN"),
        "human_time_saved": "NOT_MEASURED", "qualified": False}, sort_keys=True))
    return 0

class Tests(unittest.TestCase):
    def test_missing_handoff(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(cp08.Blocked, "BLOCKED_HANDOFF_ABSENT"):
                phase_restore(None, Path(d)/"ws", Path(d)/"missing", hashlib.sha256(cp08.FROZEN.read_bytes()).hexdigest(), "unused")
    def test_changed_source(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(cp08.Blocked, "BLOCKED_AUTHORITY_SOURCE_CHANGED"):
                phase_restore(None, Path(d)/"ws", Path(d)/"missing", "wrong", "unused")
    def test_tampered_digest(self):
        authority = cp08.read_authority()
        with self.assertRaisesRegex(cp08.Blocked, "BLOCKED_HANDOFF_DIGEST_MISMATCH"):
            check_snapshot(b'{}\n', "0"*64, authority)
    def test_invalid_handshake_schema(self):
        authority = cp08.read_authority()
        content = b'{}\n'
        with self.assertRaisesRegex(cp08.Blocked, "BLOCKED_HANDOFF_ISSUE_SET"):
            check_snapshot(content, hashlib.sha256(content).hexdigest(), authority)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--phase", choices=["seed", "restore"])
    p.add_argument("--archive", type=Path)
    p.add_argument("--workspace", type=Path)
    p.add_argument("--transport", type=Path)
    p.add_argument("--source-sha")
    p.add_argument("--handoff-sha")
    a=p.parse_args()
    if a.self_test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    if not (a.phase and a.archive and a.workspace and a.transport):
        p.error("phase/archive/workspace/transport required")
    try:
        if a.phase == "seed":
            return phase_seed(a.archive,a.workspace,a.transport)
        if not (a.source_sha and a.handoff_sha):
            p.error("restore requires --source-sha and --handoff-sha")
        return phase_restore(a.archive,a.workspace,a.transport,a.source_sha,a.handoff_sha)
    except Exception as exc:
        print("CP09_RESULT " + json.dumps({"disposition":"FAIL_OR_BLOCKED", "error_code":str(exc)[:250],"class":type(exc).__name__,"qualified":False},sort_keys=True))
        return 20

if __name__=="__main__":
    sys.exit(main())
