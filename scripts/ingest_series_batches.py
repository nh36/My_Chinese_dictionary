from __future__ import annotations

import argparse
import ast
import csv
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = REPO_ROOT / "data/series_ingest_queue.txt"
COVERAGE_CSV = REPO_ROOT / "data/derived/gsc_series_coverage.csv"
PROMOTE_SCRIPT = REPO_ROOT / "scripts/promote_series_packets.py"
RENDER_SCRIPT = REPO_ROOT / "scripts/render_curated_series.py"
DEFAULT_ID_FILES = (PROMOTE_SCRIPT, RENDER_SCRIPT)
PROTECTED_REPORT = "reports/gsc_series_coverage.md"
QUEUE_HEAD = ("23-24", "23-25", "23-26", "23-28", "23-29", "23-31")
TARGETED_TEST_MODULES = (
    "tests.test_build_coverage_model",
    "tests.test_promote_series_packets",
    "tests.test_resolve_series_roots",
    "tests.test_build_semantic_evidence",
    "tests.test_number_phonetic_transcriptions",
    "tests.test_render_curated_series",
    "tests.test_render_integrated_dictionary",
    "tests.test_pilot_regressions",
)

ALLOWED_EXACT_FILES = {
    "build/generated_curated_series_sample.pdf",
    "build/generated_curated_series_sample.tex",
    "build/generated_integrated_dictionary.pdf",
    "build/generated_integrated_dictionary.tex",
    "data/current_semantic_components.json",
    "data/semantic_components/integrated_semantic_components.json",
    "data/series_ingest_queue.txt",
    "reports/ab_subseries_classification.md",
    "reports/generated_curated_series_sample.md",
    "reports/integrated_series_conflicts.md",
    "reports/integration_summary.md",
    "reports/pilot_render_readiness.md",
    "reports/semantic_components_inventory.md",
    "reports/semantic_evidence_reuse.md",
    "reports/series_root_resolution.md",
    "reports/transcription_numbering.md",
    "reports/wiktionary_component_validation.md",
    "scripts/promote_series_packets.py",
    "scripts/render_curated_series.py",
}


def run_command(command: list[str]) -> None:
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def capture_stdout(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=REPO_ROOT, text=True).strip()


def git_status_map() -> dict[str, str]:
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=REPO_ROOT, text=True
    )
    status: dict[str, str] = {}
    if not output:
        return status
    for line in output.splitlines():
        if len(line) < 4:
            continue
        xy = line[:2]
        raw_path = line[3:]
        if " -> " in raw_path:
            path = raw_path.split(" -> ", 1)[1]
        else:
            path = raw_path
        status[path] = xy
    return status


def find_unmerged_paths(status_map: dict[str, str]) -> list[str]:
    unmerged: list[str] = []
    for path, xy in status_map.items():
        if "U" in xy or xy in {"AA", "DD"}:
            unmerged.append(path)
    return sorted(unmerged)


def changed_paths_since(
    baseline: dict[str, str], current: dict[str, str]
) -> list[str]:
    all_paths = set(baseline) | set(current)
    return sorted(path for path in all_paths if baseline.get(path) != current.get(path))


def is_allowed_path(path: str, batch_ids: set[str]) -> bool:
    if path == PROTECTED_REPORT:
        return True
    if path == "main.tex":
        return False
    if path in ALLOWED_EXACT_FILES:
        return True
    if path.startswith("data/entries/curation/") and path.endswith(".json"):
        return True
    if path.startswith("data/entries/integrated_series/") and path.endswith(".json"):
        return True
    if path.startswith("data/raw/wiktionary/"):
        return True
    if path.startswith("data/series_packets/") and path.endswith(".json"):
        return Path(path).stem in batch_ids
    if path.startswith("reports/series_packets/") and path.endswith(".md"):
        return Path(path).stem in batch_ids
    return False


