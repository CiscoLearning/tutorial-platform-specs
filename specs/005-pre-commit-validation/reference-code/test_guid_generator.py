#!/usr/bin/env python3
"""
Tests for guid_generator.py - GUID checking and auto-generation.

These tests verify the GUID validation and generation logic without
needing to create actual tutorials or run the full CI pipeline.
"""

import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

import pytest

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from guid_generator import (
    is_valid_guid,
    is_placeholder_guid,
    generate_guid,
    check_guids,
    fix_guids,
    load_guid_cache,
    GuidIssue
)


class TestGuidValidation:
    """Tests for GUID format validation."""

    def test_valid_uuid_lowercase(self):
        """Valid lowercase UUID should pass."""
        assert is_valid_guid("17a101eb-70b0-444a-9852-0667563ecc52")

    def test_valid_uuid_uppercase(self):
        """Valid uppercase UUID should pass."""
        assert is_valid_guid("17A101EB-70B0-444A-9852-0667563ECC52")

    def test_valid_uuid_mixed_case(self):
        """Valid mixed case UUID should pass."""
        assert is_valid_guid("17a101eb-70B0-444A-9852-0667563ecc52")

    def test_invalid_uuid_too_short(self):
        """Short string should fail."""
        assert not is_valid_guid("17a101eb-70b0")

    def test_invalid_uuid_wrong_format(self):
        """Wrong format should fail."""
        assert not is_valid_guid("not-a-uuid-at-all")

    def test_invalid_uuid_empty(self):
        """Empty string should fail."""
        assert not is_valid_guid("")

    def test_invalid_uuid_none(self):
        """None should fail."""
        assert not is_valid_guid(None)

    def test_invalid_uuid_number(self):
        """Number should fail."""
        assert not is_valid_guid(12345)


class TestPlaceholderDetection:
    """Tests for placeholder GUID detection."""

    def test_todo_placeholder(self):
        """'TODO' should be detected as placeholder."""
        assert is_placeholder_guid("TODO")
        assert is_placeholder_guid("todo")
        assert is_placeholder_guid("TODO-guid")

    def test_test_placeholder(self):
        """'test' strings should be detected as placeholder."""
        assert is_placeholder_guid("test-guid")
        assert is_placeholder_guid("test-ia-guid")

    def test_placeholder_word(self):
        """'placeholder' should be detected."""
        assert is_placeholder_guid("placeholder")

    def test_short_strings(self):
        """Short strings should be detected as placeholder."""
        assert is_placeholder_guid("abc")
        assert is_placeholder_guid("123")
        assert is_placeholder_guid("guid")

    def test_valid_uuid_not_placeholder(self):
        """Valid UUIDs should not be placeholders."""
        assert not is_placeholder_guid("17a101eb-70b0-444a-9852-0667563ecc52")

    def test_empty_is_placeholder(self):
        """Empty/None should be placeholder."""
        assert is_placeholder_guid("")
        assert is_placeholder_guid(None)


class TestGuidGeneration:
    """Tests for GUID generation."""

    def test_generates_valid_uuid(self):
        """Generated GUID should be valid UUID format."""
        guid = generate_guid()
        assert is_valid_guid(guid)

    def test_generates_lowercase(self):
        """Generated GUID should be lowercase."""
        guid = generate_guid()
        assert guid == guid.lower()

    def test_generates_unique(self):
        """Each call should generate unique GUID."""
        guids = [generate_guid() for _ in range(100)]
        assert len(set(guids)) == 100


