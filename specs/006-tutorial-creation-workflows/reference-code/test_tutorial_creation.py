#!/usr/bin/env python3
"""
Unit tests for tutorial creation tools (FF-2).

Tests cover:
- Issue body parsing
- Slug generation
- Checkbox parsing
- Sidecar generation
- Step file generation

Run with: pytest tests/test_tutorial_creation.py -v
"""

import json
import os
import sys
import tempfile
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

# Import after path is set
import create_tutorial_from_issue
from create_tutorial_from_issue import (
    parse_issue_body,
    generate_slug,
    parse_duration,
    parse_checkboxes,
    parse_num_steps,
    generate_guid,
    create_sidecar,
    create_step_file,
)


class TestParseIssueBody:
    """Tests for parsing GitHub issue form body."""

    def test_parse_simple_fields(self):
        """Test parsing simple text fields."""
        body = """### Tutorial Title

Getting Started with Ansible

### Description

Learn automation basics."""

        result = parse_issue_body(body)
        assert result['tutorial_title'] == 'Getting Started with Ansible'
        assert result['description'] == 'Learn automation basics.'

    def test_parse_multiline_field(self):
        """Test parsing multiline text fields."""
        body = """### Step Titles (optional)

Install Ansible
Configure Inventory
Run First Playbook"""

        result = parse_issue_body(body)
        assert 'Install Ansible' in result['step_titles_(optional)']
        assert 'Configure Inventory' in result['step_titles_(optional)']
        assert 'Run First Playbook' in result['step_titles_(optional)']

    def test_parse_no_response(self):
        """Test that _No response_ is handled correctly."""
        body = """### Tutorial Slug (optional)

_No response_

### Tutorial Title

My Tutorial"""

        result = parse_issue_body(body)
        assert result.get('tutorial_slug_(optional)', '') == ''
        assert result['tutorial_title'] == 'My Tutorial'

    def test_parse_checkboxes(self):
        """Test parsing checkbox fields."""
        body = """### Technologies

- [X] Networking
- [ ] Security
- [x] Software
- [ ] Cloud"""

        result = parse_issue_body(body)
        assert '- [X] Networking' in result['technologies']
        assert '- [x] Software' in result['technologies']


class TestGenerateSlug:
    """Tests for slug generation."""

    def test_simple_title(self):
        """Test slug from simple title."""
        assert generate_slug('Hello World') == 'hello-world'

    def test_special_characters(self):
        """Test slug removes special characters."""
        assert generate_slug("What's New in Python 3.10?") == 'whats-new-in-python-310'

    def test_multiple_spaces(self):
        """Test slug handles multiple spaces."""
        assert generate_slug('Hello   World') == 'hello-world'

    def test_leading_trailing_spaces(self):
        """Test slug trims spaces."""
        assert generate_slug('  Hello World  ') == 'hello-world'

    def test_uppercase(self):
        """Test slug is lowercase."""
        assert generate_slug('ANSIBLE AUTOMATION') == 'ansible-automation'


class TestParseDuration:
    """Tests for duration parsing."""

    def test_15_minutes(self):
        """Test 15 minute duration."""
        total, duration_str = parse_duration('15 minutes')
        assert total == 15
        assert duration_str == '15m00s'

    def test_30_minutes(self):
        """Test 30 minute duration."""
        total, duration_str = parse_duration('30 minutes')
        assert total == 30
        assert duration_str == '30m00s'

    def test_45_minutes(self):
        """Test 45 minute duration."""
        total, duration_str = parse_duration('45 minutes')
        assert total == 45
        assert duration_str == '45m00s'

    def test_60_minutes(self):
        """Test 60 minute duration (max)."""
        total, duration_str = parse_duration('60 minutes')
        assert total == 60
        assert duration_str == '1h00m00s'

    def test_unknown_duration(self):
        """Test unknown duration defaults to 30 minutes."""
        total, duration_str = parse_duration('unknown')
        assert total == 30
        assert duration_str == '30m00s'


class TestParseCheckboxes:
    """Tests for checkbox parsing."""

    def test_checked_boxes(self):
        """Test parsing checked checkboxes."""
        text = """- [X] Networking
- [ ] Security
- [x] Software"""

        result = parse_checkboxes(text)
        assert 'Networking' in result
        assert 'Software' in result
        assert 'Security' not in result

    def test_no_checked_boxes(self):
        """Test parsing when nothing is checked."""
        text = """- [ ] Option 1
- [ ] Option 2"""

        result = parse_checkboxes(text)
        assert result == []

    def test_empty_text(self):
        """Test parsing empty text."""
        result = parse_checkboxes('')
        assert result == []


