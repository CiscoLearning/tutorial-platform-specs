<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (MAJOR: initial constitution ratification)

Modified principles: N/A (initial creation)

Added sections:
- Core Principles (5 principles)
- Content Standards section
- Workflow Standards section
- Governance section

Removed sections: N/A

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ No changes needed (Constitution Check section is generic)
- .specify/templates/spec-template.md: ✅ No changes needed (requirements structure aligns)
- .specify/templates/tasks-template.md: ✅ No changes needed (task categorization aligns)

Follow-up TODOs: None
==================
-->

# Cisco U. Tutorial Content Constitution

This document defines the governing principles and development guidelines for the Cisco U. Tutorial Content ecosystem.

## Core Principles

### I. Tutorial Quality First

Tutorials MUST balance theory and hands-on practice to enable effective learning for network engineers.

- Duration: 15 minutes to 1 hour
- Target audience: Network engineers at Beginner, Intermediate, Advanced, or Expert skill levels
- Writing style: Conversational tone that references both author and learner
- All content MUST be technically accurate and validated by Technical Advocates before merge

**Rationale:** Network engineers learn best through practical application combined with conceptual understanding. Time-bounded tutorials ensure focused, achievable learning objectives.

### II. Structured Content Organization

Every tutorial MUST follow the standardized step-based structure to ensure consistency and platform compatibility.

- Step 1: Overview with "What you'll learn" and "What you'll need" sections
- Steps 2 through N-1: Content steps progressing through the tutorial material
- Final step: Congratulations with call-to-action and additional resources
- One tutorial per pull request; one author per tutorial
- Folder naming MUST match branch name (`tc-{tutorial-name}`)

**Rationale:** Consistent structure enables automated validation, platform compatibility, and a predictable learner experience across all tutorials.

### III. Validate Early, Fail Fast

All validation MUST occur at PR time, not after merge. Errors discovered post-merge increase cost and delay publication.

- Schema validation for `sidecar.json` (GUIDs, durations, required fields)
- Markdown structure validation (step naming, images folder, file references)
- Duration sum verification (step durations MUST equal top-level duration)
- XML conversion compatibility checks (whitespace, entity encoding)

**Rationale:** Shifting validation left reduces the feedback loop for authors and prevents invalid content from reaching the publishing pipeline.

### IV. Editorial Consistency Through Automation

Manual editorial review MUST be supplemented by automated style enforcement to maintain quality at scale.

- Heading style: Imperative mood, title case (e.g., "Access the Learn Tab" not "Accessing the Learn Tab")
- Acronyms: Expand on first use with abbreviation in parentheses
- Punctuation: Em dashes without spaces, serial comma, end punctuation on all sentences
- Technical terms: Proper hyphenation (e.g., GCMP-256), code formatting for commands/status codes
- Bold for UI elements and concepts; backticks for technical identifiers

**Rationale:** Consistent editorial style improves readability and reduces cognitive load for learners while decreasing the burden on part-time editorial reviewers.

### V. Transparent Pipeline Feedback

Authors MUST receive actionable, specific feedback that enables self-correction.

- PR comments MUST categorize issues as blocking vs. suggestions
- Validation errors MUST include specific line references and fix instructions
- AI-powered editorial feedback MUST cite relevant style guide rules
- XML conversion errors MUST explain the cause and remediation steps

**Rationale:** Empowering authors to fix their own issues reduces review cycles and accelerates time-to-publish.

## Content Standards

### sidecar.json Requirements

| Field | Format | Constraint |
|-------|--------|------------|
| `id` | lowercase alphanumeric + hyphens | MUST match folder name |
| `duration` | `XXmXXs` or `XhXXmXXs` | MUST equal sum of step durations |
| `date` | `YYYY-MM-DD` | Valid date |
| `files[].duration` | `MM:SS` | Valid time format |
| `ia-guid`, `lesson-guid`, `xy-guid` | UUID | MUST be unique (checked against `guid_cache.json`) |
| `authors` | Single object | Exactly one author allowed |
| `active` | Boolean | MUST be `true` |
| `skill-levels` | String | Beginner, Intermediate, Advanced, or Expert |
| `technologies` | Array | From allowed list: Application Performance, Cloud and Computing, Collaboration, Data Center, Mobility and Wireless, Networking, Other, Security, Software |

### Markdown to XML Compatibility

The following patterns cause XML conversion failures and MUST be avoided:

- Whitespace (newlines) immediately before or after `[link](url)` syntax
- Unescaped `&` characters (use `&amp;`)
- Complex nested formatting that produces malformed XML
- Incomplete or malformed markdown syntax

## Workflow Standards

### Contribution Workflow

1. Create branch: `tc-{tutorial-name}`
2. Create folder matching branch name with required structure
3. Open PR to trigger validation pipeline
4. Address all blocking validation errors
5. Editorial review by part-time editors (Jill, Matt)
6. Technical review and approval by Technical Advocates
7. Merge triggers auto-publish to staging
8. L&C UAT team approves staging content
9. Publishing team deploys to production

### Stakeholder Responsibilities

| Role | Responsibility |
|------|----------------|
| Technical Advocates | Primary authors, PR approval, technical accuracy |
| Learn with Cisco Instructors | Contributing authors |
| TMEs | Contributing authors |
| Part-time Editors | Editorial review (grammar, style, consistency) |
| L&C UAT Team | Staging approval before production |
| Publishing Team | Platform publication via REST API |

## Governance

This constitution supersedes all other practices for the Cisco U. tutorial content ecosystem. All changes MUST be documented and approved through the standard PR process.

### Amendment Process

1. Propose amendment via PR to this file
2. Document rationale for change
3. Obtain approval from at least one Technical Advocate
4. Update version number according to semantic versioning:
   - MAJOR: Backward-incompatible changes (principle removal/redefinition)
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording, non-semantic refinements
5. Update `LAST_AMENDED_DATE` to amendment date

### Compliance

- All PRs and reviews MUST verify compliance with these principles
- Complexity beyond these standards MUST be justified
- Validation tools MUST be updated to enforce new requirements

**Version**: 1.0.0 | **Ratified**: 2026-02-18 | **Last Amended**: 2026-02-18
