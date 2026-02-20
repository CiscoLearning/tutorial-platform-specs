#!/usr/bin/env python3
"""
Check and auto-generate GUIDs for tutorial sidecar.json files.

This script validates GUID fields in sidecar.json and can auto-generate
new UUIDs for missing, invalid, or duplicate GUIDs.

Usage:
    # Check only (report issues, don't fix)
    python tools/guid_generator.py tc-my-tutorial/sidecar.json

    # Fix mode (generate new GUIDs for issues)
    python tools/guid_generator.py tc-my-tutorial/sidecar.json --fix

    # JSON output for CI integration
    python tools/guid_generator.py tc-my-tutorial/sidecar.json --json

Exit codes:
    0 - All GUIDs valid (or fixed with --fix)
    1 - GUID issues found (check-only mode)
    2 - Error (file not found, invalid JSON, etc.)
"""

import argparse
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Optional


# UUID regex pattern (lowercase, with optional braces)
UUID_PATTERN = re.compile(
    r'^(?:\{)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?:\})?$',
    re.IGNORECASE
)


class GuidIssue:
    """Represents a GUID issue found in sidecar.json."""

    def __init__(self, field: str, issue_type: str, current_value: Optional[str] = None,
                 file_name: Optional[str] = None):
        self.field = field
        self.issue_type = issue_type  # 'missing', 'invalid', 'duplicate'
        self.current_value = current_value
        self.file_name = file_name  # For xy-guid, which file it belongs to
        self.new_value: Optional[str] = None

    def __repr__(self):
        if self.file_name:
            return f"GuidIssue({self.file_name}/{self.field}: {self.issue_type})"
        return f"GuidIssue({self.field}: {self.issue_type})"

    def to_dict(self):
        return {
            'field': self.field,
            'issue_type': self.issue_type,
            'current_value': self.current_value,
            'file_name': self.file_name,
            'new_value': self.new_value
        }


def generate_guid() -> str:
    """Generate a new lowercase UUID."""
    return str(uuid.uuid4()).lower()


def is_valid_guid(value: Optional[str]) -> bool:
    """Check if a value is a valid UUID format."""
    if not value or not isinstance(value, str):
        return False
    return bool(UUID_PATTERN.match(value.strip()))


def is_placeholder_guid(value: Optional[str]) -> bool:
    """Check if a value looks like a placeholder (not a real GUID)."""
    if not value or not isinstance(value, str):
        return True

    placeholders = [
        'todo', 'test', 'placeholder', 'xxx', 'guid', 'uuid',
        'replace', 'change', 'fill', 'add', 'new'
    ]
    lower_val = value.lower().strip()

    # Check for common placeholder patterns
    for placeholder in placeholders:
        if placeholder in lower_val:
            return True

    # Check if it's just a simple pattern like "123" or "abc"
    if len(lower_val) < 10:
        return True

    return False


