# Cisco U. Tutorial Platform Requirements

## System Context

### Current State
The Cisco U. tutorial platform enables technical content creation through a GitHub-based workflow:

1. **Authors** create tutorials as markdown files with metadata in `sidecar.json`
2. **CI Pipeline** validates structure, schema, and converts markdown to Cisco U. XML format
3. **Editors** manually review PRs for style, grammar, and consistency
4. **Technical Advocates** approve and merge PRs
5. **Automation** pushes XML to publishing team via REST API
6. **Publishing Team** deploys to staging, then production after UAT approval

### Pain Points
- **XML Conversion Errors**: Whitespace issues around links and file references cause XML parsing failures; authors must manually fix based on pipeline error messages
- **Manual Editorial Review**: Two part-time editors review English quality on every PR
- **Inconsistent Style**: Authors don't always follow style conventions (heading format, acronym expansion, punctuation)
- **Validation Feedback Loop**: Authors discover issues late in the process

## Stakeholder Requirements

### Tutorial Authors (Technical Advocates, Instructors, TMEs)

| ID | Requirement | Priority |
|----|-------------|----------|
| AUTH-1 | Get clear, actionable feedback on validation errors before merge | High |
| AUTH-2 | Receive AI-powered editorial suggestions during PR review | High |
| AUTH-3 | Scaffold new tutorials with correct structure automatically | Medium |
| AUTH-4 | Preview how tutorial will render in Cisco U. format | Low |

### Editorial Team (Jill, Matt Sperling)

| ID | Requirement | Priority |
|----|-------------|----------|
| EDIT-1 | AI should catch common style issues before human review | High |
| EDIT-2 | Style guide violations should be flagged automatically | High |
| EDIT-3 | Reduce volume of PRs requiring manual corrections | High |

### Technical Advocates (Reviewers/Approvers)

| ID | Requirement | Priority |
|----|-------------|----------|
| TA-1 | Trust that merged PRs will convert to valid XML | High |
| TA-2 | See editorial quality score/summary before approving | Medium |
| TA-3 | One tutorial per PR enforced automatically | Medium |

### Publishing Team

| ID | Requirement | Priority |
|----|-------------|----------|
| PUB-1 | Receive valid XML that doesn't require manual fixes | High |
| PUB-2 | Clear differentiation between NEW and EXISTING tutorials | Medium |

## Functional Requirements

### FR-0: Tutorial-Testing Environment Setup (PREREQUISITE) ✅ COMPLETE

**Status:** Completed 2026-02-18 | [Spec](../../specs/001-tutorial-testing-sync/spec.md)

**Priority:** Critical - Must be completed before other features

**Current State:**
- `tutorial-testing` is the development environment where tools were built (intern work, summer 2025)
- Contains 27 test tutorials, 8 poplartest folders, experimental branches
- Has `tools/` folder with all validation scripts
- Production (`ciscou-tutorial-content`) has 137 real tutorials

**Goals:**
1. Sync production tutorials into testing for realistic validation testing
2. Preserve existing test fixtures and development work
3. Keep workflows in sync between repos

**Implementation approach:**

1. **Archive intern work:**
   - Move test tutorials (tc-avocado-test, tc-jira-demo, etc.) to `_test-fixtures/` folder
   - Document purpose of poplartest* folders, archive or remove
   - Keep experimental branches as-is for reference

2. **Sync production content:**
   - GitHub Action to pull all `tc-*` tutorials from prod on schedule (daily) or manual trigger
   - Sync to a `tutorials/` or root folder (TBD based on workflow expectations)
   - Update `guid_cache.json` from prod

3. **Sync workflows:**
   - Mirror all `.github/workflows/*.yml` from prod
   - Testing-specific workflows (if any) should be clearly named

4. **Preserve tools development:**
   - `tools/` folder stays in tutorial-testing (this is the source of truth for tools)
   - Changes to tools are developed here, then deployed to prod workflows

