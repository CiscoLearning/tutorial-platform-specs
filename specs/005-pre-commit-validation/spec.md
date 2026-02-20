# Feature Specification: Pre-commit Validation & Automated GUID Handling

**Feature ID**: FR-4
**Created**: 2026-02-20
**Completed**: 2026-02-20
**Status**: Complete
**Input**: FR-4 from requirements.md - Pre-commit validation with GUID automation

## Problem Statement

Authors creating tutorials face two friction points:

1. **Manual GUID generation**: Authors must manually generate UUIDs using `uuidgen` for `ia-guid`, `lesson-guid`, and `xy-guid` fields. This is error-prone - authors often use placeholders like "TODO" or copy GUIDs from other tutorials (causing duplicates).

2. **Late feedback loop**: Authors don't discover validation issues until CI runs, which can take several minutes. Power users with local dev environments want faster iteration.

**Evidence from production:**
- GUID cache was 7+ months out of date due to disabled auto-commit
- Multiple PRs failed GUID uniqueness checks requiring manual fixes
- Most authors (non-technical) edit markdown in GitHub UI without local tools

## User Scenarios & Testing

### User Story 1 - Author Creates New Tutorial (Priority: P1)

A tutorial author creates a new tutorial with placeholder or missing GUIDs. The CI pipeline automatically generates valid GUIDs and commits them to the PR branch.

**Acceptance Scenarios:**

1. **Given** sidecar.json has `"ia-guid": "TODO"`, **When** PR is created, **Then** a valid UUID is generated and committed to the PR branch.

2. **Given** sidecar.json is missing `xy-guid` for step-3.md, **When** PR validation runs, **Then** a new UUID is generated and added to the file entry.

3. **Given** an author copies a GUID from another tutorial, **When** duplicate is detected against guid_cache.json, **Then** a new unique GUID is generated.

4. **Given** GUIDs are auto-generated, **When** PR comment is posted, **Then** author sees which GUIDs were generated and why.

---

### User Story 2 - GUID Cache Stays in Sync (Priority: P1)

After a PR is merged, the GUID cache is automatically updated so future uniqueness checks work correctly.

**Acceptance Scenarios:**

1. **Given** a PR with new tutorial is merged, **When** jira-closer workflow runs, **Then** guid_cache.json is updated with new GUIDs and committed to main.

2. **Given** guid_cache.json was updated, **When** next PR runs GUID check, **Then** it checks against the latest cache.

---

### User Story 3 - Power User Local Validation (Priority: P2)

A technical author with local dev environment can run validation before pushing to catch issues early.

**Acceptance Scenarios:**

1. **Given** author runs `validate_tutorial.py tc-my-tutorial/`, **When** validation completes, **Then** all checks (schema, GUIDs, content, markdown) run and report results.

2. **Given** author runs with `--fix` flag, **When** issues are found, **Then** markdown is auto-fixed and GUIDs are generated.

3. **Given** author runs with `--quick` flag, **When** validation runs, **Then** slow checks (URL validation) are skipped.

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Detect missing GUID fields (ia-guid, lesson-guid, xy-guid) | P1 | Complete |
| FR-002 | Detect invalid GUID format (not UUID pattern) | P1 | Complete |
| FR-003 | Detect placeholder GUIDs (TODO, test, placeholder, etc.) | P1 | Complete |
| FR-004 | Detect duplicate GUIDs within single sidecar.json | P1 | Complete |
| FR-005 | Detect duplicate GUIDs against guid_cache.json | P1 | Complete |
| FR-006 | Generate valid lowercase UUIDs for all issue types | P1 | Complete |
| FR-007 | Update sidecar.json in place with generated GUIDs | P1 | Complete |
| FR-008 | Commit GUID updates to PR branch automatically | P1 | Complete |
| FR-009 | Update guid_cache.json on PR merge | P1 | Complete |
| FR-010 | Provide local validation CLI for power users | P2 | Complete |
| FR-011 | Support --fix flag for auto-correction | P2 | Complete |
| FR-012 | Support --quick flag to skip slow checks | P2 | Complete |

### Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-001 | GUID generation completes in < 5 seconds | Complete |
| NFR-002 | Zero false positives (don't flag valid UUIDs) | Complete |
| NFR-003 | Preserve valid existing GUIDs (don't regenerate) | Complete |
| NFR-004 | Local validation works without CI dependencies | Complete |

## Technical Approach

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PR Created/Updated                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               tutorial-linting.yml                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. guid_generator.py --fix                          │    │
│  │     - Check ia-guid, lesson-guid, xy-guid            │    │
│  │     - Detect missing/invalid/duplicate               │    │
│  │     - Generate new UUIDs                             │    │
│  │     - Update sidecar.json                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2. Commit GUID updates to PR branch                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  3. Continue with schema/pytest/markdown validation  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PR Merged to Main                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               jira-closer.yml                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. guid_update.py                                   │    │
│  │     - Extract GUIDs from merged tutorial             │    │
│  │     - Add to guid_cache.json                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2. Commit updated guid_cache.json to main           │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| `guid_generator.py` | Check and generate GUIDs | `tools/guid_generator.py` |
| `validate_tutorial.py` | Local validation CLI | `tools/validate_tutorial.py` |
| `guid_update.py` | Update GUID cache | `tools/guid_update.py` (existing) |
| `guid_cache.json` | Known GUIDs for uniqueness | `tools/guid_cache.json` |

## Implementation Details

### GUID Detection Rules

```python
# Valid UUID pattern
UUID_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

# Placeholder patterns that trigger regeneration
PLACEHOLDERS = ['todo', 'test', 'placeholder', 'xxx', 'guid', 'uuid',
                'replace', 'change', 'fill', 'add', 'new']
```

### Issue Types

| Type | Description | Action |
|------|-------------|--------|
| `missing` | Field not present or empty | Generate new UUID |
| `invalid` | Not valid UUID format | Generate new UUID |
| `duplicate` | Same as another GUID in file or cache | Generate new UUID |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All GUIDs valid (or fixed with --fix) |
| 1 | GUID issues found (check-only mode) |
| 2 | Error (file not found, invalid JSON) |

## Files Modified/Created

| File | Change | Repository |
|------|--------|------------|
| `tools/guid_generator.py` | Created | Both |
| `tools/validate_tutorial.py` | Created | Both |
| `.github/workflows/tutorial-linting.yml` | Added GUID generation step | ciscou-tutorial-content |
| `.github/workflows/jira-closer.yml` | Enabled cache commit | ciscou-tutorial-content |
| `.github/workflows/tools-test.yml` | Created | ciscou-tutorial-content |
| `tests/test_guid_generator.py` | Created | Both |

## Testing

### Unit Tests (29 tests)

```bash
pytest tests/test_guid_generator.py -v
```

Test categories:
- `TestGuidValidation` - UUID format validation
- `TestPlaceholderDetection` - Detect TODO, test, etc.
- `TestGuidGeneration` - Generate valid unique UUIDs
- `TestCheckGuids` - Detect issues in sidecar.json
- `TestGuidCache` - Cache loading and duplicate detection
- `TestFixGuids` - Fix issues while preserving valid GUIDs
- `TestNewTutorialFlow` - End-to-end new tutorial simulation

### CI Workflows

| Workflow | Trigger | Tests |
|----------|---------|-------|
| `tools-test.yml` | Push to tools/*.py or tests/*.py | Unit tests |
| `e2e-test.yml` | Push to tests/e2e_tutorials/** | Full pipeline |

## Usage

### CI Pipeline (Automatic)

GUIDs are automatically checked and generated on every PR. Authors don't need to do anything.

### Local Validation (Power Users)

```bash
# Basic validation
python tools/validate_tutorial.py tc-my-tutorial/

# With auto-fix
python tools/validate_tutorial.py tc-my-tutorial/ --fix

# Quick mode (skip URL checking)
python tools/validate_tutorial.py tc-my-tutorial/ --quick
```

### GUID Generator (Standalone)

```bash
# Check only
python tools/guid_generator.py tc-my-tutorial/sidecar.json

# Fix issues
python tools/guid_generator.py tc-my-tutorial/sidecar.json --fix

# JSON output
python tools/guid_generator.py tc-my-tutorial/sidecar.json --json
```

## Related Documentation

- [Requirements](../../.specify/specs/requirements.md) - FR-4 definition
- [Architecture](../../.specify/specs/architecture.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Common commands
