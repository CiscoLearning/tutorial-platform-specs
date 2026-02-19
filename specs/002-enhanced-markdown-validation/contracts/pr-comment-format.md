# PR Comment Format Contract

## Overview

When markdown validation runs and makes auto-fixes, a PR comment is posted showing all changes. This allows authors to review and revert if needed.

## Comment Structure

```markdown
## Markdown Validation Results

### Auto-Fixed Issues

The following issues were automatically fixed. Review the changes below and revert if needed.

<details>
<summary>📝 step-3.md (2 fixes)</summary>

**Line 45: HTML tag removed**
```diff
- Download the file<br>and extract it.
+ Download the file
+
+ and extract it.
```

**Line 67-72: Nested list reformatted by AI**
```diff
- - Item 1
-   - Subitem with bad indent
-      - Wrong level
+ - Item 1
+   - Subitem with consistent indent
+     - Correct level
```

</details>

<details>
<summary>📝 step-5.md (1 fix)</summary>

**Line 23: Link spacing added**
```diff
- Click[here](https://example.com)to continue.
+ Click [here](https://example.com) to continue.
```

</details>

### Summary

| Type | Count | Action |
|------|-------|--------|
| 🔴 Blocking | 2 | Auto-fixed |
| 🟡 Warning | 1 | Auto-fixed |

✅ All issues resolved. Pipeline continuing.

---
<sub>To disable auto-fix, add `[no-autofix]` to your commit message.</sub>
```

## Severity Indicators

| Icon | Severity | Meaning |
|------|----------|---------|
| 🔴 | BLOCKING | Would cause XML conversion failure |
| 🟡 | WARNING | May cause issues; recommended to fix |
| ✅ | FIXED | Issue was auto-fixed |

## Comment Conditions

| Condition | Comment Behavior |
|-----------|------------------|
| No issues found | "No markdown issues found! ✅" |
| Issues found, all auto-fixed | Full diff comment (as above) |
| Issues found, `--no-fix` mode | List issues without fixes |
| Blocking issues not fixable | List issues, fail pipeline |

## GitHub API Usage

```python
def post_pr_comment(pr_number: int, body: str) -> None:
    """Post validation results as PR comment."""
    subprocess.run([
        "gh", "pr", "comment", str(pr_number),
        "--body", body
    ], check=True)
```

## Character Limits

- GitHub PR comments have a 65,536 character limit
- If diff exceeds limit, truncate with: "... and N more changes. See workflow logs for full details."

## Revert Instructions

If an author wants to revert an auto-fix:

1. Check out the branch locally
2. Run `git diff HEAD~1` to see changes
3. Use `git checkout HEAD~1 -- <file>` to revert specific files
4. Commit and push

Alternative: Add `[no-autofix]` to commit message to skip auto-fix on next push.
