# PROJ-0071 Beads v1.3.1 — Public Synthetic Evaluation

**Status:** CANDIDATE — genuine GitHub-hosted Beads test not yet evidenced. This repository contains only a synthetic, disposable evaluation fixture. Nothing here qualifies Beads for PROJ-0071 or PROJ-0072.

## Scope
- Evaluate Beads CLI's ability to preserve synthetic issue dependencies and blocked/unblocked state across independent subprocess invocations.
- No production data, project records, secrets, operational authority, Copiers/MAP artifacts, agent installation, hooks, or local machine configuration.
- Uses standard `ubuntu-24.04` hosted runner in this **public** repository. No larger, self-hosted, or private runners. The workflow runs only on manual `workflow_dispatch`.
- No artifact uploads, caches, releases, deployment, registry mutation, or recurring triggers.

## Pin and provenance
- Upstream: https://github.com/gastownhall/beads/releases/tag/v1.3.1
- Linux: `beads_1.3.1_linux_amd64.tar.gz`
- Expected SHA-256: `3219443a9734b89b93fb16ee8d65844759fa1b3cd3cf139c606b7353cfb0715c`
- Windows (reference only, not tested here): `48cd82e1d3e311c9bf9a5d6d67ad1a8542ae13d4e20c5bfb527656c5e666af76`
- The workflow checks the actual Linux archive digest before the fixture extracts the single `bd` executable.
- The fixture itself independently rechecks the same full archive digest before extraction.

## Run
Open **Actions → PROJ-0071 Beads pinned synthetic recovery MANUAL ONLY → Run workflow → main → Run workflow**.

The job runs eight Python harness self-tests, downloads and checks the exact pinned Linux release, and performs a four-issue/two-dependency synthetic recovery check. Review the run's job and step logs (including `ARCHIVE_SHA256` and the JSON disposition printed by the fixture). This JSON is not uploaded as an artifact.

**Interpretation:** `PASS_SYNTHETIC_RECOVERY_ONLY` demonstrates a narrow CLI behavior, not independent acceptance, full H3 cold-start recovery, or permission to adopt Beads. A failing/missing download or unexecuted CLI remains BLOCKED/NOT_RUN. Windows and real factory use are out of scope.
