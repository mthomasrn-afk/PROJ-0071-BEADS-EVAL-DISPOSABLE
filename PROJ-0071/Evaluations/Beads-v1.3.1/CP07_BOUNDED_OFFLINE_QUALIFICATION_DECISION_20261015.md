# CP07 — Beads v1.3.1 Bounded Offline Qualification Decision (2026-10-15)

**Candidate scope:** synthetic local Beads CLI issue graph, dependency gating, checkpoint close, and restart recovery on public standard GitHub-hosted Linux/Windows environments. **No qualified parent change; no local host deployment; no agent authority.**

## Original execution and adverse evidence

| Run | Environment / claim | Original disposition |
| --- | --- | --- |
| [38759321780](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38759321780) | First Linux pinned v1.3.1 synthetic Beads behavior, 8 harness tests | SUCCESS; fixture `PASS_SYNTHETIC_RECOVERY_ONLY` |
| [38763887075](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38763887075) | Linux and Windows isolated synthetic project, separate-process restart, six harness tests each | SUCCESS / SUCCESS; `PASS_SYNTHETIC_COLD_START_ONLY` |
| [38765782370](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38765782370) | Linux network-none container and Windows outbound-deny | **Overall FAILURE**. Windows job SUCCESS; Linux failed to start Beads because slim container lacked Git; `OFFLINE_PROBE 101` did verify Linux network denial |
| [38766554693](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38766554693) | Linux-only recovery with Git-equipped, runtime image-ID-bound network-none container, separate restarted containers | SUCCESS; archive verified, Git present, `OFFLINE_PROBE 101`, six tests OK, `PASS_SYNTHETIC_COLD_START_ONLY` |

The first CP05 failure is retained unchanged. CP06 recovered by altering **only the disposable test infrastructure**. CP06 original job 116531166316 and CP05 successful Windows job 116528490835 are the primary offline behavior evidence.

## Evidence-defined qualification boundary

**PASS — BOUNDED_OFFLINE_SYNTHETIC_CLI_RECOVERY (Linux).** Network-disabled container, checkpoint seed, and process+container restart recovery were executed successfully.

**PASS — BOUNDED_BLOCKED_EGRESS_SYNTHETIC_CLI_RECOVERY (Windows).** Verified Python outbound deny probe (`OFFLINE_PROBE 10013`), firewall app rules for Python and Beads path, checkpoint seed and separate-process recovery. No positive Beads-specific outbound attempt was tested; the evidence is not whole-host network isolation.

**NOT ESTABLISHED — FULL_PROJ0071_OFFLINE_QUALIFICATION / PRODUCT_ACCEPTANCE.** The evidence lacks an H3/PCR cross-session recovery comparison with existing state authority, independent cold-start acceptance, comprehensive robustness/security, explicit formal acceptance criteria, and applicable governance/router gate PASS. No qualified factory Tool Registry disposition is changed.

**Candidate decision: PROCEED_TO_INDEPENDENT_H3_RECOVERY_EVALUATION**, without adoption. PROJ-0072 qualified tooling remains unchanged, and its separate previously observed byte-verification blocker is not bypassed.

All runners were standard GitHub-hosted on a public disposable repository; workflows manual-only. The complete source-of-truth execution artifacts are original GitHub run and job logs. This assistant-authored report is a **derived interpretation**, not a tool-generated signed native acceptance receipt.

## Checkpoint closeout

- Preserve the successful CP01, CP03 and CP06 original GitHub logs, and adverse CP05 original log plus CP05 evidence index.
- CP06 read-back verified index: [CP06](CP06_LINUX_OFFLINE_RECOVERY_38766554693.md).
- No completed test should be rerun merely to generate additional summaries.
- There are no disposable local runtime checkpoints to delete; GitHub-hosted test containers and workspaces were ephemeral.
- Separate independent H3/continuity evaluation may begin under current governance when its acceptance substrate and criteria are recovered; do not back-label these synthetic tests as full qualification.
