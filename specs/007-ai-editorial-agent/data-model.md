# Data Model: AI Editorial Agent

**Branch**: `007-ai-editorial-agent` | **Date**: 2026-02-20

## Core Entities

### EditorialRule

Defines a single validation rule from the editorial style guide.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `id` | string | Unique rule identifier (e.g., "ACRONYM-001") | Yes |
| `category` | enum | Rule category (see Categories below) | Yes |
| `severity` | enum | HIGH, MEDIUM, LOW | Yes |
| `pattern` | string | Regex pattern for detection (null for stateful rules) | No |
| `message_template` | string | Human-readable issue description with placeholders | Yes |
| `fix_suggestion` | string | Suggested correction with placeholders | Yes |
| `fix_type` | enum | AUTO (regex replace), AI (needs context), MANUAL (human) | Yes |
| `examples` | array | Before/after examples for documentation | No |
| `source` | string | Editor who established rule (Matt, Jill, or both) | No |

**Categories**:
- `ACRONYM` - Acronym expansion and usage
- `PRODUCT` - Cisco product naming and branding
- `HEADING` - Heading style and formatting
- `BOLD` - Bold/italic usage for GUI elements
- `PUNCT` - Punctuation rules
- `PROC` - Procedural structure (intros, lists)
- `TERM` - Terminology and word choice
- `XREF` - Cross-references and links

### EditorialIssue

Represents a detected rule violation.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `rule_id` | string | Reference to EditorialRule.id | Yes |
| `file_path` | string | Path to file containing issue | Yes |
| `line_number` | int | Line number (1-indexed) | Yes |
| `column` | int | Column position (0-indexed) | No |
| `original_text` | string | The problematic text | Yes |
| `suggested_text` | string | Corrected text | No |
| `message` | string | Rendered message from template | Yes |
| `severity` | enum | Inherited from rule | Yes |
| `fix_type` | enum | Inherited from rule | Yes |
| `ai_verified` | boolean | Whether AI confirmed this issue | No |
| `is_query` | boolean | Whether this needs author decision | No |

### EditorialResult

Aggregated validation result for a tutorial.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `tutorial_folder` | string | Path to tutorial (e.g., "tc-example") | Yes |
| `timestamp` | string | ISO 8601 validation timestamp | Yes |
| `files_scanned` | array[string] | List of step files processed | Yes |
| `issues` | array[EditorialIssue] | All detected issues | Yes |
| `quality_score` | float | Calculated score (1.0-10.0) | Yes |
| `high_priority_count` | int | Count of HIGH severity issues | Yes |
| `medium_priority_count` | int | Count of MEDIUM severity issues | Yes |
| `low_priority_count` | int | Count of LOW severity issues | Yes |
| `ai_enhanced` | boolean | Whether AI analysis was applied | Yes |
| `ai_unavailable_reason` | string | Reason if AI not used (optional) | No |

### AcronymState

Tracks acronym usage across tutorial steps.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `acronym` | string | The acronym (e.g., "VLAN") | Yes |
| `first_file` | string | File where first used | Yes |
| `first_line` | int | Line of first occurrence | Yes |
| `first_column` | int | Column of first occurrence | No |
| `expanded` | boolean | Whether expanded at first use | Yes |
| `expansion_text` | string | The expansion used (if any) | No |
| `occurrences` | int | Total occurrences in tutorial | No |

### QualityScore

Quality score calculation result.

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `score` | float | Final score (1.0-10.0) | Yes |
| `base_score` | float | Starting score (10.0) | Yes |
| `deductions` | array[Deduction] | Itemized deductions | Yes |
| `assessment` | string | Text summary (Excellent/Good/Needs Work/Major Issues) | Yes |

**Deduction** sub-entity:
| Field | Type | Description |
|-------|------|-------------|
| `category` | string | Rule category |
| `count` | int | Number of issues |
| `weight` | float | Per-issue deduction |
| `total` | float | count * weight |

## Entity Relationships

```
EditorialRule (1) ────────< EditorialIssue (*)
      │                           │
      │                           │
      └──────── category ────────►│
                                  │
EditorialResult (1) ─────────────<┘
      │
      │
      └──────► QualityScore (1)

AcronymState (*) ◄───────── EditorialResult (1)
                  (computed during validation)
```

## Validation Rules

### EditorialRule Constraints
- `id` must be unique and follow pattern: `CATEGORY-NNN`
- `pattern` required unless rule uses stateful check function
- `severity` determines quality score deduction weight

### EditorialIssue Constraints
- `line_number` must be ≥ 1
- `original_text` should be ≤ 200 characters (truncate with "...")
- If `is_query` is true, `fix_type` should be MANUAL

### EditorialResult Constraints
- `quality_score` calculated as: `max(1.0, 10.0 - weighted_deductions)`
- `files_scanned` must be sorted numerically (step-1.md, step-2.md, ...)
- `issues` must be sorted by file, then line number

## State Transitions

### Issue Lifecycle

```
[DETECTED] ──AI verify──► [VERIFIED] ──merge──► [REPORTED]
     │                        │
     │                        ▼
     └──AI reject──► [REJECTED] (filtered out)
```

### Acronym State Lifecycle

```
[UNKNOWN] ──first seen──► [UNVERIFIED]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    [EXPANDED] (correct)           [NOT_EXPANDED] (violation)
```

## Data Formats

### Rule Definition (YAML)

```yaml
rules:
  - id: ACRONYM-001
    category: ACRONYM
    severity: HIGH
    pattern: null  # Uses stateful check
    message_template: "Acronym '{acronym}' used on line {line} without first-use expansion"
    fix_suggestion: "Change to '{expansion} ({acronym})'"
    fix_type: AI
    source: both
    examples:
      - before: "Configure the VLAN settings"
        after: "Configure the virtual LAN (VLAN) settings"

  - id: PUNCT-001
    category: PUNCT
    severity: MEDIUM
    pattern: "\\s+—\\s+"
    message_template: "Em dash should not have spaces around it"
    fix_suggestion: "Remove spaces: '—'"
    fix_type: AUTO
    source: Jill
```

### Validation Output (JSON)

```json
{
  "tutorial_folder": "tc-tacacs-basics",
  "timestamp": "2026-02-20T14:30:00Z",
  "files_scanned": ["step-1.md", "step-2.md", "step-3.md"],
  "quality_score": 7.5,
  "high_priority_count": 2,
  "medium_priority_count": 3,
  "low_priority_count": 1,
  "ai_enhanced": true,
  "issues": [
    {
      "rule_id": "ACRONYM-001",
      "file_path": "tc-tacacs-basics/step-1.md",
      "line_number": 15,
      "original_text": "Configure the ISE settings",
      "suggested_text": "Configure the Cisco Identity Services Engine (ISE) settings",
      "message": "Acronym 'ISE' used without first-use expansion",
      "severity": "HIGH",
      "fix_type": "AI",
      "ai_verified": true,
      "is_query": false
    }
  ]
}
```

### PR Comment Output (Markdown)

See `research.md` RQ-4 for full template. Key sections:
1. Header with quality score and issue counts
2. Global Edits table (aggregated by rule)
3. Queries for Author (checkbox items)
4. Step-by-Step Review (per-file tables)
5. Footer with links
