# CP08 — Beads v1.3.1 synthetic H3/PCR comparison evidence (2026-10-15)

**Disposition:** BOUNDED_SYNTHETIC_H3_PCR_COMPARISON_EXECUTION_PASS; **independent ChatGPT H3/PCR cold-recovery acceptance NOT ESTABLISHED**, no Beads factory adoption. This derived evaluation record is **not** an independent signed/qualified acceptance receipt and does not supersede original GitHub execution logs.

## Original execution evidence

- **GitHub workflow run:** [38771620150](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38771620150) — status `completed`, conclusion `success`, attempt 1.
- **Job:** `h3-pcr-compare`, ID `116548611652`, conclusion `success`; original logs linked from the run. This execution is the evidence; this document is only a derived read-back.
- **Commit under test:** `9d690f254622fe20119a6ea6d9eef6c72dbfe906`. CP07 and prior committed evidence were not rerun or modified.
- **Runner:** standard `ubuntu-24.04` GitHub-hosted runner in a PUBLIC disposable repository; `workflow_dispatch` only, `contents: read`, no secrets or private project fixtures.
- **Binary pin:** official Beads v1.3.1 Linux SHA-256 `3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c`; original log `beads_1.3.1_linux_amd64.tar.gz: OK`. Tested image digest `python@sha256:b99029c95d3d37fb1e4e76d287f7984373dca77c665885986e31b2c95260c13c`; observed image ID `sha256:c9560247cd9a86b83392940ea3c2ee25266c2803be9c97a7eae2e57689b428ae`.
- **Network control:** prefetch outside containers, then separate `--network none` test containers sharing ephemeral workspace; original `CP08_OFFLINE_PROBE 101`. Git prerequisite present in isolated container (`git version 2.39.5`). Not a complete network-isolation proof for the runner host.
- **Harness:** `Ran 4 tests`, `OK`.

## Frozen synthetic inputs

The public `cp08_authority_frozen.json` groups simulated H3, PCR, decision and failure records, not private governance source bytes. Five tasks S100–S140; completed accepted S100/S110; first incomplete S120, dependent on S110; promotion S130 must remain blocked until acceptance for S140. Synthetic fixture and methods are linked from the commit above.

## Observed normal case — original `CP08_RESULT` in job log

- Baseline H3/PCR reconstruction: first incomplete `S120`; completed preserved `S100`, `S110`; promotion `S130` blocked.
- Beads ready graph: `S120` and `S140` (only S120 is the baseline's designated first incomplete). Both agree on the first authorized next step. `same_next_action: true`; `promotion_preserved: true`; original result label `PASS_BOUNDED_COMPARISON_CANDIDATE_ONLY`.
- The candidate reports four authority-record categories with or without Beads, one additional machine query, `human_reconstruction_time: NOT_MEASURED`, and `human_reconstruction_savings: NOT_ESTABLISHED`. It does **not** prove time savings or independent H3 recovery improvement.

## Negative cases — actual expected blocking outcomes

| Case | Observed Beads ready list | Observed disposition | Claim boundary |
| --- | --- | --- | --- |
| Stale Beads has already closed S120 | `S140` | `EXPECTED_BLOCKED`, `BEADS_VS_H3_PCR_CONFLICT` | Authoritative H3/PCR outranks stale Beads |
| Beads leaves accepted S110 open | `S110, S140` | `EXPECTED_BLOCKED`, `BEADS_VS_H3_PCR_CONFLICT` | Conflicting incomplete dependency does not silently rewrite accepted H3/PCR |
| Beads checkpoint absent | no checkpoint | `EXPECTED_BLOCKED`, `MISSING_BEADS_CHECKPOINT` | No invented Beads continuity; baseline remains readable |

All are bounded, deterministic negative controls using fixture expectations; they do not test every corruption, archive mismatch, real-world conflict or threat model.

## Comparative decision and next gate

**Value finding:** Beads v1.3.1 provides a queryable auxiliary issue/dependency graph, and the comparison demonstrated correct consistency checks with H3/PCR. It **did not demonstrate** a better next-step answer, a reduction in number of authoritative record categories, or measured operator effort savings. For this frozen scenario the existing H3/PCR/decision/failure evidence alone was sufficient.

**Decision:** retain Beads as `ACCEPT_FOR_FURTHER_EVALUATION_ONLY` / **DO_NOT_ADOPT_YET**. Do not replace the authoritative H3/PCR/GitHub mechanisms, add agent hooks, change PROJ-0072 parent infrastructure, update the qualified Tool Registry, or claim full offline/product acceptance. A production decision would require independently demonstrated incremental utility in a more realistic multi-session recovery workflow with authenticated original evidence and separately applicable governance/qualification gates.

**Still unqualified:** independent ChatGPT cold-start H3/PCR reconstruction across distinct chat sessions and full evaluation acceptance, longitudinal robustness and real-workflow savings, MSI/K2-SO acceptance, full network security, external tool qualification and governance authority. These remain **NOT ESTABLISHED**; the successful GitHub outcome is not a qualification receipt.

## Preservation / closeout

Preserve [CP05 adverse record](CP05_ISOLATION_RUN_38765782370.md), [CP06 corrected isolation record](CP06_LINUX_OFFLINE_RECOVERY_38766554693.md), and [CP07 bounded decision](CP07_BOUNDED_OFFLINE_QUALIFICATION_DECISION_20261015.md) unchanged. Original GitHub Actions run/job logs are primary. No durable test evidence or run logs should be deleted. Disposable runner containers/workspaces expired on completion. No active PCR, Established Work registry, qualified tooling or host was altered by CP08.
