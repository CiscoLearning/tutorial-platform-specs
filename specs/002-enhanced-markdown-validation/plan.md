# Implementation Plan: Enhanced Markdown Validation

**Branch**: `002-enhanced-markdown-validation` | **Date**: 2026-02-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-enhanced-markdown-validation/spec.md`

## Summary

Enhance the tutorial validation pipeline to detect markdown patterns that break XML conversion (HTML tags, nested lists, link spacing) before conversion runs, and auto-fix issues by default using both regex (simple issues) and AI (complex structural issues). Authors see a PR comment with all changes for easy revert.

## Technical Context

**Language/Version**: Python 3.10 (per CI workflow)
**Primary Dependencies**: jsonschema, pytest, requests (existing); Cisco Chat-AI API (existing ai_analysis.py)
**Storage**: N/A (file-based validation)
**Testing**: pytest (existing test framework in tools/pytest_validation.py)
**Target Platform**: GitHub Actions (ubuntu-22.04)
**Project Type**: CI/CD tooling enhancement
**Performance Goals**: Validation completes within 30 seconds for largest tutorial (NFR-001)
**Constraints**: Zero false positives for blocking issues (NFR-002); <5% false negatives (NFR-003)
**Scale/Scope**: ~150 tutorials, ~8 validation tools, 2 CI workflows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Tutorial Quality First | PASS | Feature improves tutorial quality by catching errors early |
| II. Structured Content Organization | PASS | No structural changes to tutorials; validates existing structure |
| III. Validate Early, Fail Fast | PASS | Core purpose: catch XML conversion issues at PR time, not after merge |
| IV. Editorial Consistency Through Automation | PASS | Auto-fix reduces manual editorial work |
| V. Transparent Pipeline Feedback | PASS | Provides actionable line references, fix suggestions, and PR comments showing changes |
| Markdown to XML Compatibility | PASS | Directly addresses known failure patterns (whitespace around links, etc.) |

**Gate Result**: PASS - All principles aligned. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-enhanced-markdown-validation/
├── plan.md              # This file
├── research.md          # Phase 0 output - already exists from prior session
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (if applicable)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
tutorial-testing/
├── tools/
│   ├── clean_markdown.py        # MODIFY: Add P1 detection + P2 auto-fix
│   ├── schema_validation.py     # MODIFY: Add duration format auto-fix
│   ├── ai_analysis.py           # REFERENCE: Pattern for AI integration
│   ├── markdown_validator.py    # NEW (Phase 2): Refactored pluggable validator
│   └── pytest_validation.py     # Existing - no changes needed
├── .github/workflows/
│   └── tutorial-linting.yml     # MODIFY: Add auto-fix commit step
└── tests/
    └── test_markdown_validator.py  # NEW: Unit tests for new validation rules
```

**Structure Decision**: Enhance existing `tutorial-testing/tools/` structure. Start by modifying `clean_markdown.py` for P1, create new `markdown_validator.py` for P2/P3 when rule complexity warrants refactoring.

## Complexity Tracking

> No constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |

## Phase 0: Research Summary

Research was completed in prior session. Key findings documented in [research.md](./research.md):

| Topic | Decision | Rationale |
|-------|----------|-----------|
| HTML tag detection | Regex pattern `<(br\|p\|div\|span\|hr\|img)[^>]*\/?>` | Catches common tags from PR #177 |
| Nested list issues | AI reformatting + PR comment | Regex insufficient for complex structural fixes |
| Link spacing | Detect missing whitespace before/after `[text](url)` | Documented XML failure cause in constitution |
| Auto-fix default | Opt-OUT (`--no-fix` flag) | Most authors prefer automated cleanup |
| Duration format | Auto-convert `60m00s` → `1h00m00s` | Schema requires hour format for 60+ minutes |

## Phase 1: Design Artifacts

### Validation Rules Model

See [data-model.md](./data-model.md) for:
- ValidationRule entity (id, pattern, severity, message, auto_fixable)
- ValidationIssue entity (rule_id, file_path, line_number, message, fixed)
- ValidationResult entity (issues, files_modified, summary)

### API/CLI Contracts

See [contracts/](./contracts/) for:
- `clean_markdown.py` CLI interface (`--no-fix`, `--json-output`)
- PR comment format specification
- AI reformatting prompt template

### Quickstart

See [quickstart.md](./quickstart.md) for:
- Local development setup
- Running validation manually
- Testing against historical PRs

## Implementation Phases

### Phase 1: Detection (P1 Requirements)

1. Add HTML tag detection regex to `clean_markdown.py`
2. Add link spacing detection (whitespace before/after `[text](url)`)
3. Add nested list indentation validation
4. Add code-block-in-list indentation check
5. Map errors to source line numbers
6. Generate actionable fix suggestions per error type
7. Unit tests for all new rules
8. Test against PRs #177, #196 markdown samples

### Phase 2: Auto-Fix (P2 Requirements)

1. Uncomment/enable auto-fix in `clean_markdown.py`
2. Add `--no-fix` flag for opt-out
3. Add duration format auto-fix to `schema_validation.py`
4. Create AI reformatting function using existing `ai_analysis.py` pattern
5. Generate unified PR comment with all changes (before/after diff)
6. Update `tutorial-linting.yml` to commit auto-fixed files
7. Integration tests for auto-fix workflow

### Phase 3: Categorization (P3 Requirements)

1. Add severity field to each rule (BLOCKING vs WARNING)
2. Update CI exit code logic (fail only on blockers)
3. Enhance PR comment format with color-coded severity
4. Refactor to `markdown_validator.py` with pluggable rule system

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design artifacts completed.*

| Principle | Status | Post-Design Evidence |
|-----------|--------|---------------------|
| I. Tutorial Quality First | PASS | Auto-fix improves quality without author burden |
| II. Structured Content Organization | PASS | Validates existing structure; doesn't impose new requirements |
| III. Validate Early, Fail Fast | PASS | All validation at PR time; PR comment shows changes |
| IV. Editorial Consistency Through Automation | PASS | Automated fixes for whitespace, formatting, link spacing |
| V. Transparent Pipeline Feedback | PASS | PR comment format shows diffs, line numbers, severity indicators |
| Markdown to XML Compatibility | PASS | AI-reformatting prompt preserves content while fixing structure |
| External Dependencies (sidecar.json) | PASS | Duration fix uses existing schema format; no schema changes |

**Post-Design Gate Result**: PASS - All principles maintained. Ready for task generation.

## Next Steps

1. ~~Generate `data-model.md` with entity definitions~~ ✓
2. ~~Generate `contracts/` with CLI and PR comment specifications~~ ✓
3. ~~Generate `quickstart.md` with local dev instructions~~ ✓
4. Run `/speckit.tasks` to generate `tasks.md`
