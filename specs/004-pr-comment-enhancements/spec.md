# Feature Specification: PR Comment Enhancements

**Feature Branch**: `004-pr-comment-enhancements`
**Created**: 2026-02-19
**Status**: Draft
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
