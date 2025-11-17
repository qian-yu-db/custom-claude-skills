#!/usr/bin/env python3
"""
Format Python code using appropriate tools.

- Databricks notebooks (.py): blackbricks
- Regular Python files: isort + black
- All files: ruff for linting and auto-fixes
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class CodeFormatter:
    """Format Python code with appropriate tools."""

    def __init__(
        self,
        path: Path,
        skip_databricks: bool = False,
        skip_regular: bool = False,
        check_only: bool = False,
        verbose: bool = False,
    ):
        self.path = path
        self.skip_databricks = skip_databricks
        self.skip_regular = skip_regular
        self.check_only = check_only
        self.verbose = verbose

        self.databricks_files: List[Path] = []
        self.regular_files: List[Path] = []
        self.errors: List[Tuple[Path, str]] = []

    def is_databricks_notebook(self, file_path: Path) -> bool:
        """Check if file is a Databricks notebook."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                return '# Databricks notebook source' in first_line
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not read {file_path}: {e}")
            return False

    def scan_files(self) -> None:
        """Scan for Python files and categorize them."""
        if self.path.is_file():
            if self.path.suffix == '.py':
                if self.is_databricks_notebook(self.path):
                    self.databricks_files.append(self.path)
                else:
                    self.regular_files.append(self.path)
        elif self.path.is_dir():
            for py_file in self.path.rglob("*.py"):
                # Skip common directories
                if any(part in py_file.parts for part in ['.venv', 'venv', '__pycache__', 'build', 'dist', '.git']):
                    continue

                if self.is_databricks_notebook(py_file):
                    self.databricks_files.append(py_file)
                else:
                    self.regular_files.append(py_file)

    def run_command(self, cmd: List[str], error_ok: bool = False) -> bool:
        """Run a command and return success status."""
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=not self.verbose,
                text=True,
                check=False
            )

            if result.returncode != 0 and not error_ok:
                if self.verbose or result.stderr:
                    print(f"Error: {result.stderr}")
                return False

            return True

        except FileNotFoundError:
            tool = cmd[2] if len(cmd) > 2 else cmd[0]
            print(f"Error: '{tool}' not found. Install with: uv add --dev {tool}")
            return False
        except Exception as e:
            print(f"Error running command: {e}")
            return False

    def format_databricks_notebooks(self) -> int:
        """Format Databricks notebooks with blackbricks."""
        if not self.databricks_files or self.skip_databricks:
            return 0

        print(f"\n📓 Formatting {len(self.databricks_files)} Databricks notebook(s)...")

        formatted = 0
        for nb_file in self.databricks_files:
            cmd = ["uv", "run", "blackbricks"]
            if self.check_only:
                cmd.append("--check")
            cmd.append(str(nb_file))

            if self.run_command(cmd, error_ok=self.check_only):
                formatted += 1
                if self.verbose or self.check_only:
                    status = "✓" if not self.check_only else "✓ (formatted correctly)"
                    print(f"  {status} {nb_file}")
            else:
                status = "✗ needs formatting" if self.check_only else "✗ failed"
                print(f"  {status} {nb_file}")
                self.errors.append((nb_file, "blackbricks"))

        return formatted

    def format_regular_files(self) -> int:
        """Format regular Python files with isort + black."""
        if not self.regular_files or self.skip_regular:
            return 0

        print(f"\n🐍 Formatting {len(self.regular_files)} regular Python file(s)...")

        # Run isort
        isort_cmd = ["uv", "run", "isort"]
        if self.check_only:
            isort_cmd.append("--check")
        isort_cmd.extend([str(f) for f in self.regular_files])

        isort_success = self.run_command(isort_cmd, error_ok=self.check_only)

        # Run black
        black_cmd = ["uv", "run", "black"]
        if self.check_only:
            black_cmd.append("--check")
        black_cmd.extend([str(f) for f in self.regular_files])

        black_success = self.run_command(black_cmd, error_ok=self.check_only)

        if isort_success and black_success:
            if not self.check_only:
                print(f"  ✓ Formatted {len(self.regular_files)} file(s)")
            else:
                print(f"  ✓ All files formatted correctly")
            return len(self.regular_files)
        else:
            if self.check_only:
                print(f"  ✗ Some files need formatting")
            else:
                print(f"  ✗ Some files failed to format")
            return 0

    def run_ruff(self) -> bool:
        """Run ruff for linting and auto-fixes."""
        print(f"\n🔍 Running ruff on {self.path}...")

        cmd = ["uv", "run", "ruff", "check"]
        if not self.check_only:
            cmd.append("--fix")
        cmd.append(str(self.path))

        success = self.run_command(cmd, error_ok=True)

        if success:
            print("  ✓ No issues found" if self.check_only else "  ✓ Fixed all auto-fixable issues")
        else:
            print("  ⚠ Some issues remain (see above)")

        return success

    def format(self) -> bool:
        """Run all formatting steps."""
        print(f"{'Checking' if self.check_only else 'Formatting'} Python code in: {self.path}")

        # Scan files
        self.scan_files()

        if not self.databricks_files and not self.regular_files:
            print("No Python files found.")
            return True

        print(f"\nFound:")
        print(f"  - {len(self.databricks_files)} Databricks notebook(s)")
        print(f"  - {len(self.regular_files)} regular Python file(s)")

        # Format files
        db_formatted = self.format_databricks_notebooks()
        regular_formatted = self.format_regular_files()

        # Run ruff
        ruff_success = self.run_ruff()

        # Summary
        print(f"\n{'=' * 60}")
        if self.check_only:
            all_good = len(self.errors) == 0 and ruff_success
            if all_good:
                print("✓ All files are properly formatted!")
            else:
                print("✗ Some files need formatting:")
                for file, tool in self.errors:
                    print(f"  - {file} ({tool})")
            return all_good
        else:
            print(f"Summary:")
            print(f"  - Databricks notebooks formatted: {db_formatted}/{len(self.databricks_files)}")
            print(f"  - Regular Python files formatted: {regular_formatted}/{len(self.regular_files)}")
            if self.errors:
                print(f"  - Errors: {len(self.errors)}")
                for file, tool in self.errors:
                    print(f"    - {file} ({tool})")
            return len(self.errors) == 0

    def check_dependencies(self) -> List[str]:
        """Check which formatting tools are installed."""
        tools = {
            'blackbricks': self.databricks_files and not self.skip_databricks,
            'black': self.regular_files and not self.skip_regular,
            'isort': self.regular_files and not self.skip_regular,
            'ruff': True,
        }

        missing = []
        for tool, needed in tools.items():
            if not needed:
                continue

            try:
                result = subprocess.run(
                    ["uv", "run", tool, "--version"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    missing.append(tool)
            except FileNotFoundError:
                missing.append(tool)

        return missing


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Format Python code with appropriate tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Format single file
  python format_code.py script.py

  # Format directory
  python format_code.py src/

  # Check formatting without modifying
  python format_code.py --check src/

  # Format only regular Python files
  python format_code.py --skip-databricks src/

  # Verbose output
  python format_code.py -v src/
        """
    )

    parser.add_argument(
        "path",
        type=str,
        help="Path to Python file or directory"
    )
    parser.add_argument(
        "--skip-databricks",
        action="store_true",
        help="Skip Databricks notebook formatting"
    )
    parser.add_argument(
        "--skip-regular",
        action="store_true",
        help="Skip regular Python file formatting"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check formatting without modifying files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install missing dependencies and exit"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Create formatter
    formatter = CodeFormatter(
        path=path,
        skip_databricks=args.skip_databricks,
        skip_regular=args.skip_regular,
        check_only=args.check,
        verbose=args.verbose,
    )

    # Scan files first to know what we need
    formatter.scan_files()

    # Check dependencies
    missing = formatter.check_dependencies()

    if args.install_deps or missing:
        if missing:
            print(f"Installing missing dependencies: {', '.join(missing)}")
            cmd = ["uv", "add", "--dev"] + missing
            subprocess.run(cmd, check=True)
            print("✓ Dependencies installed")

        if args.install_deps:
            sys.exit(0)

    # Format code
    success = formatter.format()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