def assert_expected_dirty_state(
    *,
    baseline: dict[str, str],
    batch_ids: set[str],
    protected_was_staged: bool,
) -> None:
    current = git_status_map()
    unmerged = find_unmerged_paths(current)
    if unmerged:
        joined = ", ".join(unmerged)
        raise RuntimeError(f"Merge conflict detected: {joined}")
    changed = changed_paths_since(baseline, current)
    if "main.tex" in changed:
        raise RuntimeError("Unexpected dirty file: main.tex")
    unexpected = [path for path in changed if not is_allowed_path(path, batch_ids)]
    if unexpected:
        joined = ", ".join(unexpected)
        raise RuntimeError(f"Unexpected dirty file(s): {joined}")
    protected_status = current.get(PROTECTED_REPORT)
    if protected_status and not protected_was_staged and protected_status[0] != " ":
        raise RuntimeError(
            f"{PROTECTED_REPORT} became staged; leaving it unstaged is required."
        )


def read_queue_file() -> list[str]:
    if not QUEUE_FILE.exists():
        return []
    queue: list[str] = []
    for line in QUEUE_FILE.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        queue.append(item)
    return queue


def write_queue_file(queue_ids: list[str]) -> None:
    if queue_ids:
        content = "".join(f"{series_id}\n" for series_id in queue_ids)
    else:
        content = ""
    QUEUE_FILE.write_text(content, encoding="utf-8")


def find_matching_bracket(text: str, start_index: int) -> int:
    depth = 0
    in_string: str | None = None
    escape = False
    for index, char in enumerate(text[start_index:], start=start_index):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == in_string:
                in_string = None
            continue
        if char in {"'", '"'}:
            in_string = char
            continue
        if char == "[":
            depth += 1
            continue
        if char == "]":
            depth -= 1
            if depth == 0:
                return index
    raise RuntimeError("Failed to parse DEFAULT_IDS list.")


def read_default_ids(script_path: Path) -> list[str]:
    text = script_path.read_text(encoding="utf-8")
    match = re.search(r"^DEFAULT_IDS\s*=\s*\[", text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"DEFAULT_IDS assignment not found in {script_path}")
    list_start = match.end() - 1
    list_end = find_matching_bracket(text, list_start)
    default_ids = ast.literal_eval(text[list_start : list_end + 1])
    if not isinstance(default_ids, list) or not all(
        isinstance(item, str) for item in default_ids
    ):
        raise RuntimeError(f"DEFAULT_IDS in {script_path} is not a string list.")
    return default_ids


def update_default_ids(script_path: Path, batch_ids: list[str]) -> bool:
    text = script_path.read_text(encoding="utf-8")
    match = re.search(r"^DEFAULT_IDS\s*=\s*\[", text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"DEFAULT_IDS assignment not found in {script_path}")
    list_start = match.end() - 1
    list_end = find_matching_bracket(text, list_start)
    current_ids = ast.literal_eval(text[list_start : list_end + 1])
    if not isinstance(current_ids, list) or not all(
        isinstance(item, str) for item in current_ids
    ):
        raise RuntimeError(f"DEFAULT_IDS in {script_path} is not a string list.")
    merged = list(current_ids)
    for series_id in batch_ids:
        if series_id not in merged:
            merged.append(series_id)
    if merged == current_ids:
        return False
    rendered = "[\n" + "".join(f'    "{series_id}",\n' for series_id in merged) + "]"
    updated = text[:list_start] + rendered + text[list_end + 1 :]
    script_path.write_text(updated, encoding="utf-8")
    return True


def find_sequence(haystack: list[str], needle: list[str]) -> int | None:
    if not needle:
        return 0
    max_start = len(haystack) - len(needle)
    for start in range(max_start + 1):
        if haystack[start : start + len(needle)] == needle:
            return start
    return None


