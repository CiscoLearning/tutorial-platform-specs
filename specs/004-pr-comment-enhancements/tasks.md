# Tasks: PR Comment Enhancements

**Input**: Design documents from `/specs/004-pr-comment-enhancements/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the specification. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

All paths relative to `tutorial-testing/` repository:
- Tools: `tools/`
- Templates: `tools/pr_comment_templates/`
- Workflow: `.github/workflows/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base formatter script structure

- [ ] T001 Create directory structure for templates in tools/pr_comment_templates/
- [ ] T002 Create base format_pr_comment.py with CLI argument parsing in tools/format_pr_comment.py
- [ ] T003 [P] Add ValidationError dataclass matching contracts/validation-error.schema.json in tools/format_pr_comment.py
- [ ] T004 [P] Add ValidationResult dataclass matching contracts/validation-result.schema.json in tools/format_pr_comment.py
- [ ] T005 [P] Add PRCommentPayload dataclass matching contracts/pr-comment-payload.schema.json in tools/format_pr_comment.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Modify pytest_validation.py to add --json-output flag that outputs pytest_results.json in tools/pytest_validation.py
- [ ] T007 Add JSON parsing functions to read pytest_results.json, transform_stderr.log, linting_output.log in tools/format_pr_comment.py
- [ ] T008 Implement markdown comment generation base class with header/footer/status in tools/format_pr_comment.py
- [ ] T009 Add truncation helper function (10KB limit with link to Actions log) in tools/format_pr_comment.py
- [ ] T010 Add collapsible section generator function (<details> tag wrapper) in tools/format_pr_comment.py
- [ ] T011 Add severity icon helper (🚫 for blocking, ⚠️ for warning) per FR-009 in tools/format_pr_comment.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Broken Link Errors Directly in PR (Priority: P1) 🎯 MVP

**Goal**: Display broken URLs and missing images directly in PR comments with file, line, URL in formatted table

**Independent Test**: Create a PR with a broken URL and verify the comment displays the broken URL details in a table without requiring log navigation

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create broken URL table formatter function that outputs markdown table with File|Line|URL|Status columns in tools/format_pr_comment.py
- [ ] T013 [P] [US1] Create missing image formatter function that outputs file and image path in tools/format_pr_comment.py
- [ ] T014 [US1] Add broken_url.md template with example fix instructions in tools/pr_comment_templates/broken_url.md
- [ ] T015 [US1] Add grouping logic to group errors by file per FR-003 in tools/format_pr_comment.py
- [ ] T016 [US1] Handle edge case: more than 10 broken URLs - show first 10, collapse rest in tools/format_pr_comment.py
- [ ] T017 [US1] Update workflow to capture pytest JSON output in .github/workflows/tutorial-linting.yml
- [ ] T018 [US1] Update workflow pytest comment step to use format_pr_comment.py for broken links in .github/workflows/tutorial-linting.yml

**Checkpoint**: User Story 1 complete - broken URL/image errors now appear in PR comments with formatted tables

---

## Phase 4: User Story 2 - View XML Conversion Errors with Fix Guidance (Priority: P2)

**Goal**: Display XML conversion errors with plain-language explanations and before/after fix examples

**Independent Test**: Create a PR with a known XML-breaking pattern (code block in list) and verify the comment explains the fix in plain language

### Implementation for User Story 2

- [ ] T019 [P] [US2] Create XML error parser to extract line number, error type, tags from transform_stderr.log in tools/format_pr_comment.py
- [ ] T020 [P] [US2] Create XML error explanation mapping (tag mismatch → "Code block inside list item") in tools/format_pr_comment.py
- [ ] T021 [US2] Add xml_error.md template with before/after examples for common patterns in tools/pr_comment_templates/xml_error.md
- [ ] T022 [US2] Implement XML error formatter that shows plain explanation with raw error collapsed per FR-004/FR-005 in tools/format_pr_comment.py
- [ ] T023 [US2] Update workflow to pass transform_stderr.log to format_pr_comment.py in .github/workflows/tutorial-linting.yml

**Checkpoint**: User Story 2 complete - XML errors now show plain-language explanations with collapsed raw output

---

## Phase 5: User Story 3 - View Duration Mismatch Warnings (Priority: P3)

**Goal**: Display duration mismatch warnings with expected vs actual values and auto-fix command

**Independent Test**: Create a PR with a duration mismatch and verify the comment shows expected vs actual and the fix_sidecar.py command

### Implementation for User Story 3

