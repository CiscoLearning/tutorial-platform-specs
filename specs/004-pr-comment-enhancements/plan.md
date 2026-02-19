# Implementation Plan: PR Comment Enhancements

**Branch**: `004-pr-comment-enhancements` | **Date**: 2026-02-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-pr-comment-enhancements/spec.md`

## Summary

Enhance PR comments in the tutorial-testing CI pipeline to surface validation errors directly instead of requiring authors to navigate GitHub Actions logs. The implementation adds a Python script (`format_pr_comment.py`) that parses structured JSON output from pytest and other validation steps, then generates formatted markdown comments with actionable error details.

Primary approach: Modify `pytest_validation.py` to output JSON alongside text, create a new `format_pr_comment.py` to consume JSON and generate rich markdown, and update the workflow to use the new comment format.

## Technical Context

**Language/Version**: Python 3.10 (matches existing tools in tutorial-testing)
**Primary Dependencies**: pytest, requests, jsonschema (already in use)
**Storage**: N/A (file-based JSON output for inter-step communication)
**Testing**: pytest (existing test framework)
**Target Platform**: GitHub Actions (ubuntu-22.04 runner)
**Project Type**: Single project (CLI tools in `tools/` directory)
**Performance Goals**: Comment generation < 5 seconds (non-blocking CI step)
**Constraints**: GitHub PR comment size limit (65,536 characters); must truncate large output
**Scale/Scope**: ~20 PRs/month, 9 validation steps to capture

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| III. Validate Early, Fail Fast | PASS | Surfacing errors in PR comments aligns with "shifting validation left" |
| V. Transparent Pipeline Feedback | PASS | Core principle - "Authors MUST receive actionable, specific feedback that enables self-correction" |
| - PR comments MUST categorize issues | PASS | FR-009 requires visual indicators for blocking vs warning |
| - Validation errors MUST include line references | PASS | FR-001/FR-003 require file name and line number |
| - XML conversion errors MUST explain cause | PASS | FR-004/FR-005 require plain-language explanations |

**Gate Status**: PASS - No violations. This feature directly implements Constitution Principle V.

## Project Structure

### Documentation (this feature)

```text
specs/004-pr-comment-enhancements/
├── plan.md              # This file
├── research.md          # Phase 0 output (already complete)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (JSON schemas)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (tutorial-testing repository)

```text
tutorial-testing/
├── .github/workflows/
│   └── tutorial-linting.yml    # Modified: Add JSON output capture, new comment step
├── tools/
│   ├── pytest_validation.py    # Modified: Add --json-output flag
│   ├── format_pr_comment.py    # NEW: Comment formatter script
│   └── pr_comment_templates/   # NEW: Markdown templates for error types
│       ├── broken_url.md
│       ├── xml_error.md
│       ├── duration_mismatch.md
│       └── fallback.md
└── tests/
    └── test_format_pr_comment.py  # NEW: Unit tests for formatter
```

**Structure Decision**: Single project structure. All tools live in `tools/` directory of tutorial-testing repository. Templates stored alongside formatter for co-location.

## Complexity Tracking

> No violations requiring justification. Implementation follows existing patterns.
