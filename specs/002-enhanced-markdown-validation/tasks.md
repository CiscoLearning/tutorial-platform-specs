# Tasks: Enhanced Markdown Validation

**Input**: Design documents from `/specs/002-enhanced-markdown-validation/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Tests**: Unit tests included per user story to verify detection patterns work correctly.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this project modifies existing CI tooling:

```text
tutorial-testing/
├── tools/
│   ├── clean_markdown.py        # MODIFY
│   ├── schema_validation.py     # MODIFY
│   └── ai_analysis.py           # REFERENCE
├── .github/workflows/
│   └── tutorial-linting.yml     # MODIFY
└── tests/
    └── test_markdown_validator.py  # NEW
```

---

## Phase 1: Setup

**Purpose**: Prepare codebase for new validation features

- [x] T001 Create test fixtures directory with sample markdown files from PRs #177 and #196 in tutorial-testing/tests/fixtures/
- [x] T002 [P] Create test_markdown_validator.py skeleton in tutorial-testing/tests/test_markdown_validator.py
- [x] T003 [P] Add ValidationRule, ValidationIssue, ValidationResult dataclasses to tutorial-testing/tools/clean_markdown.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure needed by all user stories

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Refactor clean_markdown.py to use ValidationRule pattern for existing whitespace checks in tutorial-testing/tools/clean_markdown.py
- [x] T005 [P] Add argparse CLI with --no-fix, --json-output, --verbose flags and JSON output mode in tutorial-testing/tools/clean_markdown.py
- [x] T006 Update clean_folder() to use new ValidationResult return type in tutorial-testing/tools/clean_markdown.py

**Checkpoint**: Foundation ready - validation framework in place, user story implementation can begin

---

## Phase 3: User Story 1 - Pre-Conversion Detection (Priority: P1)

**Goal**: Authors get immediate feedback about markdown patterns that will break XML conversion, with specific line numbers and fix suggestions.

**Independent Test**: Run `python tools/clean_markdown.py --no-fix tc-test-fixture` and verify all known breaking patterns are detected with correct line numbers.

### Tests for User Story 1

- [x] T008 [P] [US1] Unit test for HTML_TAG detection (detects `<br>`, `<p>`, `<div>`) in tutorial-testing/tests/test_markdown_validator.py
- [x] T009 [P] [US1] Unit test for LINK_NO_SPACE_BEFORE detection in tutorial-testing/tests/test_markdown_validator.py
- [x] T010 [P] [US1] Unit test for LINK_NO_SPACE_AFTER detection in tutorial-testing/tests/test_markdown_validator.py
- [x] T011 [P] [US1] Unit test for LIST_INDENT_INCONSISTENT detection in tutorial-testing/tests/test_markdown_validator.py
- [x] T012 [P] [US1] Unit test for CODE_BLOCK_IN_LIST detection in tutorial-testing/tests/test_markdown_validator.py
- [x] T013 [P] [US1] Unit test for LINK_BROKEN detection (line breaks inside link syntax) in tutorial-testing/tests/test_markdown_validator.py

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement HTML_TAG rule with regex `<(br|p|div|span|hr|img)[^>]*/?>` in tutorial-testing/tools/clean_markdown.py
- [x] T015 [P] [US1] Implement LINK_NO_SPACE_BEFORE rule with regex `\S\[[^\]]+\]\([^)]+\)` in tutorial-testing/tools/clean_markdown.py
- [x] T016 [P] [US1] Implement LINK_NO_SPACE_AFTER rule with regex `\[[^\]]+\]\([^)]+\)\S` in tutorial-testing/tools/clean_markdown.py
- [x] T017 [P] [US1] Implement LINK_BROKEN rule for line breaks inside `[text](url)` syntax in tutorial-testing/tools/clean_markdown.py
- [x] T018 [US1] Implement LIST_INDENT_INCONSISTENT stateful check in tutorial-testing/tools/clean_markdown.py
- [x] T019 [US1] Implement CODE_BLOCK_IN_LIST stateful check in tutorial-testing/tools/clean_markdown.py
- [x] T020 [US1] Add fix_suggestion text for each rule (actionable instructions) in tutorial-testing/tools/clean_markdown.py
- [x] T021 [US1] Add line number mapping to all detection functions in tutorial-testing/tools/clean_markdown.py
- [x] T022 [US1] Test detection against PR #177 markdown sample (HTML tags) in tutorial-testing/tests/test_markdown_validator.py
- [x] T023 [US1] Test detection against PR #196 markdown sample (nested lists) in tutorial-testing/tests/test_markdown_validator.py

**Checkpoint**: User Story 1 complete - all detection rules work, line numbers reported, fix suggestions shown. Authors can now see what's wrong before XML conversion fails.

---

## Phase 4: User Story 2 - Auto-Fix (Priority: P2)

**Goal**: Simple issues are automatically fixed by default, reducing manual cleanup. Authors can opt out with `--no-fix` flag or commit message tags.

**Independent Test**: Run `python tools/clean_markdown.py tc-test-fixture` (without --no-fix) and verify files are modified with fixes applied.

**Depends on**: User Story 1 (detection must work before auto-fix)

### Tests for User Story 2

- [ ] T022 [P] [US2] Unit test for trailing whitespace auto-fix in tutorial-testing/tests/test_markdown_validator.py
- [ ] T023 [P] [US2] Unit test for double space auto-fix in tutorial-testing/tests/test_markdown_validator.py
- [ ] T024 [P] [US2] Unit test for duration format auto-fix (60m00s → 1h00m00s) in tutorial-testing/tests/test_markdown_validator.py
- [ ] T025 [P] [US2] Unit test for --no-fix flag (issues reported but files unchanged) in tutorial-testing/tests/test_markdown_validator.py
- [ ] T026 [P] [US2] Unit test for AI retry with exponential backoff in tutorial-testing/tests/test_markdown_validator.py
- [ ] T027 [P] [US2] Unit test for AI response validation (URL preservation, content length, code blocks) in tutorial-testing/tests/test_markdown_validator.py
- [ ] T028 [P] [US2] Unit test for `[no-autofix]` commit message flag detection in tutorial-testing/tests/test_markdown_validator.py
- [ ] T029 [P] [US2] Unit test for `[no-ai-fix]` commit message flag detection in tutorial-testing/tests/test_markdown_validator.py

### Implementation for User Story 2

- [x] T030 [US2] Enable auto-fix for TRAILING_WHITESPACE rule (uncomment and enhance existing code) in tutorial-testing/tools/clean_markdown.py
- [x] T031 [US2] Enable auto-fix for DOUBLE_SPACE rule in tutorial-testing/tools/clean_markdown.py
- [x] T032 [US2] Add auto-fix for HTML_TAG rule (replace `<br>` with blank line) in tutorial-testing/tools/clean_markdown.py
- [x] T033 [US2] Add auto-fix for LINK_SPACING rules (add space before/after links) in tutorial-testing/tools/clean_markdown.py
- [ ] T034 [US2] Add duration format auto-fix to schema_validation.py (convert 60m00s → 1h00m00s) in tutorial-testing/tools/schema_validation.py
- [x] T035 [US2] Create ai_reformat_markdown() function following ai_analysis.py pattern in tutorial-testing/tools/clean_markdown.py
- [x] T036 [US2] Implement AI retry logic with exponential backoff (3 retries) in tutorial-testing/tools/clean_markdown.py
- [x] T037 [US2] Implement validate_ai_response() to check URL preservation, content length ±20%, code blocks unchanged in tutorial-testing/tools/clean_markdown.py
- [x] T038 [US2] Add fallback behavior when AI fails: skip AI fixes, report WARNING, continue with regex-only in tutorial-testing/tools/clean_markdown.py
- [x] T039 [US2] Add fallback behavior when AI response validation fails: reject fix, keep original, report WARNING in tutorial-testing/tools/clean_markdown.py
- [x] T040 [US2] Implement AI reformatting for LIST_INDENT_INCONSISTENT rule in tutorial-testing/tools/clean_markdown.py
- [x] T041 [US2] Implement AI reformatting for CODE_BLOCK_IN_LIST rule in tutorial-testing/tools/clean_markdown.py
- [x] T042 [US2] Add commit message parsing for `[no-autofix]` flag (skip all fixes) in tutorial-testing/tools/clean_markdown.py
- [x] T043 [US2] Add commit message parsing for `[no-ai-fix]` flag (skip AI only, regex still applies) in tutorial-testing/tools/clean_markdown.py
- [x] T044 [US2] Generate PR comment body with before/after diffs per pr-comment-format.md spec in tutorial-testing/tools/clean_markdown.py
- [x] T045 [US2] Add PR comment footer with opt-out instructions ("To disable auto-fix, add [no-autofix]...") in tutorial-testing/tools/clean_markdown.py
- [x] T046 [US2] Update tutorial-linting.yml to call clean_markdown.py with new interface in tutorial-testing/.github/workflows/tutorial-linting.yml
- [x] T047 [US2] Add commit message extraction step to tutorial-linting.yml for flag detection in tutorial-testing/.github/workflows/tutorial-linting.yml
- [x] T048 [US2] Add git commit step for auto-fixed files to tutorial-linting.yml in tutorial-testing/.github/workflows/tutorial-linting.yml
- [x] T049 [US2] Add PR comment posting step to tutorial-linting.yml in tutorial-testing/.github/workflows/tutorial-linting.yml

**Checkpoint**: User Story 2 complete - auto-fix works by default, AI has retry/validation/fallback, commit message flags work, PR shows diff with opt-out instructions.

---

## Phase 5: User Story 3 - Blocking vs Warning Categorization (Priority: P3)

**Goal**: Validation clearly distinguishes between issues that will definitely fail (BLOCKING) vs those that might cause problems (WARNING).

**Independent Test**: Run validation on file with mixed issues and verify BLOCKING issues fail pipeline while WARNING issues only show warning summary.

**Depends on**: User Story 1 (detection), User Story 2 (auto-fix)

### Tests for User Story 3

- [x] T050 [P] [US3] Unit test for BLOCKING severity on HTML_TAG rule in tutorial-testing/tests/test_markdown_validator.py
- [x] T051 [P] [US3] Unit test for WARNING severity on TRAILING_WHITESPACE rule in tutorial-testing/tests/test_markdown_validator.py
- [x] T052 [P] [US3] Unit test for exit code 0 when only warnings exist in tutorial-testing/tests/test_markdown_validator.py
- [x] T053 [P] [US3] Unit test for exit code 1 when unfixed blockers exist in tutorial-testing/tests/test_markdown_validator.py

### Implementation for User Story 3

- [x] T054 [US3] Add severity field to all ValidationRule definitions in tutorial-testing/tools/clean_markdown.py
- [x] T055 [US3] Update exit code logic to fail only on BLOCKING issues in tutorial-testing/tools/clean_markdown.py
- [x] T056 [US3] Add color-coded severity indicators to text output in tutorial-testing/tools/clean_markdown.py
- [x] T057 [US3] Add severity emoji (red/yellow) to PR comment format in tutorial-testing/tools/clean_markdown.py
- [x] T058 [US3] Update tutorial-linting.yml to handle warning-only case (continue pipeline) in tutorial-testing/.github/workflows/tutorial-linting.yml
- [ ] T059 [US3] Refactor validation rules into markdown_validator.py with pluggable rule system in tutorial-testing/tools/markdown_validator.py

**Checkpoint**: User Story 3 complete - clear distinction between blocking and warning issues, pipeline behavior matches severity.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T060 [P] Run full validation against all 150 tutorials to check for false positives
- [x] T061 [P] Update CLAUDE.md with new tool usage in tutorial-platform-specs/CLAUDE.md
- [ ] T062 Validate against quickstart.md scenarios (local dev, historical PRs) in specs/002-enhanced-markdown-validation/quickstart.md
- [x] T063 Performance test: verify validation completes in <30 seconds for largest tutorial
- [x] T064 Code review and cleanup of clean_markdown.py and markdown_validator.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase
- **User Story 2 (Phase 4)**: Depends on User Story 1 (detection must work before auto-fix)
- **User Story 3 (Phase 5)**: Depends on User Story 1 and 2 (severity affects both detection and auto-fix)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

```
Setup → Foundational → US1 (Detection) → US2 (Auto-Fix) → US3 (Categorization) → Polish
                           ↓
                       (MVP complete - authors get feedback)
