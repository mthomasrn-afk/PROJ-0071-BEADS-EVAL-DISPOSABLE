# CP06 — Linux network-isolated Beads v1.3.1 recovery

**Date:** 2026-10-15  
**Evidence class:** read-back verified observation index; **NOT** an original native or signed execution receipt.  
**Original GitHub Actions run:** https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38766554693  
**Job:** 116531166316 — `linux-network-isolated`  
**Run attempt:** 1  
**Tested commit:** `cedd35671a9aa982ed347fa79603e660c67aec5c`  
**GitHub workflow and job conclusion:** SUCCESS / SUCCESS

## Observed in authentic job logs

- Free standard GitHub-hosted `ubuntu-24.04` runner, manual-only workflow.
- Beads upstream `v1.3.1` Linux archive SHA-256 validated: `3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c`; log: `beads_1.3.1_linux_amd64.tar.gz: OK`.
- Git-equipped Python container `python:3.11.16-bookworm` downloaded before isolation; recorded content-addressed image ID `sha256:c9560247cd9a86b83392940ea3c2ee25266c2803be9c97a7eae2e57689b428ae`; registry repo digest `python@sha256:b99029c95d3d37fb1e4e76d287f7984373dca77c665885986e31b2c95260c13c`. The runtime containers were selected by image ID.
- Inside isolated container `git version 2.39.5` verified; `--network none` socket probe: `OFFLINE_PROBE 101` (network unreachable).
- Six harness self-tests passed (negative/format tests).
- Seed executed in a network-disabled temporary container: `SEED_COMPLETE`, 4 synthetic issues, 2 dependency edges.
- Recovery executed in **another network-disabled temporary container**, sharing only the bounded test workspace: `PASS_SYNTHETIC_COLD_START_ONLY`.
- Recovery fixture returned `first_incomplete_recovered=true`, `unverified_promotion_blocked=true`, `factory_qualified=false`, `full_H3_PCR_acceptance=false`; log marker `LINUX_ISOLATED_RESTARTED_CONTAINER_RECOVERY_PASS_CANDIDATE`.

## Prior failure preserved

Original CP05 mixed-platform run **failed overall**, despite successful Windows job 116528490835: https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38765782370. Linux job 116528490988 failed because `python:3.11-slim-bookworm` lacked the `git` executable. Its original logs and prior written evidence remain unchanged.

## Bounded disposition

**PASS — Linux isolated synthetic Beads dependency recovery**, within the demonstrated process/container restart boundary only.

**Windows separate prior check PASS** for per-program outbound-rule blocked synthetic recovery, recorded in CP05. That Windows result is **not** a network-airgap or all-executable deny proof.

**NOT ESTABLISHED**: full PROJ-0071 qualification, genuinely independent H3/PCR cross-session reconstruction, longitudinal robustness, source-evidence reconciliation, Windows host-level airgap, factory use/adoption, agent authorization, local MSI/K2-SO execution, or the separate PROJ-0072 governance/router tool gate. Do not conflate these with the bounded offline result.

No production or qualified tooling was changed; all experiments ran in the disposable public GitHub repository on free standard runners. The original GitHub logs remain the execution evidence.
