# Feature Specification: Enhanced Markdown Validation

**Feature Branch**: `002-enhanced-markdown-validation`
**Created**: 2026-02-18
**Completed**: 2026-02-18
**Status**: Complete
**Input**: FR-1 from requirements.md - Validate markdown for XML conversion issues

## Problem Statement

Authors submit markdown tutorials that pass schema validation but fail during XML conversion. The XML converter (`tutorial_md2xml` + Solomon) produces cryptic error messages with line numbers referencing the generated XML, not the source markdown. Authors must manually debug and fix issues through trial and error.

**Evidence from PRs:**
- PR #177: `<br>` tag caused cascading XML parse errors
- PR #196: Nested list issues caused 12+ XML tag mismatch errors
- PR #216: Schema issues (separate from markdown)

## User Scenarios & Testing

### User Story 1 - Author Gets Pre-Conversion Feedback (Priority: P1)

A tutorial author submits a PR and receives immediate feedback about markdown patterns that will break XML conversion, with specific line numbers and fix suggestions.

**Acceptance Scenarios:**

1. **Given** a markdown file contains `<br>` or other HTML tags, **When** validation runs, **Then** author sees "Line 45: HTML tag `<br>` will break XML conversion. Use blank line for paragraph breaks instead."

2. **Given** a nested list has inconsistent indentation, **When** validation runs, **Then** author sees "Line 23-28: Nested list indentation inconsistent. Use 2 or 4 spaces consistently."

3. **Given** markdown passes all new validations, **When** XML conversion runs, **Then** it succeeds without parse errors (eliminate false negatives).

---

### User Story 2 - Auto-Fix (Priority: P2)

Simple issues are automatically fixed by default, reducing manual cleanup. Authors can opt out with `--no-fix` flag.

**Acceptance Scenarios:**

1. **Given** a file has trailing whitespace on lines 10, 15, 20, **When** validation runs (default), **Then** trailing whitespace is removed and changes are committed.

2. **Given** a file has `60m00s` duration in sidecar.json, **When** validation runs, **Then** it's converted to `1h00m00s`.

3. **Given** a nested list has inconsistent indentation, **When** AI reformatting runs, **Then** list is fixed and PR comment shows "Auto-fixed nested list on lines 23-28: [diff or before/after]".

4. **Given** a file link `[text](url)` is missing required spacing around it, **When** AI reformatting runs, **Then** spacing is added and change is shown in PR comment.

5. **Given** author runs with `--no-fix` flag, **When** issues are found, **Then** only warnings are shown, no files modified.

6. **Given** auto-fix modifies files, **When** PR is updated, **Then** author sees summary comment of all changes made (can revert if needed).

---

### User Story 3 - Blocking vs Warning Categorization (Priority: P3)

Validation clearly distinguishes between issues that will definitely fail vs those that might cause problems.

**Acceptance Scenarios:**

1. **Given** HTML tags are found, **When** validation reports, **Then** it's marked as BLOCKING with red indicator.

2. **Given** trailing whitespace is found, **When** validation reports, **Then** it's marked as WARNING with yellow indicator.

3. **Given** only warnings exist (no blockers), **When** CI runs, **Then** pipeline continues but shows warning summary.

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Detect HTML tags (`<br>`, `<p>`, `<div>`, etc.) in markdown content | P1 |
| FR-002 | Detect inconsistent nested list indentation | P1 |
| FR-003 | Detect line breaks inside link/image syntax `[text](url)` | P1 |
| FR-004 | Detect links/images missing required whitespace around them | P1 |
| FR-005 | Detect code blocks inside lists with incorrect indentation | P1 |
| FR-006 | Map validation errors to source markdown line numbers | P1 |
| FR-007 | Provide actionable fix suggestions for each error type | P1 |
| FR-008 | Auto-fix trailing whitespace (default on, opt-out via `--no-fix`) | P2 |
| FR-009 | Auto-fix double spaces outside code blocks (default on) | P2 |
| FR-010 | Auto-fix duration format in sidecar.json (default on) | P2 |
| FR-011 | AI-powered markdown reformatting (nested lists, link spacing, complex structures) with PR comment showing changes | P2 |
| FR-012 | Categorize issues as BLOCKING or WARNING | P3 |
| FR-013 | Continue pipeline on warnings, fail on blockers | P3 |

### Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-001 | Validation completes within 30 seconds for largest tutorial |
| NFR-002 | Zero false positives for blocking issues (don't block valid markdown) |
| NFR-003 | <5% false negatives (catch 95%+ of patterns that break XML) |

## Technical Approach

### Option A: Enhance `clean_markdown.py` (Recommended)

Extend the existing tool with new pattern detection:

```python
# New patterns to detect
HTML_TAG_PATTERN = re.compile(r'<(br|p|div|span|hr|img)[^>]*/?>')
BROKEN_LINK_PATTERN = re.compile(r'\[[^\]]*\n[^\]]*\]\([^\)]*\)')
LIST_INDENT_PATTERN = re.compile(r'^(\s*)[-*+]\s')
```

**Pros:**
- Builds on existing, tested code
- Already integrated into CI workflow
- Familiar to team

**Cons:**
- File getting large, may need refactoring

### Option B: New Dedicated Validator

Create `markdown_validator.py` with pluggable rule system:

```python
class MarkdownValidator:
    rules = [HTMLTagRule(), ListIndentRule(), LinkSyntaxRule()]

    def validate(self, file_path) -> List[ValidationIssue]:
        ...
```

**Pros:**
- Cleaner architecture
- Easier to add/remove rules
- Better testability

**Cons:**
- More work upfront
- Need to integrate into CI

### Recommendation

Start with **Option A** for P1 requirements (quick win), refactor to **Option B** when adding P2/P3 features.

## Implementation Phases

### Phase 1: Detection (P1 Requirements)
1. Add HTML tag detection to `clean_markdown.py`
2. Add nested list validation
3. Add link syntax validation
4. Enhance error messages with fix suggestions
5. Test against historical failing PRs

### Phase 2: Auto-Fix (P2 Requirements)
1. Enable auto-fix by default in `clean_markdown.py`
2. Add duration format auto-fix to `schema_validation.py`
3. Add `--no-fix` flag for opt-out
4. Integrate AI (Cisco Chat-AI) for complex markdown reformatting (nested lists, link spacing, code blocks in lists)
5. Generate PR comment with diff of all auto-fixed changes
6. Update CI to apply fixes and commit changes

### Phase 3: Categorization (P3 Requirements)
1. Classify each rule as BLOCKING or WARNING
2. Update CI to fail only on blockers
3. Enhance PR comment format with severity indicators

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| XML conversion failures | Reduce by 80% | Compare failure rate before/after |
| Time to fix validation issues | Reduce by 50% | Author feedback survey |
| Auto-fix adoption | 70% of authors use it | CI logs |
| False positive rate | <1% | Manual review of blocked PRs |

## Dependencies

- Access to historical failing PRs for test cases
- Understanding of `tutorial_md2xml` converter behavior
- CI workflow modification permissions
- Cisco Chat-AI API access (for AI-powered nested list reformatting)

## Out of Scope

- Modifying the XML converter itself
- Editorial/style validation (that's FR-2/FR-3)
- Changes to sidecar.json schema (owned by L&C UAT team)

## Design Decisions

1. **Auto-fix is opt-OUT** - Enabled by default. Most authors don't want to deal with manual fixes for trivial issues. Add `--no-fix` flag for those who want control.

2. **No XML preview** - Authors work in markdown; XML conversion is a black box they don't need to see. Focus on catching issues early with clear markdown-centric feedback.

3. **AI-powered markdown reformatting** - Use AI to auto-fix complex issues that regex can't handle reliably: nested lists, link spacing (links need whitespace around them), code blocks in lists, and other structural problems. Include a PR comment showing exactly what was changed so authors can revert or adjust if the AI's formatting doesn't match their intent.

4. **AI failure handling** - If Cisco Chat-AI is unavailable (timeout, rate limit, error), retry up to 3 times with exponential backoff. If still failing, skip AI fixes, report the issue as WARNING in PR comment ("AI reformatting unavailable, manual fix recommended for lines X-Y"), and continue pipeline with regex-only fixes.

5. **AI response validation** - Before applying AI-generated fixes, validate that: (a) URLs are preserved, (b) content length is within 20% of original, (c) code blocks are unchanged. If validation fails, reject the AI fix, keep original content, and report as WARNING ("AI fix rejected - manual fix recommended").

6. **Commit message opt-out** - Authors have two options:
   - `[no-autofix]` - Skip ALL auto-fixes (both regex and AI)
   - `[no-ai-fix]` - Skip AI fixes only (regex fixes still apply)

7. **User education** - Every PR comment footer includes: "To disable auto-fix, add `[no-autofix]` to your commit message. Use `[no-ai-fix]` to skip AI fixes only."

## Clarifications

### Session 2026-02-18

- Q: When AI API fails, what should happen? → A: Retry up to 3 times with exponential backoff, then skip AI fixes and report as WARNING (continue pipeline)
- Q: If AI returns invalid/broken markdown, what should happen? → A: Reject the AI fix, keep original content, report as WARNING with "AI fix rejected - manual fix recommended"
- Q: Support commit message flag to skip auto-fix? → A: Yes, support both `[no-autofix]` (skip all) and `[no-ai-fix]` (skip AI only, regex still applies). Document in PR comment footer to educate users.

## Related Features

- **FF-4 (GUID Cache Updates)**: Could be added to same CI enhancement effort
- **FR-2 (Editorial Style)**: Will build on this validation framework

## Lessons Learned

### 1. False Positive Detection is Critical

**Problem**: Initial CODE_BLOCK_IN_LIST detection flagged 848 issues in first 50 production tutorials (96% of all blocking issues). Investigation revealed most were false positives.

**Root Cause**: The detection logic set `in_list = True` when seeing a list item but never reset it. Any code block appearing anywhere after a list started was flagged, even when properly separated by blank lines.

**Fix**: Track blank lines after list content. A blank line followed by non-indented content ends the list context. Only flag code blocks that appear immediately after list items without blank line separation.

**Impact**: ~90% reduction in CODE_BLOCK_IN_LIST issues (from 848 to ~100 in first 50 tutorials).

**Lesson**: Always test detection rules against real-world content before deployment. High issue counts are a red flag for false positives.

### 2. Comprehensive Unit Tests Prevent Regressions

Created `tests/test_detection_rules.py` with 38 tests covering:
- Edge cases for each detection rule
- Real-world patterns extracted from production tutorials
- Both positive cases (should detect) and negative cases (should NOT detect)

Test categories:
- `TestHTMLTags`: 6 tests
- `TestLinkSpacing`: 8 tests
- `TestBrokenLinks`: 4 tests
- `TestListIndent`: 4 tests
- `TestCodeBlockInList`: 9 tests (most critical after false positive discovery)
- `TestTrailingWhitespace`: 4 tests
- `TestDoubleSpace`: 3 tests

### 3. Production Tutorials May Have Hidden Fixes

Many tutorials with "blocking" issues still work on Cisco U. because:
- UAT team applied manual XML fixes after conversion
- XML converter is more tolerant than expected
- Issues were fixed in UAT but source markdown was never updated

This means the repo markdown is not always the source of truth for what's live.

### 4. AI Context Matters for Complex Fixes

For AI-powered fixes (nested lists, code blocks in lists), the detection function must capture the FULL context block, not just the problematic line. Original implementation only passed single lines to AI, which couldn't understand the structure to fix.

**Fix**: Detection functions now capture entire list blocks or list-item-plus-code-block contexts for AI processing.

### 5. Image Syntax vs Link Syntax

**Problem**: LINK_NO_SPACE_BEFORE flagged 80 issues in first 100 tutorials, many were false positives.

**Root Cause**: Pattern `\S\[[^\]]+\]\([^)]+\)` matches any non-whitespace before `[`. But image syntax `![alt](url)` intentionally has `!` before `[`.

**Fix**: Changed pattern to `[^\s!]\[[^\]]+\]\([^)]+\)` - excludes `!` from triggering the rule.

**Impact**: 92% reduction (80 → 6 issues in first 100 tutorials).

**Lesson**: When detecting patterns, consider related syntax that shares similar structure.

### 6. Graceful Degradation for Optional Dependencies

The XML conversion test requires `LEARNING_TOKEN` with access to LearningAtCisco private repos. Not all contributors have this access.

**Solution**: Download step sets an output flag. Subsequent steps check the flag and skip gracefully rather than failing the entire workflow.

## Implementation Summary

**Completed**: 2026-02-18

### Deliverables

1. **Enhanced `clean_markdown.py`** (tutorial-testing/tools/)
   - All 7 detection rules implemented: HTML_TAG, LINK_NO_SPACE_BEFORE, LINK_NO_SPACE_AFTER, LINK_BROKEN, LIST_INDENT, CODE_BLOCK_IN_LIST, TRAILING_WHITESPACE
   - Auto-fix with regex for simple patterns (HTML tags, spacing, whitespace)
   - AI-powered reformatting via Cisco Chat-AI for complex issues (nested lists, code blocks in lists)
   - Severity system (BLOCKING vs WARNING)
   - CLI with --no-fix, --json-output, --verbose flags
   - Commit message opt-out support: `[no-autofix]`, `[no-ai-fix]`

2. **Integration Tests** (tutorial-testing/.github/workflows/)
   - Unit tests for all detection rules
   - Full XML conversion pipeline test with tutorial_md2xml + Solomon
   - Test fixtures with all 7 issue types

3. **AI Integration**
   - OAuth2 authentication with Cisco Chat-AI
   - Exponential backoff retry (3 attempts)
   - Response validation (URL preservation, content length, code block protection)
   - Graceful fallback to WARNING when AI unavailable

### Test Results

Integration tests verified:
- 19 blocking issues detected in test fixture
- AI successfully fixed 7/8 issues (nested lists, code blocks in lists)
- XML conversion succeeded after fixes
- Solomon transform and lint passed

### Repositories Updated

- **CiscoLearning/tutorial-testing**: PR #101 - Enhanced Markdown Validation
- **CiscoLearning/ciscou-tutorial-content**: test/integration-xml-pipeline branch (testing)
