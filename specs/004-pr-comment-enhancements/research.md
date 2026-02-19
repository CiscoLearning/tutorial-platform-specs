# FR-5: PR Comment Enhancements - Research

## Current CI Workflow Analysis

### Workflow File
**Location:** `.github/workflows/tutorial-linting.yml`

### Comment Generation Points

| Step | Comment Logic | Output Quality | Fallback Needed |
|------|---------------|----------------|-----------------|
| Folder Check | Fails silently - no comment | Poor - must check logs | Yes |
| Folder Naming | Fails silently - no comment | Poor - must check logs | Yes |
| Subfolder Requirements | Fails silently - no comment | Poor - must check logs | Yes |
| Schema Validation | Reads `schema_output.txt`, posts content | Good - shows actual errors | No |
| Pytest Checks | Generic "click for more info" message | Poor - no error details | Yes (priority) |
| Markdown Validation | Posts `pr_comment.md` | Good - shows details | No |
| XML Conversion | Posts full `transform_stderr.log` | Too verbose - needs parsing | Partial |
| Solomon Lint | Posts raw `linting_output.log` | OK - but raw format | Partial |
| AI Analysis | Posts `llm_output.txt` | Good - structured output | No |

### Pytest Test Coverage (errors hidden behind "click for more info")

| Test Name | Error Type | Current Visibility | Custom Format Needed |
|-----------|------------|-------------------|---------------------|
| `test_broken_links` | Broken URLs, Images | Hidden in logs | Yes (P1) |
| `test_duration_sum` | Duration mismatch | Hidden in logs | Yes (P3) |
| `test_guid_uniqueness` | Duplicate GUIDs | Hidden in logs | Fallback OK |
| `test_extra_md_files` | Unexpected .md files | Hidden in logs | Fallback OK |
| `test_skill_levels` | Invalid skill level | Hidden in logs | Fallback OK |
| `test_technologies` | Invalid technology | Hidden in logs | Fallback OK |

### Pytest Output Analysis

The pytest validation runs multiple tests. Current output format:

```
FAILED tools/pytest_validation.py::test_broken_links - AssertionError: Errors in `step-8.md`:
    - Broken URL: https://developer.cisco.com/automation-bootcamp/
assert not [('/path/to/step-8.md', ['Broken URL: https://...'])]
```

**Key patterns to extract:**
- Test name: `test_broken_links`, `test_duration_sum`, etc.
- File affected: `step-8.md`
- Error type: `Broken URL`, `Broken Image`
- Specific value: the URL or image path

### XML Error Output Analysis

Solomon XML errors look like:

```
-:139: parser error : Opening and ending tag mismatch: ParaBlock line 138 and ItemPara
</ItemPara>
           ^
```

**Key patterns to extract:**
- Line number: `139`
- Error type: `Opening and ending tag mismatch`
- Tags involved: `ParaBlock`, `ItemPara`

### GitHub CLI Comment Capabilities

```bash
# Create new comment
gh pr comment $PR_NUMBER --body "message"

# Update existing comment (requires comment ID)
gh api repos/{owner}/{repo}/issues/comments/{id} -X PATCH -f body="new message"

# List comments to find existing bot comments
gh pr view $PR_NUMBER --comments --json comments
```

## Error Frequency from Hugo Migration

Based on FF-5 migration data:

| Error Type | PRs Affected | Detectability |
|------------|--------------|---------------|
| Broken URL | 13 | Easy - URL in error message |
| XML Parser Error | 7 | Medium - need pattern matching |
| Missing Image | 2 | Easy - path in error message |
| Duration Mismatch | 2 | Easy - values in pytest output |
| Code in List | 3 | Hard - need content analysis |

## Existing Tools

### pytest_validation.py

**Location:** `tools/pytest_validation.py`

**Tests that produce parseable errors:**
- `test_broken_links` - outputs `Broken URL:` and `Broken Image:`
- `test_duration_sum` - outputs expected vs actual duration
- `test_extra_md_files` - outputs file names
- `test_guid_uniqueness` - outputs duplicate GUIDs

### clean_markdown.py

**Location:** `tools/clean_markdown.py`

Already has structured output with `ValidationIssue` dataclass:
- `rule_id`
- `file_path`
- `line_number`
- `message`
- `severity`

Could reuse this format for PR comments.

## Implementation Options

### Option 1: Bash Parsing in Workflow

Pros:
- No new files needed
- Simple grep/sed extraction

Cons:
- Hard to maintain
- Limited formatting options
- Error-prone

### Option 2: Python Script for Comment Formatting

Pros:
- Reusable across projects
- Easy to test
- Rich markdown generation
- Can handle complex parsing

Cons:
- Another file to maintain
- Needs to be synced to repos

### Option 3: Enhance pytest_validation.py Output

Pros:
- Single source of truth
- Already has structured data
- Can output JSON for parsing

Cons:
- Changes existing tool
- May affect other integrations

**Recommendation:** Option 2 with JSON output from pytest

## Proposed Architecture

```
pytest_validation.py
    │
    ▼ (JSON output)
pytest_results.json
    │
    ▼
format_pr_comment.py
    │
    ▼ (Markdown)
gh pr comment
```

### JSON Schema for Errors

```json
{
  "status": "failed",
  "tests_run": 15,
  "tests_passed": 13,
  "tests_failed": 2,
  "errors": [
    {
      "test": "test_broken_links",
      "file": "step-8.md",
      "line": 15,
      "type": "broken_url",
      "value": "https://example.com/broken",
      "message": "URL returns 404"
    }
  ]
}
```

## Next Steps

1. Modify `pytest_validation.py` to output JSON alongside text
2. Create `format_pr_comment.py` to consume JSON and generate markdown
3. Update workflow to use new comment format
4. Test with existing failing PRs
