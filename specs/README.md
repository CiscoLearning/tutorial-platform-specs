# Feature Specifications

This directory contains all feature specifications for the Cisco U. Tutorial Platform improvements.

## Overview

The tutorial platform has evolved through 7 major features, transforming from a manual, error-prone content pipeline into an automated, AI-assisted system.

## Features at a Glance

| # | Feature | Status | Impact |
|---|---------|--------|--------|
| 001 | Tutorial-Testing Sync | Complete | Daily sync from production to testing |
| 002 | Enhanced Markdown Validation | Complete | 20+ rules, auto-fix for XML compatibility |
| 003 | Hugo Tutorial Migration | Complete | 108 tutorials migrated, 92% auto-fix |
| 004 | PR Comment Enhancements | Complete | CI errors surfaced with fix guidance |
| 005 | Pre-commit Validation | Complete | GUID auto-generation, local CLI |
| 006 | Tutorial Creation Workflows | Complete | Issue form, Codespace, CLI wizard |
| 007 | AI Editorial Agent | In Progress | ~75% coverage of human editor changes |

---

## The Journey

### Phase 1: Foundation (001-002)

**Problem:** Tutorial testing was disconnected from production, and markdown issues caused XML conversion failures.

**Solution:**
- Automated daily sync from `ciscou-tutorial-content` to `tutorial-testing`
- Created `clean_markdown.py` with 20+ detection rules and auto-fix capabilities
- Eliminated manual copy-paste workflow

**Impact:** Authors get immediate feedback on markdown issues that would break the pipeline.

### Phase 2: Migration (003)

**Problem:** 108 tutorials from the old Hugo-based system needed migration.

**Solution:**
- Batch processing with auto-fix for common issues
- 92% of issues auto-fixed without human intervention

**Impact:** Completed migration in days instead of weeks.

### Phase 3: Developer Experience (004-006)

**Problem:** CI errors were buried in logs, GUID generation was manual, and creating new tutorials required copy-pasting templates.

**Solution:**
- PR comments now include specific error locations and fix suggestions
- GUIDs auto-generated on PR creation
- Issue form creates tutorial folder structure automatically
- Codespace support for instant development environment
- CLI wizard for local development

**Impact:** New tutorial creation time reduced from hours to minutes.

### Phase 4: AI Editorial (007)

**Problem:** Human editors (Matt and Jill) manually review every PR for non-technical editorial issues, spending **1.5-6+ hours per tutorial** (verified from commit timestamps: PR #193 = 1h36m, PR #177 = 6h21m).

**Solution:**
- Extracted 1,689 editorial changes from 24 PRs to understand editor patterns
- Parsed official Cisco Technical Content Style Guide (182 pages, 471 terms)
- Created `cisco-style-rules.json` with 75+ term substitutions
- Built `acronym-database.json` with 100+ Cisco product/networking terms
- Added heading conversion to `clean_markdown.py` for Solomon XML compatibility

**Current State:**
- ~75% estimated coverage of human editor changes (up from ~52% with inferred rules)
- Official Cisco rules as the source of truth
- Living acronym database that can evolve with new products

---

## Impact Summary

### Before This Project

- Manual sync between repos
- Markdown issues discovered late in pipeline
- XML conversion failures blocked releases
- New tutorial setup took hours
- Editors spent 1.5-6+ hours/PR on routine fixes

### After This Project

- Automated daily sync
- Immediate markdown feedback with auto-fix
- 92% auto-fix rate for common issues
- New tutorial setup in minutes
- AI agent handles ~75% of routine editorial (in progress)

---

## Directory Structure

Each feature spec follows a consistent structure:

```
NNN-feature-name/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (if applicable)
├── tasks.md             # Task breakdown (if applicable)
├── research.md          # Research findings (if applicable)
├── data-model.md        # Data model (if applicable)
├── quickstart.md        # Quick start guide (if applicable)
├── checklists/          # Pre-implementation checklists
├── contracts/           # API contracts, schemas
├── reference-code/      # Reference implementations
└── archive/             # Archived intermediate work
```

---

## Key Files

### Official Style Rules

| File | Location | Description |
|------|----------|-------------|
| `cisco-style-rules.json` | `tutorial-testing/tools/` | 75+ official Cisco terms from style guide |
| `acronym-database.json` | `tutorial-testing/.claude/references/` | 100+ acronyms with expansion rules |
| `editorial-reviewer.md` | `tutorial-testing/.claude/agents/` | AI agent instructions |

### Analysis Results

| File | Location | Description |
|------|----------|-------------|
| `COMPARISON-REPORT.md` | `tutorial-testing/analysis/v2-official-rules/` | Full v2 analysis report |
| `summary.json` | `tutorial-testing/analysis/v2-official-rules/` | Aggregated statistics |
| `pr-*.json` | `tutorial-testing/analysis/v2-official-rules/` | Individual PR analyses |

---

## Next Steps (FR-7)

1. **Implement deterministic rules engine** - `editorial_validation.py`
2. **Integrate with CI pipeline** - Run on every PR
3. **Generate PR comments** - In Jill's step-by-step format
4. **Measure actual coverage** - Compare against live editor changes

---

## Contributing

When working on new features:

1. Create a new numbered directory: `NNN-feature-name/`
2. Start with `spec.md` using the template in `.specify/templates/`
3. Use `/speckit.plan` to generate implementation plans
4. Use `/speckit.tasks` to break down into tasks
5. Archive intermediate work when feature is complete

---

*Last updated: 2026-02-21*
