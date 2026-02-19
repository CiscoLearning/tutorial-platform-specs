# CLI Interface Contract: clean_markdown.py

## Usage

```bash
python tools/clean_markdown.py [OPTIONS] <folder_path>
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `folder_path` | Yes | Path to tutorial folder (e.g., `tc-example`) |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--no-fix` | false | Disable auto-fix; report issues only |
| `--json-output` | false | Output results as JSON instead of text |
| `--strict` | false | Fail on warnings (not just blockers) |
| `--verbose` | false | Show detailed processing information |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (no blocking issues, or all issues auto-fixed) |
| 1 | Blocking issues found (and not auto-fixed) |
| 2 | Invalid arguments or file not found |

## Output Formats

### Text Output (Default)

```
Validating tc-example...

BLOCKING:
  Line 45: HTML tag `<br>` will break XML conversion.
    → Use blank line for paragraph breaks instead.
    ✓ Auto-fixed

  Line 23-28: Nested list indentation inconsistent.
    → Use 2 or 4 spaces consistently.
    ✓ Auto-fixed by AI

WARNING:
  Line 73: Trailing whitespace detected.
    ✓ Auto-fixed

Summary: 2 blocking issues fixed, 1 warning fixed
Files modified: step-3.md, step-5.md
```

### JSON Output (`--json-output`)

```json
{
  "success": true,
  "blocking_count": 0,
  "warning_count": 0,
  "issues": [
    {
      "rule_id": "HTML_TAG",
      "file": "step-3.md",
      "line": 45,
      "severity": "BLOCKING",
      "message": "HTML tag `<br>` will break XML conversion.",
      "fixed": true,
      "original": "Download the file<br>and extract it.",
      "fixed_text": "Download the file\n\nand extract it."
    }
  ],
  "files_modified": ["step-3.md", "step-5.md"],
  "auto_fix_enabled": true
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FOLDER_NAME` | Alternative to positional argument (for CI compatibility) |
| `APP_KEY` | Cisco Chat-AI application key (for AI fixes) |
| `CLIENT_ID` | Cisco OAuth client ID (for AI fixes) |
| `CLIENT_SECRET` | Cisco OAuth client secret (for AI fixes) |

## CI Integration

In `tutorial-linting.yml`:

```yaml
- name: Validate and fix markdown
  id: markdown-validation
  run: |
    python tools/clean_markdown.py --json-output "${{ env.FOLDER_NAME }}" > validation_result.json
  env:
    FOLDER_NAME: "${{ steps.folder-check.outputs.FOLDER_NAME }}"
    APP_KEY: "${{ secrets.APP_KEY }}"
    CLIENT_ID: "${{ secrets.CLIENT_ID }}"
    CLIENT_SECRET: "${{ secrets.CLIENT_SECRET }}"

- name: Commit auto-fixes if any
  if: steps.markdown-validation.outputs.files_modified != ''
  run: |
    git config user.name "github-actions"
    git config user.email "actions@github.com"
    git add -A
    git commit -m "Auto-fix markdown validation issues"
    git push
```
