#!/usr/bin/env python3
"""
Generate pytest test templates from Python source files.

This script analyzes Python source files and generates comprehensive test templates
including fixtures, parametrized tests, and appropriate test cases.
"""

import argparse
import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any


class TestGenerator:
    """Generates pytest test files from Python source code."""

    def __init__(self, source_path: Path, output_dir: Path = None):
        self.source_path = source_path
        self.output_dir = output_dir or Path("tests")
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []
        self.imports: List[str] = []

    def analyze_source(self) -> None:
        """Analyze source file to extract functions and classes."""
        with open(self.source_path, 'r') as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions unless explicitly testing them
                if not node.name.startswith('_'):
                    self.functions.append(self._extract_function_info(node))

            elif isinstance(node, ast.ClassDef):
                # Skip private classes
                if not node.name.startswith('_'):
                    self.classes.append(self._extract_class_info(node))

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports.append(node.module)

    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Extract information about a function."""
        return {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
            'returns': self._get_return_type(node),
            'docstring': ast.get_docstring(node),
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
        }

    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Extract information about a class."""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                methods.append(self._extract_function_info(item))

        return {
            'name': node.name,
            'methods': methods,
            'docstring': ast.get_docstring(node),
            'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
        }

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation if present."""
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            elif isinstance(node.returns, ast.Constant):
                return str(node.returns.value)
        return "Any"

    def generate_test_file(self) -> str:
        """Generate complete test file content."""
        self.analyze_source()

        module_name = self.source_path.stem
        # Determine source module path (handle src/ structure)
        if 'src' in self.source_path.parts:
            src_index = self.source_path.parts.index('src')
            import_path_parts = self.source_path.parts[src_index + 1:]
            import_path = '.'.join(import_path_parts[:-1]) + '.' + module_name if len(import_path_parts) > 1 else module_name
        else:
            import_path = module_name

        lines = [
            f'"""Tests for {module_name} module."""',
            '',
            'import pytest',
        ]

        # Add imports based on what we detected
        if any('async' in str(f.get('decorators', [])) for f in self.functions):
            lines.append('import pytest_asyncio')

        # Add source module import
        lines.append(f'from {import_path} import (')

        imported_items = []
        for func in self.functions:
            imported_items.append(f"    {func['name']},")
        for cls in self.classes:
            imported_items.append(f"    {cls['name']},")

        lines.extend(imported_items)
        lines.append(')')
        lines.append('')
        lines.append('')

        # Generate fixtures if we have classes
        if self.classes:
            lines.extend(self._generate_fixtures())
            lines.append('')

        # Generate function tests
        for func in self.functions:
            lines.extend(self._generate_function_tests(func))
            lines.append('')

        # Generate class tests
        for cls in self.classes:
            lines.extend(self._generate_class_tests(cls))
            lines.append('')

        return '\n'.join(lines)

    def _generate_fixtures(self) -> List[str]:
        """Generate pytest fixtures for classes."""
        lines = ['# Fixtures', '']

        for cls in self.classes:
            fixture_name = cls['name'].lower().replace('_', '')
            lines.extend([
                '@pytest.fixture',
                f"def {fixture_name}():",
                f'    """Fixture for {cls["name"]} instances."""',
                f'    return {cls["name"]}()',
                '',
            ])

        return lines

    def _generate_function_tests(self, func: Dict[str, Any]) -> List[str]:
        """Generate tests for a standalone function."""
        lines = [
            f'# Tests for {func["name"]}',
            '',
        ]

        # Basic happy path test
        lines.extend([
            f'def test_{func["name"]}_normal_case():',
            f'    """Test {func["name"]} with valid inputs."""',
        ])

        if func['args']:
            # Generate sample arguments
            sample_args = ', '.join([f'{arg}=None' for arg in func['args']])
            lines.append(f'    # TODO: Replace None with appropriate test values')
            lines.append(f'    result = {func["name"]}({sample_args})')
        else:
            lines.append(f'    result = {func["name"]}()')

        lines.extend([
            f'    # TODO: Add assertions',
            f'    assert result is not None',
            '',
        ])

        # Edge case test
        if func['args']:
            lines.extend([
                f'def test_{func["name"]}_edge_cases():',
                f'    """Test {func["name"]} with edge case inputs."""',
                f'    # TODO: Test with empty, None, or boundary values',
                f'    pass',
                '',
            ])

        # Error case test
        lines.extend([
            f'def test_{func["name"]}_invalid_input():',
            f'    """Test {func["name"]} handles invalid input appropriately."""',
            f'    # TODO: Test error handling',
            f'    # with pytest.raises(ValueError):',
            f'    #     {func["name"]}(invalid_value)',
            f'    pass',
            '',
        ])

        # Parametrized test if function has arguments
        if func['args'] and len(func['args']) <= 3:
            param_str = ', '.join(func['args'])
            lines.extend([
                f'@pytest.mark.parametrize("{param_str}", [',
                f'    # TODO: Add test cases',
                f'    # (value1, value2, ...),',
                f'])',
                f'def test_{func["name"]}_parametrized({param_str}):',
                f'    """Test {func["name"]} with multiple input combinations."""',
                f'    result = {func["name"]}({param_str})',
                f'    assert result is not None',
                '',
            ])

        return lines

    def _generate_class_tests(self, cls: Dict[str, Any]) -> List[str]:
        """Generate tests for a class."""
        fixture_name = cls['name'].lower().replace('_', '')

        lines = [
            f'# Tests for {cls["name"]}',
            '',
            f'class Test{cls["name"]}:',
            f'    """Test suite for {cls["name"]}."""',
            '',
        ]

        # Test instantiation
        lines.extend([
            f'    def test_instantiation(self, {fixture_name}):',
            f'        """Test that {cls["name"]} can be instantiated."""',
            f'        assert {fixture_name} is not None',
            f'        assert isinstance({fixture_name}, {cls["name"]})',
            '',
        ])

        # Test each method
        for method in cls['methods']:
            if method['name'] == '__init__':
                continue

            lines.extend([
                f'    def test_{method["name"]}(self, {fixture_name}):',
                f'        """Test {cls["name"]}.{method["name"]} method."""',
            ])

            if method['args']:
                sample_args = ', '.join([f'{arg}=None' for arg in method['args']])
                lines.append(f'        # TODO: Replace None with appropriate test values')
                lines.append(f'        result = {fixture_name}.{method["name"]}({sample_args})')
            else:
                lines.append(f'        result = {fixture_name}.{method["name"]}()')

            lines.extend([
                f'        # TODO: Add assertions',
                f'        assert result is not None',
                '',
            ])

        return lines

    def save_test_file(self) -> Path:
        """Save generated test file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        test_filename = f"test_{self.source_path.stem}.py"
        test_path = self.output_dir / test_filename

        content = self.generate_test_file()

        with open(test_path, 'w') as f:
            f.write(content)

        return test_path


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate pytest test templates from Python source files"
    )
    parser.add_argument(
        "source",
        type=str,
        help="Path to Python source file or directory"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="tests",
        help="Output directory for test files (default: tests/)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    source_path = Path(args.source)
    output_dir = Path(args.output)

    if not source_path.exists():
        print(f"Error: Source path '{source_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Handle directory input
    if source_path.is_dir():
        python_files = list(source_path.rglob("*.py"))
        python_files = [f for f in python_files if not f.name.startswith('test_')]

        if not python_files:
            print(f"No Python files found in '{source_path}'", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(python_files)} Python file(s) to process")

        for py_file in python_files:
            if args.verbose:
                print(f"Processing: {py_file}")

            generator = TestGenerator(py_file, output_dir)
            test_file = generator.save_test_file()

            print(f"✓ Generated: {test_file}")

    # Handle single file input
    else:
        if not source_path.suffix == '.py':
            print("Error: Source must be a Python file (.py)", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            print(f"Processing: {source_path}")

        generator = TestGenerator(source_path, output_dir)
        test_file = generator.save_test_file()

        print(f"✓ Generated: {test_file}")
        print(f"\nNext steps:")
        print(f"1. Review and complete the TODOs in {test_file}")
        print(f"2. Run tests: uv run pytest {test_file}")
        print(f"3. Check coverage: uv run pytest --cov={source_path.stem} {test_file}")


if __name__ == "__main__":
    main()