**What to preserve:**
- `tools/` - Validation scripts (source of truth)
- `template/` - Tutorial template
- `README.md` - Documentation
- Test tutorials - Move to `_test-fixtures/` for regression testing
- Experimental branches - Keep for reference

**What to sync from prod:**
- All `tc-*` tutorial folders (137+)
- `guid_cache.json`
- `.github/workflows/*.yml`
- `schema.json` (if in prod root)

### FR-1: Enhanced Markdown Validation ✅ COMPLETE

**Status:** Completed 2026-02-18 | [Spec](../../specs/002-enhanced-markdown-validation/spec.md) | [Deliverables](../../specs/002-enhanced-markdown-validation/deliverables.md)

Validate markdown files for issues that cause XML conversion failures:
- Whitespace before/after links
- Improper newlines around inline elements
- Invalid image/file references
- Code block formatting issues

**Results:** 41% reduction in false positives, 7 detection rules, 50 unit tests. See [scan results](../../specs/002-enhanced-markdown-validation/scan-results-snapshot.md) for details.

### FR-2: Editorial Style Validation
Automatically check for style guide compliance based on editorial patterns:
- Heading format (imperative mood, not gerund)
- Acronym expansion on first use
- Punctuation standards (em-dash spacing, serial comma)
- Technical term formatting (hyphenation, code vs. bold)
- Parallel structure in lists

### FR-3: AI-Powered Editorial Feedback
Enhance existing `ai_analysis.py` to provide:
- Style guide violation detection
- Suggested corrections for common issues
- Quality score with breakdown by category
- Comparison to editorial patterns from historical commits

### FR-4: Pre-commit Validation
Provide local validation before pushing:
- Schema validation
- Duration sum check
- GUID uniqueness check
- Basic style checks

### FR-5: PR Comment Enhancements
Improve automated PR comments to include:
- Categorized issues (blocking vs. suggestions)
- Specific line references for fixes
- Style guide references for violations
- Before/after examples for corrections

## Non-Functional Requirements

### NFR-1: Performance
- Validation pipeline should complete within 5 minutes
- AI analysis should complete within 2 minutes

### NFR-2: Accuracy
- Style suggestions should have <10% false positive rate
- XML conversion predictions should be >95% accurate

### NFR-3: Maintainability
- Style rules should be configurable, not hardcoded
- New validation rules should be addable without code changes

## Constraints

- Must integrate with existing GitHub Actions workflows
- Must use Cisco Chat-AI LLM API for AI features
- Cannot change the XML format required by publishing team
- Must maintain backward compatibility with existing tutorials
- **sidecar.json schema is owned by L&C UAT team** - schema changes require a formal request process and take time to implement

## Success Criteria

1. Reduce manual editorial corrections by 50%
2. Eliminate XML conversion errors at merge time
3. Authors receive actionable feedback within 5 minutes of PR creation
4. Style guide compliance rate increases to >90%

---

## Future Features (Backlog)

The following features have been identified but are not in the current scope. They require separate specification and planning.

### FF-1: AI-Powered Sidecar Generation

**Problem:** Authors manually create `sidecar.json` which is error-prone and time-consuming. Tags are free-form with no consistency across tutorials.

**Proposed Solution:**
- Auto-generate or update `sidecar.json` based on tutorial content
- AI suggests tags based on content analysis and existing tutorials with similar content
- On PR, detect if sidecar exists for new folder:
  - If missing: generate new sidecar from content + prompts
  - If exists: validate and suggest tag improvements
- Learn from existing tutorial tags to build consistent vocabulary

**Target Users:** All authors, especially non-technical contributors

**Dependencies:** Requires analysis of existing tag patterns across 146+ tutorials

### FF-2: Power User Local Workflow CLI

**Problem:** Technical authors want faster iteration without waiting for CI pipeline. Non-technical authors need guided setup.

