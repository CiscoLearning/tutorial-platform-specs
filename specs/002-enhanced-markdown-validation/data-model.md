# Data Model: Enhanced Markdown Validation

## Entities

### ValidationRule

Defines a single validation rule that checks for a specific markdown pattern.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique rule identifier (e.g., `HTML_TAG`, `LINK_SPACING`) |
| `pattern` | regex | Regular expression to detect the issue |
| `severity` | enum | `BLOCKING` or `WARNING` |
| `message_template` | string | Human-readable error message with `{line}` placeholder |
| `fix_suggestion` | string | Actionable fix instructions |
| `auto_fixable` | boolean | Whether this rule can be auto-fixed |
| `fix_type` | enum | `REGEX` (simple replacement) or `AI` (requires AI reformatting) |

**Example:**

```python
ValidationRule(
    id="HTML_TAG",
    pattern=re.compile(r'<(br|p|div|span|hr|img)[^>]*/?>'),
    severity="BLOCKING",
    message_template="Line {line}: HTML tag `{match}` will break XML conversion.",
    fix_suggestion="Use blank line for paragraph breaks instead of <br>.",
    auto_fixable=True,
    fix_type="REGEX"
)
```

### ValidationIssue

Represents a single issue found during validation.

| Field | Type | Description |
|-------|------|-------------|
| `rule_id` | string | Reference to ValidationRule.id |
| `file_path` | string | Path to the markdown file |
| `line_number` | int | 1-indexed line number where issue found |
| `column` | int | Optional column position |
| `match` | string | The actual text that matched the pattern |
| `message` | string | Rendered error message |
| `severity` | enum | Inherited from rule: `BLOCKING` or `WARNING` |
| `fixed` | boolean | Whether auto-fix was applied |
| `original_text` | string | Original line content (for diff) |
| `fixed_text` | string | Fixed line content (if auto-fixed) |

### ValidationResult

Aggregated result from validating one or more files.

| Field | Type | Description |
|-------|------|-------------|
| `issues` | list[ValidationIssue] | All issues found |
| `blocking_count` | int | Count of BLOCKING issues |
| `warning_count` | int | Count of WARNING issues |
| `files_scanned` | list[string] | Paths of all files scanned |
| `files_modified` | list[string] | Paths of files that were auto-fixed |
| `auto_fix_enabled` | boolean | Whether auto-fix was enabled |
| `summary` | string | Human-readable summary for PR comment |

## Validation Rules Registry

### P1: Blocking Rules (Must Fix)

| ID | Pattern | Fix Type | Description |
|----|---------|----------|-------------|
| `HTML_TAG` | `<(br\|p\|div\|span\|hr\|img)[^>]*/?>` | REGEX | HTML tags in markdown |
| `LINK_NO_SPACE_BEFORE` | `\S\[[^\]]+\]\([^)]+\)` | REGEX | Link missing space before |
| `LINK_NO_SPACE_AFTER` | `\[[^\]]+\]\([^)]+\)\S` | REGEX | Link missing space after |
| `LINK_BROKEN` | `\[[^\]]*\n[^\]]*\]\([^)]*\)` | AI | Line break inside link syntax |
| `LIST_INDENT_INCONSISTENT` | (stateful check) | AI | Nested list with mixed indentation |
| `CODE_BLOCK_IN_LIST` | (stateful check) | AI | Code block not properly indented in list |

### P2: Warning Rules (Auto-fix Available)

| ID | Pattern | Fix Type | Description |
|----|---------|----------|-------------|
| `TRAILING_WHITESPACE` | `[ \t]+$` | REGEX | Trailing spaces at end of line |
| `DOUBLE_SPACE` | `\S {2,}\S` | REGEX | Multiple spaces between words |
| `DURATION_FORMAT` | `^60m` in sidecar.json | REGEX | Duration >= 60m needs hour format |

## State Diagram: Validation Flow

```
┌─────────────┐
│ Start       │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Load markdown   │
│ files           │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐     ┌──────────────────┐
│ Run regex rules │────▶│ Collect issues   │
└──────┬──────────┘     └──────────────────┘
       │
       ▼
┌─────────────────┐     ┌──────────────────┐
│ Run stateful    │────▶│ Add to issues    │
│ checks (lists)  │     └──────────────────┘
└──────┬──────────┘
       │
       ▼
┌─────────────────────┐
│ Auto-fix enabled?   │
└──────┬──────┬───────┘
       │      │
      Yes     No
       │      │
       ▼      ▼
┌──────────┐  ┌──────────────┐
│ Apply    │  │ Report only  │
│ fixes    │  └──────────────┘
└──────┬───┘
       │
       ▼
┌─────────────────┐
│ Generate PR     │
│ comment with    │
│ diff            │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Return result   │
│ (exit code)     │
└─────────────────┘
```

## File Relationships

```
tutorial-testing/tools/
├── clean_markdown.py
│   └── Uses: ValidationRule, ValidationIssue, ValidationResult
├── schema_validation.py
│   └── Uses: ValidationIssue (for duration fix)
└── ai_analysis.py
    └── Referenced by: AI-type fixes
```
