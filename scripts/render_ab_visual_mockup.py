from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_SOURCE_PATH = "main.tex"
DEFAULT_OUTPUT_PATH = "build/ab_visual_mockup.tex"
DEFAULT_VARIANT = "overlay-balanced"
BODY_SNIPPETS = [
    ("18-01", 385, 450),
    ("01-67", 3036, 3152),
]

VARIANT_MACROS = {
    "current-tabular": r"\renewcommand{\textoverset}[2]{\begin{tabular}[b]{@{}c@{}}\scriptsize#1\\[-0.38em]#2\end{tabular}}",
    "overlay-compact": r"\renewcommand{\textoverset}[2]{\leavevmode\hbox{\ooalign{\hfil\smash{\raise0.74ex\hbox{\fontsize{4.8}{4.8}\selectfont #1}}\hfil\crcr\hfil#2\hfil\crcr}}}",
    "overlay-balanced": r"\renewcommand{\textoverset}[2]{\leavevmode\hbox{\ooalign{\hfil\smash{\raise0.82ex\hbox{\fontsize{5.0}{5.0}\selectfont #1}}\hfil\crcr\hfil#2\hfil\crcr}}}",
    "overlay-airy": r"\renewcommand{\textoverset}[2]{\leavevmode\hbox{\ooalign{\hfil\smash{\raise0.90ex\hbox{\fontsize{5.2}{5.2}\selectfont #1}}\hfil\crcr\hfil#2\hfil\crcr}}}",
}


def extract_preamble(source_text: str) -> str:
    marker = r"\begin{document}"
    if marker not in source_text:
        raise ValueError("main.tex does not contain \\begin{document}.")
    return source_text.split(marker, 1)[0].rstrip()


def extract_snippet(source_text: str, start_line: int, end_line: int) -> str:
    lines = source_text.splitlines()
    return "\n".join(lines[start_line - 1 : end_line]).rstrip()


def render_document(source_text: str, variant_name: str) -> str:
    if variant_name not in VARIANT_MACROS:
        raise ValueError(f"Unknown variant {variant_name!r}.")

    preamble = extract_preamble(source_text)
    snippets = [extract_snippet(source_text, start, end) for _, start, end in BODY_SNIPPETS]
    body_lines = [
        r"\begin{document}",
        "% GENERATED FILE - DO NOT EDIT BY HAND.",
        r"\section*{a/b superscript visual mockup}",
        (
            "This mockup reuses handwritten dictionary material from "
            + ", ".join(rf"\texttt{{{entry_id}}}" for entry_id, _, _ in BODY_SNIPPETS)
            + " with a candidate \\texttt{\\textoverset} definition."
        ),
        rf"Variant under review: \texttt{{{variant_name}}}.",
        r"\begin{multicols*}{2}",
        r"\raggedcolumns",
    ]
    for snippet in snippets:
        body_lines.append(snippet)
        body_lines.append("")
        body_lines.append(r"\vspace{0.8\baselineskip}")
        body_lines.append("")
    body_lines.extend(
        [
            r"\end{multicols*}",
            r"\end{document}",
        ]
    )
    return "\n".join([preamble, VARIANT_MACROS[variant_name], "", *body_lines]) + "\n"


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render final-style visual mockups for handwritten a/b subgroup notation.")
    parser.add_argument("--source-path", default=DEFAULT_SOURCE_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--variant", choices=sorted(VARIANT_MACROS), default=DEFAULT_VARIANT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source_text = Path(args.source_path).read_text(encoding="utf-8")
    write_output(Path(args.output), render_document(source_text, args.variant))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
