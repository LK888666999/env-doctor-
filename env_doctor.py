#!/usr/bin/env python3
"""
env-doctor: A lightweight CLI utility to validate, compare, and generate .env files.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Set, Tuple


def parse_env_file(filepath: Path) -> Tuple[Dict[str, str], Set[str]]:
    """Parse a .env file and return key-value pairs and a set of keys."""
    if not filepath.exists():
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)

    env_map: Dict[str, str] = {}
    keys: Set[str] = set()
    line_regex = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$")

    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = line_regex.match(line)
            if match:
                key, val = match.group(1), match.group(2)
                if (val.startswith('"') and val.endswith('"')) or (
                    val.startswith("'") and val.endswith("'")
                ):
                    val = val[1:-1]
                env_map[key] = val
                keys.add(key)

    return env_map, keys


def check_env(env_path: Path, example_path: Path, strict: bool = False) -> int:
    """Compare .env against .env.example to find missing or empty variables."""
    env_dict, env_keys = parse_env_file(env_path)
    _, example_keys = parse_env_file(example_path)

    missing_keys = example_keys - env_keys
    extra_keys = env_keys - example_keys
    empty_keys = {k for k, v in env_dict.items() if k in example_keys and v == ""}

    has_issues = False
    print(f"Comparing '{env_path}' with template '{example_path}'...\n")

    if missing_keys:
        has_issues = True
        print("Missing required keys (present in template, missing in .env):")
        for k in sorted(missing_keys):
            print(f"  - {k}")
        print()

    if empty_keys:
        print("Empty keys (defined in .env but have no value):")
        for k in sorted(empty_keys):
            print(f"  - {k}")
        print()
        if strict:
            has_issues = True

    if extra_keys:
        print("Extra keys (present in .env, not documented in template):")
        for k in sorted(extra_keys):
            print(f"  - {k}")
        print()

    if not missing_keys and not empty_keys and not extra_keys:
        print("Everything looks great! Your .env is completely in sync.")
        return 0
    elif not has_issues:
        print("Validation passed (with minor warnings).")
        return 0
    else:
        print("Validation failed. Please fix the missing/empty variables above.")
        return 1


def generate_example(env_path: Path, output_path: Path) -> int:
    """Generate a safe .env.example file by stripping sensitive values from .env."""
    if not env_path.exists():
        print(f"Error: Source file '{env_path}' does not exist.", file=sys.stderr)
        return 1

    line_regex = re.compile(r"^(\s*[A-Za-z_][A-Za-z0-9_]*\s*=).*$")
    output_lines = []

    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                output_lines.append(line)
            else:
                match = line_regex.match(line)
                if match:
                    output_lines.append(f"{match.group(1)}\n")
                else:
                    output_lines.append(line)

    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Successfully generated template at '{output_path}'.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="env-doctor: Validate and sync your .env configuration files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Validate .env against .env.example")
    check_parser.add_argument("-e", "--env", default=".env", help="Path to .env file")
    check_parser.add_argument("-t", "--template", default=".env.example", help="Path to template")
    check_parser.add_argument("--strict", action="store_true", help="Fail on empty values")

    init_parser = subparsers.add_parser("init", help="Generate .env.example from .env")
    init_parser.add_argument("-e", "--env", default=".env", help="Source .env file")
    init_parser.add_argument("-o", "--output", default=".env.example", help="Output file")

    args = parser.parse_args()

    if args.command == "check":
        return check_env(Path(args.env), Path(args.template), args.strict)
    elif args.command == "init":
        return generate_example(Path(args.env), Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
