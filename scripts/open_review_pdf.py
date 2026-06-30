from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import build_review_pdfs


DEFAULT_KIND = "curated"


def resolve_review_pdf_paths(repo_root: Path, kind: str) -> tuple[Path, Path]:
    try:
        tex_rel, pdf_rel = build_review_pdfs.REVIEW_PDF_TARGETS[kind]
    except KeyError as exc:
        raise ValueError(f"Unknown review PDF kind: {kind!r}") from exc
    return repo_root / tex_rel, repo_root / pdf_rel


def review_pdf_is_stale(tex_path: Path, pdf_path: Path) -> bool:
    if not pdf_path.exists():
        return True
    return pdf_path.stat().st_mtime < tex_path.stat().st_mtime


def refresh_review_pdf(repo_root: Path, tex_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "build_review_pdfs.py"),
            "--tex",
            str(tex_path.relative_to(repo_root)),
        ],
        cwd=repo_root,
        check=True,
    )


def open_pdf(pdf_path: Path) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", str(pdf_path)], check=True)
        return

    opener = shutil.which("xdg-open")
    if opener:
        subprocess.run([opener, str(pdf_path)], check=True)
        return

    raise RuntimeError(f"No PDF opener found for {pdf_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Open a generated review PDF from build/ after refreshing it if needed."
    )
    parser.add_argument(
        "--kind",
        choices=sorted(build_review_pdfs.REVIEW_PDF_TARGETS),
        default=DEFAULT_KIND,
        help="Which generated review PDF to open.",
    )
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Skip rebuilding even if the PDF is older than its source TeX.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    tex_path, pdf_path = resolve_review_pdf_paths(repo_root, args.kind)
    if not args.no_refresh and review_pdf_is_stale(tex_path, pdf_path):
        refresh_review_pdf(repo_root, tex_path)
    print(f"Opening review PDF: {pdf_path}")
    open_pdf(pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
