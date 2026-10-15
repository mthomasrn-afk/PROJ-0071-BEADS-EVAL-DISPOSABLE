#!/usr/bin/env python3
"""CP08: public synthetic H3/PCR comparison only; no factory adoption."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT / "cp08_authority_frozen.json"
spec = importlib.util.spec_from_file_location("cold_fixture", ROOT / "beads_cold_start_qualification.py")
cold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cold)
TASKS = ("S100", "S110", "S120", "S130", "S140")

class Blocked(Exception):
    pass

def read_authority(path=FROZEN):
    a = json.loads(Path(path).read_text(encoding="utf-8"))
    if a.get("fixture_id") != "PROJ0071-CP08-FROZEN-SYNTHETIC-01":
        raise Blocked("BLOCKED_FIXTURE_ID")
    if set(a) != {"fixture_id","h3","pcr","decisions","failures"} or set(a["pcr"]) != set(TASKS):
        raise Blocked("BLOCKED_AUTHORITY_SCHEMA")
    h, p, d, f = (a[x] for x in ("h3","pcr","decisions","failures"))
    if h != {"first_incomplete":"S120","completed":["S100","S110"],"blocked":["S130"]}:
        raise Blocked("BLOCKED_H3_MISMATCH")
    if d != {"promotion":"S130","rule":"REQUIRES_ACCEPTED_S140"}:
        raise Blocked("BLOCKED_DECISION_CONFLICT")
    if f != {"unresolved":"S140","disposition":"BLOCKED"}:
        raise Blocked("BLOCKED_FAILURE_REGISTER_CONFLICT")
    if p["S120"]["deps"] != ["S110"] or p["S130"]["deps"] != ["S140"]:
        raise Blocked("BLOCKED_DEPENDENCY_CONFLICT")
    for task, r in p.items():
        if r["state"] not in ("COMPLETE","INCOMPLETE","BLOCKED"):
            raise Blocked("BLOCKED_UNKNOWN_STATE")
        if r["accepted"] != (r["state"] == "COMPLETE"):
            raise Blocked("BLOCKED_ACCEPTANCE_CONFLICT")
        if any(dep not in p for dep in r["deps"]):
            raise Blocked("BLOCKED_UNKNOWN_DEPENDENCY")
    if any(p[t]["state"] != "COMPLETE" for t in h["completed"]):
        raise Blocked("BLOCKED_H3_COMPLETED_CONFLICT")
    if p["S120"]["state"] != "INCOMPLETE" or any(p[t]["state"] != "COMPLETE" for t in p["S120"]["deps"]):
        raise Blocked("BLOCKED_NEXT_UNREADY")
    if p["S130"]["state"] != "BLOCKED" or p["S140"]["accepted"]:
        raise Blocked("BLOCKED_PROMOTION_CONFLICT")
    return a

def without_beads(a):
    return {"first_incomplete":a["h3"]["first_incomplete"],
            "completed_preserved":a["h3"]["completed"],
            "promotion_blocked":a["decisions"]["promotion"],
            "authority_record_categories":4,
            "human_reconstruction_time":"NOT_MEASURED"}

def context(archive, workspace):
    work = workspace / "project"
    home = workspace / "home"
    work.mkdir(parents=True, exist_ok=True)
    home.mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update({"HOME":str(home),"USERPROFILE":str(home),"XDG_CONFIG_HOME":str(home/".config"),
                "GIT_CONFIG_GLOBAL":str(home/".gitconfig"),"CI":"true","BD_NON_INTERACTIVE":"1"})
    return cold.extract(archive,"linux",workspace/"bin"),work,env

def seed(archive, workspace, case):
    a = read_authority()
    if workspace.exists():
        raise Blocked("BLOCKED_EXISTING_WORKSPACE")
    workspace.mkdir(parents=True)
    bd,work,env = context(archive,workspace)
    if "1.3.1" not in cold.call(bd,work,env,"version"):
        raise Blocked("BLOCKED_VERSION")
    cold.call(bd,work,env,"init","--stealth","--skip-agents","--skip-hooks","--non-interactive")
    ids = {}
    for task in TASKS:
        ids[task] = cold.issue(cold.call(bd,work,env,"create","CP08 synthetic "+task,"--silent"))
    for task,row in a["pcr"].items():
        for dep in row["deps"]:
            cold.call(bd,work,env,"dep","add",ids[task],ids[dep])
    for task in a["h3"]["completed"]:
        if task == "S110" and case == "upstream_blocked":
            continue
        cold.call(bd,work,env,"close",ids[task],"--reason","synthetic accepted")
    if case == "stale":
        cold.call(bd,work,env,"close",ids["S120"],"--reason","intentionally stale")
    (workspace/"ids.json").write_text(json.dumps({"case":case,"ids":ids,
        "source_sha256":hashlib.sha256(FROZEN.read_bytes()).hexdigest()},sort_keys=True))
    return {"phase":"SEED","case":case,"disposition":"CANDIDATE_ONLY"}

def recover(archive,workspace,case):
    baseline = without_beads(read_authority())
    if case == "missing" and not (workspace/"ids.json").exists():
        return {"case":case,"disposition":"EXPECTED_BLOCKED","reason":"MISSING_BEADS_CHECKPOINT",
                "baseline":baseline,"qualified":False}
    if not (workspace/"ids.json").exists():
        raise Blocked("BLOCKED_MISSING_CHECKPOINT")
    m=json.loads((workspace/"ids.json").read_text())
    if m["case"] != case or m["source_sha256"] != hashlib.sha256(FROZEN.read_bytes()).hexdigest():
        raise Blocked("BLOCKED_SOURCE_DRIFT")
    ids=m["ids"]
    if set(ids)!=set(TASKS) or len(set(ids.values()))!=len(TASKS):
        raise Blocked("BLOCKED_INVALID_MAPPING")
    bd,work,env=context(archive,workspace)
    ready=cold.ready(cold.call(bd,work,env,"ready","--json"))
    wanted={ids["S120"],ids["S140"]}
    matching=ready==wanted
    out={"case":case,"baseline":baseline,
         "beads_ready_tasks":sorted(t for t in TASKS if ids[t] in ready),
         "authority_record_categories_with_beads":4,
         "additional_machine_queries":1,"human_reconstruction_savings":"NOT_ESTABLISHED",
         "qualified":False}
    if case=="normal":
        if not matching:
            raise Blocked("BLOCKED_BEADS_VS_H3_PCR_CONFLICT")
        out.update({"disposition":"PASS_BOUNDED_COMPARISON_CANDIDATE_ONLY",
                    "same_next_action":True,"promotion_preserved":ids["S130"] not in ready})
    else:
        if matching:
            raise Blocked("FAIL_NEGATIVE_CASE_NOT_DETECTED")
        out.update({"disposition":"EXPECTED_BLOCKED",
                    "reason":"BEADS_VS_H3_PCR_CONFLICT",
                    "authority_first_incomplete":baseline["first_incomplete"]})
    return out

class Tests(unittest.TestCase):
    def test_baseline(self):
        self.assertEqual(without_beads(read_authority())["first_incomplete"],"S120")
    def test_conflicting_h3(self):
        data=copy.deepcopy(read_authority())
        data["h3"]["first_incomplete"]="S140"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"altered.json"
            p.write_text(json.dumps(data))
            with self.assertRaisesRegex(Blocked,"BLOCKED_H3_MISMATCH"):
                read_authority(p)
    def test_unaccepted_marked_complete(self):
        data=copy.deepcopy(read_authority())
        data["pcr"]["S120"]["accepted"]=True
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"altered.json"
            p.write_text(json.dumps(data))
            with self.assertRaisesRegex(Blocked,"BLOCKED_ACCEPTANCE_CONFLICT"):
                read_authority(p)
    def test_missing_beads_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(recover(None,Path(d)/"uncreated","missing")["disposition"],
                             "EXPECTED_BLOCKED")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--phase",choices=("seed","recover"))
    ap.add_argument("--case",choices=("normal","stale","upstream_blocked","missing"),default="normal")
    ap.add_argument("--archive",type=Path)
    ap.add_argument("--workspace",type=Path)
    a=ap.parse_args()
    if a.self_test:
        return 0 if unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful() else 3
    if not a.phase or not a.workspace or (a.case!="missing" and not a.archive):
        ap.error("phase, workspace and archive are required except archive for missing case")
    try:
        result=seed(a.archive,a.workspace,a.case) if a.phase=="seed" else recover(a.archive,a.workspace,a.case)
        print("CP08_RESULT "+json.dumps(result,sort_keys=True))
        return 0
    except Exception as exc:
        print("CP08_RESULT "+json.dumps({"disposition":"FAIL_OR_BLOCKED",
              "error_code":str(exc)[:250],"error_class":type(exc).__name__,"qualified":False}))
        return 20

if __name__=="__main__":
    sys.exit(main())