- [ ] T024 [P] [US3] Create duration mismatch parser to extract expected/actual values from pytest output in tools/format_pr_comment.py
- [ ] T025 [US3] Add duration_mismatch.md template with table format and fix command in tools/pr_comment_templates/duration_mismatch.md
- [ ] T026 [US3] Implement duration mismatch formatter showing Expected|Actual table and fix command per FR-006/FR-007 in tools/format_pr_comment.py
- [ ] T027 [US3] Mark duration mismatch as warning severity (⚠️) not blocking in tools/format_pr_comment.py

**Checkpoint**: User Story 3 complete - duration mismatches now show in PR comments with auto-fix command

---

## Phase 6: User Story 4 - Fallback for Unspecified Error Types (Priority: P4)

**Goal**: Capture and display raw output from any failing validation step that lacks custom formatting

**Independent Test**: Trigger an error type without custom formatting (e.g., GUID uniqueness) and verify raw output appears in collapsible section

### Implementation for User Story 4

- [ ] T028 [P] [US4] Create fallback formatter that wraps raw output in collapsible section with step name header in tools/format_pr_comment.py
- [ ] T029 [P] [US4] Add fallback.md template with generic error display format in tools/pr_comment_templates/fallback.md
- [ ] T030 [US4] Implement error type detection - route known types to formatters, unknown to fallback per FR-011/FR-012 in tools/format_pr_comment.py
- [ ] T031 [US4] Add truncation for raw output >10KB with "see Actions log" link per FR-013 in tools/format_pr_comment.py
- [ ] T032 [US4] Update workflow to capture folder check output for fallback display in .github/workflows/tutorial-linting.yml
- [ ] T033 [US4] Update workflow to capture solomon lint output for fallback display in .github/workflows/tutorial-linting.yml
- [ ] T034 [US4] Update workflow to use unified format_pr_comment.py call aggregating all validation outputs in .github/workflows/tutorial-linting.yml

**Checkpoint**: User Story 4 complete - all validation errors now surface in PR comments (formatted or fallback)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, edge cases, and documentation

- [ ] T035 [P] Add multi-error-type handling - each type gets own section with clear headers per edge case spec in tools/format_pr_comment.py
- [ ] T036 [P] Update README.md in tutorial-testing with format_pr_comment.py usage documentation
- [ ] T037 Verify GitHub PR comment size limit (65,536 chars) handling with truncation in tools/format_pr_comment.py
- [ ] T038 End-to-end validation: Create test PR with multiple error types and verify comment output
- [ ] T039 Remove old "click for more info" comment logic from workflow in .github/workflows/tutorial-linting.yml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent but builds on fallback pattern

### Within Each User Story

- Templates before formatters (templates provide structure)
- Parsers before formatters (formatters use parsed data)
- Formatters before workflow updates (workflow calls formatters)
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: T003, T004, T005 can run in parallel (different dataclasses)
- **Phase 3 (US1)**: T012, T013 can run in parallel (different formatters)
- **Phase 4 (US2)**: T019, T020 can run in parallel (parser vs mapping)
- **Phase 5 (US3)**: T024 can run parallel with T025
- **Phase 6 (US4)**: T028, T029 can run in parallel (formatter vs template)
- **Phase 7**: T035, T036 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallelizable US1 tasks together:
Task: "Create broken URL table formatter function in tools/format_pr_comment.py"
Task: "Create missing image formatter function in tools/format_pr_comment.py"

# Then sequential tasks:
Task: "Add broken_url.md template in tools/pr_comment_templates/broken_url.md"
Task: "Add grouping logic in tools/format_pr_comment.py"
Task: "Update workflow in .github/workflows/tutorial-linting.yml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: User Story 1 (T012-T018)
4. **STOP and VALIDATE**: Test with broken URL PR
5. Deploy to production workflow

**MVP Scope**: 18 tasks deliver core broken URL/image surfacing

### Incremental Delivery

1. Setup + Foundational → Foundation ready (11 tasks)
2. Add User Story 1 → Test → Deploy (MVP: broken URLs) (+7 tasks = 18)
3. Add User Story 2 → Test → Deploy (XML errors) (+5 tasks = 23)
4. Add User Story 3 → Test → Deploy (duration warnings) (+4 tasks = 27)
5. Add User Story 4 → Test → Deploy (fallback) (+7 tasks = 34)
6. Polish phase → Final cleanup (+5 tasks = 39)

---

## Notes

- [P] tasks = different files or independent functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Target repository: `tutorial-testing/` (not specs repo)
