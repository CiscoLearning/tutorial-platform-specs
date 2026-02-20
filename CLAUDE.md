# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Documentation

This project uses [GitHub Spec-Kit](https://github.com/github/spec-kit) for spec-driven development. Key documents in `.specify/`:

| Document | Purpose |
|----------|---------|
| [memory/constitution.md](.specify/memory/constitution.md) | Project principles and governance |
| [specs/requirements.md](.specify/specs/requirements.md) | Stakeholder and functional requirements |
| [specs/architecture.md](.specify/specs/architecture.md) | System architecture and data flow diagrams |
| [specs/editorial-style-guide.md](.specify/specs/editorial-style-guide.md) | Editorial rules derived from reviewer patterns |
| [specs/ai-editorial-evaluation/spec.md](.specify/specs/ai-editorial-evaluation/spec.md) | Feature spec for AI-powered editorial review |

## Repository Overview

This workspace contains two related repositories for managing Cisco U. tutorial content:

- **ciscou-tutorial-content/** - Production repository with 146+ tutorials
- **tutorial-testing/** - Testing/development mirror with CI/CD pipeline tools

### Target Audience and Content Goals

- **Audience:** Network engineers at various skill levels
- **Tutorial duration:** 15 minutes to 1 hour
- **Balance:** Theory and hands-on practice
- **Style:** Conversational, referencing both author and learner
- **Authors:** Technical Advocates (primary), Learn with Cisco instructors, TMEs
- **Review:** Part-time editors review English on PRs; goal is to reduce manual editorial work through AI automation

## Common Commands

### Validation Tools (in tutorial-testing/tools/)

```bash
# Validate sidecar.json against schema
python tools/schema_validation.py <tutorial-folder-path>

# Run pytest validation suite
python tools/pytest_validation.py

# Check and auto-fix markdown formatting issues (enhanced validation)
python tools/clean_markdown.py <tutorial-folder-path>

# Check without auto-fix (report only)
python tools/clean_markdown.py <tutorial-folder-path> --no-fix

# Check without AI-powered fixes (regex fixes only)
python tools/clean_markdown.py <tutorial-folder-path> --no-ai-fix

# Output as JSON
python tools/clean_markdown.py <tutorial-folder-path> --json-output

# Generate PR comment format
python tools/clean_markdown.py <tutorial-folder-path> --pr-comment --no-fix

# Create new tutorial from template
python tools/template_bootstrap.py

# AI analysis (requires Cisco OAuth credentials)
python tools/ai_analysis.py <tutorial-folder-path> advice|questions

# Update GUID cache after adding new tutorial
python tools/guid_update.py <tutorial-folder-path>

# Update Jira ticket status
python tools/jira_update.py <tutorial-folder-path> <operation>
```

### Generate GUIDs (for sidecar.json)

```bash
uuidgen | tr "[A-Z]" "[a-z]"
```

## Architecture

### Tutorial Structure

Each tutorial lives in a `tc-*` folder with this structure:
```
tc-example/
├── sidecar.json          # Metadata (required)
├── step-1.md             # Overview (required, first step)
├── step-2.md ... step-N.md
├── step-N.md             # Congratulations (required, last step)
├── images/               # Required folder (can be empty)
└── assets/               # Optional (configs, manifests, etc.)
```

### CI/CD Pipeline

GitHub Actions workflows in `.github/workflows/`:
- **tutorial-linting.yml** - PR validation: schema check, pytest, markdown cleanup, AI analysis
- **tutorial-automation.yml** - Post-merge deployment to staging

### Validation Pipeline Flow

1. Folder structure validation (tc-* naming, images/ folder)
2. JSON schema validation against `tools/schema.json`
3. Pytest validation (skill-levels, technologies, duration sums, GUID uniqueness)
4. **Enhanced Markdown Validation** (auto-fix enabled by default)
5. Markdown → XML conversion (tutorial_md2xml + Solomon)
6. AI editorial analysis via Cisco Chat-AI

### Enhanced Markdown Validation (FR-002)

The `clean_markdown.py` tool detects and auto-fixes markdown patterns that break XML conversion:

**BLOCKING issues (will fail pipeline):**
- `HTML_TAG`: HTML tags like `<br>`, `<p>`, `<div>` (auto-fixed: replaced with markdown equivalents)
- `LINK_NO_SPACE_BEFORE/AFTER`: Missing whitespace around links (auto-fixed)
- `LINK_BROKEN`: Line breaks inside link syntax (auto-fixed)
- `LIST_INDENT_INCONSISTENT`: Inconsistent nested list indentation (AI-powered fix)
- `CODE_BLOCK_IN_LIST`: Code blocks not indented within lists (AI-powered fix)

**WARNING issues (pipeline continues):**
- `TRAILING_WHITESPACE`: Trailing spaces/tabs (auto-fixed)
- `DOUBLE_SPACE`: Multiple consecutive spaces (auto-fixed)

**Opt-out options:**
- Add `[no-autofix]` to commit message to disable all auto-fixes
- Add `[no-ai-fix]` to disable AI fixes (regex fixes still apply)
- Use `--no-fix` flag for report-only mode

### Markdown to XML Conversion

Tutorials are converted from markdown to Cisco U. platform-specific XML. Common issues that cause XML conversion failures:

- **Whitespace around links:** Extra newlines before/after `[link](url)` syntax
- **Invalid entities:** Unescaped `&` characters (use `&amp;`)
- **Nested formatting:** Complex nested markdown can produce malformed XML

**Note:** Most of these issues are now auto-fixed by the Enhanced Markdown Validation step.

Authors currently fix these manually based on pipeline error messages. See [architecture.md](.specify/specs/architecture.md) for the full conversion flow.

## sidecar.json Requirements

**Critical format rules:**
- `id`: lowercase alphanumeric with hyphens only (must match folder name)
- `duration`: format `XXmXXs` or `XhXXmXXs` (e.g., "30m00s", "1h30m00s")
- `date`: format `YYYY-MM-DD`
- `files[].duration`: format `MM:SS` (e.g., "5:00", "10:00")
- Sum of file durations must equal top-level duration
- `ia-guid`, `lesson-guid`, `xy-guid`: unique UUIDs (checked against `guid_cache.json`)
- `authors`: exactly one author allowed
- `active`: must be `true`

**Valid skill-levels:** Beginner, Intermediate, Advanced, Expert

**Valid technologies:** Application Performance, Cloud and Computing, Collaboration, Data Center, Mobility and Wireless, Networking, Other, Security, Software

**Valid certifications:** CCNA, CCNP (various), CCIE (various), Cisco Certified DevNet Associate/Professional/Expert, Cisco Certified Cybersecurity Associate/Professional, Cisco Certified Design Expert

**Step naming rules:**
- First step label must be "Overview"
- Last step label must be "Congratulations"
- Files must be named sequentially: step-1.md, step-2.md, etc.
- Minimum 3 steps required

## Environment Variables

For AI analysis and Jira integration:
- `APP_KEY` - Cisco Chat-AI application key
- `CLIENT_ID`, `CLIENT_SECRET` - Cisco OAuth credentials
- `EMAIL`, `API_TOKEN` - Jira API credentials (cisco-learning.atlassian.net)

## Maintenance Requirements

**Keep these files up to date as the project evolves:**

1. **README.md** (top-level)
   - Update feature backlog table when features move between states
   - Update "Completed" section when features are done
   - Keep repository structure diagram current

2. **requirements.md** (.specify/specs/)
   - Add new features to backlog (FF-X)
   - Update feature priorities as they change
   - Mark completed features

3. **CLAUDE.md** (this file)
   - Update common commands when new tools are added
   - Keep architecture section current
   - Document new environment variables

## Completed Features

| Feature | Spec Location | Date |
|---------|---------------|------|
| FR-0: Tutorial-Testing Sync | specs/001-tutorial-testing-sync/ | 2026-02-18 |

## Active Technologies
- Python 3.10 (per CI workflow) + jsonschema, pytest, requests (existing); Cisco Chat-AI API (existing ai_analysis.py) (002-enhanced-markdown-validation)
- N/A (file-based validation) (002-enhanced-markdown-validation)
- Python 3.10 (matches existing tools in tutorial-testing) + pytest, requests, jsonschema (already in use) (004-pr-comment-enhancements)
- N/A (file-based JSON output for inter-step communication) (004-pr-comment-enhancements)

## Recent Changes
- 002-enhanced-markdown-validation: Added Python 3.10 (per CI workflow) + jsonschema, pytest, requests (existing); Cisco Chat-AI API (existing ai_analysis.py)
