# Feature Specification: PR Comment Enhancements

**Feature Branch**: `004-pr-comment-enhancements`
**Created**: 2026-02-19
**Completed**: 2026-02-20
**Status**: Complete
**PR**: [ciscou-tutorial-content#343](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/343)
**Input**: User description: "FR-5: PR Comment Enhancements - Improve automated PR comments to surface specific errors directly instead of requiring authors to navigate GitHub Actions logs. Based on pain points discovered during Hugo migration where broken URLs, missing images, and XML errors were hidden in logs."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Broken Link Errors Directly in PR (Priority: P1)

A tutorial author submits a PR and the CI detects broken URLs or missing images. Instead of seeing "Pytest check failed. Please click the below GitHub action for more information", the author sees a formatted comment listing exactly which files have broken links, the specific URLs that are broken, and actionable instructions to fix them.

**Why this priority**: This is the most common error type (13+ PRs during Hugo migration) and currently provides the worst user experience - authors must navigate through 3-4 clicks and scroll through logs to find the actual error.

**Independent Test**: Can be fully tested by creating a PR with a broken URL and verifying the comment displays the broken URL details directly without requiring log navigation.

**Acceptance Scenarios**:

1. **Given** a PR contains a markdown file with a broken URL, **When** CI completes, **Then** the PR comment shows the file name, line number, and specific broken URL in a formatted table
2. **Given** a PR contains a markdown file with a missing image reference, **When** CI completes, **Then** the PR comment shows the file name and missing image path
3. **Given** a PR has multiple broken links across multiple files, **When** CI completes, **Then** all broken links are grouped by file in the comment

---

### User Story 2 - View XML Conversion Errors with Fix Guidance (Priority: P2)

A tutorial author submits a PR with markdown that causes Solomon XML conversion to fail. Instead of seeing raw XML parser errors, the author sees a comment explaining the issue in plain language with a before/after example showing how to fix it.

**Why this priority**: XML errors are blocking and confusing for non-technical authors. Plain language explanations reduce back-and-forth with reviewers.

**Independent Test**: Can be fully tested by creating a PR with a known XML-breaking pattern (e.g., code block in list) and verifying the comment explains the fix in plain language.

**Acceptance Scenarios**:

1. **Given** a PR has markdown that causes XML parser errors, **When** CI completes, **Then** the PR comment explains the issue type (e.g., "Code block inside list item") and shows how to restructure
2. **Given** an XML error occurs, **When** the comment is displayed, **Then** the raw error is collapsed in a details section while the plain explanation is visible

---

### User Story 3 - View Duration Mismatch Warnings with Auto-Fix Option (Priority: P3)

A tutorial author submits a PR where the total duration in sidecar.json doesn't match the sum of step durations. The author sees a warning comment showing the mismatch and a command they can run to auto-fix it.

**Why this priority**: Duration mismatches are common but easily auto-fixable. Showing the fix command reduces manual work.

**Independent Test**: Can be fully tested by creating a PR with a duration mismatch and verifying the comment shows the expected vs actual values and the auto-fix command.

**Acceptance Scenarios**:

1. **Given** a PR has a duration mismatch in sidecar.json, **When** CI completes, **Then** the comment shows expected and actual duration values
2. **Given** a duration mismatch warning is shown, **When** author views the comment, **Then** they see the command to run the auto-fix tool

---

### User Story 4 - Fallback for Unspecified Error Types (Priority: P4)

A tutorial author submits a PR and the CI fails with an error type that doesn't have custom formatting (e.g., GUID uniqueness, extra markdown files, Solomon lint warnings). Instead of seeing only "click for more info", the author sees the raw output from that validation step captured directly in the PR comment.

**Why this priority**: Future-proofs the system. As new validation checks are added, they automatically get surfaced even before custom formatting is implemented.

**Independent Test**: Can be tested by intentionally triggering an error type without custom formatting and verifying the raw output appears in the comment.

**Acceptance Scenarios**:

1. **Given** a PR fails a validation step without custom error formatting, **When** CI completes, **Then** the PR comment includes the raw output from that step in a collapsible section
2. **Given** a new validation check is added to CI, **When** it produces errors, **Then** those errors are surfaced in PR comments without requiring code changes to the comment formatter
3. **Given** multiple unformatted error types occur, **When** CI completes, **Then** each is displayed in its own labeled section

---

### Edge Cases

- What happens when a PR has multiple error types (broken URLs AND XML errors)?
  - Each error type should be displayed in its own section with clear headers
- What happens when there are more than 10 broken URLs?
  - Show first 10 with a count of remaining, collapse full list in details section
- How does the system handle URLs that timeout vs return 404?
  - Both should be reported as "Broken URL" with the HTTP status or timeout indicated
- What happens when an error type has no custom formatter?
  - Fall back to displaying raw output in a collapsible section with the step name as header
- What happens when raw output is extremely large (>10KB)?
  - Truncate with "... output truncated, see Actions log for full details"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display broken URLs directly in PR comments without requiring log navigation
- **FR-002**: System MUST display missing image paths directly in PR comments
- **FR-003**: System MUST group errors by file when displaying in comments
- **FR-004**: System MUST provide plain-language explanations for XML conversion errors
- **FR-005**: System MUST show before/after examples for common XML-breaking patterns
- **FR-006**: System MUST display duration mismatch warnings with expected vs actual values
- **FR-007**: System MUST provide auto-fix commands where applicable (duration mismatch)
- **FR-008**: System MUST collapse verbose output (raw logs, full error traces) in expandable sections
- **FR-009**: System MUST use visual indicators (icons/emoji) to distinguish error severity (blocking vs warning)
- **FR-010**: System MUST continue showing schema validation errors in current format (already working well)
- **FR-011**: System MUST capture raw output from any failing validation step that lacks custom formatting
- **FR-012**: System MUST display unformatted errors in labeled collapsible sections using step name as header
- **FR-013**: System MUST truncate raw output exceeding 10KB with link to full Actions log
- **FR-014**: System MUST surface errors from all validation steps (pytest, solomon transform, solomon lint, folder checks) rather than generic "click for more info"

### Key Entities

- **ValidationError**: Represents a single error found during validation
  - Type (broken_url, missing_image, xml_error, duration_mismatch, guid_uniqueness, extra_files, skill_level, solomon_lint, folder_structure, other)
  - Source step (pytest, schema, markdown, solomon_transform, solomon_lint, folder_check)
  - File path and line number (if available)
  - Specific error value (URL, image path, etc.)
  - Severity (blocking, warning)
  - Fix suggestion (if available)
  - Raw output (for fallback display when no custom formatter exists)

- **PRComment**: The formatted markdown comment posted to the PR
  - Error sections grouped by type
  - Collapsible raw output
  - Action items for author

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Authors can understand the specific error within 30 seconds of viewing the PR comment (vs 2-5 minutes navigating logs)
- **SC-002**: 90% of broken URL errors are understood without clicking into GitHub Actions logs
- **SC-003**: Authors fix issues on first attempt 85% of the time (vs ~60% currently)
- **SC-004**: Support questions about "why did CI fail?" decrease by 75%
- **SC-005**: Each error type (broken URL, XML error, duration mismatch) has a dedicated comment format

## Assumptions

- The existing pytest_validation.py already captures all the error information needed; it just needs to be surfaced differently
- Authors have basic markdown reading skills to understand formatted tables
- GitHub PR comment markdown rendering supports tables, collapsible sections, and emoji
- The CI workflow has permissions to post comments (already established)

## Out of Scope

- Auto-fixing broken URLs (would require finding replacement URLs)
- Preventing errors before commit (covered by FR-4: Pre-commit Validation)
- Changing the underlying validation logic
- Modifying the PR review/approval workflow

---

## Implementation Details

### Code Files (ciscou-tutorial-content repo)

| File | Purpose | Key Functions |
|------|---------|---------------|
| `tools/conftest.py` | Pytest plugin for JSON output | `JSONResultCollector`, `_parse_broken_urls()`, `_parse_missing_images()`, `_parse_duration_mismatch()` |
| `tools/format_pr_comment.py` | PR comment markdown generator | `format_broken_url_errors()`, `format_missing_image_errors()`, `format_duration_mismatch()`, `format_xml_errors()` |
| `tools/pytest_validation.py` | Validation tests with line tracking | `extract_links_with_lines()`, `check_file()`, `test_broken_links()` |
| `.github/workflows/tutorial-linting.yml` | CI workflow integration | Added `--json-output` flag and formatter step |

### Architecture

```
pytest_validation.py                    conftest.py                     format_pr_comment.py
┌─────────────────────┐                ┌─────────────────────┐         ┌─────────────────────┐
│ test_broken_links() │ ──failures──▶ │ JSONResultCollector │ ──JSON─▶│ generate_comment()  │
│ test_duration()     │                │ _parse_broken_urls()│         │ format_*_errors()   │
│ etc.                │                │ _parse_images()     │         │ collapsible_section │
└─────────────────────┘                └─────────────────────┘         └─────────────────────┘
        │                                       │                              │
        │ Outputs:                              │ Outputs:                     │ Outputs:
        │ "Broken URL (line 15): url"           │ pytest_results.json          │ pytest_comment.md
        │ "Broken Image (line 20): path"        │ {errors: [...]}              │ (markdown tables)
```

### Key Design Decisions

1. **Pytest plugin via conftest.py**: Pytest automatically loads `conftest.py`, making plugin registration seamless
2. **Regex-based error parsing**: Parse structured error messages from pytest output rather than modifying pytest internals
3. **Line number tracking**: Modified `extract_links_with_lines()` to return `(value, line_num)` tuples throughout the chain
4. **Severity levels**: Blocking (broken URLs, missing images) vs Warning (duration mismatch) for visual distinction

---

## Development Notes & Lessons Learned

### Iteration 1: Initial Implementation (tutorial-testing repo)
- Created `conftest.py` with JSON output plugin
- Created `format_pr_comment.py` with table formatters
- Updated workflow to use `--json-output`

### Iteration 2: YAML Syntax Error
**Problem**: Workflow failed to parse - `**Status:**` at the start of a line inside a multiline string was interpreted as a YAML alias (`*Status`).

**Fix**: Added indentation before the `**` to prevent YAML from treating it as an alias marker.

```yaml
# Before (broken)
gh pr comment "$PR_NUMBER" --body "## Report
**Status:** passed"   # YAML sees *Status as alias

# After (fixed)
gh pr comment "$PR_NUMBER" --body "## Report
          **Status:** passed"   # Indented, not at line start
```

### Iteration 3: Pytest Plugin Not Loading
**Problem**: `--json-output` flag was "unrecognized" because the plugin code was in `pytest_validation.py` but pytest wasn't loading it.

**Fix**: Moved plugin registration to `tools/conftest.py`. Pytest automatically discovers and loads `conftest.py` files.

### Iteration 4: URL Parsing Artifacts
**Problem**: URLs showing trailing characters like `https://example.com/page')])]`

**Root cause**: Regex `https?://[^\s]+` was too greedy, capturing brackets and quotes from surrounding markdown/code.

**Fix**: Improved regex to stop at common delimiters:
```python
# Before
url_pattern = re.compile(r"(https?://[^\s]+)")

# After
url_pattern = re.compile(r"(https?://[^\s\n\]\)\"']+)")
# Also added post-processing:
clean_url = re.sub(r"[\]\)\'\"\,\.]+$", "", url)
```

### Iteration 5: Line Numbers Missing
**Problem**: PR comment showed `| unknown | - |` for file and line columns.

**Root cause**: `pytest_validation.py` was outputting `"Broken URL: {url}"` without line numbers, so `conftest.py` couldn't parse them.

**Fix**:
1. Added `extract_links_with_lines()` function to track line numbers during link extraction
2. Modified `check_file()` to return `(url, line_num)` tuples
3. Updated error output format to `"Broken URL (line {n}): {url}"`

```python
def extract_links_with_lines(md_content):
    """Extract links with line numbers."""
    url_links = []
    for line_num, line in enumerate(md_content.split('\n'), start=1):
        urls = re.findall(MARKDOWN_URL_REGEX, line)
        for url in urls:
            url_links.append((url, line_num))
    return url_links, image_links
```

### Iteration 6: Duration Table Placeholders
**Problem**: Duration mismatch table showed `(from step sum)` and `(in sidecar)` instead of actual values like `35m00s` and `25m00s`.

**Root cause**: `format_pr_comment.py` wasn't parsing the expected/actual values from the error message.

**Fix**: Added regex to extract values from message:
```python
# Parse "Duration mismatch: expected 35m00s, got 25m00s"
duration_pattern = re.compile(r"expected\s+(\d+[hm]?\d*[ms]?\d*s?),?\s+got\s+(\d+[hm]?\d*[ms]?\d*s?)")
match = duration_pattern.search(error.message)
if match:
    expected_val = match.group(1)  # "35m00s"
    actual_val = match.group(2)    # "25m00s"
```

### Iteration 7: CI Not Triggering (tutorial-testing)
**Problem**: After fixing YAML, GitHub Actions workflows weren't triggering on new commits/PRs.

**Investigation**: Workflow only had `on: pull_request:` trigger. When the workflow file itself had a syntax error, GitHub cached the invalid state.

**Workaround**: Tested on production repo (ciscou-tutorial-content) instead, which had working CI. The fixes were validated there.

### Iteration 8: Test Tutorial vs Production Code
**Problem**: Initial test PR included both the test fixture (`tc-fr5-validation-test/`) and the actual code changes.

**Fix**: Created clean branch from main, cherry-picked only the code files:
```bash
git checkout main
git checkout -b feat/fr5-pr-comment-enhancements
git checkout test/fr5-validation -- tools/conftest.py tools/format_pr_comment.py \
    tools/pytest_validation.py .github/workflows/tutorial-linting.yml
```

### Key Takeaways

1. **Test on prod when CI is broken on test**: When tutorial-testing CI had issues, validating on ciscou-tutorial-content provided faster feedback
2. **YAML multiline strings are tricky**: Special characters at line starts can be misinterpreted as YAML syntax
3. **Pytest plugin discovery**: Use `conftest.py` for automatic plugin loading
4. **Parse structured output**: Design error messages to be both human-readable AND machine-parseable
5. **Separate test fixtures from production code**: Keep dummy test data out of production branches
