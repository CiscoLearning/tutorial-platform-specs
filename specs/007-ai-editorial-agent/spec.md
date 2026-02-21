# Feature Specification: AI Editorial Agent

**Feature Branch**: `007-ai-editorial-agent`
**Created**: 2026-02-20
**Updated**: 2026-02-21
**Status**: In Progress (~75% rule coverage achieved)

## Current State

### Completed

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Official Style Rules | `tutorial-testing/tools/cisco-style-rules.json` | 75+ term substitutions from Cisco Technical Content Style Guide |
| Acronym Database | `tutorial-testing/.claude/references/acronym-database.json` | 100+ entries with Cisco products, networking, security terms |
| Editorial Agent Instructions | `tutorial-testing/.claude/agents/editorial-reviewer.md` | Agent instructions with official Cisco rules |
| Heading Conversion | `tutorial-testing/tools/clean_markdown.py` | `fix_headings_for_xml()` for Solomon XML compatibility |
| PR Analysis (24 PRs) | `tutorial-testing/analysis/v2-official-rules/` | Comparison of human editor changes vs agent detection |

### Key Metrics

| Metric | Value |
|--------|-------|
| PRs Analyzed | 24 |
| Total Editor Changes | 1,689 |
| Estimated Agent Coverage | ~75% |
| Official Rules Extracted | 75+ terms |
| Acronyms Documented | 100+ entries |

### Remaining Work

1. Implement deterministic rules engine (`editorial_validation.py`)
2. Integrate with CI pipeline
3. Generate PR comments in Jill's step-by-step format
4. Measure actual coverage on live PRs

---

## Overview

The AI Editorial Agent automates the non-technical editorial review process for Cisco U. tutorial PRs. Currently, two part-time human editors (Matt Sperling and Jill Lauterbach) manually review every PR for style guide compliance, grammar, acronym usage, and Cisco branding standards. This agent will replicate their editorial patterns to provide immediate, consistent feedback on PRs while reducing the editorial bottleneck.

**Key Constraints:**
- Advisory only - provides feedback via PR comments but does not block merge
- Must follow patterns documented in `editor-comments-reference.md` (extracted from actual editor comments)
- Uses `acronym-database.json` and `cisco-product-naming-guide.md` as living reference documents
- Generates PR comments in Jill's step-by-step format
- Includes quality score to help authors and reviewers prioritize fixes

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Author Receives Immediate Editorial Feedback (Priority: P1)

A tutorial author submits a PR with their content. Within 5 minutes, they receive an automated PR comment with categorized editorial feedback, allowing them to fix issues before human review.

**Why this priority**: This is the core value proposition - reducing the feedback loop from days (waiting for editor availability) to minutes. Authors can iterate faster and learn style expectations.

**Independent Test**: Can be fully tested by submitting a test PR with known editorial issues and verifying the comment appears with correct categorization and suggestions.

**Acceptance Scenarios**:

1. **Given** a PR with acronym "VLAN" not expanded on first use, **When** the CI pipeline runs, **Then** a PR comment is posted identifying the acronym issue with suggested expansion "virtual LAN (VLAN)"
2. **Given** a PR with heading "Configuring the Network" (gerund form), **When** the CI pipeline runs, **Then** a PR comment is posted suggesting imperative form "Configure the Network"
3. **Given** a PR with "Cisco ISE box" terminology, **When** the CI pipeline runs, **Then** a PR comment is posted suggesting "Cisco ISE server"
4. **Given** a PR with no editorial issues, **When** the CI pipeline runs, **Then** a PR comment is posted with quality score 10/10 and congratulatory message

---

### User Story 2 - Reviewer Sees Quality Score Before Approval (Priority: P2)

A technical advocate reviewing a PR can quickly see the editorial quality score and categorized issues to understand if the content is ready for merge or needs author attention.

**Why this priority**: Reviewers currently must read through content to assess editorial quality. A score provides at-a-glance readiness assessment.

**Independent Test**: Can be tested by reviewing the PR comment format and verifying the quality score accurately reflects issue severity and count.

**Acceptance Scenarios**:

1. **Given** a PR with 3 high-priority issues, **When** the editorial agent runs, **Then** the quality score reflects the deduction (approximately 7/10)
2. **Given** a PR with only minor suggestions, **When** the editorial agent runs, **Then** the quality score remains high (9-10/10)
3. **Given** a PR with issues, **When** reviewer views the comment, **Then** issues are categorized as "Global Edits", "Queries for Author", and "Step-by-Step Review"

---

### User Story 3 - Editorial Team Focuses on Complex Issues (Priority: P2)

Human editors can focus their limited time on complex editorial decisions (tone, clarity, technical accuracy) rather than routine style checks that the agent handles.

**Why this priority**: Maximizes the value of editor time by automating detectable patterns, leaving nuanced decisions to humans.

**Independent Test**: Can be tested by comparing agent-flagged issues against historical editor comments and measuring coverage percentage.

**Acceptance Scenarios**:

1. **Given** the agent runs on a tutorial, **When** compared to historical editor feedback on similar content, **Then** at least 70% of style-related issues are detected
2. **Given** a query the agent cannot resolve (e.g., "Is this acronym expansion correct in this context?"), **When** the agent runs, **Then** the query is flagged for human review under "Queries for Author"

---

### User Story 4 - Living Reference Documents Stay Current (Priority: P3)

Editorial team members can update the product naming guide and acronym database as Cisco products evolve, and the agent automatically uses the updated rules.

**Why this priority**: Ensures the agent remains accurate as products are renamed, deprecated, or introduced.

**Independent Test**: Can be tested by updating a product name in the guide, then verifying the agent uses the new name in subsequent runs.

