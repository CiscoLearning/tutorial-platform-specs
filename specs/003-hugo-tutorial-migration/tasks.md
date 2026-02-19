# Tasks: Hugo Tutorial Migration

**Input**: Design documents from `/specs/003-hugo-tutorial-migration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Unit tests included per existing test patterns in tutorial-testing repository.

**Organization**: Tasks are organized by functional capability, following the CLI tool architecture in plan.md.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md project structure:
- **Tools**: `tutorial-testing/tools/`
- **Tests**: `tutorial-testing/tests/`
- **Fixtures**: `tutorial-testing/tests/fixtures/`

---

## Phase 1: Setup

**Purpose**: Project initialization and test fixtures

- [x] T001 Create test fixture directory at tutorial-testing/tests/fixtures/sample_hugo_tutorial/
- [x] T002 Create sample Hugo tutorial index.md with standard frontmatter and 3 steps in tutorial-testing/tests/fixtures/sample_hugo_tutorial/index.md
- [x] T003 [P] Create sample images folder with test image in tutorial-testing/tests/fixtures/sample_hugo_tutorial/images/
- [x] T004 [P] Add PyYAML to requirements.txt (or setup.py) if not already present in tutorial-testing/

---

## Phase 2: Core Parser (MIG-001, MIG-006, MIG-007)

**Purpose**: Parse Hugo index.md files - extract frontmatter and steps

**Independent Test**: Run `python -m pytest tests/test_hugo_parser.py` - should parse fixture and extract all fields

### Tests for Hugo Parser

- [x] T005 [P] Create test_hugo_parser.py in tutorial-testing/tests/test_hugo_parser.py with tests for:
  - test_parse_frontmatter_extracts_all_fields
  - test_parse_frontmatter_handles_null_values
  - test_extract_steps_basic
  - test_extract_steps_with_optional_xy_guid
  - test_extract_steps_handles_spacing_variants
  - test_parse_complete_tutorial

### Implementation for Hugo Parser

- [x] T006 Create hugo_parser.py with HugoFrontmatter dataclass in tutorial-testing/tools/hugo_parser.py
- [x] T007 Add HugoStep dataclass to tutorial-testing/tools/hugo_parser.py
- [x] T008 Add HugoTutorial dataclass to tutorial-testing/tools/hugo_parser.py
- [x] T009 Implement parse_frontmatter() function using PyYAML in tutorial-testing/tools/hugo_parser.py
- [x] T010 Implement STEP_PATTERN regex and extract_steps() function in tutorial-testing/tools/hugo_parser.py
- [x] T011 Implement parse_hugo_tutorial() main function that combines frontmatter + steps in tutorial-testing/tools/hugo_parser.py
- [x] T012 Run tests and verify all pass: `python -m pytest tests/test_hugo_parser.py -v`

**Checkpoint**: Hugo parser complete - can parse any Hugo tutorial index.md

---

## Phase 3: Sidecar Generator (MIG-002, MIG-003, MIG-008)

**Purpose**: Convert Hugo data to sidecar.json format with field mapping

**Independent Test**: Run `python -m pytest tests/test_sidecar_generator.py` - should generate valid sidecar from Hugo data

### Tests for Sidecar Generator

- [x] T013 [P] Create test_sidecar_generator.py in tutorial-testing/tests/test_sidecar_generator.py with tests for:
  - test_convert_duration_minutes_only
  - test_convert_duration_with_hours
  - test_map_categories_to_technologies
  - test_map_skill_levels_default
  - test_generate_tutorial_id
  - test_format_author
  - test_generate_sidecar_json_complete

### Implementation for Sidecar Generator

- [x] T014 Create sidecar_generator.py with SidecarFile, SidecarAuthor, SidecarJson dataclasses in tutorial-testing/tools/sidecar_generator.py
- [x] T015 Implement convert_duration() function per research.md R3 in tutorial-testing/tools/sidecar_generator.py
- [x] T016 Implement CATEGORY_MAPPING dict and map_categories_to_technologies() in tutorial-testing/tools/sidecar_generator.py
- [x] T017 Implement map_skill_level() with "Intermediate" default in tutorial-testing/tools/sidecar_generator.py
- [x] T018 Implement generate_tutorial_id() that adds tc- prefix in tutorial-testing/tools/sidecar_generator.py
- [x] T019 Implement format_author() to convert string to author object array in tutorial-testing/tools/sidecar_generator.py
- [x] T020 Implement generate_sidecar() main function that produces complete sidecar dict in tutorial-testing/tools/sidecar_generator.py
- [x] T021 Implement write_sidecar_json() to write formatted JSON file in tutorial-testing/tools/sidecar_generator.py
- [x] T022 Run tests and verify all pass: `python -m pytest tests/test_sidecar_generator.py -v`

**Checkpoint**: Sidecar generator complete - can create valid sidecar.json from Hugo data

---

## Phase 4: PR Description Generator (MIG-010, MIG-011)

**Purpose**: Generate PR descriptions with schema mapping documentation

**Independent Test**: Run `python -m pytest tests/test_pr_generator.py -k pr_generator`

### Tests for PR Generator

- [x] T023 [P] Add PR generator tests to existing test file or create tutorial-testing/tests/test_pr_generator.py with tests for:
  - test_generate_schema_mapping_table
  - test_generate_migration_changes_list
  - test_generate_step_files_table
  - test_generate_pr_description_complete

### Implementation for PR Generator

- [x] T024 Create pr_generator.py in tutorial-testing/tools/pr_generator.py
- [x] T025 Implement MigrationChange and MigrationWarning dataclasses in tutorial-testing/tools/pr_generator.py
- [x] T026 Implement generate_schema_mapping_table() in tutorial-testing/tools/pr_generator.py
- [x] T027 Implement generate_migration_changes() that lists all transformations in tutorial-testing/tools/pr_generator.py
- [x] T028 Implement generate_step_files_table() in tutorial-testing/tools/pr_generator.py
- [x] T029 Implement generate_pr_description() using template from contracts/pr-template.md in tutorial-testing/tools/pr_generator.py
- [x] T030 Run tests and verify all pass: `python -m pytest tests/test_pr_generator.py -v`

**Checkpoint**: PR generator complete - can create detailed PR descriptions

---

## Phase 5: Main CLI Tool (MIG-004, MIG-005, MIG-009)

**Purpose**: Main migration script with CLI interface per contracts/cli-interface.md

**Independent Test**: Run `python tools/migrate_hugo_tutorial.py --source tests/fixtures/sample_hugo_tutorial --dry-run`

### Tests for Main Migration Tool

- [x] T031 [P] Create test_migration_e2e.py in tutorial-testing/tests/test_migration_e2e.py with tests for:
  - test_migrate_single_tutorial_dry_run
  - test_migrate_single_tutorial_creates_output
  - test_migrate_copies_images_folder
  - test_migrate_creates_empty_assets_folder
  - test_migrate_generates_all_step_files
  - test_migrate_with_pr_description_flag
  - test_congratulations_step_has_boilerplate
  - test_congratulations_step_preserves_custom_links
  - test_congratulations_step_has_correct_utm_params

### Implementation for Main CLI

- [x] T032 Create migrate_hugo_tutorial.py with argparse CLI in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T033 Implement argument parsing per cli-interface.md (--source, --output, --dry-run, --pr-description, --verbose) in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T034 Implement migrate_single_tutorial() function that orchestrates parser → generator → writer in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T035 Implement create_output_directory() with images/ and assets/ folders in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T036 Implement copy_images_folder() that copies or creates .gitkeep in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T037 Implement write_step_files() that writes step-N.md files in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T037a Add CONGRATULATIONS_BOILERPLATE constant with standard template in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T037b Implement extract_custom_links() to find custom links in original Congratulations step in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T037c Implement generate_congratulations_step() that combines custom links + boilerplate with tutorial-id UTM params in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T038 Implement dry_run_report() that shows changes without writing in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T039 Implement verbose_logging() for debug output in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T040 Add exit codes per cli-interface.md (0=success, 1=parse error, etc.) in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T041 Run E2E tests and verify: `python -m pytest tests/test_migration_e2e.py -v`

**Checkpoint**: Single tutorial migration working end-to-end

---

## Phase 6: Batch Migration & Author Filter

**Purpose**: Add batch migration mode with author filtering

**Independent Test**: Run `python tools/migrate_hugo_tutorial.py --source-dir tests/fixtures --dry-run`

### Tests for Batch Mode

- [x] T042 [P] Add batch tests to test_migration_e2e.py:
  - test_batch_migrate_dry_run
  - test_batch_filter_by_author
  - test_batch_skips_already_migrated

### Implementation for Batch Mode

- [x] T043 Add --source-dir and --output-dir arguments to tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T044 Add --author filter argument to tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T045 Implement discover_hugo_tutorials() that finds all tutorials in source dir in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T046 Implement filter_by_author() using frontmatter authors field in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T047 Implement SKIP_LIST constant with 9 tutorials from spec.md in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T048 Implement batch_migrate() that processes multiple tutorials in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T049 Run batch tests and verify: `python -m pytest tests/test_migration_e2e.py -k batch -v`

**Checkpoint**: Batch migration by author working

---

## Phase 7: Validation Integration (NFR-002)

**Purpose**: Validate migrated tutorials pass CI checks

**Independent Test**: Migrate a tutorial and run `python tools/schema_validation.py <output-folder>`

### Implementation for Validation

- [x] T050 Add --skip-validation flag to bypass validation in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T051 Implement validate_migration() that calls schema_validation.py on output in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T052 Add validation step to migrate_single_tutorial() workflow in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T053 Implement validation error handling and exit code 3 in tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T054 Add test for validation integration in tutorial-testing/tests/test_migration_e2e.py

**Checkpoint**: All migrated tutorials are automatically validated against schema

---

## Phase 8: Polish & Documentation

**Purpose**: Final cleanup and documentation

- [x] T055 [P] Add JSON output mode (--json flag) to tutorial-testing/tools/migrate_hugo_tutorial.py
- [x] T056 [P] Add comprehensive docstrings to all public functions in tools/*.py
- [x] T057 [P] Create sample migration workflow in tutorial-testing/README.md or docs/
- [x] T058 Run full test suite: `python -m pytest tests/ -v`
- [x] T059 Test migration on 3-5 real Hugo tutorials from cisco-learning-codelabs
- [x] T060 Update quickstart.md with any discovered edge cases

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Parser)**: Depends on Phase 1 fixtures
- **Phase 3 (Sidecar)**: Can start in parallel with Phase 2 (no code dependency)
- **Phase 4 (PR Gen)**: Can start in parallel with Phase 2 and 3
- **Phase 5 (Main CLI)**: Depends on Phase 2, 3, 4 completion
- **Phase 6 (Batch)**: Depends on Phase 5 completion
- **Phase 7 (Validation)**: Depends on Phase 5 completion
- **Phase 8 (Polish)**: Depends on all phases completion

### Parallel Opportunities

```text
Phase 1 → Phase 2 ─────────────────────────┐
      └──► Phase 3 (parallel with Phase 2) ├──► Phase 5 ──► Phase 6 ──► Phase 8
      └──► Phase 4 (parallel with Phase 2) ┘         └──► Phase 7 ──┘
