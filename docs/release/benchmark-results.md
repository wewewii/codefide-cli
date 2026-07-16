# CodeFind Benchmark Results

Baseline recorded on 2026-07-16 for CodeFind CLI 0.1.0.

## Environment

- Execution environment: disposable Docker container
- Container image: `python:3.11-slim`
- Python: 3.11.15
- Platform: Linux 6.10.14-linuxkit, aarch64, glibc 2.41
- Filesystem: Docker container filesystem

## Methodology

The benchmark uses `scripts/benchmark.py` to generate temporary synthetic Python projects. Each
dataset has 20 lines per file and one `login` match in every 100th file. Dataset creation and
cleanup are excluded from the measured duration.

Each measured scan uses these options:

- Keyword: `login`
- Extension filter: `py`
- Context lines: `0`
- Case-insensitive literal matching
- Three scans of the same generated dataset

Run the baseline with:

```bash
python scripts/benchmark.py
```

## Results

| Files | Lines per file | Matches | Runs | Min (s) | Median (s) | Max (s) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 20 | 10 | 3 | 0.0143 | 0.0148 | 0.0155 |
| 10,000 | 20 | 100 | 3 | 0.1501 | 0.1508 | 0.1585 |

## Interpretation

The scanner completed both synthetic datasets well within the project's target of a few seconds
for small-to-medium projects. The 10,000-file median was approximately 10.2 times the 1,000-file
median, which is consistent with the scanner's sequential file traversal design.

## Limitations

- These results measure scanner execution only, not CLI startup or terminal formatting.
- Repeated scans may benefit from operating-system filesystem caching.
- Synthetic files are small, uniformly encoded UTF-8 files and do not represent every repository.
- Docker filesystem and host hardware performance vary, so results from different machines are
  not directly comparable.
- This is a preliminary baseline rather than a comparison with `grep` or `ripgrep`.
