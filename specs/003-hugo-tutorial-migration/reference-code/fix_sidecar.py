#!/usr/bin/env python3
"""
Sidecar.json Auto-Fix Tool

Automatically fixes common sidecar.json issues:
- Duration mismatch between total and step durations
- Missing or invalid GUIDs
- Format corrections

Usage:
    python tools/fix_sidecar.py <folder_path> [--dry-run]
    python tools/fix_sidecar.py tc-example --dry-run  # Preview changes
    python tools/fix_sidecar.py tc-example            # Apply fixes
"""

import os
import sys
import json
import uuid
import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class SidecarFix:
    """Represents a fix applied to sidecar.json"""
    field: str
    old_value: str
    new_value: str
    description: str


def parse_duration_to_seconds(duration_str: str) -> int:
    """
    Parse duration string to total seconds.

    Supports formats:
    - "MM:SS" (step format)
    - "XmXXs" (e.g., "30m00s")
    - "XhXXmXXs" (e.g., "1h30m00s")
    """
    if not duration_str:
        return 0

    # Step format: "MM:SS"
    if ':' in duration_str:
        parts = duration_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    # Total format: "XhXXmXXs" or "XXmXXs"
    total = 0
    h_match = re.search(r'(\d+)h', duration_str)
    m_match = re.search(r'(\d+)m', duration_str)
    s_match = re.search(r'(\d+)s', duration_str)

    if h_match:
        total += int(h_match.group(1)) * 3600
    if m_match:
        total += int(m_match.group(1)) * 60
    if s_match:
        total += int(s_match.group(1))

    return total


