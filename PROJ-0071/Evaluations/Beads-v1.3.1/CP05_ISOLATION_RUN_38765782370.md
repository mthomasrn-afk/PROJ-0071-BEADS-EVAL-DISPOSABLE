# CP05 — Network-Isolation Adverse Evidence (2026-10-15)

**Original run:** https://github.com/mthomasrn-afk/PROJ-0071-BEADS-EVAL-DISPOSABLE/actions/runs/38765782370

- Event: manual `workflow_dispatch`; exact tested commit `30b36d20e9867dd7e0bd05a414256b383b3a704d`
- Overall conclusion: **failure** — preserve as adverse evidence, do not rename or convert into overall PASS.

## Windows job 116528490835: success

- Standard `windows-2025` GitHub-hosted runner; checksum-pinned official Windows v1.3.1 archive.
- SHA-256 observed: `48cd82e1d3e311c9bf9a5d6d67ad1a8542ae13d4e20c5bfb527656c5e666af76`.
- Program-specific outbound Windows firewall deny rules added for Python and intended `bd.exe` path. Runtime Python socket probe returned `OFFLINE_PROBE 10013` (denied); runner emitted `WINDOWS_PROCESS_EGRESS_BLOCK_VERIFIED`.
- Synthetic seed reported `SEED_COMPLETE`, 4 issues / 2 dependencies.
- Separate process recovered `PASS_SYNTHETIC_COLD_START_ONLY` with `first_incomplete_recovered=true` and `unverified_promotion_blocked=true`.
- Runner emitted `WINDOWS_NETWORK_BLOCKED_RECOVERY_COMPLETE` and cleanup step succeeded.
- Claim boundary: per-program Windows firewall isolation only, not host-wide airgap, H3/PCR cold-start or factory adoption.

## Linux job 116528490988: failure

- Standard `ubuntu-24.04` GitHub-hosted runner; checksum-pinned official Linux v1.3.1 archive.
- Download + image prefetch succeeded. Source image: `python:3.11-slim-bookworm`; observed container image ID `sha256:141fe9b385f3bb6d618c07ace1836c0b3c72bf525566ac3eb13cd1f405069877`.
- Container started with `--network none`, dropped capabilities, and `no-new-privileges`; connectivity probe returned `OFFLINE_PROBE 101` (network unreachable).
- Six Python harness negative/format tests passed.
- Beads synthetic seed **failed**: `BD_COMMAND_FAILED_init_1` with `Error: failed to initialize git repository: exec: "git": executable file not found in $PATH`.
- Interpretation: concrete missing Git dependency in slim Python container, **not evidence of Beads functional failure**. Linux network-isolated recovery result is **BLOCKED**, not PASS.

## Corrective action

No modification to the completed initial or process-cold-start tests; no Windows rerun is required. Run one bounded Linux-only recovery with a Git-containing content-addressed Python container image, verified `git --version` before the isolated test. Preserve this CP05 failure record; never overwrite original GitHub run logs. No paid runner or production software factory changes.

This Markdown is an assistant-curated evidence index; the original linked GitHub run/job logs are authoritative execution evidence.
