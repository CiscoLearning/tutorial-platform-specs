# Feature Specification: Tutorial-Testing Environment Sync

**Feature Branch**: `001-tutorial-testing-sync`
**Created**: 2026-02-18
**Status**: Complete
**Input**: FR-0 (Tutorial-Testing sync) - Establish tutorial-testing as a proper mirror of production

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Tests Validation Against Real Tutorials (Priority: P1)

A developer working on validation tool improvements needs to test their changes against the full corpus of production tutorials (137+) to ensure the tools work correctly before deploying to production.

**Why this priority**: Without access to real tutorial content, developers cannot verify that validation tools work correctly. This is the core value of having a testing environment.

**Independent Test**: Can be fully tested by running validation tools against synced tutorials and comparing results to production pipeline output.

**Acceptance Scenarios**:

1. **Given** the testing repository has been synced, **When** a developer runs the validation suite, **Then** it executes against all 137+ production tutorials
2. **Given** a new tutorial was added to production yesterday, **When** sync runs today, **Then** that tutorial appears in the testing repository
3. **Given** a tutorial was updated in production, **When** sync runs, **Then** the testing repository reflects those updates

---

### User Story 2 - Preserve Intern Test Fixtures (Priority: P2)

The testing repository contains 27 test tutorials and other test fixtures created by an intern. These must be preserved as they serve as regression test cases for validation tools.

**Why this priority**: Losing test fixtures would require recreating them, and they contain specific edge cases that are valuable for testing.

**Independent Test**: After sync completes, all original test fixtures remain accessible and unchanged.

**Acceptance Scenarios**:

1. **Given** test tutorials exist (tc-avocado-test, tc-jira-demo, etc.), **When** production sync runs, **Then** test tutorials are preserved in a designated archive location
2. **Given** the tools/ folder contains validation scripts, **When** sync runs, **Then** the tools/ folder remains unchanged
3. **Given** experimental branches exist in the testing repo, **When** sync runs, **Then** those branches are not affected

---

### User Story 3 - Automated Daily Sync (Priority: P3)

The testing repository should automatically stay in sync with production without manual intervention, ensuring developers always have access to current content.

**Why this priority**: Manual syncing is error-prone and creates drift between environments. Automation ensures consistency.

**Independent Test**: After 24 hours without manual intervention, the testing repository contains content matching production.

**Acceptance Scenarios**:

1. **Given** sync is configured, **When** 24 hours pass, **Then** sync runs automatically
2. **Given** sync runs automatically, **When** a developer checks the repository the next day, **Then** they see tutorials added to production the previous day
3. **Given** sync fails for any reason, **When** a developer or admin checks status, **Then** they can see the failure and its cause

---

### User Story 4 - Manual Sync Trigger (Priority: P4)

A developer needs to force a sync immediately when they need the latest production content without waiting for the scheduled sync.

**Why this priority**: Important for time-sensitive testing, but daily sync covers most needs.

**Independent Test**: Developer can trigger sync on demand and see updated content within minutes.

**Acceptance Scenarios**:

1. **Given** new content was just added to production, **When** a developer triggers manual sync, **Then** content appears in testing within 10 minutes
2. **Given** sync is already running, **When** a developer triggers manual sync, **Then** they receive feedback that sync is in progress

---

### Edge Cases

- What happens when a tutorial is deleted from production? (Sync should remove it from testing, but preserve in archive if it was a test fixture)
- What happens when sync runs but production repository is unavailable? (Sync should fail gracefully with clear error message)
- What happens when there are merge conflicts between production content and local changes? (Production should win; local experimental work should be on branches)
- What happens when guid_cache.json has conflicts? (Production version takes precedence)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST sync all tutorial folders (tc-*) from production repository to testing repository
- **FR-002**: System MUST preserve existing test fixtures by moving them to a designated archive folder (_test-fixtures/) before first sync
- **FR-003**: System MUST sync the guid_cache.json file to ensure GUID validation works correctly
- **FR-004**: System MUST sync workflow files (.github/workflows/*.yml) to keep CI/CD pipelines consistent
- **FR-005**: System MUST NOT modify the tools/ folder during sync (this is the source of truth for validation tools)
- **FR-006**: System MUST NOT modify the template/ folder during sync
- **FR-007**: System MUST provide a manual trigger mechanism for on-demand sync
- **FR-008**: System MUST run automatically on a daily schedule (overnight), with manual trigger available for on-demand sync
- **FR-009**: System MUST report sync status and any errors encountered
- **FR-010**: System MUST handle the case where testing repository has local changes on main branch (production content takes precedence)

### Key Entities

- **Tutorial Folder**: A tc-* directory containing sidecar.json, step-*.md files, images/, and optional assets/
- **Test Fixture**: A tutorial or folder created for testing purposes, not present in production
- **Workflow File**: A YAML file in .github/workflows/ that defines CI/CD automation
- **GUID Cache**: A JSON file tracking all unique GUIDs across tutorials to prevent duplicates

## Assumptions

- The testing repository has read access to the production repository (same organization or configured access)
- Test fixtures can be identified by their absence in production (tutorials that exist only in testing)
- The tools/ folder in testing is the source of truth and should never be overwritten
- Experimental work should be done on feature branches, not main branch
- Production repository structure is stable and follows documented conventions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Testing repository contains 100% of production tutorials within 24 hours of any production change
- **SC-002**: All existing test fixtures (27 tutorials, 8 poplartest folders) remain accessible after sync
- **SC-003**: Validation tools in testing can process all synced tutorials without errors caused by missing content
- **SC-004**: Sync completes within 15 minutes for full repository (137+ tutorials)
- **SC-005**: Manual sync trigger provides feedback within 1 minute of activation
- **SC-006**: Zero manual intervention required for routine sync operations over a 30-day period

## Dependencies

- Access permissions between production and testing repositories
- Existing test fixture inventory must be documented before first sync
- Current state of both repositories must be audited to identify conflicts

## Out of Scope

- Syncing from testing back to production (one-way sync only)
- Modifying the validation tools as part of this feature
- Creating new test fixtures (separate effort)
- Migrating to a different repository structure
