#!/usr/bin/env python3
"""
Run pytest with coverage and generate comprehensive reports.

This script provides a convenient wrapper around pytest with sensible defaults
for coverage reporting, HTML output, and result summarization.
"""

import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Manages pytest execution and coverage reporting."""

    def __init__(
        self,
        test_path: Optional[Path] = None,
        source_dir: str = "src",
        coverage: bool = True,
        html_report: bool = False,
        verbose: bool = False,
        markers: Optional[str] = None,
        keyword: Optional[str] = None,
    ):
        self.test_path = test_path or Path("tests")
        self.source_dir = source_dir
        self.coverage = coverage
        self.html_report = html_report
        self.verbose = verbose
        self.markers = markers
        self.keyword = keyword

    def build_command(self) -> List[str]:
        """Build the pytest command with all options."""
        cmd = ["uv", "run", "pytest"]

        # Add test path
        cmd.append(str(self.test_path))

        # Verbosity
        if self.verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        # Add coverage options
        if self.coverage:
            cmd.extend([
                f"--cov={self.source_dir}",
                "--cov-report=term-missing",
            ])

            if self.html_report:
                cmd.append("--cov-report=html")

        # Add marker filter
        if self.markers:
            cmd.extend(["-m", self.markers])

        # Add keyword filter
        if self.keyword:
            cmd.extend(["-k", self.keyword])

        # Additional useful options
        cmd.extend([
            "--strict-markers",  # Error on unknown markers
            "-ra",  # Show summary of all results except passed
            "--tb=short",  # Shorter traceback format
        ])

        return cmd

    def run(self) -> int:
        """Execute pytest and return exit code."""
        cmd = self.build_command()

        print("Running tests...")
        print(f"Command: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(cmd, check=False)
            return_code = result.returncode

            # Open HTML report if requested and tests passed
            if self.html_report and return_code == 0:
                html_path = Path("htmlcov/index.html")
                if html_path.exists():
                    print(f"\n✓ Coverage HTML report generated: {html_path}")
                    print("  Opening in browser...")
                    webbrowser.open(f"file://{html_path.absolute()}")

            return return_code

        except FileNotFoundError:
            print("Error: 'uv' command not found.", file=sys.stderr)
            print("Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\n\nTests interrupted by user.", file=sys.stderr)
            return 130

    def check_dependencies(self) -> bool:
        """Check if required test dependencies are installed."""
        try:
            result = subprocess.run(
                ["uv", "pip", "list"],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout

            required = ["pytest", "pytest-cov"]
            missing = [dep for dep in required if dep not in output.lower()]

            if missing:
                print(f"Missing dependencies: {', '.join(missing)}")
                print("\nInstall them with:")
                print(f"  uv add --dev {' '.join(missing)}")
                return False

            return True

        except (FileNotFoundError, subprocess.CalledProcessError):
            return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run pytest with coverage reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests with coverage
  python run_tests.py --coverage

  # Run specific test file
  python run_tests.py tests/test_auth.py

  # Run with HTML coverage report
  python run_tests.py --coverage --html

  # Run tests matching a keyword
  python run_tests.py -k "authentication"

  # Run tests with specific marker
  python run_tests.py -m "slow"

  # Verbose output
  python run_tests.py -v
        """
    )

    parser.add_argument(
        "path",
        nargs="?",
        default="tests",
        help="Path to test file or directory (default: tests/)"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        default=True,
        help="Generate coverage report (default: enabled)"
    )
    parser.add_argument(
        "--no-coverage",
        dest="coverage",
        action="store_false",
        help="Disable coverage reporting"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML coverage report and open in browser"
    )
    parser.add_argument(
        "-s", "--source",
        default="src",
        help="Source directory for coverage (default: src)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose test output"
    )
    parser.add_argument(
        "-m", "--markers",
        type=str,
        help="Run tests matching given mark expression (e.g., 'slow', 'not slow')"
    )
    parser.add_argument(
        "-k", "--keyword",
        type=str,
        help="Run tests matching given keyword expression"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check if required dependencies are installed"
    )

    args = parser.parse_args()

    runner = TestRunner(
        test_path=Path(args.path) if args.path else None,
        source_dir=args.source,
        coverage=args.coverage,
        html_report=args.html,
        verbose=args.verbose,
        markers=args.markers,
        keyword=args.keyword,
    )

    # Check dependencies if requested
    if args.check_deps:
        if runner.check_dependencies():
            print("✓ All required dependencies are installed")
            return 0
        else:
            return 1

    # Check dependencies before running
    if not runner.check_dependencies():
        print("\nPlease install missing dependencies before running tests.")
        return 1

    # Run tests
    exit_code = runner.run()

    # Print summary
    if exit_code == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ Tests failed with exit code {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
