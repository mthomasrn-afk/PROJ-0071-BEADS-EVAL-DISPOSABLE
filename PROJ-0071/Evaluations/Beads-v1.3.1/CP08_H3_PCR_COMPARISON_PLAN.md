# CP08 — Synthetic H3/PCR comparison candidate

This is an additional evaluation, not a replacement for completed CP01–CP07 or for PROJ-0071/PROJ-0072 qualified infrastructure.

Use the existing public disposable repository and CP06-tested pattern: standard free GitHub \`ubuntu-24.04\` runner, pinned Beads v1.3.1 SHA-256, Git-equipped network-disabled Docker containers, manual-only \`workflow_dispatch\`, no secrets/caches/artifact upload/automatic triggers.

The frozen scenario has four synthetic record categories: H3, PCR, decisions and failures. S100 and S110 are accepted complete, S120 is first incomplete, S130 promotion stays blocked by pending S140 acceptance. Compare baseline read-only authority interpretation without Beads to Beads dependency graph from the same records; do not accept conflicting or absent Beads as authoritative. Deliberately stale and blocked-upstream Beads states must fail closed.

Each fresh container performs an independent Python process on a shared ephemeral Actions workspace. This does **not** establish different GitHub job recovery, independent ChatGPT cold-start acceptance, any private governance authority, real-world manual effort savings, host-wide airgapping, or factory adoption. The four-document-category count is not a human-time metric. Script stdout is not independent acceptance; only original GitHub run/job outcome and logs establish actual execution.

Execute once manually from GitHub Actions → **PROJ-0071 Beads H3 PCR comparison MANUAL ONLY** → Run workflow → main. Preserve adverse logs and original run IDs. Do not rerun CP07.
