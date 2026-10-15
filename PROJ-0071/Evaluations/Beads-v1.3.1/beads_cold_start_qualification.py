#!/usr/bin/env python3
"""Disposable PROJ-0071 Beads v1.3.1 cold-start candidate; synthetic only."""
import argparse, hashlib, json, os, re, subprocess, sys, tarfile, unittest, zipfile
from pathlib import Path, PurePosixPath
PIN = {
 "linux": ("beads_1.3.1_linux_amd64.tar.gz","3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c","bd"),
 "windows": ("beads_1.3.1_windows_amd64.zip","48cd82e1d3e311c9bf9a5d6d67ad1a8542ae13d4e20c5bfb527656c5e666af76","bd.exe"),
}
def digest(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
def verify(p,platform):
 if Path(p).name!=PIN[platform][0] or digest(p)!=PIN[platform][1]:raise ValueError("BLOCKED_PIN_MISMATCH")
def safe(name,executable):
 path=PurePosixPath(name.replace(chr(92),"/"))
 return path.name==executable and not path.is_absolute() and ".." not in path.parts and len(path.parts)<=3 and ":" not in name
def extract(p,platform,folder):
 verify(p,platform)
 folder.mkdir(parents=True,exist_ok=True)
 exe=PIN[platform][2];out=folder/exe
 if platform=="linux":
  with tarfile.open(p,"r:gz") as t:
   found=[x for x in t if x.isfile() and safe(x.name,exe) and 0<x.size<350000000]
   if len(found)!=1:raise ValueError("BLOCKED_ARCHIVE_ENTRY_COUNT")
   with t.extractfile(found[0]) as inp,out.open("wb") as dst:
    for b in iter(lambda:inp.read(1048576),b""):dst.write(b)
  out.chmod(0o700)
 else:
  with zipfile.ZipFile(p) as z:
   found=[x for x in z.infolist() if not x.is_dir() and safe(x.filename,exe) and 0<x.file_size<350000000]
   if len(found)!=1:raise ValueError("BLOCKED_ARCHIVE_ENTRY_COUNT")
   with z.open(found[0]) as inp,out.open("wb") as dst:
    for b in iter(lambda:inp.read(1048576),b""):dst.write(b)
 return out
def issue(v):
 v=v.strip()
 if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*-[A-Za-z0-9._-]+",v):raise ValueError("BLOCKED_UNEXPECTED_ISSUE_ID")
 return v
def ready(v):
 x=json.loads(v)
 if isinstance(x,dict):x=x.get("issues",x.get("results"))
 if not isinstance(x,list) or any(not isinstance(z,dict) or not isinstance(z.get("id"),str) for z in x):raise ValueError("BLOCKED_READY_SCHEMA")
 return {z["id"] for z in x}
def call(bd,work,env,*args):
 p=subprocess.run([str(bd),*args],cwd=work,env=env,capture_output=True,text=True,timeout=90)
 if p.returncode:raise RuntimeError("BD_COMMAND_FAILED_"+args[0]+"_"+str(p.returncode)+":"+(p.stderr or p.stdout)[-240:])
 return p.stdout
def phase(platform,archive,workspace,step):
 workspace=workspace.resolve()
 if step=="seed":
  if workspace.exists():raise ValueError("BLOCKED_EXISTING_WORKSPACE")
  workspace.mkdir(parents=True)
 elif not workspace.is_dir():raise ValueError("BLOCKED_NO_CHECKPOINT")
 bd=extract(archive,platform,workspace/"bin")
 home=workspace/"home";work=workspace/"synthetic"
 home.mkdir(exist_ok=True);work.mkdir(exist_ok=True)
 env=os.environ.copy()
 env.update({"HOME":str(home),"USERPROFILE":str(home),"XDG_CONFIG_HOME":str(home/".config"),
             "GIT_CONFIG_GLOBAL":str(home/".gitconfig"),"BD_NON_INTERACTIVE":"1","CI":"true"})
 if not re.search(r"(?<![\d.])v?1\.3\.1(?![\d.])",call(bd,work,env,"version")):raise ValueError("BLOCKED_VERSION_MISMATCH")
 checkpoint=workspace/"checkpoint.json"
 if step=="seed":
  call(bd,work,env,"init","--stealth","--skip-agents","--skip-hooks","--non-interactive")
  ids={}
  for key,title in [("done","Synthetic completed checkpoint"),("next","Synthetic first incomplete action"),
                    ("unverified","Synthetic unresolved acceptance"),("promotion","Synthetic blocked promotion")]:
   ids[key]=issue(call(bd,work,env,"create",title,"--silent"))
  call(bd,work,env,"dep","add",ids["next"],ids["done"])
  call(bd,work,env,"dep","add",ids["promotion"],ids["unverified"])
  before=ready(call(bd,work,env,"ready","--json"))
  if not {ids["done"],ids["unverified"]}<=before or {ids["next"],ids["promotion"]}&before:raise ValueError("FAIL_INITIAL_GRAPH")
  call(bd,work,env,"close",ids["done"],"--reason","synthetic completed checkpoint")
  ids["phase"]="SEED_COMPLETE";checkpoint.write_text(json.dumps(ids,sort_keys=True))
  return {"phase":"SEED_COMPLETE","checksum_verified":True,"issues":4,"dependencies":2,"factory_qualified":False}
 ids=json.loads(checkpoint.read_text())
 if ids.get("phase")!="SEED_COMPLETE":raise ValueError("BLOCKED_CHECKPOINT_PHASE")
 done,next_,unverified,promotion=[issue(ids[k]) for k in ("done","next","unverified","promotion")]
 if len({done,next_,unverified,promotion})!=4:raise ValueError("BLOCKED_DUPLICATE_ISSUE")
 after=ready(call(bd,work,env,"ready","--json"))
 if next_ not in after or unverified not in after or done in after or promotion in after:raise ValueError("FAIL_FRESH_PROCESS_RECOVERY")
 call(bd,work,env,"close",next_,"--reason","synthetic next checkpoint complete")
 again=ready(call(bd,work,env,"ready","--json"))
 if promotion in again or unverified not in again:raise ValueError("FAIL_UNVERIFIED_PROMOTION")
 return {"phase":"RESUME","disposition":"PASS_SYNTHETIC_COLD_START_ONLY","checksum_verified":True,
         "version":"1.3.1","first_incomplete_recovered":True,"unverified_promotion_blocked":True,
         "factory_qualified":False,"full_H3_PCR_acceptance":False}
class Tests(unittest.TestCase):
 def test_hash_format(self):
  for name,pin,exe in PIN.values():self.assertRegex(pin,r"^[0-9a-f]{64}$")
 def test_id_strict(self):
  self.assertEqual(issue("bd-abc"),"bd-abc")
  with self.assertRaises(ValueError):issue("Created bd-abc")
 def test_ready_strict(self):
  self.assertEqual(ready('[{"id":"bd-a"}]'),{"bd-a"})
  with self.assertRaises(ValueError):ready('{"other":[]}')
 def test_path_traversal(self):
  self.assertFalse(safe("../../bd","bd"));self.assertFalse(safe("/tmp/bd","bd"))
 def test_windows_drive(self):
  self.assertFalse(safe("C:/tmp/bd.exe","bd.exe"))
  self.assertTrue(safe("beads_1.3.1_windows_amd64/bd.exe","bd.exe"))
 def test_wrong_archive(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/PIN["linux"][0];p.write_bytes(b"invalid")
   with self.assertRaisesRegex(ValueError,"BLOCKED_PIN_MISMATCH"):verify(p,"linux")
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--self-test",action="store_true")
 p.add_argument("--phase",choices=["seed","resume"])
 p.add_argument("--platform",choices=["linux","windows"])
 p.add_argument("--archive",type=Path);p.add_argument("--workspace",type=Path)
 a=p.parse_args()
 if a.self_test:return 0 if unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful() else 1
 if not all([a.phase,a.platform,a.archive,a.workspace]):p.error("phase, platform, archive, workspace required")
 try:
  result=phase(a.platform,a.archive,a.workspace,a.phase)
  print(json.dumps(result,sort_keys=True));return 0
 except Exception as e:
  print(json.dumps({"disposition":"FAIL_OR_BLOCKED","error_class":type(e).__name__,
                   "error_code":str(e)[:400],"factory_qualified":False},sort_keys=True));return 20
if __name__=="__main__":sys.exit(main())