class TestParseNumSteps:
    """Tests for number of steps parsing."""

    def test_3_steps(self):
        """Test parsing 3 steps."""
        assert parse_num_steps('3 (Overview + 3 steps + Congratulations = 5 total)') == 3

    def test_6_steps(self):
        """Test parsing 6 steps."""
        assert parse_num_steps('6 (Overview + 6 steps + Congratulations = 8 total)') == 6

    def test_10_steps(self):
        """Test parsing 10 steps."""
        assert parse_num_steps('10 (Overview + 10 steps + Congratulations = 12 total)') == 10

    def test_invalid_format(self):
        """Test invalid format defaults to 1."""
        assert parse_num_steps('invalid') == 1


class TestGenerateGuid:
    """Tests for GUID generation."""

    def test_guid_format(self):
        """Test GUID is valid UUID format."""
        guid = generate_guid()
        # Should not raise
        uuid.UUID(guid)

    def test_guid_lowercase(self):
        """Test GUID is lowercase."""
        guid = generate_guid()
        assert guid == guid.lower()

    def test_guid_unique(self):
        """Test GUIDs are unique."""
        guids = [generate_guid() for _ in range(100)]
        assert len(set(guids)) == 100


class TestCreateSidecar:
    """Tests for sidecar.json generation."""

    @pytest.fixture
    def sample_data(self):
        """Sample parsed issue data."""
        return {
            'tutorial_title': 'Getting Started with Ansible',
            'description': 'Learn automation basics.',
            'author_name': 'Jason Belk',
            'author_email': 'jabelk@cisco.com',
            'estimated_duration': '30 minutes',
            'skill_level': 'Intermediate',
            'technologies': '- [X] Networking\n- [X] Software',
            'related_certifications_(optional)': '- [X] Cisco Certified DevNet Associate',
            'tags': 'ansible, automation, python',
        }

    def test_sidecar_required_fields(self, sample_data):
        """Test sidecar has all required fields."""
        sidecar = create_sidecar(sample_data, 'tc-test', 2)

        required_fields = [
            'id', 'title', 'description', 'date', 'duration',
            'ia-guid', 'lesson-guid', 'skill-levels', 'tags',
            'technologies', 'files', 'authors', 'active'
        ]
        for field in required_fields:
            assert field in sidecar, f"Missing required field: {field}"

    def test_sidecar_id(self, sample_data):
        """Test sidecar id matches folder name."""
        sidecar = create_sidecar(sample_data, 'tc-my-tutorial', 2)
        assert sidecar['id'] == 'tc-my-tutorial'

    def test_sidecar_duration_format(self, sample_data):
        """Test duration is in correct format."""
        sidecar = create_sidecar(sample_data, 'tc-test', 2)
        assert sidecar['duration'] == '30m00s'

    def test_sidecar_files_count(self, sample_data):
        """Test correct number of step files."""
        # 2 content steps + Overview + Congratulations = 4
        sidecar = create_sidecar(sample_data, 'tc-test', 2)
        assert len(sidecar['files']) == 4

    def test_sidecar_first_step_overview(self, sample_data):
        """Test first step is Overview."""
        sidecar = create_sidecar(sample_data, 'tc-test', 2)
        assert sidecar['files'][0]['label'] == 'Overview'
        assert sidecar['files'][0]['file'] == 'step-1.md'

    def test_sidecar_last_step_congratulations(self, sample_data):
        """Test last step is Congratulations."""
        sidecar = create_sidecar(sample_data, 'tc-test', 2)
        assert sidecar['files'][-1]['label'] == 'Congratulations'

    def test_sidecar_guids_unique(self, sample_data):
        """Test all GUIDs are unique."""
        sidecar = create_sidecar(sample_data, 'tc-test', 3)

        guids = [sidecar['ia-guid'], sidecar['lesson-guid']]
        guids.extend([f['xy-guid'] for f in sidecar['files']])

        assert len(set(guids)) == len(guids), "GUIDs are not unique"

    def test_sidecar_technologies_parsed(self, sample_data):
        """Test technologies are parsed correctly."""
        sidecar = create_sidecar(sample_data, 'tc-test', 1)
        techs = [t['tech'] for t in sidecar['technologies']]
        assert 'Networking' in techs
        assert 'Software' in techs

    def test_sidecar_tags_parsed(self, sample_data):
        """Test tags are parsed correctly."""
        sidecar = create_sidecar(sample_data, 'tc-test', 1)
        tags = [t['tag'] for t in sidecar['tags']]
        assert 'ansible' in tags
        assert 'automation' in tags
        assert 'python' in tags

    def test_sidecar_active_true(self, sample_data):
        """Test active is always True."""
        sidecar = create_sidecar(sample_data, 'tc-test', 1)
        assert sidecar['active'] is True

    def test_sidecar_author_info(self, sample_data):
        """Test author info is correct."""
        sidecar = create_sidecar(sample_data, 'tc-test', 1)
        assert len(sidecar['authors']) == 1
        assert sidecar['authors'][0]['name'] == 'Jason Belk'
        assert sidecar['authors'][0]['email'] == 'jabelk@cisco.com'


