#!/usr/bin/env python3
"""PROJ-0071: Beads 1.3.1 isolated synthetic recovery fixture (not accepted product)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest

VERSION = "1.3.1"
LINUX_ARCHIVE_SHA256 = "3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c"
WINDOWS_ARCHIVE_SHA256 = "48cd82e1d3e311c9bf9a5d6d67ad1a8542ae13d4e20c5bfb527656c5e666af76"
RELEASE_URL = "https://github.com/gastownhall/beads/releases/tag/v1.3.1"
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*-[A-Za-z0-9._-]+$")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def assert_pinned(path, expected=LINUX_ARCHIVE_SHA256):
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("PIN_FORMAT_INVALID")
    if digest(path) != expected:
        raise ValueError("PIN_MISMATCH")


def parse_issue_id(value):
    value = value.strip()
    if not ID_RE.fullmatch(value):
        raise ValueError("NO_EXPLICIT_ISSUE_ID")
    return value


def ready_ids(obj):
    if isinstance(obj, dict):
        obj = obj.get("issues", obj.get("results"))
    if not isinstance(obj, list):
        raise ValueError("READY_SCHEMA_INVALID")
    if any(not isinstance(x, dict) or not isinstance(x.get("id"), str) for x in obj):
        raise ValueError("READY_ITEM_INVALID")
    return {x["id"] for x in obj}


def pinned_version(value):
    return bool(re.search(r"(?<![\d.])v?1\.3\.1(?![\d.])", value))


def get_bd_linux(archive, directory):
    # No archive-tree extraction, tar link following, or execution before pin check.
    assert_pinned(archive)
    with tarfile.open(archive, "r:gz") as tar:
        matches = [m for m in tar if m.isfile() and Path(m.name).name == "bd"
                   and len(Path(m.name).parts) <= 3 and m.size < 350_000_000]
        if len(matches) != 1:
            raise ValueError("EXPECTED_SINGLE_BD_EXECUTABLE")
        reader = tar.extractfile(matches[0])
        if reader is None:
            raise ValueError("BD_CONTENT_UNAVAILABLE")
        bd = directory / "bd"
        with bd.open("wb") as out:
            while True:
                block = reader.read(1024 * 1024)
                if not block:
                    break
                out.write(block)
        bd.chmod(0o700)
        return bd


def run_trial(archive):
    with tempfile.TemporaryDirectory(prefix="proj0071-beads-") as base:
        root = Path(base)
        bd = get_bd_linux(archive, root)
        home = root / "home"
        home.mkdir()
        work = root / "synthetic"
        work.mkdir()
        env = os.environ.copy()
        env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
                    "GIT_CONFIG_GLOBAL": str(home / ".gitconfig"),
                    "BD_NON_INTERACTIVE": "1", "CI": "true"})
        def run(*args):
            p = subprocess.run([str(bd), *args], cwd=work, env=env, capture_output=True,
                               text=True, timeout=90)
            if p.returncode:
                raise RuntimeError("BD_COMMAND_FAILED_" + str(args[0]) + "_" + str(p.returncode))
            return p.stdout
        if not pinned_version(run("version")):
            raise ValueError("VERSION_MISMATCH")
        run("init", "--stealth", "--skip-agents", "--skip-hooks", "--non-interactive")
        verified = parse_issue_id(run("create", "Synthetic verified checkpoint", "--silent"))
        continue_task = parse_issue_id(run("create", "Synthetic continue after checkpoint", "--silent"))
        unresolved = parse_issue_id(run("create", "Synthetic unresolved acceptance", "--silent"))
        blocked = parse_issue_id(run("create", "Synthetic blocked promotion", "--silent"))
        run("dep", "add", continue_task, verified)
        run("dep", "add", blocked, unresolved)
        before = ready_ids(json.loads(run("ready", "--json")))
        if verified not in before or unresolved not in before or continue_task in before or blocked in before:
            raise ValueError("INITIAL_DEPENDENCIES_INCORRECT")
        run("close", verified, "--reason", "synthetic evidence checkpoint complete")
        # New CLI subprocesses approximate process interruption/restart.
        after = ready_ids(json.loads(run("ready", "--json")))
        if continue_task not in after or unresolved not in after or blocked in after or verified in after:
            raise ValueError("RESTART_STATE_INCORRECT")
        return {"disposition": "PASS_SYNTHETIC_RECOVERY_ONLY", "pinned_version": VERSION,
                "checks": ["VERSION_PIN", "ISOLATED_INIT", "BLOCKING_DEPENDENCIES",
                           "CHECKPOINT_CLOSE", "STATE_REOPEN", "UNRESOLVED_STAYS_BLOCKED"],
                "qualifies_factory": False, "governance_modified": False,
                "local_agent_authorization": False}


class SelfTests(unittest.TestCase):
    def test_linux_pin_format(self):
        self.assertRegex(LINUX_ARCHIVE_SHA256, r"^[0-9a-f]{64}$")
    def test_windows_pin_format(self):
        self.assertRegex(WINDOWS_ARCHIVE_SHA256, r"^[0-9a-f]{64}$")
    def test_mismatched_archive_fails_closed(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "fake.tar.gz"
            f.write_bytes(b"no")
            with self.assertRaisesRegex(ValueError, "PIN_MISMATCH"):
                get_bd_linux(f, Path(p))
    def test_malformed_pin_fails(self):
        with tempfile.TemporaryDirectory() as p:
            f = Path(p) / "fake"
            f.write_bytes(b"no")
            with self.assertRaisesRegex(ValueError, "PIN_FORMAT_INVALID"):
                assert_pinned(f, "0")
    def test_explicit_id_accepted(self):
        self.assertEqual(parse_issue_id("bd-abc123\n"), "bd-abc123")
    def test_unreliable_id_rejected(self):
        with self.assertRaises(ValueError):
            parse_issue_id("Created issue bd-abc123")
    def test_ready_json_strict(self):
        self.assertEqual(ready_ids([{"id": "bd-a"}]), {"bd-a"})
        with self.assertRaises(ValueError):
            ready_ids({"unknown": []})
    def test_version_exact(self):
        self.assertTrue(pinned_version("bd version 1.3.1 (release)"))
        self.assertFalse(pinned_version("bd version 1.3.11"))
        self.assertFalse(pinned_version("bd version 1.3.2"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--archive", type=Path, help="Pinned Linux amd64 v1.3.1 tar.gz (supplied externally)")
    ap.add_argument("--result", type=Path, help="Optional results JSON path")
    args = ap.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(SelfTests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    result = {"disposition": "BLOCKED_NO_VERIFIED_BINARY", "qualifies_factory": False}
    if args.archive is not None:
        try:
            result = run_trial(args.archive)
        except Exception as ex:
            result = {"disposition": "FAIL_OR_BLOCKED", "error_class": type(ex).__name__,
                      "error_code": str(ex)[:120], "qualifies_factory": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.result:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["disposition"].startswith("PASS_") else 20


if __name__ == "__main__":
    sys.exit(main())
