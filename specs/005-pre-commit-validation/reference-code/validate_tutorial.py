#!/usr/bin/env python3
"""
Local validation tool for tutorial folders.

Run this script before pushing to catch issues early and reduce CI failures.
Designed for power users who have a local development environment.

Usage:
    # Basic validation
    python tools/validate_tutorial.py tc-my-tutorial/

    # With auto-fix (markdown + GUIDs)
    python tools/validate_tutorial.py tc-my-tutorial/ --fix

    # Quick mode (skip URL checking)
    python tools/validate_tutorial.py tc-my-tutorial/ --quick

    # Auto-detect tutorial folder (run from within tc-* folder)
    python tools/validate_tutorial.py

Exit codes:
    0 - All validations passed
    1 - Validation failures found
    2 - Error (missing files, invalid input)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def supports_color() -> bool:
    """Check if terminal supports colors."""
    if os.environ.get('NO_COLOR'):
        return False
    if not hasattr(sys.stdout, 'isatty'):
        return False
    return sys.stdout.isatty()


USE_COLORS = supports_color()


def colorize(text: str, color: str) -> str:
    """Apply color to text if colors are supported."""
    if USE_COLORS:
        return f"{color}{text}{Colors.RESET}"
    return text


def print_header(text: str):
    """Print a section header."""
    print(f"\n{colorize(text, Colors.BOLD + Colors.BLUE)}")


def print_success(text: str):
    """Print a success message."""
    print(f"  {colorize('✓', Colors.GREEN)} {text}")


def print_error(text: str):
    """Print an error message."""
    print(f"  {colorize('✗', Colors.RED)} {text}")


def print_warning(text: str):
    """Print a warning message."""
    print(f"  {colorize('⚠', Colors.YELLOW)} {text}")


def print_info(text: str):
    """Print an info message."""
    print(f"  {colorize('→', Colors.CYAN)} {text}")


def find_tutorial_folder() -> Optional[Path]:
    """Auto-detect tutorial folder from current directory."""
    cwd = Path.cwd()

    # Check if we're in a tc-* folder
    if cwd.name.startswith('tc-'):
        return cwd

    # Check if we're in the repo root with tc-* folders
    tc_folders = list(cwd.glob('tc-*'))
    if len(tc_folders) == 1:
        return tc_folders[0]

    return None


def validate_folder_structure(tutorial_path: Path) -> list:
    """Validate folder naming and structure."""
    errors = []

    # Check tc-* naming
    if not tutorial_path.name.startswith('tc-'):
        errors.append(f"Folder must start with 'tc-': {tutorial_path.name}")

    # Check images folder exists
    images_dir = tutorial_path / "images"
    if not images_dir.exists():
        errors.append("Missing required 'images' folder")

    # Check sidecar.json exists
    sidecar_file = tutorial_path / "sidecar.json"
    if not sidecar_file.exists():
        errors.append("Missing required 'sidecar.json'")

    # Check step files exist
    step_files = list(tutorial_path.glob("step-*.md"))
    if len(step_files) < 3:
        errors.append(f"Minimum 3 step files required, found {len(step_files)}")

    return errors


def validate_schema(tutorial_path: Path) -> tuple:
    """Run schema validation on sidecar.json."""
    tools_dir = Path(__file__).parent
    schema_script = tools_dir / "schema_validation.py"

    if not schema_script.exists():
        return [], ["schema_validation.py not found"]

    sidecar_path = tutorial_path / "sidecar.json"
    result = subprocess.run(
        [sys.executable, str(schema_script), str(sidecar_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Parse error output
        errors = []
        for line in result.stdout.split('\n'):
            if 'validation failed' in line.lower() or 'error' in line.lower():
                errors.append(line.strip())
        if not errors:
            errors = [result.stdout.strip() or result.stderr.strip()]
        return errors, []

    return [], []


def validate_guids(tutorial_path: Path, fix: bool = False) -> tuple:
    """Check and optionally fix GUID issues."""
    tools_dir = Path(__file__).parent
    guid_script = tools_dir / "guid_generator.py"

    if not guid_script.exists():
        return [], ["guid_generator.py not found"]

    sidecar_path = tutorial_path / "sidecar.json"
    cache_path = tools_dir / "guid_cache.json"

    args = [sys.executable, str(guid_script), str(sidecar_path), "--json"]
    if cache_path.exists():
        args.extend(["--cache", str(cache_path)])
    if fix:
        args.append("--fix")

    result = subprocess.run(args, capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
        issues = data.get('issues', [])
        errors = []
        warnings = []

        for issue in issues:
            field = issue.get('field', '')
            issue_type = issue.get('issue_type', '')
            file_name = issue.get('file_name', '')
            new_value = issue.get('new_value')

            location = f"{file_name}/{field}" if file_name else field
            msg = f"{location}: {issue_type.upper()}"

            if fix and new_value:
                warnings.append(f"{msg} -> Generated: {new_value[:8]}...")
            else:
                errors.append(msg)

        return errors, warnings
    except json.JSONDecodeError:
        if result.returncode != 0:
            return [result.stdout.strip() or "GUID check failed"], []
        return [], []


def validate_content(tutorial_path: Path, quick: bool = False) -> tuple:
    """Run pytest validation checks."""
    tools_dir = Path(__file__).parent
    pytest_script = tools_dir / "pytest_validation.py"

    if not pytest_script.exists():
        return [], ["pytest_validation.py not found"]

    # Set environment variables
    env = os.environ.copy()
    env['SIDECAR_FILE'] = str(tutorial_path / "sidecar.json")
    env['FOLDER_NAME'] = tutorial_path.name
    env['EXISTING_FOLDER'] = 'false'

    # Build pytest args
    args = [sys.executable, "-m", "pytest", str(pytest_script), "-v", "--tb=no", "-q"]

    if quick:
        # Skip URL checking tests
        args.extend(["-k", "not broken_links"])

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        env=env,
        cwd=tools_dir.parent
    )

    errors = []
    warnings = []

    # Parse pytest output for failures
    for line in result.stdout.split('\n'):
        if 'FAILED' in line:
            # Extract test name and reason
            test_match = line.split('::')[-1].split(' ')[0] if '::' in line else line
            errors.append(f"Test failed: {test_match}")
        elif 'PASSED' in line:
            continue
        elif 'SKIPPED' in line:
            warnings.append(line.strip())

    if result.returncode != 0 and not errors:
        errors.append("Content validation failed")

    return errors, warnings


def validate_markdown(tutorial_path: Path, fix: bool = False) -> tuple:
    """Run markdown validation and optional cleanup."""
    tools_dir = Path(__file__).parent
    clean_script = tools_dir / "clean_markdown.py"

    if not clean_script.exists():
        return [], ["clean_markdown.py not found"]

    args = [sys.executable, str(clean_script), str(tutorial_path), "--json"]
    if not fix:
        args.append("--no-fix")

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=tools_dir.parent
    )

    errors = []
    warnings = []

    try:
        data = json.loads(result.stdout)

        blocking = data.get('blocking_issues', [])
        warning_issues = data.get('warning_issues', [])
        auto_fixed = data.get('auto_fixed', [])

        for issue in blocking:
            file_name = issue.get('file', '')
            line = issue.get('line', 0)
            rule = issue.get('rule', '')
            msg = f"{file_name}:{line} - {rule}"
            if fix and issue.get('fixed'):
                warnings.append(f"{msg} (auto-fixed)")
            else:
                errors.append(msg)

        for issue in warning_issues:
            file_name = issue.get('file', '')
            line = issue.get('line', 0)
            rule = issue.get('rule', '')
            warnings.append(f"{file_name}:{line} - {rule}")

        for fixed in auto_fixed:
            warnings.append(f"Auto-fixed: {fixed}")

    except json.JSONDecodeError:
        # Fall back to text parsing
        if 'BLOCKING' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'BLOCKING' in line or 'ERROR' in line:
                    errors.append(line.strip())

    return errors, warnings


def run_validation(tutorial_path: Path, fix: bool = False, quick: bool = False) -> bool:
    """Run all validations and return True if passed."""
    print(f"\n{colorize('='*60, Colors.BOLD)}")
    print(f"{colorize(f'Validating: {tutorial_path.name}', Colors.BOLD)}")
    print(f"{colorize('='*60, Colors.BOLD)}")

    all_passed = True
    total_errors = 0
    total_warnings = 0

    # Step 1: Folder Structure
    print_header("[1/5] Folder Structure")
    errors = validate_folder_structure(tutorial_path)
    if errors:
        for err in errors:
            print_error(err)
        all_passed = False
        total_errors += len(errors)
        print(f"\n{colorize('Stopping: Fix folder structure issues first.', Colors.RED)}")
        return False
    else:
        print_success("Folder structure valid")

    # Step 2: Schema Validation
    print_header("[2/5] Schema Validation")
    errors, warnings = validate_schema(tutorial_path)
    if errors:
        for err in errors:
            print_error(err)
        all_passed = False
        total_errors += len(errors)
    else:
        print_success("sidecar.json is valid")
    for warn in warnings:
        print_warning(warn)
        total_warnings += 1

    # Step 3: GUID Check
    print_header("[3/5] GUID Check")
    errors, warnings = validate_guids(tutorial_path, fix=fix)
    if errors:
        for err in errors:
            print_error(err)
        all_passed = False
        total_errors += len(errors)
        if not fix:
            print_info("Run with --fix to auto-generate new GUIDs")
    else:
        print_success("All GUIDs are valid and unique")
    for warn in warnings:
        print_warning(warn)
        total_warnings += 1

    # Step 4: Content Validation
    print_header("[4/5] Content Validation")
    errors, warnings = validate_content(tutorial_path, quick=quick)
    if errors:
        for err in errors:
            print_error(err)
        all_passed = False
        total_errors += len(errors)
    else:
        print_success("Content validation passed")
    for warn in warnings:
        print_warning(warn)
        total_warnings += 1

    # Step 5: Markdown Quality
    print_header("[5/5] Markdown Quality")
    errors, warnings = validate_markdown(tutorial_path, fix=fix)
    if errors:
        for err in errors:
            print_error(err)
        all_passed = False
        total_errors += len(errors)
        if not fix:
            print_info("Run with --fix to auto-fix markdown issues")
    else:
        print_success("Markdown quality check passed")
    for warn in warnings:
        print_warning(warn)
        total_warnings += 1

    # Summary
    print(f"\n{colorize('='*60, Colors.BOLD)}")

    if all_passed:
        if total_warnings > 0:
            print(f"{colorize('Result: PASSED', Colors.GREEN)} with {total_warnings} warning(s)")
        else:
            print(f"{colorize('Result: PASSED', Colors.GREEN)}")
        print(f"\n{colorize('Ready to push!', Colors.GREEN)} Run: git add . && git commit -m \"Your message\"")
    else:
        print(f"{colorize(f'Result: FAILED ({total_errors} error(s))', Colors.RED)}")
        if not fix:
            print(f"\n{colorize('Tip:', Colors.CYAN)} Run with --fix to auto-correct some issues")

    print(f"{colorize('='*60, Colors.BOLD)}\n")

    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Local validation tool for tutorial folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        help="Path to tutorial folder (auto-detected if not provided)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix markdown issues and generate missing GUIDs"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip slow checks (URL validation)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    args = parser.parse_args()

    # Handle color preference
    global USE_COLORS
    if args.no_color:
        USE_COLORS = False

    # Find tutorial path
    tutorial_path = args.path
    if not tutorial_path:
        tutorial_path = find_tutorial_folder()
        if not tutorial_path:
            print("Error: Could not auto-detect tutorial folder.", file=sys.stderr)
            print("Please specify the path: python tools/validate_tutorial.py tc-my-tutorial/", file=sys.stderr)
            sys.exit(2)

    # Validate path exists
    if not tutorial_path.exists():
        print(f"Error: Path does not exist: {tutorial_path}", file=sys.stderr)
        sys.exit(2)

    if not tutorial_path.is_dir():
        print(f"Error: Path is not a directory: {tutorial_path}", file=sys.stderr)
        sys.exit(2)

    # Run validation
    passed = run_validation(tutorial_path, fix=args.fix, quick=args.quick)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