class TestCheckGuids:
    """Tests for GUID checking in sidecar.json."""

    @pytest.fixture
    def valid_sidecar(self, tmp_path):
        """Create a valid sidecar.json for testing."""
        sidecar = {
            "id": "tc-test",
            "ia-guid": "17a101eb-70b0-444a-9852-0667563ecc52",
            "lesson-guid": "873fa67a-2cea-451d-a2d5-459798b68bb1",
            "files": [
                {"file": "step-1.md", "xy-guid": "2efacb5f-6bd9-4891-a156-b3e712f8bebf"},
                {"file": "step-2.md", "xy-guid": "f75ef5cd-4d2c-4bfe-a3b7-0be261be70cc"},
                {"file": "step-3.md", "xy-guid": "71d24778-08e0-4913-8911-e37a38d47487"}
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    @pytest.fixture
    def missing_guids_sidecar(self, tmp_path):
        """Create sidecar with missing GUIDs."""
        sidecar = {
            "id": "tc-test",
            "lesson-guid": "873fa67a-2cea-451d-a2d5-459798b68bb1",
            "files": [
                {"file": "step-1.md"},  # Missing xy-guid
                {"file": "step-2.md", "xy-guid": "f75ef5cd-4d2c-4bfe-a3b7-0be261be70cc"},
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    @pytest.fixture
    def invalid_guids_sidecar(self, tmp_path):
        """Create sidecar with invalid GUIDs."""
        sidecar = {
            "id": "tc-test",
            "ia-guid": "TODO",
            "lesson-guid": "invalid-guid",
            "files": [
                {"file": "step-1.md", "xy-guid": "test"},
                {"file": "step-2.md", "xy-guid": "placeholder"},
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    @pytest.fixture
    def duplicate_guids_sidecar(self, tmp_path):
        """Create sidecar with duplicate GUIDs."""
        duplicate_guid = "17a101eb-70b0-444a-9852-0667563ecc52"
        sidecar = {
            "id": "tc-test",
            "ia-guid": duplicate_guid,
            "lesson-guid": duplicate_guid,  # Duplicate!
            "files": [
                {"file": "step-1.md", "xy-guid": duplicate_guid},  # Duplicate!
                {"file": "step-2.md", "xy-guid": "f75ef5cd-4d2c-4bfe-a3b7-0be261be70cc"},
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    def test_valid_sidecar_no_issues(self, valid_sidecar):
        """Valid sidecar should have no issues."""
        issues = check_guids(valid_sidecar)
        assert len(issues) == 0

    def test_detects_missing_ia_guid(self, missing_guids_sidecar):
        """Should detect missing ia-guid."""
        issues = check_guids(missing_guids_sidecar)
        ia_issues = [i for i in issues if i.field == 'ia-guid']
        assert len(ia_issues) == 1
        assert ia_issues[0].issue_type == 'missing'

    def test_detects_missing_xy_guid(self, missing_guids_sidecar):
        """Should detect missing xy-guid in files."""
        issues = check_guids(missing_guids_sidecar)
        xy_issues = [i for i in issues if i.field == 'xy-guid']
        assert len(xy_issues) == 1
        assert xy_issues[0].file_name == 'step-1.md'

    def test_detects_invalid_guids(self, invalid_guids_sidecar):
        """Should detect invalid/placeholder GUIDs."""
        issues = check_guids(invalid_guids_sidecar)
        assert len(issues) == 4  # ia-guid, lesson-guid, 2 xy-guids
        assert all(i.issue_type == 'invalid' for i in issues)

    def test_detects_duplicate_guids(self, duplicate_guids_sidecar):
        """Should detect duplicate GUIDs within file."""
        issues = check_guids(duplicate_guids_sidecar)
        duplicate_issues = [i for i in issues if i.issue_type == 'duplicate']
        assert len(duplicate_issues) == 2  # lesson-guid and step-1 xy-guid


class TestGuidCache:
    """Tests for GUID cache functionality."""

    @pytest.fixture
    def guid_cache(self, tmp_path):
        """Create a test GUID cache."""
        cache = [
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "11111111-2222-3333-4444-555555555555"
        ]
        cache_path = tmp_path / "guid_cache.json"
        with open(cache_path, 'w') as f:
            json.dump(cache, f)
        return cache_path

    @pytest.fixture
    def sidecar_with_cached_guid(self, tmp_path):
        """Create sidecar using a GUID that's in the cache."""
        sidecar = {
            "id": "tc-test",
            "ia-guid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",  # In cache!
            "lesson-guid": "873fa67a-2cea-451d-a2d5-459798b68bb1",
            "files": []
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    def test_loads_cache(self, guid_cache):
        """Should load cache as set of lowercase GUIDs."""
        cache = load_guid_cache(guid_cache)
        assert len(cache) == 2
        assert "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee" in cache

    def test_detects_cache_duplicate(self, sidecar_with_cached_guid, guid_cache):
        """Should detect GUID that exists in cache."""
        issues = check_guids(sidecar_with_cached_guid, guid_cache)
        assert len(issues) == 1
        assert issues[0].field == 'ia-guid'
        assert issues[0].issue_type == 'duplicate'


class TestFixGuids:
    """Tests for GUID fixing/generation."""

    @pytest.fixture
    def broken_sidecar(self, tmp_path):
        """Create sidecar with various GUID issues."""
        sidecar = {
            "id": "tc-test",
            "ia-guid": "TODO",
            "lesson-guid": "",
            "files": [
                {"file": "step-1.md"},  # Missing xy-guid
                {"file": "step-2.md", "xy-guid": "valid-guid-here"},  # Invalid
                {"file": "step-3.md", "xy-guid": "17a101eb-70b0-444a-9852-0667563ecc52"}  # Valid
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)
        return sidecar_path

    def test_fixes_all_issues(self, broken_sidecar):
        """Should fix all GUID issues."""
        issues = check_guids(broken_sidecar)
        assert len(issues) == 4  # ia, lesson, step-1, step-2

        result = fix_guids(broken_sidecar, issues)
        assert result['changes']
        assert len(result['changes']) == 4

        # Verify file was updated
        with open(broken_sidecar) as f:
            fixed = json.load(f)

        assert is_valid_guid(fixed['ia-guid'])
        assert is_valid_guid(fixed['lesson-guid'])
        assert is_valid_guid(fixed['files'][0]['xy-guid'])
        assert is_valid_guid(fixed['files'][1]['xy-guid'])

    def test_preserves_valid_guids(self, broken_sidecar):
        """Should not change valid GUIDs."""
        original_valid = "17a101eb-70b0-444a-9852-0667563ecc52"

        issues = check_guids(broken_sidecar)
        fix_guids(broken_sidecar, issues)

        with open(broken_sidecar) as f:
            fixed = json.load(f)

        # step-3 had valid GUID, should be unchanged
        assert fixed['files'][2]['xy-guid'] == original_valid

    def test_generates_unique_guids(self, broken_sidecar):
        """All generated GUIDs should be unique."""
        issues = check_guids(broken_sidecar)
        fix_guids(broken_sidecar, issues)

        with open(broken_sidecar) as f:
            fixed = json.load(f)

        all_guids = [
            fixed['ia-guid'],
            fixed['lesson-guid'],
            fixed['files'][0]['xy-guid'],
            fixed['files'][1]['xy-guid'],
            fixed['files'][2]['xy-guid']
        ]

        assert len(set(all_guids)) == len(all_guids)


class TestNewTutorialFlow:
    """
    Integration tests simulating a new tutorial being created.

    These tests simulate the CI pipeline flow without actually
    creating PRs or running the full workflow.
    """

    @pytest.fixture
    def new_tutorial_sidecar(self, tmp_path):
        """Simulate a new tutorial with placeholder GUIDs."""
        sidecar = {
            "id": "tc-new-tutorial",
            "title": "New Tutorial",
            "description": "A test tutorial",
            "date": "2026-02-20",
            "duration": "10m00s",
            "ia-guid": "TODO-replace-me",
            "lesson-guid": "TODO-replace-me",
            "certifications": None,
            "skill-levels": "Beginner",
            "tags": [{"tag": "Test"}],
            "technologies": [{"tech": "Other"}],
            "files": [
                {"label": "Overview", "duration": "3:00", "file": "step-1.md", "xy-guid": "TODO"},
                {"label": "Main Content", "duration": "5:00", "file": "step-2.md", "xy-guid": ""},
                {"label": "Congratulations", "duration": "2:00", "file": "step-3.md"}  # Missing xy-guid
            ],
            "authors": [{"name": "Test Author", "email": "test@cisco.com"}],
            "active": True
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f, indent=2)
        return sidecar_path

    def test_new_tutorial_guid_flow(self, new_tutorial_sidecar):
        """
        Test the complete flow for a new tutorial:
        1. Detect all GUID issues
        2. Generate new GUIDs
        3. Update sidecar.json
        4. Verify all GUIDs are now valid
        """
        # Step 1: Check for issues
        issues = check_guids(new_tutorial_sidecar)

        # Should find 5 issues: ia-guid, lesson-guid, 3 xy-guids
        assert len(issues) == 5

        # Step 2: Fix issues
        result = fix_guids(new_tutorial_sidecar, issues)
        assert len(result['changes']) == 5

        # Step 3: Verify no more issues
        recheck = check_guids(new_tutorial_sidecar)
        assert len(recheck) == 0

        # Step 4: Verify sidecar structure is intact
        with open(new_tutorial_sidecar) as f:
            fixed = json.load(f)

        assert fixed['id'] == 'tc-new-tutorial'
        assert fixed['title'] == 'New Tutorial'
        assert len(fixed['files']) == 3
        assert is_valid_guid(fixed['ia-guid'])
        assert is_valid_guid(fixed['lesson-guid'])
        for file_entry in fixed['files']:
            assert 'xy-guid' in file_entry
            assert is_valid_guid(file_entry['xy-guid'])

    def test_existing_tutorial_update_flow(self, tmp_path):
        """
        Test flow for updating an existing tutorial:
        - Some GUIDs are valid (should be preserved)
        - Some are missing (should be generated)
        """
        existing_guid = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        sidecar = {
            "id": "tc-existing",
            "ia-guid": existing_guid,  # Valid, should keep
            "lesson-guid": existing_guid,  # Duplicate! Should regenerate
            "files": [
                {"file": "step-1.md", "xy-guid": "11111111-2222-3333-4444-555555555555"},  # Valid
                {"file": "step-2.md"}  # Missing, should generate
            ]
        }
        sidecar_path = tmp_path / "sidecar.json"
        with open(sidecar_path, 'w') as f:
            json.dump(sidecar, f)

        issues = check_guids(sidecar_path)
        # lesson-guid is duplicate, step-2 xy-guid is missing
        assert len(issues) == 2

        fix_guids(sidecar_path, issues)

        with open(sidecar_path) as f:
            fixed = json.load(f)

        # ia-guid should be unchanged
        assert fixed['ia-guid'] == existing_guid
        # lesson-guid should be new
        assert fixed['lesson-guid'] != existing_guid
        assert is_valid_guid(fixed['lesson-guid'])
        # step-1 xy-guid should be unchanged
        assert fixed['files'][0]['xy-guid'] == "11111111-2222-3333-4444-555555555555"
        # step-2 xy-guid should be new
        assert is_valid_guid(fixed['files'][1]['xy-guid'])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