**Acceptance Scenarios**:

1. **Given** a new product "Cisco XYZ" is added to `cisco-product-naming-guide.md`, **When** a PR uses "XYZ" without "Cisco", **Then** the agent suggests adding "Cisco" prefix
2. **Given** an acronym is marked deprecated in `acronym-database.json`, **When** a PR uses that acronym, **Then** the agent suggests the replacement term

---

### Edge Cases

- What happens when the acronym database contains conflicting expansions (e.g., NAS = "network-attached storage" vs "Network Access Server")? → Agent flags as "Context-dependent - verify correct expansion" with both options
- How does the system handle non-English content or code blocks? → Code blocks are skipped; non-English flagged for human review
- What happens when a PR modifies multiple tutorials? → Agent runs on each modified tutorial folder independently
- How does the system handle markdown formatting edge cases? → Defers to existing `clean_markdown.py` for structural issues; editorial agent focuses on content
- What happens when Anthropic API is unavailable? → Editorial review is skipped; pipeline continues without blocking (deterministic fallback is a backlog item)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST post a PR comment within 5 minutes of pipeline trigger containing categorized editorial feedback
- **FR-002**: System MUST calculate and display a quality score (1-10) based on issue severity and count
- **FR-003**: System MUST categorize issues by severity: High Priority (must fix), Medium Priority (should fix), Low Priority (suggestions)
- **FR-004**: System MUST identify acronyms used without first-use expansion by tracking acronym state across all step files
- **FR-005**: System MUST detect heading style violations (gerund vs imperative mood)
- **FR-006**: System MUST flag Cisco product naming violations using the living reference document
- **FR-007**: System MUST flag deprecated acronyms and suggest replacements per the acronym database
- **FR-008**: System MUST detect punctuation issues (em dash spacing, excessive exclamation marks)
- **FR-009**: System MUST flag missing procedural introduction lines before numbered steps
- **FR-010**: System MUST detect "click on" vs "click" usage and bold/italic misuse
- **FR-011**: System MUST format PR comments in step-by-step format matching Jill's style (Global Edits → Queries → Step-by-Step Review)
- **FR-012**: System MUST load rules from `acronym-database.json` and `cisco-product-naming-guide.md` at runtime
- **FR-013**: System MUST NOT block PR merge - advisory feedback only
- **FR-014**: System MUST provide before/after examples for suggested corrections
- **FR-015**: System MUST verify duration sums in sidecar.json match step durations

### Key Entities

- **Editorial Rule**: Represents a single validation rule with ID, pattern/detection logic, severity level, message template, and suggested fix
- **Editorial Issue**: An instance of a rule violation with file path, line number, original text, suggested correction, and severity
- **Quality Score**: Calculated metric (1-10) based on weighted issue counts that indicates editorial readiness
- **Acronym State**: Tracks first-use of acronyms across tutorial steps to detect expansion requirements
- **Product Reference**: Entry in the living product guide with official name, abbreviations, and usage rules

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Authors receive editorial feedback within 5 minutes of PR creation (measured by timestamp between PR open and comment post)
- **SC-002**: Agent detects at least 70% of issues that human editors would flag on the same content (measured by comparison study on 10 historical PRs)
- **SC-003**: False positive rate is below 15% for high-priority issues (measured by author/editor override rate)
- **SC-004**: Editorial team time spent on routine style corrections is reduced by 50% (measured by editor time tracking before/after deployment)
- **SC-005**: 80% of authors report the feedback is actionable and clear (measured by optional feedback survey in PR comment)
- **SC-006**: Agent successfully processes 100% of PRs without pipeline failures (measured by CI logs over 30-day period)

## Dependencies

- Anthropic API for Claude Opus via `claude-code-action` GitHub Action
- GitHub Actions workflow integration (`tutorial-linting.yml`)
- Living reference documents maintained by editorial team

## Assumptions

- Editors will maintain `cisco-product-naming-guide.md` and `acronym-database.json` as products evolve
- Anthropic API rate limits are sufficient for PR volume (5-10 PRs per month typical)
- Authors have GitHub notification preferences set to receive PR comments
- Editorial patterns documented in `editor-comments-reference.md` represent the desired style standards
- The existing CI pipeline has capacity for additional processing time (estimated 2-3 minutes per tutorial)
- Testing will use `workflow_dispatch` triggers on branches to avoid creating PRs visible to current editors

## Related Documents

### In This Directory

- [Editor Comments Reference](./editor-comments-reference.md) - Rules extracted from 24 PRs of editor feedback
- [Cisco Product Naming Guide](./cisco-product-naming-guide.md) - Product names and trademarks
- [Acronym Database](./acronym-database.json) - Initial acronym reference (superseded by live version)
- [Plan](./plan.md) - Implementation plan
- [Tasks](./tasks.md) - Task breakdown
- [Research](./research.md) - Research findings

### In tutorial-testing/

- `tools/cisco-style-rules.json` - Official Cisco Style Guide rules (75+ terms)
- `.claude/references/acronym-database.json` - Live acronym database (100+ entries)
- `.claude/agents/editorial-reviewer.md` - Agent instructions
- `analysis/v2-official-rules/COMPARISON-REPORT.md` - Full v2 analysis report

### Source Documents

- `stylegd.pdf` - Cisco Technical Content Style Guide (August 2022, 182 pages)
- `Tutorials Guidelines.pdf` - Cisco U. Tutorial Guidelines

### Archived

See `archive/` for intermediate work products:
- `pr-comparisons/` - Individual PR analyses (v1)
- `reference-data/` - Raw editor comments
- `test-tutorial/` - Test fixtures
