# Research: Enhanced Markdown Validation

## Source PRs Analyzed

- PR #216: Schema validation errors (tags, email format)
- PR #196: XML conversion errors + schema (duration format)
- PR #177: XML conversion errors (br tags, whitespace)

## XML Conversion Error Patterns

### 1. Line Break / `<br>` Tags

**Error:**
```
-:104: parser error : Opening and ending tag mismatch: br line 103 and ParaBlock
Download the </ParaBlock>
```

**Cause:** Markdown line breaks or HTML `<br>` tags create unclosed elements in XML output.

**Markdown patterns that cause this:**
- Explicit `<br>` tags in markdown
- Double newlines in unexpected places
- Line breaks inside inline elements

### 2. Nested List Structure Issues

**Error:**
```
-:2151: parser error : Opening and ending tag mismatch: Item line 2130 and ItemPara
-:2162: parser error : Opening and ending tag mismatch: ItemBlock line 2129 and Item
-:2259: parser error : Opening and ending tag mismatch: SubList line 2197 and ItemBlock
```

**Cause:** Complex nested lists with improper indentation or inline elements break XML structure.

**Markdown patterns that cause this:**
- Lists with code blocks that aren't properly indented
- Nested lists with inconsistent indentation
- Inline elements (links, code) spanning list item boundaries

### 3. Extra Whitespace Issues

**Warning from pipeline:**
```
Extra spaces found in tc-flask-restx-rbac/step-5.md on lines: 73
Extra spaces found in tc-webhook-flask-restx-rbac/step-2.md on lines: 9, 15, 19, 23, 27, 31, 39, 43, 47, 51, 55, 61, 65, 69, 73, 77, 85, 89, 93, 97
```

**Types:**
- Trailing spaces at end of lines
- Double spaces within text
- Extra blank lines

**Impact:** Currently detected as warnings, sometimes correlates with XML conversion failures.

## Schema Validation Patterns

### 1. Duration Format

**Error:**
```
JSON schema validation failed: The main 'duration' field must follow 'XXmXXs' or 'XhXXmXXs' format
Full error message: '60m00s' does not match pattern
```

**Root cause:** Durations >= 60 minutes must use hour format (`1h00m00s`), not `60m00s`.

**Regex pattern:** `^([1-9]\d?h[0-5]?\d{1}m[0-5]?\d{1}s|[0-5]?\d{1}m[0-5]?\d{1}s)$`

### 2. Missing Required Fields

**Error:**
```
JSON schema validation failed: The 'tags' field must be an array of objects
JSON schema validation failed: For an author, the 'email' address must follow a standard format
```

**Common issues:**
- Empty email string `""`
- Missing `tag` key in tags array
- Malformed author object

## Current Pipeline Detection

| Issue Type | Currently Detected? | Actionable Feedback? |
|------------|---------------------|---------------------|
| Schema errors | Yes | Yes - clear messages |
| Whitespace warnings | Yes | Partial - line numbers given |
| XML conversion errors | Yes (after failure) | No - cryptic line numbers in XML |
| Nested list issues | No (until XML fails) | No |
| `<br>` tag issues | No (until XML fails) | No |

## Gap Analysis

**What's missing:**

1. **Pre-conversion markdown validation** - Catch patterns that will break XML before running converter
2. **Actionable line mapping** - XML error line numbers don't map to source markdown
3. **Auto-fix capability** - Some issues (whitespace, duration format) could be auto-corrected
4. **Pattern-specific guidance** - "Line 73 has trailing space" vs "Your nested list on line 45 needs consistent indentation"

## Proposed Validation Rules

### P1: Blocking (will cause XML failure)

1. **No HTML tags in markdown** - Detect `<br>`, `<p>`, etc.
2. **Nested list indentation** - Validate consistent 2 or 4 space indentation
3. **Code blocks in lists** - Ensure proper indentation (4 spaces beyond list level)
4. **Link/image syntax** - Validate no line breaks inside `[text](url)` syntax

### P2: Warning (may cause issues)

1. **Trailing whitespace** - Already detected, enhance line-specific feedback
2. **Double spaces** - Already detected
3. **Excessive blank lines** - More than 2 consecutive

### P3: Auto-fixable

1. **Trailing whitespace** - Strip automatically
2. **Double spaces** - Replace with single (except in code blocks)
3. **Duration format** - Convert `60m00s` to `1h00m00s` automatically
4. **Normalize line endings** - CRLF to LF

## Related: FF-4 GUID Cache Updates

Since we're enhancing the validation pipeline, we could also add:
- Auto-regenerate `guid_cache.json` on push to main
- Validate GUID uniqueness before merge (already done via pytest)
- Sync cache from production automatically (done in FR-0)

## Next Steps

1. Examine `tutorial_md2xml` converter source to understand exact failure points
2. Create regex patterns for detecting problematic markdown
3. Determine which checks should block merge vs warn
4. Design feedback format that maps to source lines
