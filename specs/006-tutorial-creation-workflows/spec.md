# FF-2: Tutorial Creation Workflows

**Status:** Complete
**PR:** [ciscou-tutorial-content#344](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/344)
**Date:** 2026-02-20

## Problem Statement

Tutorial authors have varying technical skill levels:

1. **Non-technical authors** (instructors, TMEs) don't have local development environments and struggle with Git workflows
2. **Light technical users** can work in a browser but need guidance
3. **Power users** want fast local iteration without waiting for CI

The previous workflow required all authors to:
- Clone the repository locally
- Manually create folder structure and sidecar.json
- Know Git commands for branching and committing

This created a significant barrier to entry for content creation.

## Solution

Implement three parallel workflows targeting different user personas:

### 1. GitHub Issue Form (Non-Technical Users)

Zero setup required - authors fill out a form and get a PR automatically.

```
User fills form → GitHub Action runs → Folder created → PR opened → User edits in GitHub UI
```

**Implementation:**
- `.github/ISSUE_TEMPLATE/new-tutorial.yml` - Form with all required fields
- `.github/workflows/create-tutorial.yml` - Action that processes the issue
- `tools/create_tutorial_from_issue.py` - Parses form data and generates files

### 2. GitHub Codespace (Light Technical Users)

Pre-configured VS Code in browser with all dependencies installed.

**Implementation:**
- `.devcontainer/devcontainer.json` - Container with Python 3.10, extensions
- `.devcontainer/welcome.md` - Quick start instructions
- `.vscode/tasks.json` - VS Code tasks for common operations

### 3. Interactive CLI Wizard (Power Users)

Step-by-step prompts that generate everything with one command.

**Implementation:**
- `tools/tutorial_wizard.py` - Interactive CLI

## User Stories

### US-1: Non-Technical Author Creates Tutorial

**As a** non-technical author
**I want to** create a tutorial by filling out a form
**So that** I don't need to learn Git or set up a development environment

**Acceptance Criteria:**
- [ ] I can click "New Issue" and select "Create New Tutorial"
- [ ] The form collects all required metadata
- [ ] A PR is automatically created with my tutorial folder
- [ ] I receive a comment with a link to edit my content
- [ ] I can edit markdown directly in GitHub UI

### US-2: Codespace User Creates Tutorial

**As a** user who prefers browser-based development
**I want to** use a pre-configured Codespace
**So that** I don't need to install anything locally

**Acceptance Criteria:**
- [ ] Codespace has Python 3.10 and all dependencies
- [ ] Welcome message explains how to get started
- [ ] VS Code tasks are available for common operations
- [ ] `tutorial_wizard.py` works in Codespace

### US-3: Power User Creates Tutorial Quickly

**As a** power user with a local environment
**I want to** run an interactive wizard
**So that** I can create tutorials quickly without manual file creation

**Acceptance Criteria:**
- [ ] Wizard prompts for all required fields
- [ ] Wizard generates valid sidecar.json with GUIDs
- [ ] Wizard creates step files with templates
- [ ] Wizard optionally creates git branch and commits

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tutorial Creation Flows                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Issue Form     │    │    Codespace     │    │   Local CLI      │
│  (Non-Technical) │    │(Light Technical) │    │  (Power User)    │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ create-tutorial  │    │ tutorial_wizard  │    │ tutorial_wizard  │
│ .yml (Action)    │    │ .py (in VS Code) │    │ .py (terminal)   │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────────────────────────────┐
│ create_tutorial  │    │            Generated Files               │
│ _from_issue.py   │───▶│  tc-tutorial-name/                       │
└──────────────────┘    │  ├── sidecar.json (valid GUIDs)          │
                        │  ├── step-1.md (Overview template)        │
                        │  ├── step-N.md (Content templates)        │
                        │  └── images/ (.gitkeep)                   │
                        └──────────────────────────────────────────┘
```

## Issue Form Fields

| Field | Type | Required | Maps To |
|-------|------|----------|---------|
| Tutorial Title | input | Yes | `sidecar.title` |
| Tutorial Slug | input | No | `sidecar.id` (auto-generated if empty) |
| Description | textarea | Yes | `sidecar.description` |
| Author Name | input | Yes | `sidecar.authors[0].name` |
| Author Email | input | Yes | `sidecar.authors[0].email` |
| Duration | dropdown | Yes | `sidecar.duration` |
| Skill Level | dropdown | Yes | `sidecar.skill-levels` |
| Technologies | checkboxes | Yes | `sidecar.technologies` |
| Certifications | checkboxes | No | `sidecar.certifications` |
| Tags | input | Yes | `sidecar.tags` |
| Number of Steps | dropdown | Yes | Determines file count |
| Step Titles | textarea | No | `sidecar.files[].label` |

## Generated Files

### sidecar.json
- All GUIDs auto-generated (valid UUIDs)
- Duration distributed evenly across steps
- Date set to current date
- All required fields populated

### step-1.md (Overview)
```markdown
## Overview

Welcome to this tutorial on **{title}**!

### What You'll Learn
- [ ] First learning objective
- [ ] Second learning objective

### Prerequisites
- Basic understanding of [topic]

### Time to Complete
This tutorial takes approximately [X] minutes.
```

### step-N.md (Content)
```markdown
## {step_title}

[Add your content here]

### Section Heading
Explain the concept or task.

### Example
```code
# Add code examples
```

### Try It Yourself
1. First step
2. Second step
```

### step-final.md (Congratulations)
```markdown
## Congratulations!

You have successfully completed **{title}**!

### What You Learned
- ✅ First accomplishment
- ✅ Second accomplishment

### Next Steps
- Explore [related topic]
- Try [advanced tutorial]
```

## VS Code Tasks

| Task | Command | Description |
|------|---------|-------------|
| Create New Tutorial | `python tools/tutorial_wizard.py` | Interactive wizard |
| Validate Current Tutorial | `python tools/validate_tutorial.py ${fileDirname}` | Check for errors |
| Validate and Fix Tutorial | `python tools/validate_tutorial.py ${fileDirname} --fix` | Auto-fix issues |
| Fix Markdown Issues | `python tools/clean_markdown.py ${fileDirname}` | Clean formatting |
| Check GUIDs | `python tools/guid_generator.py ${fileDirname}/sidecar.json` | Validate GUIDs |
| Generate New GUIDs | `python tools/guid_generator.py ${fileDirname}/sidecar.json --fix` | Auto-generate |

## Testing

### Manual Test: Issue Form
1. Go to repository → Issues → New Issue
2. Select "Create New Tutorial"
3. Fill out form with test data
4. Submit issue
5. Verify:
   - Action runs successfully
   - PR is created
   - Folder contains correct files
   - sidecar.json passes schema validation

### Manual Test: Codespace
1. Open Codespace from repository
2. Wait for container to build
3. Run `python tools/tutorial_wizard.py`
4. Follow prompts
5. Verify generated files

### Manual Test: Local CLI
1. Run `python tools/tutorial_wizard.py`
2. Follow prompts
3. Verify:
   - Folder created with correct structure
   - sidecar.json valid
   - Git branch created (if selected)

## Related Documentation

- [CONTRIBUTING.md](https://github.com/CiscoLearning/ciscou-tutorial-content/blob/main/CONTRIBUTING.md) - Full author guide
- [FR-4: Pre-commit Validation](../005-pre-commit-validation/spec.md) - GUID handling
- [FR-1: Enhanced Markdown Validation](../002-enhanced-markdown-validation/spec.md) - Markdown rules
