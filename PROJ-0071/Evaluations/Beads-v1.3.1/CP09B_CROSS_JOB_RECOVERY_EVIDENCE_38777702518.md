# CP09B — Bounded issue-level cross-job recovery evidence and decision

**Date:** 2026-10-15 UTC / America-Chicago. **Disposition:** `PASS_BOUNDED_SYNTHETIC_ISSUE_LEVEL_CROSS_JOB_RECOVERY`. **Independent ChatGPT H3/PCR recovery, full factory-tool qualification, and Beads adoption:** **NOT ESTABLISHED**.

This is a derived decision record with authentic original GitHub Actions execution evidence. It is not a native signed independent product acceptance receipt.

## Original executable evidence (do not reconstruct or rerun)

- Corrected manual workflow: [run 38777702518](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38777702518), attempt 1, branch `main`, commit **`69c65266654f48b404d70cd62b92122d6141aa17`**. GitHub API read-back: **completed/success**.
- **Seed job 116569536274:** completed/success. Four synthetic negative-control unit tests ran: `Ran 4 tests`, `OK`. Pinned archive `beads_1.3.1_linux_amd64.tar.gz: OK`. Actual execution emitted `CP09_RESULT` with `phase: SEED_JOB`, `issue_count: 5`, `disposition: CANDIDATE_ONLY`, `qualified: false`.
- **Restore job 116569832624:** completed/success, in a separate standard GitHub-hosted `ubuntu-24.04` job. New-job transport verification emitted `CP09_NEW_JOB_TRANSPORT_DIGEST_PASS`; independent downloaded archive pin check emitted `beads_1.3.1_linux_amd64.tar.gz: OK`. The final recovery output emitted `CP09_RESULT` with `phase: FRESH_JOB_RESTORE`, `disposition: PASS_BOUNDARY_ONLY`, `matched_handoff_digest: true`, `first_incomplete: S120`, `baseline_first_incomplete: S120`, `beads_ready: [S120,S140]`, `completed_preserved: [S100,S110]`, `promotion_blocked: true`, `human_time_saved: NOT_MEASURED`, `qualified: false`. Output marker: `CP09_TWO_JOB_SYNTHETIC_CANDIDATE_ONLY`.
- Original snapshot SHA-256 from seed and restore: **`da5db1a96e27c76d7d377a75cea619f0d2a9a268a5da0ab3d6fa03f48af46fad`**.
- Frozen authority-source SHA-256 from seed and restore: **`7e189e476a11eebc6d98ddb8f955203fc49426b0f66e2b5edf835ffe6ee591c8`**.
- Beads archive SHA-256 pin: **`3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c`**.
- Container image registry digest: **`sha256:b99029c95d3d37fb1e4e76d287f7984373dca77c665885986e31b2c95260c13c`**; observed image ID `sha256:c9560247cd9a86b83392940ea3c2ee25266c2803be9c97a7eae2e57689b428ae`.
- The script prints `job: UNKNOWN` and `run_id: UNKNOWN` because the runner environment fields were not forwarded into the network-disabled container; **job identities are established from GitHub API and original job logs, not inferred from the script fields**.

## Exact boundary proved

1. A synthetic five-issue/two-dependency Beads graph was seeded on a public, standard GitHub-hosted runner.
2. Only the issue-level JSONL snapshot was passed through native workflow job outputs; SHA-256 and schema/authority checks were required before import.
3. A separate new GitHub job initialized a fresh Beads instance from the snapshot. The run verified that accepted tasks remained accepted, the first incomplete H3/PCR task was recovered, and an unaccepted dependent promotion remained blocked.
4. Offline execution was constrained to the Docker test containers (`--network none`); pinned archives and container images were downloaded on the GitHub-hosted runner before the offline containers. **This is not runner-host airgapping.**
5. Four deterministic adverse tests covered missing transport, source mismatch, checkpoint digest mismatch, and invalid issue set; they are not proof of all possible adversarial inputs.
6. The original workflow [run 38776897854](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38776897854) **failed** with `BLOCKED_PIN_MISMATCH` when a workflow renamed the archive. That failure and skipped restore remain preserved in [CP09A adverse evidence](CP09A_FAILED_RUN_38776897854.md). Only the CP09 workflow's archive basename was corrected, and the existing hash+basename contract was retained. Do not recast the failed run as PASS.

## Comparison with authoritative continuity

The synthetic H3/PCR/decision/failure baseline (CP08) recovered first incomplete task S120 and blocked promotion S130 **without Beads**. CP09 recovered the identical authorized next action using an auxiliary checkpoint and an additional machine-queryable graph, and added an issue-level independent-job portability demonstration. No human reconstruction time or real operator effort savings were measured; no demonstrated superiority exists.

This confirms an incremental **technical portability capability** in the bounded synthetic scope, not a demonstrated net operational benefit, because the existing H3/PCR process already provides the correct authorized action.

## Governance disposition and next gate

- **CP09 bounded cross-job issue-level portability:** **PASS, evidence-defined claim boundary only**.
- **Independent ChatGPT across-conversation H3/PCR cold-start acceptance:** **NOT ESTABLISHED**. Distinct GitHub jobs are not distinct ChatGPT conversations.
- **Complete Dolt database/working history backup/recovery:** **NOT ESTABLISHED**. This uses issue-level `bd export/import`, not complete Beads backup.
- **Real-world reconstruction burden, longitudinal operation, and adoption value:** **NOT ESTABLISHED**.
- **Offline host proof; MSI/K2-SO acceptance; security, autonomous authority, qualified PROJ-0072 tooling:** **NOT ESTABLISHED**.
- **Candidate decision:** `ACCEPT_FOR_FURTHER_EVALUATION_ONLY` / `DO_NOT_ADOPT_IN_FACTORY`. Preserve qualified PROJ-0071/PROJ-0072 parent workflows and artifacts unchanged.

Future qualification should test whether independently recovering across actual ChatGPT sessions offers measurable improvement against the same authoritative H3/PCR/GitHub baseline. If no incremental benefit is established, recommend closing Beads as an evaluated candidate instead of perpetuating tests without a value criterion.

## Preservation

Preserve original GitHub run/job logs for all CP01–CP09, especially CP05 Linux adverse case, CP09A failed seed, and CP09B successful seed/restore. This document is additive; no existing evidence or tooling has been removed, no PCR/Registry promoted, no local Windows/MSI/K2-SO execution occurred, and no new factory publication/qualification authority is claimed.
