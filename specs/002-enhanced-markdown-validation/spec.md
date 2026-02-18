# Feature Specification: Enhanced Markdown Validation

**Feature Branch**: `002-enhanced-markdown-validation`
**Created**: 2026-02-18
**Status**: Draft
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

### User Story 2 - Whitespace Auto-Fix (Priority: P2)

Authors can opt to have simple whitespace issues automatically fixed, reducing manual cleanup.

**Acceptance Scenarios:**

1. **Given** a file has trailing whitespace on lines 10, 15, 20, **When** auto-fix runs, **Then** trailing whitespace is removed and commit is amended/pushed.

2. **Given** a file has `60m00s` duration in sidecar.json, **When** auto-fix runs, **Then** it's converted to `1h00m00s`.

3. **Given** auto-fix modifies files, **When** PR is updated, **Then** author sees summary of changes made.

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
| FR-004 | Detect code blocks inside lists with incorrect indentation | P1 |
| FR-005 | Map validation errors to source markdown line numbers | P1 |
| FR-006 | Provide actionable fix suggestions for each error type | P1 |
| FR-007 | Auto-fix trailing whitespace (opt-in) | P2 |
| FR-008 | Auto-fix double spaces outside code blocks (opt-in) | P2 |
| FR-009 | Auto-fix duration format in sidecar.json (opt-in) | P2 |
| FR-010 | Categorize issues as BLOCKING or WARNING | P3 |
| FR-011 | Continue pipeline on warnings, fail on blockers | P3 |

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
1. Uncomment and enhance auto-fix code in `clean_markdown.py`
2. Add duration format auto-fix to `schema_validation.py`
3. Add `--fix` flag to validation scripts
4. Update CI to optionally apply fixes

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

## Out of Scope

- Modifying the XML converter itself
- Editorial/style validation (that's FR-2/FR-3)
- Changes to sidecar.json schema (owned by L&C UAT team)

## Open Questions

1. Should auto-fix be opt-in or opt-out?
2. Should we add a "preview XML" step that catches errors before full conversion?
3. How do we handle edge cases in nested lists that are valid but unusual?

## Related Features

- **FF-4 (GUID Cache Updates)**: Could be added to same CI enhancement effort
- **FR-2 (Editorial Style)**: Will build on this validation framework