```

### Within Each User Story

- Tests SHOULD be written first and FAIL before implementation
- Detection rules can be implemented in parallel (different functions)
- Fix implementation follows detection
- CI integration is final step per story

### Parallel Opportunities

**Phase 1 Setup:**
```
T002 (test skeleton) || T003 (dataclasses)
```

**Phase 2 Foundational:**
```
T005 (CLI flags) || T006 (JSON output)
```

**Phase 3 User Story 1 - Tests:**
```
T008 || T009 || T010 || T011 || T012  (all test files)
```

**Phase 3 User Story 1 - Implementation:**
```
T013 || T014 || T015  (regex rules can be parallel)
Then: T016 → T017 (stateful checks sequential)
```

**Phase 4 User Story 2 - Tests:**
```
T022 || T023 || T024 || T025 || T026 || T027 || T028 || T029  (all test files)
```

**Phase 5 User Story 3 - Tests:**
```
T050 || T051 || T052 || T053  (all test files)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Detection)
4. **STOP and VALIDATE**: Authors can now see what's wrong with their markdown
5. Deploy and gather feedback before proceeding to auto-fix

### Incremental Delivery

1. **Setup + Foundational** → Framework ready
2. **Add User Story 1** → Authors get pre-conversion feedback (MVP!)
3. **Add User Story 2** → Auto-fix with AI retry/validation/fallback + commit message opt-out
4. **Add User Story 3** → Clear blocking vs warning distinction
5. **Polish** → Production-ready

