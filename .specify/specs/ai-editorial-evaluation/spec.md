# Feature: AI-Powered Editorial Evaluation

## Overview

Enhance the CI pipeline to provide automated editorial feedback that catches style guide violations, suggests corrections, and reduces the need for manual editorial review. The goal is to reduce manual editorial corrections by 50% while maintaining quality standards.

## User Stories

### US-1: Author Receives Style Feedback on PR
**As a** tutorial author
**I want** automated feedback on style guide violations in my PR
**So that** I can fix issues before editorial review

#### Acceptance Criteria
- [ ] PR comment includes categorized style issues (blocking, warning, suggestion)
- [ ] Each issue includes specific line reference and file
- [ ] Each issue includes the violated rule from the style guide
- [ ] Suggested correction is provided where applicable
- [ ] Feedback appears within 5 minutes of PR creation

### US-2: Editor Sees Pre-Screened PRs
**As an** editor (Jill/Matt)
**I want** PRs to be pre-screened for common style issues
**So that** I can focus on higher-level editorial concerns

#### Acceptance Criteria
- [ ] Common issues from editorial-style-guide.md are caught automatically
- [ ] False positive rate is below 10%
- [ ] AI suggestions align with historical editorial patterns
- [ ] PR shows quality score indicating editorial readiness

### US-3: Author Gets Acronym Expansion Reminders
**As a** tutorial author
**I want** to be reminded when I use an acronym without first expanding it
**So that** my content is accessible to all readers

#### Acceptance Criteria
- [ ] System tracks first use of each acronym in the tutorial
- [ ] Flags acronyms used without expansion on first occurrence
- [ ] Provides suggested expansion for common networking/Cisco acronyms
- [ ] Ignores acronyms that are well-known (e.g., API, URL, HTTP)

### US-4: Author Fixes Heading Style
**As a** tutorial author
**I want** to be notified when my headings use gerund form instead of imperative
**So that** my headings match the style guide

#### Acceptance Criteria
- [ ] Detects headings starting with -ing verbs
- [ ] Suggests imperative form alternative
- [ ] Handles compound headings (e.g., "Creating and Deploying")
- [ ] Provides before/after example in feedback

## Functional Requirements

### FR-1: Style Rule Engine
Implement a configurable rule engine that can evaluate markdown content against style rules.

**Inputs:**
- Markdown file content (step-*.md)
- Style rules configuration (derived from editorial-style-guide.md)
- Tutorial metadata (sidecar.json for skill level context)

**Outputs:**
- List of violations with severity (blocking, warning, suggestion)
- Line number and character position for each violation
- Suggested fix where deterministic
- Rule ID and description

**Rules to Implement (Phase 1):**

| Rule ID | Description | Severity |
|---------|-------------|----------|
| HEADING-001 | Heading uses gerund instead of imperative | warning |
| HEADING-002 | Heading not in title case | warning |
| ACRONYM-001 | Acronym used without expansion on first use | blocking |
| ACRONYM-002 | Redundant acronym expansion after first use | suggestion |
| PUNCT-001 | Em dash with surrounding spaces | warning |
| PUNCT-002 | Missing serial comma | suggestion |
| PUNCT-003 | Missing end punctuation | warning |
| TECH-001 | Technical term missing hyphen | warning |
| TECH-002 | Missing space before unit | suggestion |

### FR-2: AI-Enhanced Analysis
Extend existing `ai_analysis.py` to incorporate style guide rules in the LLM prompt.

**Current Flow:**
1. Read step-*.md files
2. Send to Cisco Chat-AI with "advice" prompt
3. Return general editorial feedback

**Enhanced Flow:**
1. Read step-*.md files
2. Run deterministic style rule engine (FR-1)
3. Send to Cisco Chat-AI with enhanced prompt including:
   - Style guide rules as system context
   - Detected violations for confirmation/expansion
   - Request for additional stylistic improvements
4. Merge deterministic and AI-generated feedback
5. Deduplicate and rank by severity