def derive_remaining_from_coverage(default_ids: list[str]) -> list[str]:
    if not COVERAGE_CSV.exists():
        raise RuntimeError(f"Missing coverage model: {COVERAGE_CSV}")
    default_set = set(default_ids)
    curation_dir = REPO_ROOT / "data/entries/curation"
    existing_curation = {path.stem for path in curation_dir.glob("*.json")}
    remaining: list[str] = []
    with COVERAGE_CSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            series_id = row["gsc_id"].strip()
            if row["in_tex"].strip() != "no":
                continue
            if row["schuessler_cross_reference_only"].strip() == "yes":
                continue
            if series_id in default_set or series_id in existing_curation:
                continue
            remaining.append(series_id)
    return remaining


def derive_initial_queue() -> list[str]:
    default_ids = read_default_ids(PROMOTE_SCRIPT)
    head = list(QUEUE_HEAD)
    start = find_sequence(default_ids, head)
    if start is not None:
        return default_ids[start:]
    remaining = derive_remaining_from_coverage(default_ids)
    start = find_sequence(remaining, head)
    if start is None:
        preview = ", ".join(remaining[:12])
        raise RuntimeError(
            "Unable to derive queue head from defaults or coverage candidates. "
            f"Expected head {', '.join(head)}; remaining candidates start with: {preview}"
        )
    return remaining[start:]


def ensure_queue_file_exists() -> list[str]:
    if QUEUE_FILE.exists():
        return read_queue_file()
    queue = derive_initial_queue()
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_queue_file(queue)
    print(
        f"Created {QUEUE_FILE.relative_to(REPO_ROOT)} with {len(queue)} remaining IDs.",
        flush=True,
    )
    return queue


def batched(queue_ids: list[str], batch_size: int) -> list[list[str]]:
    return [
        queue_ids[index : index + batch_size]
        for index in range(0, len(queue_ids), batch_size)
    ]


def batch_test_command(*, full_tests: bool) -> list[str]:
    command = ["python3", "-m", "unittest"]
    if full_tests:
        return command
    return [*command, *TARGETED_TEST_MODULES]


def pipeline_commands(batch_ids: list[str], *, full_tests: bool) -> list[list[str]]:
    return [
        ["python3", "scripts/export_series_packets.py", "--ids", *batch_ids],
        ["python3", "scripts/promote_series_packets.py", "--ids", *batch_ids],
        ["python3", "scripts/fetch_wiktionary_component_roles.py"],
        ["python3", "scripts/resolve_series_roots.py"],
        ["python3", "scripts/build_semantic_evidence.py"],
        ["python3", "scripts/number_phonetic_transcriptions.py"],
        ["python3", "scripts/render_curated_series.py"],
        batch_test_command(full_tests=full_tests),
    ]


def chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def stage_batch_changes(
    *,
    baseline: dict[str, str],
    batch_ids: set[str],
    protected_was_staged: bool,
) -> list[str]:
    current = git_status_map()
    changed = changed_paths_since(baseline, current)
    to_stage = [
        path
        for path in changed
        if is_allowed_path(path, batch_ids)
        and (path != PROTECTED_REPORT or protected_was_staged)
    ]
    if not to_stage:
        raise RuntimeError("No staged files for batch commit; aborting.")
    for chunk in chunked(sorted(to_stage), 200):
        run_command(["git", "add", "--", *chunk])
    if not protected_was_staged:
        protected_status = git_status_map().get(PROTECTED_REPORT)
        if protected_status and protected_status[0] != " ":
            raise RuntimeError(
                f"{PROTECTED_REPORT} became staged during add; aborting batch."
            )
    return sorted(to_stage)


def print_preexisting_changes(status_map: dict[str, str]) -> None:
    if not status_map:
        print("Pre-existing working tree changes: none", flush=True)
        return
    print("Pre-existing working tree changes:", flush=True)
    for path in sorted(status_map):
        print(f"  {status_map[path]} {path}", flush=True)