### Suggested MVP Scope

**User Story 1 only** provides immediate value:
- Authors see what will break XML conversion
- Specific line numbers and fix suggestions
- No more cryptic XML error messages

Auto-fix (US2) and categorization (US3) can be added incrementally after MVP validation.

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | 3 | 2 |
| Foundational | 3 | 1 |
| US1 (Detection) | 16 | 10 |
| US2 (Auto-Fix) | 28 | 8 |
| US3 (Categorization) | 10 | 4 |
| Polish | 5 | 2 |
| **Total** | **65** | **27** |

### New Tasks from Clarifications & Analysis

The following tasks were added based on clarification and analysis sessions:

| Task | Source |
|------|--------|
| T013, T017 | Analysis: FR-003 LINK_BROKEN coverage gap |
| T059 | Analysis: markdown_validator.py refactoring in-scope |
| T026, T036, T038 | Clarification: AI retry with exponential backoff + fallback |
| T027, T037, T039 | Clarification: AI response validation (URLs, length, code blocks) |
| T028, T029, T042, T043 | Clarification: `[no-autofix]` and `[no-ai-fix]` commit flags |
| T045 | Clarification: PR comment footer with opt-out instructions |
| T047 | Clarification: Commit message extraction in CI |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently testable once complete
- Commit after each task or logical group
- Test fixtures from PRs #177 and #196 are critical for validation
- AI fixes have 3 retries with exponential backoff before falling back to WARNING
- Authors can use `[no-autofix]` (skip all) or `[no-ai-fix]` (skip AI only) in commit messages