```

Within each phase:
- All tests marked [P] can run in parallel before implementation
- T003, T004 can run in parallel (Phase 1)
- T005, T013, T023, T031, T042 (tests) can all be written in parallel

---

## Implementation Strategy

### MVP First (Phases 1-5)

1. Complete Phase 1: Setup fixtures
2. Complete Phase 2: Hugo parser
3. Complete Phase 3: Sidecar generator (can parallel with 2)
4. Complete Phase 4: PR generator (can parallel with 2, 3)
5. Complete Phase 5: Main CLI
6. **STOP and VALIDATE**: Migrate 1 tutorial and verify CI passes

### Incremental Delivery

1. Phases 1-5 → Single tutorial migration works → Test on real tutorial
2. Phase 6 → Batch migration by author → Test on Jason Belk tutorials
3. Phase 7 → Validation integration → Ensure CI compliance
4. Phase 8 → Polish → Ready for production use

### Estimated Task Counts

| Phase | Task Count | Parallel Opportunities |
|-------|------------|----------------------|
| Phase 1: Setup | 4 | 2 |
| Phase 2: Parser | 8 | 1 |
| Phase 3: Sidecar | 10 | 1 |
| Phase 4: PR Gen | 8 | 1 |
| Phase 5: Main CLI | 14 | 1 |
| Phase 6: Batch | 8 | 1 |
| Phase 7: Validation | 5 | 0 |
| Phase 8: Polish | 6 | 3 |
| **Total** | **63** | **10** |

---

## Notes

- [P] tasks = different files, no dependencies
- Verify tests fail before implementing (TDD)
- Commit after each phase completion
- Test on real Hugo tutorials after Phase 5
- Stop at any checkpoint to validate functionality
- Avoid: vague tasks, same file conflicts
