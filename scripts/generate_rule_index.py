#!/usr/bin/env python3
"""Generate the browsable rule index from rules/*.md."""

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
INDEX = RULES / "README.md"
FIELDS = ("Rule ID", "Description", "Target", "Impact")
FIELD_RE = re.compile(r"^\*\*(Rule ID|Description|Target|Impact):\*\*\s*(.*)$")


def rule_fields(path):
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FIELD_RE.fullmatch(line)
        if not match:
            continue
        name, value = match.groups()
        if name in fields:
            raise ValueError(f"{path.name}: duplicate {name} field")
        fields[name] = value.strip()

    missing = [name for name in FIELDS if not fields.get(name)]
    if missing:
        raise ValueError(f"{path.name}: missing or empty {', '.join(missing)} field")
    if fields["Rule ID"] != path.stem:
        raise ValueError(f"{path.name}: Rule ID does not match filename")
    return fields


def cell(value):
    return value.replace("|", r"\|")


def generate():
    rows = []
    for path in sorted(RULES.glob("*.md")):
        if path.name in {"_template.md", "README.md"}:
            continue
        fields = rule_fields(path)
        rows.append(
            f'| [{fields["Rule ID"]}](./{path.name}) | '
            f'{cell(fields["Description"])} | '
            f'{cell(fields["Target"])} | {cell(fields["Impact"])} |'
        )

    return (
        "# Rule index\n\n"
        "Browse the current rules by ID, description, target, and impact. "
        "Follow a rule link for its rationale and evaluation criteria.\n\n"
        "This index is generated from the rule files. After adding or editing a rule, "
        "run `python3 scripts/generate_rule_index.py` from the repository root "
        "and include the updated index in your PR.\n\n"
        "| Rule | Description | Target | Impact |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the index needs updating")
    args = parser.parse_args()

    try:
        content = generate()
        if args.check:
            if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != content:
                print("rules/README.md is out of date; run python3 scripts/generate_rule_index.py", file=sys.stderr)
                return 1
            print("Rule index is up to date.")
        else:
            INDEX.write_text(content, encoding="utf-8")
            print(f"Updated {INDEX.relative_to(ROOT)}")
    except (OSError, UnicodeError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
