# Tasks: Tutorial-Testing Environment Sync

**Input**: Design documents from `/specs/001-tutorial-testing-sync/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No automated tests requested - this is a CI/CD infrastructure feature with manual verification steps.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Target repository**: `tutorial-testing/`
- **Workflow files**: `tutorial-testing/.github/workflows/`
- **Archive folder**: `tutorial-testing/_test-fixtures/`

---

## Phase 1: Setup (Repository Configuration)

**Purpose**: Configure repository access and secrets required for cross-repo sync

- [x] T001 Create Personal Access Token (PAT) with `repo` scope for org member with production repo access
- [x] T002 [P] Add secret `PROD_REPO_TOKEN` in tutorial-testing repository Settings → Secrets → Actions
- [x] T003 [P] Add variable `PROD_REPO` with value `{org}/ciscou-tutorial-content` in tutorial-testing repository Settings → Variables → Actions

**Checkpoint**: Repository has credentials configured for cross-repo access

---

## Phase 2: Foundational (Test Fixture Archival)

**Purpose**: Preserve existing test content before enabling production sync - MUST complete before sync workflow runs

**⚠️ CRITICAL**: Running sync without completing this phase will overwrite/delete test fixtures permanently

- [x] T004 Document current test fixture inventory by running `ls tutorial-testing/tc-* | wc -l` and comparing to production
- [x] T005 Create archive directory `tutorial-testing/_test-fixtures/`
- [x] T006 Move 27 test tutorials to archive in `tutorial-testing/_test-fixtures/tc-*/`
- [x] T007 Move 8 poplartest folders to archive in `tutorial-testing/_test-fixtures/poplartest*/`
- [x] T008 Commit archive changes with message "Archive test fixtures before enabling production sync" and push to remote

**Checkpoint**: Test fixtures archived and safe - sync workflow can now be implemented

---

## Phase 3: User Story 1 - Developer Tests Validation Against Real Tutorials (Priority: P1) 🎯 MVP

**Goal**: Enable developers to test validation tools against all 137+ production tutorials

**Independent Test**: Run `python tools/pytest_validation.py` against synced content and verify it processes all tutorials

### Implementation for User Story 1

- [x] T009 [US1] Create sync workflow file `tutorial-testing/.github/workflows/sync-from-production.yml`
- [x] T010 [US1] Add checkout step for production repository using `actions/checkout@v4` with `PROD_REPO_TOKEN`
- [x] T011 [US1] Add checkout step for testing repository using `actions/checkout@v4`
- [x] T012 [US1] Add rsync step to sync all `tc-*/` folders from production to testing with `--delete` flag (handles tutorial deletions automatically)
- [x] T013 [US1] Add step to sync `guid_cache.json` from production to testing
- [x] T014 [US1] Add step to sync workflow files from `production/.github/workflows/*.yml` to testing
- [x] T015 [US1] Add change detection step to check `git status --porcelain`
- [x] T016 [US1] Add commit and push step (only if changes detected)

**Checkpoint**: Manual workflow trigger syncs production content to testing repository

---

## Phase 4: User Story 2 - Preserve Intern Test Fixtures (Priority: P2)

**Goal**: Ensure test fixtures remain accessible after sync operations

**Independent Test**: After sync runs, verify all 35 items exist in `_test-fixtures/` and tools/ folder is unchanged

### Implementation for User Story 2

- [x] T017 [US2] Update rsync exclusion rules in `tutorial-testing/.github/workflows/sync-from-production.yml` to exclude `_test-fixtures/`
- [x] T018 [US2] Add explicit exclusion for `tools/` directory in sync workflow
- [x] T019 [US2] Add explicit exclusion for `template/` directory in sync workflow
- [x] T020 [US2] Add explicit exclusion for `README.md` in sync workflow
- [x] T021 [US2] Add verification step to confirm tools/ folder unchanged after sync

**Checkpoint**: Sync preserves all designated content while updating production tutorials

---

## Phase 5: User Story 3 - Automated Daily Sync (Priority: P3)

**Goal**: Repository automatically syncs overnight without manual intervention

**Independent Test**: Wait 24+ hours and verify new production content appears in testing without manual trigger

### Implementation for User Story 3

- [x] T022 [US3] Add `schedule` trigger with cron `'0 4 * * *'` (4 AM UTC) to `tutorial-testing/.github/workflows/sync-from-production.yml`
- [x] T023 [US3] Add sync status summary step that outputs sync statistics (files added, modified, deleted)
- [x] T024 [US3] Configure GitHub notification settings for workflow failures

**Checkpoint**: Daily sync runs automatically at 4 AM UTC

---

## Phase 6: User Story 4 - Manual Sync Trigger (Priority: P4)

**Goal**: Developers can force immediate sync when needed

**Independent Test**: Trigger workflow manually via Actions UI and see new content within 10 minutes

### Implementation for User Story 4

- [x] T025 [US4] Add `workflow_dispatch` trigger with optional `force_full_sync` input to `tutorial-testing/.github/workflows/sync-from-production.yml`
- [x] T026 [US4] Add concurrency group to prevent multiple syncs running simultaneously
- [x] T027 [US4] Add early exit message when sync is already running

**Checkpoint**: Manual trigger available via Actions UI with in-progress feedback

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and error handling improvements

- [x] T028 [P] Add error handling for production repo unavailable scenario with clear message: "Sync failed: Unable to access production repository. Check PROD_REPO_TOKEN permissions and expiration."
- [x] T029 [P] Add error handling for permission denied on push
- [x] T030 Update `tutorial-testing/README.md` with sync workflow documentation including: sync schedule, manual trigger instructions, and warning that production content overwrites local changes on main
- [ ] T031 Create token rotation reminder in team calendar (90-day expiration)
- [ ] T032 Run full verification checklist from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - core sync functionality
- **User Story 2 (Phase 4)**: Depends on US1 - adds preservation rules to existing workflow
- **User Story 3 (Phase 5)**: Depends on US1 - adds schedule trigger to existing workflow
- **User Story 4 (Phase 6)**: Depends on US1 - adds manual trigger to existing workflow
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - Creates the base workflow file
- **User Story 2 (P2)**: Depends on US1 - Modifies workflow to add exclusions
- **User Story 3 (P3)**: Depends on US1 - Modifies workflow to add schedule
- **User Story 4 (P4)**: Depends on US1 - Modifies workflow to add manual trigger

Note: US2, US3, and US4 all modify the same workflow file created in US1, so they should be done sequentially.

### Within Each User Story

- Configuration before workflow changes
- Workflow triggers before sync logic
- Sync logic before error handling
- Commit changes after each logical group

### Parallel Opportunities

- T002 and T003 (secrets and variables) can run in parallel
- T028 and T029 (error handling) can run in parallel
- US2, US3, US4 could theoretically be combined into a single workflow edit, but are separated for clarity

---

## Parallel Example: Phase 1 Setup

```bash
# These can run in parallel (different GitHub settings):
Task: "Add secret PROD_REPO_TOKEN in tutorial-testing repository"
Task: "Add variable PROD_REPO in tutorial-testing repository"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (credentials)
2. Complete Phase 2: Foundational (archive test fixtures)
3. Complete Phase 3: User Story 1 (basic sync)
4. **STOP and VALIDATE**: Manually trigger sync, verify tutorials appear
5. Deploy/use immediately

### Incremental Delivery

1. Complete Setup + Foundational → Ready for sync
2. Add User Story 1 → Manual sync works → **MVP Complete!**
3. Add User Story 2 → Test fixtures protected
4. Add User Story 3 → Daily automation enabled
5. Add User Story 4 → Manual trigger with feedback
6. Polish → Documentation and error handling

### Single Developer Strategy

Since all user stories modify the same workflow file:

1. Complete Setup + Foundational
2. Implement all workflow features in US1-US4 sequentially
3. Commit after each user story is complete
4. Test each story independently before moving to next

---

## Notes

- [P] tasks = different files/systems, no dependencies
- [Story] label maps task to specific user story for traceability
- All US2-US4 tasks modify the same workflow file created in US1
- Manual verification steps are defined in quickstart.md Verification section
- Token rotation is a maintenance task, not an implementation task
- Avoid: making workflow changes in parallel (will cause conflicts)
