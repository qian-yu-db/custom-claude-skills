#!/usr/bin/env python3
"""
Check Python code formatting without modifying files.

Useful for CI/CD pipelines to ensure code is properly formatted.
"""

import sys
from pathlib import Path
from format_code import CodeFormatter


def main():
    """Check formatting without modifications."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check Python code formatting (CI/CD mode)"
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path to check (default: current directory)"
    )
    parser.add_argument(
        "--skip-databricks",
        action="store_true",
        help="Skip Databricks notebooks"
    )
    parser.add_argument(
        "--skip-regular",
        action="store_true",
        help="Skip regular Python files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Create formatter in check-only mode
    formatter = CodeFormatter(
        path=path,
        skip_databricks=args.skip_databricks,
        skip_regular=args.skip_regular,
        check_only=True,
        verbose=args.verbose,
    )

    # Check dependencies
    formatter.scan_files()
    missing = formatter.check_dependencies()

    if missing:
        print(f"Error: Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        print(f"Install with: uv add --dev {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # Check formatting
    all_formatted = formatter.format()

    if all_formatted:
        print("\n✓ All code is properly formatted")
        sys.exit(0)
    else:
        print("\n✗ Code formatting issues found")
        print("Run: python scripts/format_code.py . to fix")
        sys.exit(1)


if __name__ == "__main__":
    main()
