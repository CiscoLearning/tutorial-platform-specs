# Reference Code - FR-1 Enhanced Markdown Validation

**Snapshot Date:** 2026-02-18 (final version after all false positive fixes)
**Canonical Source:** `CiscoLearning/tutorial-testing` repository

This directory contains snapshots of deployed code for audit, rollback, and reference purposes.

---

## Files

| File | Lines | Purpose |
|------|-------|---------|
| `clean_markdown.py` | ~1,500 | Main validation tool with 7 detection rules |
| `test_detection_rules.py` | ~490 | 50 unit tests covering edge cases |
| `integration_test.py` | ~370 | Integration tests with XML pipeline |
| `integration-tests.yml` | ~330 | GitHub Actions CI workflow |

---

## Version History

### v1.0 - Final Release (2026-02-18)

**Changes from initial implementation:**

1. **CODE_BLOCK_IN_LIST** - Fixed false positives
   - Added `blank_line_seen` tracking
   - Added `is_in_code_block()` check for list patterns inside code
   - Impact: 848 → 42 issues (-95%)

2. **LINK_NO_SPACE_BEFORE** - Fixed false positives
   - Excluded `!` (images), `(` (parenthetical), `*` (bold)
   - Pattern: `[^\s!(*]\[[^\]]+\]\([^)]+\)`
   - Impact: 80 → 3 issues (-96%)

3. **LINK_NO_SPACE_AFTER** - Fixed false positives
   - Excluded `*`, `_` (markdown), `'` (possessive)
   - Pattern: `[^\s\.\,\!\?\;\:\)\]\}\*\_\']\`
   - Impact: 19 → 9 issues (-53%)

---

## Detection Rules

### Blocking Rules (will fail CI)

| Rule ID | Function | Pattern/Logic |
|---------|----------|---------------|
| HTML_TAG | `check_html_tags()` | `<(br\|p\|div\|span\|hr\|img)[^>]*\/?>` |
| LINK_NO_SPACE_BEFORE | `check_link_spacing_before()` | Non-whitespace immediately before `[` |
| LINK_NO_SPACE_AFTER | `check_link_spacing_after()` | Non-punctuation immediately after `)` |
| LINK_BROKEN | `check_link_broken()` | Newline inside `[text](url)` |
| LIST_INDENT_INCONSISTENT | `check_list_indent()` | Mixed 2/3/4 space indentation |
| CODE_BLOCK_IN_LIST | `check_code_block_in_list()` | Stateful: tracks list context and blank lines |

### Warning Rules (won't fail CI)

| Rule ID | Function | Pattern |
|---------|----------|---------|
| TRAILING_WHITESPACE | `check_trailing_whitespace()` | `[ \t]+$` |
| DOUBLE_SPACE | `check_double_space()` | `  ` (two spaces) |

---

## Key Implementation Details

### Code Block Detection

```python
def is_in_code_block(lines: List[str], line_index: int) -> bool:
    """Check if a line is inside a fenced code block."""
    in_code_block = False
    for i in range(line_index + 1):
        line = lines[i].strip()
        if line.startswith('```'):
            in_code_block = not in_code_block
    return in_code_block
```

### CODE_BLOCK_IN_LIST Logic

```python
# Key insight: blank line after list item ends the list context
blank_line_seen = False

for line_num, line in enumerate(lines, 1):
    # Skip lines inside code blocks - they may contain list-like syntax
    if is_in_code_block(lines, line_num - 1):
        continue

    if is_list_item(line):
        in_list = True
        blank_line_seen = False  # Reset - we're in active list content
    elif not line.strip():
        if in_list:
            blank_line_seen = True
    elif in_list and blank_line_seen and not line.startswith(' '):
        # Non-indented content after blank line = list has ended
        in_list = False
        blank_line_seen = False
```

### Link Spacing Patterns

```python
# BEFORE: Exclude !, (, * (images, parenthetical, bold)
LINK_NO_SPACE_BEFORE_PATTERN = re.compile(r'[^\s!(*]\[[^\]]+\]\([^)]+\)')

# AFTER: Exclude punctuation, ), ], }, *, _, ' (markdown, possessive)
LINK_NO_SPACE_AFTER_PATTERN = re.compile(r'\[[^\]]+\]\([^)]+\)[^\s\.\,\!\?\;\:\)\]\}\*\_\']')
```

---

## Test Categories

### TestCodeBlockInList (12 tests) - Most Critical

```python
def test_not_flagged_after_blank_line(self):
    """Code block after blank line should NOT be flagged"""

def test_list_inside_code_block_not_flagged(self):
    """List-like syntax inside code block should NOT be detected"""

def test_real_world_pattern_model_name(self):
    """Real pattern from tc-ai-lm-studio - should NOT be flagged"""
```

### TestLinkSpacing (15 tests)

```python
def test_parenthetical_link_not_flagged(self):
    """([RFC 8894](url)) should not be flagged"""

def test_bold_link_not_flagged(self):
    """**[Cowrie](url)** should not be flagged"""

def test_possessive_after_link(self):
    """([CA](url))'s should not be flagged"""
```

---

## Usage

### CLI

```bash
# Validate without fixing
python clean_markdown.py path/to/tc-tutorial --no-fix

# Validate with auto-fix
python clean_markdown.py path/to/tc-tutorial

# JSON output for CI
python clean_markdown.py path/to/tc-tutorial --json-output

# Skip AI fixes
python clean_markdown.py path/to/tc-tutorial --no-ai-fix
```

### Commit Message Flags

- `[no-autofix]` - Skip ALL auto-fixes
- `[no-ai-fix]` - Skip AI fixes only (regex still applies)

---

## Known Limitations

1. **4-backtick fences** - ```` with nested ``` may cause false positives
2. **LINK_BROKEN** - Doesn't detect all newline patterns in URLs
3. **AI dependency** - Complex fixes require Cisco Chat-AI availability

---

## Deployment

Code is deployed to `CiscoLearning/tutorial-testing`:
- PR #101 merged 2026-02-18
- Branch: `feature/enhanced-markdown-validation` → `main`
