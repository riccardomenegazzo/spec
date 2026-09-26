#!/usr/bin/env python3
"""Build the browsable rule index from the rule files."""

import argparse
import difflib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
INDEX = RULES / "README.md"
RULE_FILE = re.compile(r"[A-Z]{3}-[0-9]{3}\.md\Z")


def field(content: str, name: str, path: Path) -> str:
    matches = re.findall(rf"^\*\*{name}:\*\*[ \t]*([^\r\n]*?)[ \t]*$", content, re.MULTILINE)
    if len(matches) != 1 or not matches[0]:
        raise ValueError(f"{path.relative_to(ROOT)}: expected one non-empty {name} field")
    return matches[0].strip()


def render() -> str:
    lines = [
        "# Rule index",
        "",
        "This index is generated from the rule descriptions. Search this page to check",
        "whether a rule already covers an idea, then follow its link for the criteria.",
        "",
        "To update it after editing a rule, run `python3 scripts/generate_rule_index.py`.",
        "",
    ]
    files = sorted(p for p in RULES.iterdir() if RULE_FILE.fullmatch(p.name))
    if not files:
        raise ValueError("no rule files found")

    previous_prefix = None
    for path in files:
        content = path.read_text(encoding="utf-8")
        rule_id = field(content, "Rule ID", path)
        if rule_id != path.stem:
            raise ValueError(f"{path.relative_to(ROOT)}: Rule ID {rule_id!r} does not match filename")
        description = field(content, "Description", path)
        prefix = rule_id.split("-", 1)[0]
        if prefix != previous_prefix:
            if previous_prefix is not None:
                lines.append("")
            lines.extend([f"## {prefix}", ""])
            previous_prefix = prefix
        lines.append(f"- [{rule_id}]({path.name}): {description}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed index is out of date")
    args = parser.parse_args()
    try:
        expected = render()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.check:
        actual = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        if actual != expected:
            sys.stderr.writelines(difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(INDEX.relative_to(ROOT)),
                tofile="generated index",
            ))
            print("Run python3 scripts/generate_rule_index.py to update the index.", file=sys.stderr)
            return 1
        return 0

    INDEX.write_text(expected, encoding="utf-8")
    print(f"Updated {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
