# AI Reformatting Prompt Contract

## Purpose

For complex markdown issues that regex cannot reliably fix (nested lists, structural problems), we use Cisco Chat-AI to reformat the content while preserving meaning.

## Prompt Template

```text
You are a markdown formatting assistant for technical tutorials.

TASK: Fix the markdown formatting issues in the following content while preserving the exact meaning and information.

RULES:
1. Fix nested list indentation to use consistent 2-space indentation
2. Ensure links have whitespace before and after: ` [text](url) `
3. Ensure code blocks within lists are indented 4 spaces beyond the list level
4. Do NOT change any text content, only formatting
5. Do NOT add or remove any information
6. Preserve all code block contents exactly as-is

ISSUES DETECTED:
{issue_descriptions}

ORIGINAL CONTENT (lines {start_line}-{end_line}):
```markdown
{original_content}
```

OUTPUT: Return ONLY the fixed markdown, no explanations. Preserve line breaks exactly where they should be.
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{issue_descriptions}` | List of detected issues | "Nested list on line 23 has inconsistent indentation" |
| `{start_line}` | First line of affected region | 23 |
| `{end_line}` | Last line of affected region | 28 |
| `{original_content}` | Raw markdown content | The actual markdown text |

## API Integration

Uses existing `ai_analysis.py` pattern:

```python
def ai_reformat_markdown(content: str, issues: list[str]) -> str:
    """
    Send markdown to Cisco Chat-AI for reformatting.

    Args:
        content: The markdown content to fix
        issues: List of issue descriptions

    Returns:
        Reformatted markdown content
    """
    prompt = REFORMAT_PROMPT_TEMPLATE.format(
        issue_descriptions="\n".join(f"- {i}" for i in issues),
        start_line=1,  # Context from calling code
        end_line=len(content.splitlines()),
        original_content=content
    )

    # Use existing OAuth flow from ai_analysis.py
    response = call_cisco_chat_ai(prompt)
    return response.strip()
```

## Response Validation

Before applying AI-generated fixes:

1. **Line count check**: New content should have similar line count (±20%)
2. **Content preservation**: All code blocks must be unchanged
3. **Link preservation**: All URLs must be preserved
4. **Diff generation**: Create diff for PR comment

```python
def validate_ai_response(original: str, fixed: str) -> bool:
    """Validate AI didn't break anything."""
    orig_lines = len(original.splitlines())
    fixed_lines = len(fixed.splitlines())

    # Line count sanity check
    if abs(fixed_lines - orig_lines) / orig_lines > 0.2:
        return False

    # All URLs must be preserved
    orig_urls = re.findall(r'https?://[^\s\)]+', original)
    fixed_urls = re.findall(r'https?://[^\s\)]+', fixed)
    if set(orig_urls) != set(fixed_urls):
        return False

    return True
```

## Fallback Behavior

If AI reformatting fails or validation fails:

1. Log the failure
2. Keep original content unchanged
3. Report issue as WARNING (not BLOCKING)
4. Include in PR comment: "AI reformatting failed for lines X-Y. Manual fix recommended."

## Rate Limiting

- Cisco Chat-AI has rate limits
- Batch multiple issues in same file into single API call
- Maximum 3 AI calls per PR validation run
- If limit exceeded, prioritize BLOCKING issues