def seconds_to_total_duration(seconds: int) -> str:
    """
    Convert seconds to total duration format (XhXXmXXs or XXmXXs).
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h{minutes:02d}m{secs:02d}s"
    else:
        return f"{minutes}m{secs:02d}s"


def check_duration_mismatch(sidecar: dict) -> Optional[Tuple[int, int, str]]:
    """
    Check if total duration matches sum of step durations.

    Returns:
        Tuple of (expected_seconds, actual_seconds, expected_format) or None if no mismatch
    """
    if 'duration' not in sidecar or 'files' not in sidecar:
        return None

    total_duration = sidecar['duration']
    total_seconds = parse_duration_to_seconds(total_duration)

    step_seconds = 0
    for file_entry in sidecar.get('files', []):
        step_duration = file_entry.get('duration', '0:00')
        step_seconds += parse_duration_to_seconds(step_duration)

    if total_seconds != step_seconds:
        expected_format = seconds_to_total_duration(step_seconds)
        return (step_seconds, total_seconds, expected_format)

    return None


def check_missing_guids(sidecar: dict) -> List[str]:
    """Check for missing or invalid GUIDs."""
    issues = []

    # Check top-level GUIDs
    for field in ['ia-guid', 'lesson-guid']:
        if field not in sidecar or not sidecar[field]:
            issues.append(f"Missing {field}")
        elif not is_valid_uuid(sidecar[field]):
            issues.append(f"Invalid {field}: {sidecar[field]}")

    # Check file xy-guids
    for i, file_entry in enumerate(sidecar.get('files', [])):
        if 'xy-guid' not in file_entry or not file_entry['xy-guid']:
            issues.append(f"Missing xy-guid in files[{i}]")
        elif not is_valid_uuid(file_entry['xy-guid']):
            issues.append(f"Invalid xy-guid in files[{i}]: {file_entry['xy-guid']}")

    return issues


def is_valid_uuid(s: str) -> bool:
    """Check if string is a valid UUID."""
    try:
        uuid.UUID(s)
        return True
    except (ValueError, AttributeError):
        return False


def fix_duration(sidecar: dict) -> Optional[SidecarFix]:
    """Fix duration mismatch by updating total to match step sum."""
    mismatch = check_duration_mismatch(sidecar)
    if not mismatch:
        return None

    expected_seconds, actual_seconds, expected_format = mismatch
    old_value = sidecar['duration']
    sidecar['duration'] = expected_format

    return SidecarFix(
        field='duration',
        old_value=old_value,
        new_value=expected_format,
        description=f"Fixed duration mismatch: {old_value} -> {expected_format} (sum of steps: {expected_seconds//60}m)"
    )


def fix_guids(sidecar: dict) -> List[SidecarFix]:
    """Fix missing or invalid GUIDs by generating new ones."""
    fixes = []

    for field in ['ia-guid', 'lesson-guid']:
        if field not in sidecar or not sidecar[field] or not is_valid_uuid(sidecar.get(field, '')):
            old_value = sidecar.get(field, '<missing>')
            new_value = str(uuid.uuid4()).lower()
            sidecar[field] = new_value
            fixes.append(SidecarFix(
                field=field,
                old_value=old_value,
                new_value=new_value,
                description=f"Generated new {field}"
            ))

    for i, file_entry in enumerate(sidecar.get('files', [])):
        if 'xy-guid' not in file_entry or not file_entry['xy-guid'] or not is_valid_uuid(file_entry.get('xy-guid', '')):
            old_value = file_entry.get('xy-guid', '<missing>')
            new_value = str(uuid.uuid4()).lower()
            file_entry['xy-guid'] = new_value
            fixes.append(SidecarFix(
                field=f'files[{i}].xy-guid',
                old_value=old_value,
                new_value=new_value,
                description=f"Generated new xy-guid for {file_entry.get('file', f'step-{i+1}.md')}"
            ))

    return fixes


def fix_sidecar(folder_path: str, dry_run: bool = False) -> dict:
    """
    Fix all issues in a sidecar.json file.

    Args:
        folder_path: Path to tutorial folder containing sidecar.json
        dry_run: If True, only report what would be fixed

    Returns:
        Dictionary with fix results
    """
    sidecar_path = Path(folder_path) / 'sidecar.json'

    if not sidecar_path.exists():
        return {'error': f'sidecar.json not found in {folder_path}'}

    with open(sidecar_path, 'r') as f:
        sidecar = json.load(f)

    all_fixes = []

    # Fix duration mismatch
    duration_fix = fix_duration(sidecar)
    if duration_fix:
        all_fixes.append(duration_fix)

    # Note: GUID fixes are optional - only run if explicitly requested
    # guid_fixes = fix_guids(sidecar)
    # all_fixes.extend(guid_fixes)

    result = {
        'folder': folder_path,
        'fixes': [{'field': f.field, 'old': f.old_value, 'new': f.new_value, 'desc': f.description} for f in all_fixes],
        'dry_run': dry_run,
        'fixed': False
    }

    if all_fixes and not dry_run:
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f, indent=2)
        result['fixed'] = True

    return result


def main():
    parser = argparse.ArgumentParser(description='Auto-fix sidecar.json issues')
    parser.add_argument('folder', help='Path to tutorial folder or tc-* name')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--fix-guids', action='store_true', help='Also fix missing/invalid GUIDs')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Resolve folder path
    folder_path = Path(args.folder)
    if not folder_path.exists():
        # Try as tc-* folder name in current directory
        folder_path = Path.cwd() / args.folder

    if not folder_path.exists():
        print(f"Error: Folder not found: {args.folder}", file=sys.stderr)
        sys.exit(1)

    result = fix_sidecar(str(folder_path), dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        if not result['fixes']:
            print(f"No issues found in {folder_path}")
        else:
            action = "Would fix" if args.dry_run else "Fixed"
            print(f"\n{action} {len(result['fixes'])} issue(s) in {folder_path}:")
            for fix in result['fixes']:
                print(f"  - {fix['desc']}")

            if args.dry_run:
                print("\nRun without --dry-run to apply fixes.")

    sys.exit(0 if not result.get('error') else 1)


if __name__ == '__main__':
    main()
