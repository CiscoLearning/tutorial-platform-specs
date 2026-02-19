#!/usr/bin/env python3
"""
Test markdown validation against real tutorials from ciscou-tutorial-content.

This script:
1. Scans all tc-* folders in a tutorial repository
2. Runs validation on each tutorial
3. Reports issues found (without modifying files)
4. Identifies potential false positives

Usage:
    # Test against local clone of ciscou-tutorial-content
    python tests/test_real_tutorials.py /path/to/ciscou-tutorial-content

    # Test with auto-fix to see what would change
    python tests/test_real_tutorials.py /path/to/ciscou-tutorial-content --dry-run-fix

    # Test specific tutorial
    python tests/test_real_tutorials.py /path/to/ciscou-tutorial-content/tc-example

    # Output as JSON for analysis
    python tests/test_real_tutorials.py /path/to/ciscou-tutorial-content --json > results.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from clean_markdown import validate_folder, Severity


def find_tutorials(repo_path: Path) -> list[Path]:
    """Find all tc-* tutorial folders in the repository."""
    tutorials = []

    for item in repo_path.iterdir():
        if item.is_dir() and item.name.startswith("tc-"):
            tutorials.append(item)

    return sorted(tutorials)


def analyze_tutorials(tutorials: list[Path], dry_run_fix: bool = False) -> dict:
    """
    Analyze all tutorials and collect issue statistics.

    Returns:
        Dictionary with analysis results
    """
    results = {
        "total_tutorials": len(tutorials),
        "tutorials_with_issues": 0,
        "tutorials_with_blocking": 0,
        "total_issues": 0,
        "total_blocking": 0,
        "total_warnings": 0,
        "issues_by_rule": defaultdict(int),
        "tutorials_by_status": defaultdict(list),
        "tutorial_details": [],
    }

    for i, tutorial_path in enumerate(tutorials, 1):
        print(f"\r[{i}/{len(tutorials)}] Scanning {tutorial_path.name}...", end="", flush=True)

        try:
            result = validate_folder(str(tutorial_path), auto_fix=False, skip_ai=True)

            tutorial_info = {
                "name": tutorial_path.name,
                "path": str(tutorial_path),
                "issues": len(result.issues),
                "blocking": result.blocking_count,
                "warnings": result.warning_count,
                "issue_types": list(set(i.rule_id for i in result.issues)),
            }

            if result.issues:
                results["tutorials_with_issues"] += 1

            if result.blocking_count > 0:
                results["tutorials_with_blocking"] += 1
                results["tutorials_by_status"]["blocking"].append(tutorial_path.name)
            elif result.warning_count > 0:
                results["tutorials_by_status"]["warnings_only"].append(tutorial_path.name)
            else:
                results["tutorials_by_status"]["clean"].append(tutorial_path.name)

            results["total_issues"] += len(result.issues)
            results["total_blocking"] += result.blocking_count
            results["total_warnings"] += result.warning_count

            for issue in result.issues:
                results["issues_by_rule"][issue.rule_id] += 1

            # Add sample issues for debugging
            if result.issues and len(tutorial_info.get("sample_issues", [])) < 3:
                tutorial_info["sample_issues"] = [
                    {
                        "rule": i.rule_id,
                        "file": os.path.basename(i.file_path),
                        "line": i.line_number,
                        "message": i.message[:100],
                    }
                    for i in result.issues[:3]
                ]

            results["tutorial_details"].append(tutorial_info)

        except Exception as e:
            results["tutorial_details"].append({
                "name": tutorial_path.name,
                "error": str(e),
            })

    print()  # New line after progress
    return results


def print_report(results: dict):
    """Print a human-readable report."""
    print("\n" + "=" * 70)
    print("TUTORIAL VALIDATION REPORT")
    print("=" * 70)

    print(f"\nTotal tutorials scanned: {results['total_tutorials']}")
    print(f"Tutorials with issues: {results['tutorials_with_issues']}")
    print(f"Tutorials with blocking issues: {results['tutorials_with_blocking']}")

    print(f"\nTotal issues found: {results['total_issues']}")
    print(f"  BLOCKING: {results['total_blocking']}")
    print(f"  WARNING: {results['total_warnings']}")

    print("\n" + "-" * 70)
    print("ISSUES BY RULE:")
    print("-" * 70)

    for rule, count in sorted(results["issues_by_rule"].items(), key=lambda x: -x[1]):
        print(f"  {rule}: {count}")

    if results["tutorials_by_status"]["blocking"]:
        print("\n" + "-" * 70)
        print("TUTORIALS WITH BLOCKING ISSUES:")
        print("-" * 70)
        for name in results["tutorials_by_status"]["blocking"][:20]:
            print(f"  - {name}")
        if len(results["tutorials_by_status"]["blocking"]) > 20:
            print(f"  ... and {len(results['tutorials_by_status']['blocking']) - 20} more")

    # Clean tutorials
    clean_count = len(results["tutorials_by_status"]["clean"])
    print(f"\n✅ Clean tutorials (no issues): {clean_count}")

    # Potential false positives analysis
    if results["total_tutorials"] > 0:
        blocking_rate = results["tutorials_with_blocking"] / results["total_tutorials"] * 100
        print(f"\nBlocking issue rate: {blocking_rate:.1f}%")

        if blocking_rate > 50:
            print("⚠️  High blocking rate - check for potential false positives!")
        elif blocking_rate > 20:
            print("⚠️  Moderate blocking rate - review sample issues")
        else:
            print("✅ Blocking rate looks reasonable")


def main():
    parser = argparse.ArgumentParser(
        description="Test markdown validation against real tutorials"
    )
    parser.add_argument(
        "path",
        help="Path to tutorial repository or specific tc-* folder"
    )
    parser.add_argument(
        "--dry-run-fix",
        action="store_true",
        help="Show what auto-fix would change (doesn't modify files)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of tutorials to scan"
    )

    args = parser.parse_args()

    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path not found: {path}")
        sys.exit(1)

    # Determine if this is a single tutorial or a repo
    if path.name.startswith("tc-"):
        tutorials = [path]
    else:
        tutorials = find_tutorials(path)

    if not tutorials:
        print(f"No tutorials found in: {path}")
        sys.exit(1)

    if args.limit:
        tutorials = tutorials[:args.limit]

    print(f"Found {len(tutorials)} tutorial(s) to scan")

    results = analyze_tutorials(tutorials, dry_run_fix=args.dry_run_fix)

    if args.json:
        # Convert defaultdicts to regular dicts for JSON
        results["issues_by_rule"] = dict(results["issues_by_rule"])
        results["tutorials_by_status"] = dict(results["tutorials_by_status"])
        print(json.dumps(results, indent=2))
    else:
        print_report(results)


if __name__ == "__main__":
    main()