class TestCreateStepFile:
    """Tests for step file generation."""

    def test_overview_step(self):
        """Test Overview step content."""
        content = create_step_file(1, 'Overview', is_overview=True, title='Test Tutorial')
        assert '## Overview' in content
        assert 'Test Tutorial' in content
        assert "What You'll Learn" in content

    def test_congratulations_step(self):
        """Test Congratulations step content."""
        content = create_step_file(3, 'Congratulations', is_congrats=True, title='Test Tutorial')
        assert '## Congratulations' in content
        assert 'Test Tutorial' in content
        assert 'What You Learned' in content

    def test_content_step(self):
        """Test regular content step."""
        content = create_step_file(2, 'Install Ansible')
        assert '## Install Ansible' in content
        assert 'Add your content' in content


class TestEndToEndFlow:
    """End-to-end integration tests."""

    def test_full_issue_to_sidecar_flow(self):
        """Test complete flow from issue body to sidecar."""
        issue_body = """### Tutorial Title

Getting Started with Network Automation

### Tutorial Slug (optional)

_No response_

### Description

Learn how to automate network tasks with Python.

### Author Name

Test Author

### Author Email

test@cisco.com

### Estimated Duration

30 minutes

### Skill Level

Beginner

### Technologies

- [X] Networking
- [ ] Security
- [X] Software

### Related Certifications (optional)

- [X] CCNA
- [ ] CCNP Enterprise

### Tags

python, netmiko, automation

### Number of Steps

2 (Overview + 2 steps + Congratulations = 4 total)

### Step Titles (optional)

Set Up Your Environment
Write Your First Script

### Acknowledgment

- [X] I understand that a PR will be created"""

        # Parse issue body
        data = parse_issue_body(issue_body)

        # Verify parsing
        assert data['tutorial_title'] == 'Getting Started with Network Automation'
        assert data['skill_level'] == 'Beginner'

        # Generate slug
        slug = generate_slug(data['tutorial_title'])
        assert slug == 'getting-started-with-network-automation'
        folder_name = f'tc-{slug}'

        # Parse num steps
        num_steps = parse_num_steps(data['number_of_steps'])
        assert num_steps == 2

        # Create sidecar
        sidecar = create_sidecar(data, folder_name, num_steps)

        # Verify sidecar
        assert sidecar['id'] == 'tc-getting-started-with-network-automation'
        assert sidecar['title'] == 'Getting Started with Network Automation'
        assert sidecar['skill-levels'] == 'Beginner'
        assert len(sidecar['files']) == 4  # Overview + 2 steps + Congratulations
        assert sidecar['files'][0]['label'] == 'Overview'
        assert sidecar['files'][1]['label'] == 'Set Up Your Environment'
        assert sidecar['files'][2]['label'] == 'Write Your First Script'
        assert sidecar['files'][3]['label'] == 'Congratulations'

    def test_sidecar_schema_compatibility(self):
        """Test generated sidecar is compatible with schema."""
        data = {
            'tutorial_title': 'Test Tutorial',
            'description': 'Test description',
            'author_name': 'Test Author',
            'author_email': 'test@cisco.com',
            'estimated_duration': '15 minutes',
            'skill_level': 'Beginner',
            'technologies': '- [X] Other',
            'tags': 'test',
        }

        sidecar = create_sidecar(data, 'tc-test', 1)

        # Verify all required schema fields exist and have correct types
        assert isinstance(sidecar['id'], str)
        assert isinstance(sidecar['title'], str)
        assert isinstance(sidecar['description'], str)
        assert isinstance(sidecar['date'], str)
        assert isinstance(sidecar['duration'], str)
        assert isinstance(sidecar['ia-guid'], str)
        assert isinstance(sidecar['lesson-guid'], str)
        assert isinstance(sidecar['skill-levels'], str)
        assert isinstance(sidecar['tags'], list)
        assert isinstance(sidecar['technologies'], list)
        assert isinstance(sidecar['files'], list)
        assert isinstance(sidecar['authors'], list)
        assert sidecar['active'] is True

        # Verify GUID format
        uuid.UUID(sidecar['ia-guid'])
        uuid.UUID(sidecar['lesson-guid'])
        for f in sidecar['files']:
            uuid.UUID(f['xy-guid'])

        # Verify duration format
        assert sidecar['duration'] == '15m00s'

        # Verify date format (YYYY-MM-DD)
        from datetime import datetime
        datetime.strptime(sidecar['date'], '%Y-%m-%d')

        # Verify files have required fields
        for f in sidecar['files']:
            assert 'label' in f
            assert 'duration' in f
            assert 'xy-guid' in f
            assert 'file' in f
            assert f['file'].startswith('step-')
            assert f['file'].endswith('.md')
