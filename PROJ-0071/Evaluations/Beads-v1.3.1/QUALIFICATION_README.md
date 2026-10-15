# PROJ-0071 — Beads v1.3.1 additional synthetic qualification

This new isolated manual-only workflow is **not** a qualified product and does not replace the already successful Linux run 38759321780. It uses only ordinary free public `ubuntu-24.04` and `windows-2025` GitHub-hosted standard runners, read-only contents, 12-minute per-job ceilings, no artifacts, no secrets, and no automatic triggers.

Run from **Actions → PROJ-0071 Beads cold-start Linux Windows MANUAL ONLY → Run workflow → main**. The separate Linux and Windows jobs each check the pinned upstream asset SHA-256 and then execute **two independent Python processes in different Actions steps**. A synthetic completed checkpoint is closed in seed; resume opens its persisted workspace and asserts the first incomplete issue becomes ready while an unrelated unverified promotion remains blocked. Six pure-Python harness negative/format tests run first; those are not Beads executable evidence.

Expected dispositions: `PASS_SYNTHETIC_COLD_START_ONLY` means *process* cold-start and simple synthetic issue graph recovery only. It is not a GitHub-job cold-start, ChatGPT H3/PCR reconstruction, security qualification, governance authorization, or accepted PROJ-0072 integration. `FAIL_OR_BLOCKED` means something failed or could not be established, and requires log review.

Actual network acquisition happens in the checksum download step; thereafter the test calls the locally extracted CLI with temporary HOME and no hooks/agents. The workflow **does not prove network isolation**, and no air-gapped claim is made.

Retain original run IDs/job IDs/logs as the execution evidence. Do not turn a model-written status JSON into a run receipt. Do not run on MSI/K2-SO, modify private repositories, add automatic triggers, or change qualified parent infrastructure during this candidate screen.
