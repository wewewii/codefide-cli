from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import platform
from statistics import median
import tempfile
from time import perf_counter

from codefind.scanner import SearchOptions, scan_directory


@dataclass(frozen=True)
class BenchmarkResult:
    files: int
    lines_per_file: int
    matches: int
    durations: list[float]

    @property
    def median_seconds(self) -> float:
        return median(self.durations)


def positive_integer(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return number


def create_dataset(
    root: Path,
    file_count: int,
    lines_per_file: int,
    match_every: int,
) -> int:
    expected_matches = 0
    ordinary_line = "value = compute_result()"

    for index in range(file_count):
        directory = root / f"module_{index // 100:04d}"
        directory.mkdir(exist_ok=True)
        lines = [ordinary_line] * lines_per_file
        if index % match_every == 0:
            lines[lines_per_file // 2] = "result = login(user)"
            expected_matches += 1
        (directory / f"file_{index:06d}.py").write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    return expected_matches


def run_benchmark(
    file_count: int,
    repeats: int,
    lines_per_file: int,
    match_every: int,
) -> BenchmarkResult:
    with tempfile.TemporaryDirectory(prefix="codefind-benchmark-") as temp_directory:
        root = Path(temp_directory)
        expected_matches = create_dataset(root, file_count, lines_per_file, match_every)
        options = SearchOptions(
            keyword="login",
            root=root,
            extensions={"py"},
            context=0,
        )
        durations: list[float] = []

        for _ in range(repeats):
            started = perf_counter()
            report = scan_directory(options)
            durations.append(perf_counter() - started)
            if len(report.results) != expected_matches:
                raise RuntimeError(
                    f"expected {expected_matches} matches, found {len(report.results)}"
                )

    return BenchmarkResult(
        files=file_count,
        lines_per_file=lines_per_file,
        matches=expected_matches,
        durations=durations,
    )


def format_markdown(results: list[BenchmarkResult]) -> str:
    rows = [
        "# CodeFind Benchmark Results",
        "",
        f"- Python: {platform.python_version()}",
        f"- Platform: {platform.platform()}",
        f"- Machine: {platform.machine()}",
        "- Keyword: `login`",
        "- Extension filter: `py`",
        "- Context lines: `0`",
        "",
        "| Files | Lines per file | Matches | Runs | Min (s) | Median (s) | Max (s) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        rows.append(
            f"| {result.files:,} | {result.lines_per_file} | {result.matches} | "
            f"{len(result.durations)} | {min(result.durations):.4f} | "
            f"{result.median_seconds:.4f} | {max(result.durations):.4f} |"
        )
    return "\n".join(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark CodeFind's directory scanner.")
    parser.add_argument(
        "--files",
        nargs="+",
        type=positive_integer,
        default=[1_000, 10_000],
        help="Dataset sizes to benchmark (default: 1000 10000).",
    )
    parser.add_argument(
        "--repeats",
        type=positive_integer,
        default=3,
        help="Number of scans per dataset (default: 3).",
    )
    parser.add_argument(
        "--lines-per-file",
        type=positive_integer,
        default=20,
        help="Lines generated in each file (default: 20).",
    )
    parser.add_argument(
        "--match-every",
        type=positive_integer,
        default=100,
        help="Add one match to every Nth file (default: 100).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = [
        run_benchmark(
            file_count=file_count,
            repeats=args.repeats,
            lines_per_file=args.lines_per_file,
            match_every=args.match_every,
        )
        for file_count in args.files
    ]
    print(format_markdown(results))


if __name__ == "__main__":
    main()