def validate_starting_state(status_map: dict[str, str]) -> bool:
    unmerged = find_unmerged_paths(status_map)
    if unmerged:
        joined = ", ".join(unmerged)
        raise RuntimeError(f"Cannot start with merge conflicts: {joined}")
    preexisting_staged = [
        path for path, xy in status_map.items() if xy[0] not in {" ", "?"}
    ]
    unexpected_staged = [
        path for path in preexisting_staged if path != PROTECTED_REPORT
    ]
    if unexpected_staged:
        joined = ", ".join(sorted(unexpected_staged))
        raise RuntimeError(
            "Pre-existing staged file(s) would contaminate automated batch commits: "
            f"{joined}"
        )
    protected_status = status_map.get(PROTECTED_REPORT, "  ")
    return protected_status[0] != " "


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministically ingest GSC series in fixed-size batches."
    )
    parser.add_argument("--batch-size", type=int, default=6)
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--full-tests",
        action="store_true",
        help="Run the full unittest suite instead of the targeted ingestion regression suite.",
    )
    args = parser.parse_args()
    if args.batch_size <= 0:
        parser.error("--batch-size must be greater than zero.")
    if args.max_batches is not None and args.max_batches <= 0:
        parser.error("--max-batches must be greater than zero.")
    return args


def run() -> int:
    args = parse_args()
    baseline = git_status_map()
    print_preexisting_changes(baseline)
    protected_was_staged = validate_starting_state(baseline)
    queue = ensure_queue_file_exists()
    if not queue:
        print("Queue is empty; nothing to ingest.", flush=True)
        return 0
    plan = batched(queue, args.batch_size)
    if args.max_batches is not None:
        plan = plan[: args.max_batches]
    if args.dry_run:
        print("Dry run only; no commands executed.", flush=True)
        for index, batch in enumerate(plan, start=1):
            print(f"Batch {index}: {', '.join(batch)}", flush=True)
        next_head = ", ".join(queue[: args.batch_size])
        print(f"Current queue head: {next_head}", flush=True)
        return 0

    commit_shas: list[str] = []
    queue_remaining = list(queue)
    for index, batch_ids in enumerate(plan, start=1):
        batch_set = set(batch_ids)
        print(f"\n=== Running batch {index}: {', '.join(batch_ids)} ===", flush=True)

        for script_path in DEFAULT_ID_FILES:
            update_default_ids(script_path, batch_ids)
        assert_expected_dirty_state(
            baseline=baseline,
            batch_ids=batch_set,
            protected_was_staged=protected_was_staged,
        )

        for command in pipeline_commands(batch_ids, full_tests=args.full_tests):
            run_command(command)
            assert_expected_dirty_state(
                baseline=baseline,
                batch_ids=batch_set,
                protected_was_staged=protected_was_staged,
            )

        queue_remaining = queue_remaining[len(batch_ids) :]
        write_queue_file(queue_remaining)
        assert_expected_dirty_state(
            baseline=baseline,
            batch_ids=batch_set,
            protected_was_staged=protected_was_staged,
        )

        stage_batch_changes(
            baseline=baseline,
            batch_ids=batch_set,
            protected_was_staged=protected_was_staged,
        )

        commit_message = f"Ingest GSC series {', '.join(batch_ids)}"
        run_command(["git", "commit", "-m", commit_message])
        commit_sha = capture_stdout(["git", "rev-parse", "--short", "HEAD"])
        pushed = False
        if args.push:
            run_command(["git", "push"])
            pushed = True
        commit_shas.append(commit_sha)
        next_head = ", ".join(queue_remaining[: args.batch_size]) or "(empty)"
        print(
            "Batch summary: "
            f"IDs={', '.join(batch_ids)} | commit={commit_sha} | "
            f"pushed={'yes' if pushed else 'no'} | next queue head={next_head}",
            flush=True,
        )

    print("\nIngestion run complete.", flush=True)
    print(f"Batches completed: {len(plan)}", flush=True)
    print(f"Commits: {', '.join(commit_shas)}", flush=True)
    final_head = ", ".join(queue_remaining[: args.batch_size]) or "(empty)"
    print(f"Final queue head: {final_head}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except subprocess.CalledProcessError as error:
        print(
            f"Command failed with exit code {error.returncode}: {' '.join(error.cmd)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
