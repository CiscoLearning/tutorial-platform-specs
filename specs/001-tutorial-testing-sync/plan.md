# Implementation Plan: Tutorial-Testing Environment Sync

**Branch**: `001-tutorial-testing-sync` | **Date**: 2026-02-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-tutorial-testing-sync/spec.md`

## Summary

Establish the `tutorial-testing` repository as a proper mirror of the production `ciscou-tutorial-content` repository. This enables developers to test validation tool changes against real production content (137+ tutorials) while preserving existing test fixtures created by an intern. The sync runs daily overnight with a manual trigger for on-demand updates.

## Technical Context

**Language/Version**: YAML (GitHub Actions), Bash (scripting)
**Primary Dependencies**: GitHub Actions, git commands
**Storage**: Git repositories (file-based)
**Testing**: Manual verification of sync results, automated workflow status checks
**Target Platform**: GitHub-hosted runners (ubuntu-latest)
**Project Type**: CI/CD automation (no application code)
**Performance Goals**: Full sync completes within 15 minutes for 137+ tutorials
**Constraints**: Must not modify tools/ or template/ folders; production content takes precedence
**Scale/Scope**: ~137 tutorials, ~500MB repository size estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | This Feature | Status |
|-----------|-------------|--------------|--------|
| I. Tutorial Quality First | Content must be technically accurate | N/A - infrastructure feature | PASS |
| II. Structured Content Organization | Standard step-based structure | N/A - syncs existing content | PASS |
| III. Validate Early, Fail Fast | Validation at PR time | Sync enables testing validation tools | PASS |
| IV. Editorial Consistency | Automated style enforcement | N/A - infrastructure feature | PASS |
| V. Transparent Pipeline Feedback | Actionable feedback | Sync status reporting required | PASS |

**Gate Status**: PASS - This is an infrastructure feature that supports the constitution principles by enabling proper testing of validation tools.

## Project Structure

### Documentation (this feature)

```text
specs/001-tutorial-testing-sync/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A for this feature)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
tutorial-testing/
├── .github/
│   └── workflows/
│       └── sync-from-production.yml  # NEW: Sync workflow
├── _test-fixtures/                   # NEW: Archived test content
│   ├── tc-avocado-test/
│   ├── tc-jira-demo/
│   ├── poplartest/
│   └── ...
├── tc-*/                             # SYNCED: Production tutorials
├── tools/                            # PRESERVED: Validation scripts
├── template/                         # PRESERVED: Tutorial template
├── guid_cache.json                   # SYNCED: From production
└── README.md                         # PRESERVED
```

**Structure Decision**: This is a CI/CD automation feature. The implementation lives entirely in the `tutorial-testing` repository's `.github/workflows/` directory, with a one-time migration of test fixtures to `_test-fixtures/`.

## Complexity Tracking

> No constitution violations. This is a straightforward automation feature.

| Aspect | Approach | Justification |
|--------|----------|---------------|
| Sync mechanism | Git operations via GitHub Actions | Native GitHub integration, no external dependencies |
| Test fixture preservation | One-time archive to _test-fixtures/ | Clear separation between production content and test data |
| Schedule | cron + workflow_dispatch | Standard GitHub Actions patterns |
