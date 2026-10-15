# CP03 — Beads v1.3.1 Linux and Windows process recovery (2026-10-15)

**Result:** both GitHub jobs SUCCESS. **Scope:** synthetic Beads CLI subprocess cold-start screen; not comprehensive offline qualification or adoption.

**Unmodified original evidence:** https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38759321780 (first Linux run successful).
**Second-stage original execution:** https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38763887075
**Evaluated commit:** `258ed7c12f18b35e2d9face33ab5aa9ce04e4578` (manual dispatch; workflow conclusion success).

## Linux: job 116521957813

- Standard `ubuntu-24.04` runner. Six Python harness tests: OK.
- Downloaded official `beads_1.3.1_linux_amd64.tar.gz`; runner SHA-256 check: `3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c` — OK.
- Seed output: `SEED_COMPLETE`, four synthetic issues, two dependencies.
- Separate-step, separate-process recovery: `PASS_SYNTHETIC_COLD_START_ONLY`, `first_incomplete_recovered=true`, `unverified_promotion_blocked=true`.

## Windows: job 116521958311

- Standard `windows-2025` runner. Six Python harness tests: OK.
- Downloaded official `beads_1.3.1_windows_amd64.zip`; logged SHA-256: `48cd82e1d3e311c9bf9a5d6d67ad1a8542ae13d4e20c5bfb527656c5e666af76`.
- Seed output: `SEED_COMPLETE`, four synthetic issues, two dependencies.
- Separate-step, separate-process recovery: `PASS_SYNTHETIC_COLD_START_ONLY`, `first_incomplete_recovered=true`, `unverified_promotion_blocked=true`.

## Claim boundary / next incomplete gates

- The CLI was exercised after network download; **network egress was not prohibited**, so true network-isolated offline operation remains NOT TESTED.
- Separate processes on the same job/runner are not independent GitHub-job or ChatGPT cold-start H3/PCR reconciliation.
- Not tested: H3-vs-Beads recovery comparison, multi-session evidence provenance, Windows MSI/K2-SO, agent hooks, local installation or factory deployment.
- Existing unrelated ChatGPT-native qualified-tool gate receipt indicates registry-byte mismatch; no PROJ-0072 tool invocation or qualified-tool PASS is asserted.
- `ACCEPT_FOR_FURTHER_EVALUATION` only. Complete outstanding gates using separately scoped tests before claiming OFFLINE QUALIFIED.
- Both jobs logged a non-fatal actions/checkout Node20/Node24 compatibility warning.

**This file indexes authentic original GitHub job evidence. It is not a model-substituted execution receipt.**
