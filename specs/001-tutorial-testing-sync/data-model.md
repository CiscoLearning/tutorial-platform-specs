# Data Model: Tutorial-Testing Environment Sync

**Feature**: 001-tutorial-testing-sync
**Date**: 2026-02-18

## Overview

This feature involves file-based data synchronization between two Git repositories. There are no database entities, but the following file structures and relationships are important to understand.

## Entities

### Tutorial Folder

A directory containing a complete tutorial for the Cisco U. platform.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Directory name, format: `tc-{tutorial-name}` |
| sidecar.json | file | Metadata including GUIDs, duration, skill level |
| step-*.md | files | Tutorial content (step-1.md through step-N.md) |
| images/ | directory | Required folder for image assets |
| assets/ | directory | Optional folder for configs, manifests |

**Source**: Production repository (`ciscou-tutorial-content`)
**Destination**: Testing repository (`tutorial-testing`)

### Test Fixture

A tutorial or folder created for testing purposes, not present in production.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Directory name (various formats) |
| location | path | Archived to `_test-fixtures/` |
| origin | enum | `intern` (summer 2025) or `developer` |

**Inventory** (35 items total):
- 27 test tutorials (tc-avocado-test, tc-jira-demo, etc.)
- 8 poplartest folders

### Workflow File

A YAML file defining GitHub Actions automation.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Filename (e.g., `tutorial-linting.yml`) |
| location | path | `.github/workflows/` |
| sync_direction | enum | `production → testing` |

**Files to sync**:
- tutorial-linting.yml
- tutorial-automation.yml
- jira-closer.yml
- jira-poster.yml
- push-to-staging-mitigate.yml (if exists in production)

### GUID Cache

A JSON file tracking all unique GUIDs across tutorials.

| Attribute | Type | Description |
|-----------|------|-------------|
| filename | string | `guid_cache.json` |
| location | path | Repository root |
| content | object | Map of GUID → tutorial reference |

**Sync behavior**: Always overwrite testing version with production version.

## Relationships

```
Production Repository                    Testing Repository
├── tc-*/  ─────────────────────────────> tc-*/  (SYNCED)
├── guid_cache.json ────────────────────> guid_cache.json (SYNCED)
├── .github/workflows/*.yml ────────────> .github/workflows/*.yml (SYNCED)
│
│                                        _test-fixtures/  (PRESERVED)
│                                        ├── tc-avocado-test/
│                                        ├── poplartest*/
│                                        └── ...
│
│                                        tools/  (NOT SYNCED - source of truth)
│                                        template/  (NOT SYNCED)
│                                        README.md  (NOT SYNCED)
```

## State Transitions

### Sync Workflow States

```
┌─────────────┐
│   IDLE      │ ← Waiting for trigger (schedule or manual)
└──────┬──────┘
       │ Trigger event
       ▼
┌─────────────┐
│  FETCHING   │ ← Checking out both repositories
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│  COMPARING  │ ← Detecting changes between repos
└──────┬──────┘
       │ Changes detected (or force sync)
       ▼
┌─────────────┐
│  SYNCING    │ ← Copying files from production to testing
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│ COMMITTING  │ ← Creating commit with sync changes
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│  PUSHING    │ ← Pushing to testing repository
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│  COMPLETE   │ ← Sync finished successfully
└─────────────┘

Error paths:
- FETCHING → ERROR (repo unavailable)
- SYNCING → ERROR (file operation failed)
- PUSHING → ERROR (permission denied)
```

## Validation Rules

### Tutorial Folder Identification
- MUST start with `tc-` prefix
- MUST contain `sidecar.json` file
- MUST contain at least `step-1.md`

### Test Fixture Identification
- Exists in testing repository
- Does NOT exist in production repository
- OR is in the known test fixture inventory list

### Sync Exclusions
- `tools/` directory - NEVER sync (testing is source of truth)
- `template/` directory - NEVER sync
- `_test-fixtures/` directory - NEVER sync (preserved archive)
- `README.md` - NEVER sync (may differ between repos)
- `.git/` directory - Handled by git operations

## Configuration

### Repository Variables (tutorial-testing)

| Variable | Value | Description |
|----------|-------|-------------|
| PROD_REPO | `{org}/ciscou-tutorial-content` | Production repository full name (private, org-owned) |

### Repository Secrets (tutorial-testing)

| Secret | Description |
|--------|-------------|
| PROD_REPO_TOKEN | PAT with `repo` scope for private org repository access |

### Access Requirements

The production repository (`ciscou-tutorial-content`) is:
- **Private** - requires authentication for any access
- **Organization-owned** - PAT must be from a user with org membership
- The PAT needs `repo` scope (full control) to read private repository contents

Options for the token:
1. **Personal Access Token (Classic)**: User must be org member with repo access
2. **Fine-grained PAT**: Can be scoped to specific repository (more secure)
3. **GitHub App**: Most secure, requires app installation in org (more complex setup)