**Prompt Engineering:**
```
You are an editorial assistant for Cisco U. technical tutorials targeting network engineers.

Style Guide Rules:
{rules from editorial-style-guide.md}

Tutorial Content:
{step-*.md content}

Detected Issues (verify and expand):
{output from FR-1}

Tasks:
1. Verify each detected issue is a true violation
2. Identify additional style guide violations not caught by rules
3. Suggest specific corrections with before/after examples
4. Rate overall editorial quality (1-10)
5. Highlight top 3 most important fixes

Output as structured JSON.
```

### FR-3: PR Comment Formatting
Generate well-formatted PR comments with actionable feedback.

**Comment Structure:**
```markdown
## Editorial Review Summary

**Quality Score:** 7/10 | **Issues Found:** 12 (3 blocking, 5 warnings, 4 suggestions)

### Blocking Issues (must fix)
| File | Line | Issue | Suggested Fix |
|------|------|-------|---------------|
| step-2.md | 15 | ACRONYM-001: "VLAN" used without expansion | "virtual LAN (VLAN)" |

### Warnings (should fix)
...

### Suggestions (consider)
...

### AI Recommendations
> {Free-form AI suggestions for overall improvement}

---
*Automated editorial review by Cisco U. Tutorial Pipeline*
```

### FR-4: Quality Score Calculation
Calculate a composite quality score based on violation counts and severity.

**Scoring Formula:**
```
base_score = 10
deductions:
  - blocking: -1.0 per issue
  - warning: -0.3 per issue
  - suggestion: -0.1 per issue

quality_score = max(0, base_score - deductions)
```

**Thresholds:**
- 8-10: Ready for editorial review
- 5-7: Needs author attention
- 0-4: Significant issues, author must address before review

### FR-5: Acronym Database
Maintain a database of known acronyms with expansions for suggestion generation.

**Data Structure:**
```json
{
  "VLAN": {
    "expansion": "virtual LAN",
    "domain": "networking",
    "well_known": false
  },
  "API": {
    "expansion": "Application Programming Interface",
    "domain": "general",
    "well_known": true
  }
}
```

**Well-known acronyms** (skip expansion suggestions): API, URL, HTTP, HTTPS, HTML, CSS, JSON, XML, SQL, CLI, GUI, OS

## Non-Functional Requirements

### NFR-1: Performance
- Deterministic rule engine: <10 seconds for full tutorial
- AI analysis: <2 minutes (existing constraint from Cisco Chat-AI)
- Total pipeline addition: <3 minutes

### NFR-2: Accuracy
- False positive rate: <10% for blocking issues
- False positive rate: <20% for warnings
- AI suggestion relevance: >80% actionable

### NFR-3: Maintainability
- Style rules defined in configuration file (YAML/JSON)
- New rules addable without code changes
- Acronym database extensible

## Dependencies

- Existing `ai_analysis.py` tool
- Cisco Chat-AI API (GPT-4o-mini)
- GitHub Actions workflow (`tutorial-linting.yml`)
- `editorial-style-guide.md` as source of truth

## Open Questions

- [ ] Should blocking issues prevent merge, or just flag for attention?
- [ ] How do we handle skill-level-specific style (e.g., more acronym expansion for Beginner tutorials)?
- [ ] Should we provide a local validation command for authors before pushing?
- [ ] How do we track false positive feedback to improve rules over time?

## Implementation Phases

### Phase 1: Deterministic Rules
- Implement core style rule engine
- Add 5-10 highest-value rules
- Integrate into CI pipeline
- Generate basic PR comments

### Phase 2: AI Enhancement
- Enhance LLM prompt with style guide context
- Merge deterministic and AI feedback
- Add quality scoring
- Improve comment formatting

### Phase 3: Feedback Loop
- Track false positives from author feedback
- Tune rule severity based on editorial override patterns
- Expand acronym database
- Add skill-level-aware rules

## References

- [Editorial Style Guide](./editorial-style-guide.md)
- [Requirements Document](./requirements.md)
- [Architecture Overview](./architecture.md)
- Existing tool: `tutorial-testing/tools/ai_analysis.py`
