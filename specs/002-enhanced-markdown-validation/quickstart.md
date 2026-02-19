# Quickstart: Enhanced Markdown Validation

## Prerequisites

- Python 3.10+
- Access to `tutorial-testing` repository
- (Optional) Cisco Chat-AI credentials for AI-powered fixes

## Local Setup

```bash
# Clone and navigate
cd tutorial-testing

# Install dependencies
pip install jsonschema pytest requests

# Set environment variables (optional, for AI fixes)
export APP_KEY="your-app-key"
export CLIENT_ID="your-client-id"
export CLIENT_SECRET="your-client-secret"
```

## Running Validation

### Basic Usage

```bash
# Validate a tutorial folder
python tools/clean_markdown.py tc-example

# Validate without auto-fix (report only)
python tools/clean_markdown.py --no-fix tc-example

# Get JSON output
python tools/clean_markdown.py --json-output tc-example
```

### Using Environment Variable (CI-style)

```bash
export FOLDER_NAME=tc-example
python tools/clean_markdown.py
```

## Testing Against Historical PRs

To validate the new rules catch known issues:

```bash
# PR #177 - HTML tags
git fetch origin pull/177/head:pr-177
git checkout pr-177
python tools/clean_markdown.py --no-fix tc-flask-restx-rbac

# PR #196 - Nested list issues
git fetch origin pull/196/head:pr-196
git checkout pr-196
python tools/clean_markdown.py --no-fix tc-webhook-flask-restx-rbac
```

Expected output should show the issues that originally caused XML conversion failures.

## Running Tests

```bash
# Run all validation tests
pytest tools/pytest_validation.py

# Run new markdown validator tests
pytest tests/test_markdown_validator.py -v
```

## Debugging

### Verbose Mode

```bash
python tools/clean_markdown.py --verbose tc-example
```

Shows:
- Each file being processed
- Each rule being checked
- Matches found and fixes applied

### Check Specific Rule

```python
# In Python REPL
from tools.clean_markdown import check_html_tags

issues = check_html_tags("path/to/step-3.md")
for issue in issues:
    print(f"Line {issue.line_number}: {issue.message}")
```

## Common Issues

### AI Fixes Not Working

1. Verify credentials are set:
   ```bash
   echo $APP_KEY $CLIENT_ID $CLIENT_SECRET
   ```

2. Test AI connectivity:
   ```bash
   python tools/ai_analysis.py tc-example/sidecar.json advice
   ```

### False Positives

If valid markdown is flagged:

1. Check if it's inside a code block (should be skipped)
2. Check if it's a blockquote (should be skipped)
3. Open an issue with the specific markdown that was incorrectly flagged

## Integration with VS Code

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Markdown",
      "type": "shell",
      "command": "python",
      "args": ["tools/clean_markdown.py", "--no-fix", "${fileDirname}"],
      "problemMatcher": [],
      "group": "test"
    }
  ]
}
```

Run with: `Ctrl+Shift+P` → "Run Task" → "Validate Markdown"
