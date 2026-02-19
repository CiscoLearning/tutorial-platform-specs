# Quickstart: PR Comment Enhancements

**Feature**: FR-5 PR Comment Enhancements
**Date**: 2026-02-19

## Overview

This guide explains how to integrate and test the enhanced PR comment system.

## Prerequisites

- Python 3.10+
- Access to `tutorial-testing` repository
- GitHub CLI (`gh`) installed and authenticated

## Quick Test

### 1. Generate Test Errors Locally

```bash
cd tutorial-testing

# Test with a known failing tutorial (broken URL)
export SIDECAR_FILE="tc-test-broken/sidecar.json"
export FOLDER_NAME="tc-test-broken"

# Run pytest and capture JSON output
python tools/pytest_validation.py --json-output > pytest_results.json

# Generate formatted comment
python tools/format_pr_comment.py pytest_results.json --output comment.md

# View the result
cat comment.md
```

### 2. Test Error Type Formatters

```bash
# Test broken URL formatting
echo '{
  "type": "broken_url",
  "source": "pytest",
  "file": "step-5.md",
  "line": 42,
  "value": "https://example.com/broken",
  "message": "URL returns 404",
  "severity": "blocking"
}' | python tools/format_pr_comment.py --stdin --single

# Test XML error formatting
echo '{
  "type": "xml_error",
  "source": "solomon_transform",
  "file": "step-3.md",
  "line": 139,
  "message": "Opening and ending tag mismatch: ParaBlock and ItemPara",
  "severity": "blocking",
  "fix_suggestion": "Ensure code blocks are not nested inside list items"
}' | python tools/format_pr_comment.py --stdin --single
```

## Integration Points

### Workflow Integration

The `format_pr_comment.py` script is called from GitHub Actions after each validation step:

```yaml
# In .github/workflows/tutorial-linting.yml
- name: Format and post PR comment
  run: |
    python tools/format_pr_comment.py \
      --pytest pytest_results.json \
      --schema schema_output.txt \
      --xml transform_stderr.log \
      --pr-number ${{ github.event.pull_request.number }} \
      | gh pr comment ${{ github.event.pull_request.number }} --body-file -
```

### JSON Output from pytest_validation.py

Add `--json-output` flag to enable structured output:

```bash
pytest tools/pytest_validation.py --json-output > pytest_results.json
```

Output format:

```json
{
  "status": "failed",
  "tests_run": 15,
  "tests_passed": 13,
  "tests_failed": 2,
  "errors": [
    {
      "test": "test_broken_links",
      "type": "broken_url",
      "file": "step-8.md",
      "line": 15,
      "value": "https://example.com/broken",
      "message": "URL returns 404",
      "severity": "blocking"
    }
  ]
}
```

## Example Output

### Formatted Comment for Broken URLs

```markdown
## 🚫 Validation Failed

**Tutorial:** `tc-example-tutorial`
**Blocking Issues:** 2 | **Warnings:** 1

---

### Broken URLs

| File | Line | URL | Status |
|------|------|-----|--------|
| step-5.md | 42 | https://example.com/broken | 404 Not Found |
| step-8.md | 15 | https://developer.cisco.com/old-page | 404 Not Found |

**How to fix:** Update or remove the broken URLs listed above.

---

### Duration Mismatch ⚠️

| Field | Expected | Actual |
|-------|----------|--------|
| Total Duration | 35m00s | 30m00s |

**How to fix:** Run `python tools/fix_sidecar.py tc-example-tutorial/sidecar.json`

---

<details>
<summary>Raw validation output</summary>

\`\`\`
FAILED tools/pytest_validation.py::test_broken_links - AssertionError...
\`\`\`

</details>
```

## Testing Checklist

- [ ] Broken URL errors show file, line, URL, and HTTP status
- [ ] Missing image errors show file and image path
- [ ] XML errors show plain-language explanation with fix suggestion
- [ ] Duration mismatches show expected vs actual with fix command
- [ ] Unknown error types fall back to raw output in collapsible section
- [ ] Comment truncates properly when output exceeds 10KB
- [ ] Visual indicators distinguish blocking (🚫) vs warning (⚠️)

## Troubleshooting

### Comment Not Appearing

1. Check `GH_TOKEN` environment variable is set
2. Verify PR write permissions in workflow
3. Check GitHub Actions logs for `gh pr comment` errors

### JSON Parse Errors

1. Ensure `--json-output` flag is passed to pytest
2. Validate JSON output: `python -m json.tool pytest_results.json`
3. Check for encoding issues in error messages

### Truncated Output

Large outputs (>10KB) are automatically truncated. To see full output:
1. Click "Details" link in comment
2. Navigate to Actions tab → workflow run → step logs
