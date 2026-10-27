#!/usr/bin/env python3
"""Check participant setup completeness, without changing files or using a network.

Python 3.10+, standard library only. This is not a factual, quality, or approval
check: replacing a placeholder does not establish that the replacement is true.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


REQUIRED_FILES = (
    "brand/voice-guide.md",
    "brand/rules.md",
    "brand/product.md",
    "brand/audience.md",
)
TOKEN = re.compile(r"\{\{\s*[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\s*\}\}|\bCHANGE_ME\b")
# Deliberately narrow: ordinary Markdown brackets and prose are not placeholders.
LEGACY_TOKEN = re.compile(
    r"\[(?:YOUR|INSERT|REPLACE|ADD|FILL IN)[ _][A-Z][A-Z0-9 _/-]*\]"
)
LINK_DEFINITION = re.compile(r"^ {0,3}\[([^\]\n]+)\]:\s*\S+", re.MULTILINE)
LIMITATION = (
    "Completeness only: this does not verify factual accuracy, content quality, "
    "brand fit, or approval."
)


def normalized_label(label: str) -> str:
    return " ".join(label.split()).casefold()


def placeholders(text: str) -> list[tuple[int, str]]:
    """Return unresolved marker line numbers and spelling, in reading order."""
    matches = [(match.start(), match.group()) for match in TOKEN.finditer(text)]
    reference_labels = {
        normalized_label(match.group(1)) for match in LINK_DEFINITION.finditer(text)
    }
    for match in LEGACY_TOKEN.finditer(text):
        suffix = text[match.end():]
        # Inline links, reference-style links and reference definitions have real
        # Markdown syntax after the label. A defined shortcut link is also real.
        is_link = bool(re.match(r"[ \t]*(?:\(|\[|:)", suffix))
        is_shortcut = normalized_label(match.group()[1:-1]) in reference_labels
        if not is_link and not is_shortcut:
            matches.append((match.start(), match.group()))
    return [
        (text.count("\n", 0, offset) + 1, token)
        for offset, token in sorted(matches)
    ]


def inspect_file(path: Path) -> list[str]:
    """Read one file and return actionable completeness findings."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ["missing file"]
    except (OSError, UnicodeError) as exc:
        return [f"cannot read as a UTF-8 text file ({exc})"]
    if not text.strip():
        return ["empty file (add the required context)"]
    return [
        f"line {line}: unresolved placeholder {token}"
        for line, token in placeholders(text)
    ]


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that selected brand and brief files are filled in.",
        epilog=(
            LIMITATION
            + " Exit codes: 0 = setup ready; 1 = missing, unreadable, empty, or "
            "unfinished content; 2 = invalid command-line arguments."
        ),
    )
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: this script's parent repository, not the working directory).",
    )
    parser.add_argument(
        "--visual", action="store_true",
        help="Also check brand/DESIGN.md. Omit for copy-only work.",
    )
    parser.add_argument(
        "--brief", type=Path,
        help="Also check a brief file; a relative path is resolved from --root.",
    )
    args = parser.parse_args(argv)
    args.root = args.root.expanduser().resolve()
    if not args.root.is_dir():
        parser.error(f"--root must name an existing directory: {args.root}")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_arguments(argv)
    files = [args.root / name for name in REQUIRED_FILES]
    if args.visual:
        files.append(args.root / "brand/DESIGN.md")
    if args.brief is not None:
        brief = args.brief.expanduser()
        files.append(brief if brief.is_absolute() else args.root / brief)

    print(f"Setup check: {args.root}")
    unfinished = False
    # Avoid duplicate reports if the optional brief names a required file.
    seen: set[Path] = set()
    for path in files:
        path = path.resolve()
        if path in seen:
            continue
        seen.add(path)
        try:
            label = str(path.relative_to(args.root))
        except ValueError:
            label = str(path)
        findings = inspect_file(path)
        if findings:
            unfinished = True
            print(f"[NEEDS INPUT] {label}")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print(f"[OK] {label}")

    print()
    if unfinished:
        print("Setup unfinished. Address the findings above, then run this check again.")
    else:
        print("Setup ready: all selected files are present, non-empty, and contain no recognized placeholders.")
    if not args.visual:
        print("Visual setup was not checked. Add --visual before producing visuals.")
    print(LIMITATION)
    return 1 if unfinished else 0


if __name__ == "__main__":
    sys.exit(main())
