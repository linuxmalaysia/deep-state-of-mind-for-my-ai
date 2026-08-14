---
okf_version: 0.1
type: documentation
title: "Reference: bench_brain.py"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "benchmark", "brain"]
---

# bench_brain.py reference

Spatial brain performance benchmarking utility.

## Description

The `bench_brain.py` tool measures read latency and byte throughput across brain assets and custom skills, calibrating performance multipliers for native OS and simulated mobile FUSE environments.

## Script path

`tools/bench_brain.py`

## CLI signature

```bash
uv run python tools/bench_brain.py

```

## Inputs

Scans two target paths:
- `.agents/brain`
- `.agents/skills`

## Outputs

Telemetry results printed directly to the shell terminal:
- Count of scanned files and total parsed byte volumes.
- Total read times for native OS (in milliseconds).
- Estimated mobile (Samsung Note 10) Termux FUSE latency extrapolations (using a default `3.5x` multiplier).

## Dependencies

- **Python:** Standard library only (no external packages required).

## Internal Python API

### `get_files(directories, extension)`

Recursively gathers matching files.
- **Arguments:** `directories` (string list), `extension` (string, defaults to `.md`).
- **Returns:** String path list.

### `bench_read(files)`

Evaluates overall reading performance.
- **Returns:** Tuple containing `(total_bytes, elapsed_seconds)`.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