def load_guid_cache(cache_path: Path) -> set:
    """Load existing GUIDs from cache file."""
    if not cache_path.exists():
        return set()

    try:
        with open(cache_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(g.lower() for g in data if isinstance(g, str))
    except (json.JSONDecodeError, IOError):
        pass

    return set()


def extract_guids_from_sidecar(sidecar: dict) -> dict:
    """Extract all GUID fields from sidecar.json."""
    guids = {}

    # Top-level GUIDs
    if 'ia-guid' in sidecar:
        guids['ia-guid'] = sidecar['ia-guid']
    if 'lesson-guid' in sidecar:
        guids['lesson-guid'] = sidecar['lesson-guid']

    # File-level GUIDs (xy-guid)
    for file_entry in sidecar.get('files', []):
        file_name = file_entry.get('file', 'unknown')
        if 'xy-guid' in file_entry:
            guids[f"files/{file_name}/xy-guid"] = file_entry['xy-guid']

    return guids


def check_guids(sidecar_path: Path, cache_path: Optional[Path] = None) -> list:
    """
    Check sidecar.json for GUID issues.

    Returns list of GuidIssue objects.
    """
    issues = []

    # Load sidecar
    try:
        with open(sidecar_path) as f:
            sidecar = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Failed to load sidecar: {e}")

    # Load cache for uniqueness checking
    known_guids = set()
    if cache_path:
        known_guids = load_guid_cache(cache_path)

    # Track GUIDs in this file for internal duplicate detection
    seen_guids = set()

    # Check top-level GUIDs
    for field in ['ia-guid', 'lesson-guid']:
        value = sidecar.get(field)

        if not value:
            issues.append(GuidIssue(field, 'missing'))
        elif is_placeholder_guid(value) and not is_valid_guid(value):
            issues.append(GuidIssue(field, 'invalid', value))
        elif not is_valid_guid(value):
            issues.append(GuidIssue(field, 'invalid', value))
        else:
            normalized = value.lower().strip()
            if normalized in seen_guids:
                issues.append(GuidIssue(field, 'duplicate', value))
            elif normalized in known_guids:
                issues.append(GuidIssue(field, 'duplicate', value))
            else:
                seen_guids.add(normalized)

    # Check file-level GUIDs
    for file_entry in sidecar.get('files', []):
        file_name = file_entry.get('file', 'unknown')
        value = file_entry.get('xy-guid')

        if not value:
            issues.append(GuidIssue('xy-guid', 'missing', file_name=file_name))
        elif is_placeholder_guid(value) and not is_valid_guid(value):
            issues.append(GuidIssue('xy-guid', 'invalid', value, file_name=file_name))
        elif not is_valid_guid(value):
            issues.append(GuidIssue('xy-guid', 'invalid', value, file_name=file_name))
        else:
            normalized = value.lower().strip()
            if normalized in seen_guids:
                issues.append(GuidIssue('xy-guid', 'duplicate', value, file_name=file_name))
            elif normalized in known_guids:
                issues.append(GuidIssue('xy-guid', 'duplicate', value, file_name=file_name))
            else:
                seen_guids.add(normalized)

    return issues


def fix_guids(sidecar_path: Path, issues: list) -> dict:
    """
    Fix GUID issues by generating new UUIDs.

    Returns dict with changes made.
    """
    # Load sidecar
    with open(sidecar_path) as f:
        sidecar = json.load(f)

    changes = []

    for issue in issues:
        new_guid = generate_guid()
        issue.new_value = new_guid

        if issue.field in ['ia-guid', 'lesson-guid']:
            sidecar[issue.field] = new_guid
            changes.append({
                'field': issue.field,
                'old': issue.current_value,
                'new': new_guid,
                'reason': issue.issue_type
            })
        elif issue.field == 'xy-guid' and issue.file_name:
            for file_entry in sidecar.get('files', []):
                if file_entry.get('file') == issue.file_name:
                    file_entry['xy-guid'] = new_guid
                    changes.append({
                        'field': f"{issue.file_name}/xy-guid",
                        'old': issue.current_value,
                        'new': new_guid,
                        'reason': issue.issue_type
                    })
                    break

    # Write updated sidecar
    with open(sidecar_path, 'w') as f:
        json.dump(sidecar, f, indent=2)
        f.write('\n')  # Trailing newline

    return {'changes': changes, 'file': str(sidecar_path)}


def print_issues(issues: list, verbose: bool = False):
    """Print GUID issues in human-readable format."""
    if not issues:
        print("All GUIDs are valid.")
        return

    print(f"Found {len(issues)} GUID issue(s):\n")

    for issue in issues:
        location = issue.file_name or issue.field
        if issue.file_name:
            location = f"{issue.file_name}/{issue.field}"

        if issue.issue_type == 'missing':
            print(f"  - {location}: MISSING")
        elif issue.issue_type == 'invalid':
            print(f"  - {location}: INVALID ({issue.current_value})")
        elif issue.issue_type == 'duplicate':
            print(f"  - {location}: DUPLICATE ({issue.current_value})")

        if issue.new_value:
            print(f"    -> Generated: {issue.new_value}")


def main():
    parser = argparse.ArgumentParser(
        description="Check and auto-generate GUIDs for tutorial sidecar.json files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "sidecar_path",
        type=Path,
        help="Path to sidecar.json file"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Generate new GUIDs for issues (default: check only)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--cache",
        type=Path,
        help="Path to guid_cache.json for uniqueness checking"
    )
    parser.add_argument(
        "--set-output",
        action="store_true",
        help="Set GitHub Actions output variables"
    )

    args = parser.parse_args()

    # Validate input
    if not args.sidecar_path.exists():
        print(f"Error: File not found: {args.sidecar_path}", file=sys.stderr)
        sys.exit(2)

    # Find cache file if not specified
    cache_path = args.cache
    if not cache_path:
        # Look for cache in tools/ relative to sidecar
        tools_dir = args.sidecar_path.parent.parent / 'tools'
        if tools_dir.exists():
            potential_cache = tools_dir / 'guid_cache.json'
            if potential_cache.exists():
                cache_path = potential_cache

    try:
        # Check for issues
        issues = check_guids(args.sidecar_path, cache_path)

        result = {
            'file': str(args.sidecar_path),
            'issues_found': len(issues),
            'issues': [i.to_dict() for i in issues],
            'fixed': False,
            'changes': []
        }

        if issues and args.fix:
            fix_result = fix_guids(args.sidecar_path, issues)
            result['fixed'] = True
            result['changes'] = fix_result['changes']

        # Output
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if issues:
                print_issues(issues)
                if args.fix:
                    print(f"\nFixed {len(issues)} issue(s) in {args.sidecar_path}")
                else:
                    print(f"\nRun with --fix to auto-generate new GUIDs.")
            else:
                print(f"All GUIDs are valid in {args.sidecar_path}")

        # GitHub Actions output
        if args.set_output:
            github_output = os.environ.get('GITHUB_OUTPUT', '')
            if github_output:
                with open(github_output, 'a') as f:
                    f.write(f"guids_updated={'true' if result['fixed'] else 'false'}\n")
                    f.write(f"issues_found={len(issues)}\n")

        # Exit code
        if issues and not args.fix:
            sys.exit(1)
        sys.exit(0)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
