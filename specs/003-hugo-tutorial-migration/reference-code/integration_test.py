#!/usr/bin/env python3
"""
Integration Test for Enhanced Markdown Validation

This script tests the full validation pipeline:
1. Runs validation on test fixtures with known issues
2. Verifies issues are detected correctly
3. Applies auto-fixes
4. Optionally runs the actual XML conversion tool to verify fixes work

Usage:
    # Basic test (no XML conversion)
    python tests/integration_test.py

    # Full test with XML conversion (requires tutorial_md2xml binary)
    python tests/integration_test.py --with-xml-conversion

    # Test specific fixture
    python tests/integration_test.py --fixture tests/fixtures/integration

Requirements for XML conversion testing:
    - tutorial_md2xml binary in current directory or PATH
    - sol binary for Solomon XML validation (optional)
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import argparse
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from clean_markdown import (
    validate_folder,
    ValidationResult,
    Severity,
)


class IntegrationTest:
    """Run integration tests for markdown validation pipeline."""

    def __init__(self, fixture_path: str, work_dir: str = None):
        self.fixture_path = Path(fixture_path)
        self.work_dir = Path(work_dir) if work_dir else None
        self.results = {}

    def setup_work_directory(self) -> Path:
        """Copy fixtures to a temporary work directory."""
        if self.work_dir:
            work_path = self.work_dir
            if work_path.exists():
                shutil.rmtree(work_path)
        else:
            work_path = Path(tempfile.mkdtemp(prefix="md_integration_"))

        shutil.copytree(self.fixture_path, work_path, dirs_exist_ok=True)
        print(f"Work directory: {work_path}")
        return work_path

    def run_validation(self, folder: Path, auto_fix: bool = False) -> ValidationResult:
        """Run markdown validation on a folder."""
        result = validate_folder(str(folder), auto_fix=auto_fix, skip_ai=True)
        return result

    def run_xml_conversion(self, folder: Path) -> tuple[bool, str]:
        """
        Run the tutorial_md2xml tool to convert markdown to XML.

        Returns:
            Tuple of (success, output/error message)
        """
        # Look for tutorial_md2xml binary
        md2xml_paths = [
            Path("./tutorial_md2xml"),
            Path("./tutorial_md2xml.exe"),
            Path("/usr/local/bin/tutorial_md2xml"),
        ]

        md2xml_bin = None
        for path in md2xml_paths:
            if path.exists():
                md2xml_bin = path
                break

        if not md2xml_bin:
            # Try PATH
            md2xml_bin = shutil.which("tutorial_md2xml")

        if not md2xml_bin:
            return False, "tutorial_md2xml binary not found. Download from LearningAtCisco/tutorial-md-to-xml releases."

        try:
            result = subprocess.run(
                [str(md2xml_bin), str(folder)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr or result.stdout

        except subprocess.TimeoutExpired:
            return False, "XML conversion timed out"
        except Exception as e:
            return False, f"XML conversion failed: {e}"

    def run_solomon_lint(self, xml_file: Path) -> tuple[bool, str]:
        """
        Run Solomon XML linting on the converted XML.

        Returns:
            Tuple of (success, output/error message)
        """
        sol_bin = shutil.which("sol") or Path("./sol")

        if not Path(sol_bin).exists() and not shutil.which("sol"):
            return False, "sol binary not found"

        try:
            result = subprocess.run(
                [str(sol_bin), "solomon", "lint", str(xml_file)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr or result.stdout

        except Exception as e:
            return False, f"Solomon lint failed: {e}"

    def test_detection(self, work_dir: Path) -> dict:
        """Test that validation detects expected issues."""
        print("\n" + "=" * 60)
        print("TEST: Issue Detection")
        print("=" * 60)

        result = self.run_validation(work_dir, auto_fix=False)

        # Expected issues in step-2.md
        expected_rules = {
            "HTML_TAG",
            "LINK_NO_SPACE_BEFORE",
            "LINK_NO_SPACE_AFTER",
            "LINK_BROKEN",
            "LIST_INDENT_INCONSISTENT",
            "CODE_BLOCK_IN_LIST",
            "DOUBLE_SPACE",
        }

        detected_rules = {i.rule_id for i in result.issues}

        print(f"\nExpected rules: {sorted(expected_rules)}")
        print(f"Detected rules: {sorted(detected_rules)}")

        missing = expected_rules - detected_rules
        extra = detected_rules - expected_rules - {"TRAILING_WHITESPACE"}

        test_passed = len(missing) == 0

        if missing:
            print(f"\n❌ MISSING detection for: {missing}")
        if extra:
            print(f"\n⚠️  Extra detections (not necessarily wrong): {extra}")

        print(f"\nTotal issues found: {len(result.issues)}")
        print(f"  BLOCKING: {result.blocking_count}")
        print(f"  WARNING: {result.warning_count}")

        if test_passed:
            print("\n✅ Detection test PASSED")
        else:
            print("\n❌ Detection test FAILED")

        return {
            "passed": test_passed,
            "expected": expected_rules,
            "detected": detected_rules,
            "missing": missing,
            "issues": result.issues,
        }

    def test_autofix(self, work_dir: Path) -> dict:
        """Test that auto-fix resolves issues."""
        print("\n" + "=" * 60)
        print("TEST: Auto-Fix")
        print("=" * 60)

        # Run with auto-fix
        result_before = self.run_validation(work_dir, auto_fix=False)
        issues_before = len(result_before.issues)
        blocking_before = result_before.blocking_count

        print(f"\nBefore auto-fix: {issues_before} issues ({blocking_before} blocking)")

        # Apply fixes (skip AI for faster testing)
        result_fix = self.run_validation(work_dir, auto_fix=True)

        # Check again
        result_after = self.run_validation(work_dir, auto_fix=False)
        issues_after = len(result_after.issues)
        blocking_after = result_after.blocking_count

        print(f"After auto-fix: {issues_after} issues ({blocking_after} blocking)")

        fixed_count = issues_before - issues_after
        print(f"\nIssues fixed: {fixed_count}")

        if result_fix.files_modified:
            print(f"Files modified: {result_fix.files_modified}")

        # Test passes if blocking issues are reduced
        test_passed = blocking_after < blocking_before

        if test_passed:
            print("\n✅ Auto-fix test PASSED")
        else:
            print("\n❌ Auto-fix test FAILED")

        # Show remaining issues
        if result_after.issues:
            print("\nRemaining issues (may require AI or manual fix):")
            for issue in result_after.issues[:10]:
                print(f"  - {issue.rule_id}: {issue.message[:60]}...")

        return {
            "passed": test_passed,
            "issues_before": issues_before,
            "issues_after": issues_after,
            "fixed_count": fixed_count,
            "remaining_issues": result_after.issues,
        }

    def test_xml_conversion(self, work_dir: Path) -> dict:
        """Test that fixed markdown converts to XML successfully."""
        print("\n" + "=" * 60)
        print("TEST: XML Conversion")
        print("=" * 60)

        success, output = self.run_xml_conversion(work_dir)

        if success:
            print("\n✅ XML conversion PASSED")

            # Check for data.xml
            xml_file = work_dir / "data.xml"
            if xml_file.exists():
                print(f"Output file: {xml_file}")
                print(f"File size: {xml_file.stat().st_size} bytes")

                # Optionally run Solomon lint
                sol_success, sol_output = self.run_solomon_lint(xml_file)
                if sol_success:
                    print("Solomon lint: PASSED")
                else:
                    print(f"Solomon lint: {sol_output[:200]}")
        else:
            print(f"\n❌ XML conversion FAILED")
            print(f"Error: {output[:500]}")

        return {
            "passed": success,
            "output": output,
        }

    def run_all_tests(self, with_xml: bool = False) -> bool:
        """Run all integration tests."""
        print("\n" + "=" * 60)
        print("MARKDOWN VALIDATION INTEGRATION TEST")
        print("=" * 60)
        print(f"Fixture: {self.fixture_path}")

        # Setup
        work_dir = self.setup_work_directory()

        try:
            # Test 1: Detection
            self.results["detection"] = self.test_detection(work_dir)

            # Reset for auto-fix test
            if self.results["detection"]["passed"]:
                shutil.rmtree(work_dir)
                work_dir = self.setup_work_directory()

            # Test 2: Auto-fix
            self.results["autofix"] = self.test_autofix(work_dir)

            # Test 3: XML conversion (optional)
            if with_xml:
                self.results["xml_conversion"] = self.test_xml_conversion(work_dir)

            # Summary
            print("\n" + "=" * 60)
            print("TEST SUMMARY")
            print("=" * 60)

            all_passed = True
            for test_name, result in self.results.items():
                status = "✅ PASS" if result.get("passed") else "❌ FAIL"
                print(f"  {test_name}: {status}")
                if not result.get("passed"):
                    all_passed = False

            print("\n" + ("✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"))

            return all_passed

        finally:
            # Cleanup (optional - keep for debugging)
            if os.environ.get("KEEP_WORK_DIR") != "1":
                print(f"\nCleaning up: {work_dir}")
                # shutil.rmtree(work_dir)
                print(f"(Set KEEP_WORK_DIR=1 to preserve work directory)")


def main():
    parser = argparse.ArgumentParser(description="Integration test for markdown validation")
    parser.add_argument(
        "--fixture",
        default="tests/fixtures/integration",
        help="Path to test fixture directory"
    )
    parser.add_argument(
        "--with-xml-conversion",
        action="store_true",
        help="Run XML conversion test (requires tutorial_md2xml binary)"
    )
    parser.add_argument(
        "--work-dir",
        help="Specific work directory (default: temp directory)"
    )

    args = parser.parse_args()

    # Find fixture path
    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        # Try relative to script
        fixture_path = Path(__file__).parent / args.fixture
    if not fixture_path.exists():
        # Try relative to repo root
        fixture_path = Path(__file__).parent.parent / args.fixture

    if not fixture_path.exists():
        print(f"Error: Fixture not found: {args.fixture}")
        sys.exit(1)

    test = IntegrationTest(
        fixture_path=str(fixture_path),
        work_dir=args.work_dir
    )

    success = test.run_all_tests(with_xml=args.with_xml_conversion)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
