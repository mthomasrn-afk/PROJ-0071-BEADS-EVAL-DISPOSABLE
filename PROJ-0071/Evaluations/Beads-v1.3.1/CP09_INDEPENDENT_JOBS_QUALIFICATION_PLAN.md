# CP09 — Independent GitHub job recovery candidate

**Status: COMMITTED / NOT RUN / NOT QUALIFIED.** This is a bounded, public-safe qualification test of an auxiliary Beads candidate, not an application for promotion of the existing factory Tool Registry or a replacement for H3/PCR/decisions/failures.

## Existing evidence preserved

CP01/CP03/CP05/CP06/CP07 and successful CP08 run [38771620150](https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38771620150), including the [CP08 observed results](CP08_H3_PCR_COMPARISON_EVIDENCE_38771620150.md), are preserved unchanged and are not rerun.

## Specific new behavior, no unearned generalization

Two **different GitHub Actions jobs** on standard public-repository GitHub-hosted \`ubuntu-24.04\` runners: the first creates five synthetic tasks and two dependency edges using the checksum-pinned Beads v1.3.1 executable, then exports an issue-only JSONL snapshot. The second checks out clean source in a new job, verifies that snapshot against SHA-256 and the frozen synthetic authority fixture, initializes a new local Beads database, imports the issue-level snapshot and computes ready work.

Cross-job transport uses small public-safe Base64 content via GitHub's ordinary workflow job outputs. No artifact upload, cache, secrets, paid runner, scheduled/push-triggered action, agent hook, local MSI/K2-SO, registry changes, or private data. Prefetch of archive/image happens on runner host before invoking each network-disabled Docker container. Thus only container test phases are isolated; the host is not claimed air-gapped.

JSONL is **an issue interchange snapshot, not full Dolt backup or canonical cross-machine synchronization**. Testing JSONL recovery does not qualify complete Beads database/history recovery, GitHub's job outputs as factory infrastructure, or an automated ChatGPT handoff.

## Exact execution and acceptance conditions

- **Workflow**: \`.github/workflows/proj0071-beads-independent-jobs.yml\` (\`workflow_dispatch\` only).
- **Reuses**: existing \`beads_h3_pcr_comparison.py\` and \`cp08_authority_frozen.json\`; adds one bounded \`beads_independent_job_recovery.py\` adapter; no parallel runner launcher or factory packaging.
- **Pin**: \`beads_1.3.1_linux_amd64.tar.gz\` SHA-256 \`3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c\`; original CP06-tested Python container \`python:3.11.16-bookworm\` with Docker \`--network none\`, \`--cap-drop ALL\`, no-new-privileges.
- **Expected success**: GitHub run and both jobs completed \`success\`; seed self-tests succeed; JSONL issue count 5 and digest preserved across job outputs; authority source digest matches both jobs; restored Beads has ready tasks S120/S140, completed S100/S110 absent from ready, S130 promotion blocked; first incomplete task S120 matches baseline H3/PCR. Read the original job logs, not just status or assistant text.
- **Negative behavior**: a missing handoff, changed source digest, mutated checkpoint digest, or structurally invalid JSONL must fail closed in synthetic self-tests. A real missing/GitHub-redacted job output must fail the restore job rather than be treated as PASS.
- **Do not backfill omitted evidence**: unavailable logs, checksum mismatch, issue relationship loss, or any job failure remains FAIL/BLOCKED. Preserve original adverse logs and record remediation only as a separate later candidate.

## Value and limits

A passing CP09 would qualify only bounded **issue-level cross-job portability and correct recovery**. It would not establish independent ChatGPT cross-conversation H3/PCR reconstruction, a fully restored Beads Dolt history, human-time savings, authority delegation, security hardening, host execution, or factory adoption.

The frozen baseline already found the correct next step in CP08 without Beads. Unless an independent trial later demonstrates real incremental utility, prefer the existing H3/PCR/decision/failure/GitHub process and keep Beads unadopted.

## Manual dispatch boundary

The connected GitHub capabilities can inspect jobs and preserve reports but cannot initiate a new \`workflow_dispatch\`; creating a push-triggered shortcut would violate this public candidate's manual-only restriction. A single explicit **Run workflow** click by the operator is the only execution action pending. Original run/job IDs and logs, once created, remain source of truth.
