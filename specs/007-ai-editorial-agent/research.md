# Research: AI Editorial Agent

**Branch**: `007-ai-editorial-agent` | **Date**: 2026-02-20

## Architecture Pivot

### Original Approach (Rejected)
Follow `clean_markdown.py` pattern with regex-based rule engine + AI enhancement.

### Revised Approach (Adopted)
Use `anthropics/claude-code-action` with Claude Opus as an interactive editorial agent.

### Why We Pivoted

**Industry Research Findings:**

1. **Missing Context is #1 Problem** ([Qodo State of AI Code Quality 2025](https://www.qodo.ai/reports/state-of-ai-code-quality/))
   - 65% of developers cite missing context as top issue
   - 44% cite style mismatches with team standards
   - Solution: Give AI full access to style guides and historical decisions

2. **GitHub Agentic Workflows** ([The New Stack](https://thenewstack.io/github-agentic-workflows-overview/))
   - GitHub recommends agentic workflows for "tasks that benefit from flexibility"
   - CI/CD should be deterministic; editorial review benefits from judgment
   - Editorial review is explicitly listed as an agentic use case

3. **Editorial AI Best Practices** ([Acrolinx](https://www.acrolinx.com/blog/how-to-build-an-editorial-process-that-helps-you-work-smarter-not-harder/))
   - "Adopting content governance software eliminates majority of human editing"
   - Key: Feed AI your actual style guide and editor patterns as context

4. **claude-code-action Supports Opus** ([Anthropic](https://github.com/anthropics/claude-code-action))
   - Can configure `model: claude-opus-4-6` for premium reasoning
   - Built-in commit capability and PR comment integration
   - Responds to @claude mentions for interactive workflow

### Cost Justification

| Approach | Monthly Cost |
|----------|--------------|
| Part-time human editors | ~$2,000-3,000 |
| Claude Opus (5-10 PRs) | ~$50-100 |

Volume is low enough that Opus-level reasoning is affordable and appropriate.

---

## Research Questions Resolved

### RQ-1: Rule Engine Architecture

**Decision**: Follow `clean_markdown.py` dataclass pattern with YAML-defined rules

**Rationale**:
- Existing `clean_markdown.py` provides proven architecture with `ValidationRule`, `ValidationIssue`, and `ValidationResult` dataclasses
- YAML rule definitions enable non-developer updates to rules
- Pattern already integrated into CI pipeline successfully
- Allows mixing regex-based detection with stateful checks (e.g., acronym tracking)

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| JSON Schema validation | Not suited for prose/content validation, only structural |
| AST-based parsing | Overkill for markdown; regex patterns sufficient for editorial rules |
| External linting tool (vale, proselint) | Would require maintaining config files; harder to customize for Cisco-specific rules |

### RQ-2: Acronym State Tracking

**Decision**: Multi-pass scanning with state dictionary per tutorial

**Rationale**:
- Must track first-use of acronyms across all step files in a tutorial
- Step files are already sorted numerically by existing `ai_analysis.py` pattern
- State dictionary maps acronym → {first_seen_file, first_seen_line, expanded: bool}
- Two-pass approach: Pass 1 collects acronym locations, Pass 2 validates expansion rules

**Implementation Pattern**:
```python
@dataclass
class AcronymState:
    acronym: str
    first_file: str
    first_line: int
    expanded: bool = False

# Pass 1: Build state
acronym_state: Dict[str, AcronymState] = {}
for file in sorted_step_files:
    for match in ACRONYM_PATTERN.finditer(content):
        if match.group() not in acronym_state:
            acronym_state[match.group()] = AcronymState(...)

# Pass 2: Validate
for acronym, state in acronym_state.items():
    if not state.expanded and requires_expansion(acronym):
        report_issue(ACRONYM_001, ...)
```

### RQ-3: AI Enhancement Integration

**Decision**: Hybrid approach - deterministic rules first, then AI verification/enhancement

**Rationale**:
- Deterministic rules catch 70-80% of issues reliably with no API cost
- AI analysis verifies borderline cases and catches nuanced issues
- Fallback to deterministic-only mode if API unavailable (graceful degradation)
- AI prompt includes detected issues for context-aware verification

**Integration Flow**:
1. Run `editorial_validation.py` → produces `EditorialResult` JSON
2. Pass result + content to enhanced `ai_analysis.py editorial` mode
3. AI prompt includes:
   - Editorial rules from `editorial_rules.yaml`
   - Acronym database context
   - Pre-detected issues for verification
4. AI can: verify detections, flag false positives, find additional issues
5. Merge results into final PR comment

### RQ-4: PR Comment Format

**Decision**: Adopt Jill's Global → Queries → Step-by-Step format

**Rationale**:
- Matches editor workflow that authors are already familiar with
- Groups related issues for efficient review
- Separates auto-fixable from manual decisions
- Quality score provides at-a-glance assessment

**Comment Template**:
```markdown
## Editorial Review Summary

**Quality Score:** 8/10 | **Issues Found:** 5

---

### Global Edits (Applied/Suggested)

| Rule | Count | Examples |
|------|-------|----------|
| Em dash spacing | 3 | Line 12, 45, 78 |
| "click on" → "click" | 2 | Line 22, 56 |

### Queries for Author

- [ ] **ACRONYM-003** (step-1, line 8): Is "NAS" network access server or network-attached storage?
- [ ] **HEADING-001** (step-3): Should "Configuring" be "Configure"?

---

### Step-by-Step Review

**step-1.md** (2 issues)
| Line | Rule | Issue | Suggestion |
|------|------|-------|------------|
| 15 | BOLD-001 | Bold used for emphasis | Use *italics* instead |
| 23 | ACRONYM-001 | "VLAN" not expanded | "virtual LAN (VLAN)" |

**step-2.md** (1 issue)
...

---

*Automated editorial review by Cisco U. Tutorial Pipeline*
*Rules: [editor-comments-reference.md](link) | Feedback: [link]*
```

### RQ-5: Quality Score Calculation

**Decision**: Weighted deduction formula with severity tiers

**Rationale**:
- Provides quantitative measure for reviewer triage
- Weights match editor priorities (branding > style > formatting)
- Score of 10 = no issues; score < 5 = significant revision needed

**Formula**:
```
base_score = 10
deductions = (high_priority_count * 1.0) + (medium_priority_count * 0.5) + (low_priority_count * 0.1)
quality_score = max(1, base_score - deductions)
```

**Severity Mapping**:
| Priority | Deduction | Examples |
|----------|-----------|----------|
| High | 1.0 | Cisco possessive, deprecated acronym, missing product name |
| Medium | 0.5 | Em dash spacing, "click on", heading style |
| Low | 0.1 | Serial comma, minor formatting |

### RQ-6: Living Reference Document Updates

**Decision**: JSON + Markdown files in spec folder, copied to tools/ during CI

**Rationale**:
- Spec folder provides versioned, reviewable changes
- JSON format for `acronym-database.json` enables programmatic access
- Markdown for `cisco-product-naming-guide.md` enables human-readable notes
- CI workflow copies files to ensure consistency

**Update Process**:
1. Editor updates file in `specs/007-ai-editorial-agent/`
2. Opens PR for review
3. On merge, sync workflow copies to `tutorial-testing/tools/`
4. Next PR validation uses updated rules

## Technology Decisions

### Regex Pattern Library

| Pattern Category | Technology | Notes |
|------------------|------------|-------|
| Heading style (gerund) | Regex: `^##+ \w+ing\b` | Simple pattern match |
| Acronym detection | Regex: `\b[A-Z]{2,}(?:-[A-Z0-9]+)?\b` | Handles NX-OS, L3VPN |
| Em dash spacing | Regex: `\s+—\s+` or `—` | Detect with/without spaces |
| Bold for emphasis | Context + Regex | Requires sentence analysis |
| Cisco possessive | Regex: `Cisco\s+\w+'s` | Simple pattern |
| "Click on" | Regex: `\bclick\s+on\b` (case-insensitive) | Simple replacement |

### AI Prompt Engineering

**System Prompt Structure**:
```
You are an editorial assistant for Cisco U. tutorials, trained on feedback patterns from editors Jill and Matt.

ROLE: Verify detected issues and find additional editorial problems.
CONTEXT: You will receive:
1. Pre-detected issues from deterministic rules
2. Editorial rule definitions
3. Acronym database
4. Tutorial content

TASKS:
1. For each pre-detected issue: VERIFY (correct) or REJECT (false positive)
2. Find additional issues not caught by rules
3. Provide specific before/after corrections
4. Rate overall editorial quality

OUTPUT: JSON with structure:
{
  "verified_issues": [...],
  "rejected_issues": [...],
  "new_issues": [...],
  "quality_assessment": "..."
}
```

## Implementation Dependencies

| Dependency | Version | Purpose | Status |
|------------|---------|---------|--------|
| Python | 3.10 | Runtime | ✅ Existing |
| jsonschema | latest | JSON validation | ✅ Existing |
| pytest | latest | Testing | ✅ Existing |
| requests | latest | API calls | ✅ Existing |
| PyYAML | latest | Rule definitions | ⚠️ Add to requirements |
| Cisco Chat-AI | gpt-4o-mini | AI enhancement | ✅ Existing credentials |

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| API rate limiting | Run deterministic rules first; AI is enhancement only |
| API unavailable | Graceful fallback to deterministic-only mode |
| False positives | AI verification step; query flagging for borderline cases |
| Rule drift | Living documents + PR-based updates + version tracking |
| Performance | <3 min target; parallelize file processing if needed |