**Proposed Solution:**
- Local CLI tool that provides:
  - Interactive tutorial creation wizard (prompts for title, duration, skill level, etc.)
  - Auto-creates branch (`tc-{name}`), folder structure, and initial sidecar.json
  - Local validation with auto-fix for common issues
  - Push to remote when ready
- Two modes:
  - **Guided mode:** Step-by-step prompts for non-technical users
  - **Power mode:** Quick commands with auto-fix for experienced authors

**Target Users:**
- Power users: Technical Advocates who create many tutorials
- Guided mode: Instructors and TMEs less familiar with Git

**Key Features:**
- `tutorial new` - Interactive wizard to create new tutorial
- `tutorial validate` - Run all checks locally
- `tutorial fix` - Auto-fix markdown and sidecar issues
- `tutorial push` - Validate, fix, and push to remote

### FF-3: Tutorial Preview Rendering

**Problem:** Authors cannot see how their tutorial will appear in Cisco U. before publishing (AUTH-4).

**Proposed Solution:**
- Local preview that renders markdown as Cisco U. platform would display
- Could be browser-based or VS Code extension

**Status:** Low priority, requires understanding of Cisco U. rendering engine

### FF-4: Automated GUID Cache Updates

**Problem:** The `guid_cache.json` file tracks all unique GUIDs across tutorials but is not automatically updated when tutorials are added or modified. Currently 7+ months out of date despite monthly tutorial additions.

**Proposed Solution:**
- GitHub Action in production repo that auto-regenerates `guid_cache.json` on push/merge to main
- Trigger: When any `tc-*/sidecar.json` file is added or modified
- Action: Run `python tools/guid_update.py` and commit the updated cache
- Alternative: Pre-commit hook or PR check that validates GUID uniqueness and updates cache

**Target Repository:** `ciscou-tutorial-content` (production)

**Benefits:**
- Ensures GUID uniqueness is always enforced
- Keeps cache in sync with actual tutorials
- Reduces manual maintenance burden

**Dependencies:** Requires access to modify production repo workflows

### FF-5: Legacy Hugo Tutorial Migration

**Problem:** A significant number of tutorials exist in the legacy `cisco-learning-codelabs` repository using Hugo/Codelabs format. These tutorials were never migrated to the current `ciscou-tutorial-content` repository structure (markdown + sidecar.json). This content is effectively orphaned and not accessible through the current Cisco U. platform workflow.

**Current State:**
- Legacy repo: `cisco-learning-codelabs` (Hugo-based Codelabs format)
- Unknown number of tutorials that may still be valuable
- Different folder structure and metadata format than current system
- May have outdated content, broken links, or obsolete technologies

**Proposed Solution:**

1. **Audit legacy content:**
   - Inventory all tutorials in `cisco-learning-codelabs`
   - Categorize by: still relevant, needs update, obsolete
   - Identify content owners/authors where possible

2. **Create migration tooling:**
   - Script to convert Hugo/Codelabs format to markdown + sidecar.json
   - Map legacy metadata fields to current sidecar.json schema
   - Generate GUIDs for migrated tutorials
   - Preserve images and assets

3. **Content review process:**
   - Technical review for accuracy (technologies may have changed)
   - Editorial review for style guide compliance
   - Validation through current CI pipeline

4. **Migration execution:**
   - Batch migration with PR per tutorial or small groups
   - Track migration status in spreadsheet or project board
   - Archive or deprecate legacy repo after complete migration

**Target Users:**
- Content consumers who may be missing valuable tutorials
- Authors who created legacy content

**Effort Estimate:** Medium-High (depends on number of tutorials and content freshness)

**Dependencies:**
- Access to `cisco-learning-codelabs` repository
- Content owners available for review
- Editorial capacity for review pass

**Open Questions:**
- How many tutorials are in the legacy repo?
- What percentage are still technically accurate?
- Who owns the content review responsibility?
- Should obsolete tutorials be archived or deleted?
