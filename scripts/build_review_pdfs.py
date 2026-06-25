from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_TEX_PATHS = [
    "build/generated_curated_series_sample.tex",
    "build/generated_integrated_dictionary.tex",
]
ROOT_ARTIFACT_SUFFIXES = [
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".pdf",
    ".run.xml",
    ".synctex.gz",
    ".xdv",
]


def cleanup_root_artifacts(repo_root: Path, stem: str) -> None:
    for suffix in ROOT_ARTIFACT_SUFFIXES:
        path = repo_root / f"{stem}{suffix}"
        if path.exists():
            path.unlink()


def build_review_pdf(repo_root: Path, tex_path: Path) -> None:
    subprocess.run(["latexmk", "-xelatex", str(tex_path)], cwd=repo_root, check=True)
    root_pdf = repo_root / f"{tex_path.stem}.pdf"
    if not root_pdf.exists():
        raise FileNotFoundError(f"Expected built PDF {root_pdf} was not created.")
    output_pdf = tex_path.with_suffix(".pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root_pdf, output_pdf)
    cleanup_root_artifacts(repo_root, tex_path.stem)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the generated review PDFs and sync them into build/."
    )
    parser.add_argument(
        "--tex",
        nargs="+",
        default=DEFAULT_TEX_PATHS,
        help="Generated TeX review files to compile.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    for tex in args.tex:
        build_review_pdf(repo_root, repo_root / tex)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
