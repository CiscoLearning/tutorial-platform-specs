# Hugo Tutorial Migration - Learnings

## Overview

This document captures issues discovered during the migration of 110+ tutorials from the Hugo-based cisco-learning-codelabs repository to the ciscou-tutorial-content repository.

## Issues Discovered and Fixes Applied

### 1. Workflow YAML Syntax Error

**Issue:** The CI workflow file had a multiline commit message with dashes that were being interpreted as YAML list items.

```yaml
# BROKEN - dashes interpreted as YAML sequences
git commit -m "Auto-fix: Clean markdown formatting
- Double space removal
- Link spacing fixes"
```

**Fix:** Used HEREDOC syntax to properly escape the commit message content.

```yaml
# FIXED - HEREDOC preserves content literally
git commit -m "$(cat <<'EOF'
Auto-fix: Clean markdown formatting
- Double space removal
- Link spacing fixes
EOF
)"
```

**Location:** `.github/workflows/tutorial-linting.yml`

---

### 2. Bold Text in List Items (Solomon XML Compatibility)

**Issue:** Solomon XML parser cannot handle bold formatting inside list items. Patterns like `- **Term:** description` cause ItemPara/ParaBlock tag mismatches during XML conversion.

```
parser error : Opening and ending tag mismatch: ItemPara line 38 and ParaBlock
```

**Fix:** Added automatic conversion in `clean_markdown.py` to strip bold from list items:
- Input: `- **Hub:** The main device...`
- Output: `- Hub: The main device...`

**Location:** `tools/clean_markdown.py`

**CI Integration:** The fix runs automatically during the "Check for whitespaces in markdown files" step and auto-commits the changes.

---

### 2b. Blank Lines Between List Items (Solomon XML Compatibility)

**Issue:** Solomon XML parser cannot handle blank lines between consecutive list items. This causes the same ItemPara/ParaBlock tag mismatches as bold list items.

```markdown
# BROKEN - blank lines between list items
- First item

- Second item

- Third item
```

**Fix:** Added automatic removal of blank lines between list items in `clean_markdown.py`:
- The fix detects sequences of: list item → blank line(s) → list item
- Removes the blank lines while preserving blank lines after the list ends

**Location:** `tools/clean_markdown.py` - `fix_blank_lines_in_list()` function

**Affected Tutorials:** This pattern was common in the "Learn More" sections of migrated tutorials, particularly the "Cisco U. account helps you" lists.

---

### 2c. Standalone Links Breaking List Structure

**Issue:** Some tutorials had links on their own line without list markers, breaking the list structure:

```markdown
# BROKEN - link without list marker
- Cisco Modeling Labs (2.x)
[DMVPN YAML File](./assets/DMVPN.yaml)
- Five Cisco IOS routers...
```

**Fix:** Manual fix required - see 2d below for the actual solution.

**Affected Tutorials:** DMVPN Phase 1/2/3

---

### 2d. Local File Links in List Items (Solomon XML Compatibility)

**Issue:** Solomon XML parser cannot handle local file links (e.g., `./assets/file.yaml`) inside list items, regardless of how the text is formatted. The link gets converted to a block element that breaks the ItemPara tag structure.

Multiple formatting attempts that all failed:
```markdown
# All of these FAIL
- Cisco Modeling Labs (2.x): [DMVPN YAML File](./assets/DMVPN.yaml)
- Cisco Modeling Labs (2.x) - [DMVPN YAML File](./assets/DMVPN.yaml)
- Cisco Modeling Labs (2.x) with the [DMVPN YAML File](./assets/DMVPN.yaml)
- [DMVPN YAML File](./assets/DMVPN.yaml) for Cisco Modeling Labs 2.x
```

Error pattern:
```
-:38: parser error : Opening and ending tag mismatch: ItemPara line 38 and ParaBlock
<ItemPara></ParaBlock>
```

**Important Note:** External URLs (https://) in list items work fine. The issue is specific to local/relative file paths.

**Fix:** Remove the link entirely and reference the file by name:

```markdown
# FIXED - plain text reference
- Cisco Modeling Labs 2.x with the DMVPN.yaml file from the assets folder
```

**Automated Fix:** Added `LOCAL_LINK_IN_LIST` rule to `clean_markdown.py` that:
1. Detects local file links in list items
2. Extracts the link and replaces the list item with a text reference
3. Places the extracted link after the list block

**Location:** `tools/clean_markdown.py` - `fix_local_links_in_list()` function

**Affected Tutorials:** DMVPN Phase 1/2/3

---

### 3. Invalid Certification Names

**Issue:** Hugo tutorials had certification abbreviations (SVPN, SCOR, SISE, ENCC, ENNA, SCAZT) that aren't in the valid certification list.

**Valid certifications:**
- CCNA, CCNP (various specializations), CCIE (various)
- Cisco Certified DevNet Associate/Professional/Expert
- Cisco Certified Cybersecurity Associate/Professional
- Cisco Certified Design Expert

**Fix:** Set `certifications: null` for tutorials with invalid certifications. The migration script was updated to validate certifications during migration.

---

### 4. Duration Format Mismatches

**Issue:** Hugo tutorials had duration in `MM:SS` format (e.g., `35:00`) but the target schema requires `XmXXs` or `XhXXmXXs` format (e.g., `35m00s`).

**Fix:** Added duration format conversion in the migration script and fix script.

---

### 5. Zero-Duration Steps

**Issue:** Some Hugo tutorials had `0:00` duration for all steps, with only the total duration specified.

**Fix:** Created a script to distribute total duration evenly across steps with a minimum of 1 minute per step.

---

### 6. First/Last Step Labels

**Issue:** Some tutorials didn't have "Overview" as the first step label or "Congratulations" as the last step label.

**Fix:** Added automatic correction in the CI fix script to ensure:
- First file label = "Overview"
- Last file label = "Congratulations"

---

### 7. Extra PR_DESCRIPTION.md Files

**Issue:** The migration script created `PR_DESCRIPTION.md` files inside tutorial folders, which failed the "Extra .md files not listed in sidecar" validation.

**Fix:** Added automatic removal of `PR_DESCRIPTION.md` from tutorial folders.

---

### 8. Nested Lists and Complex Markdown

**Issue:** Some tutorials (particularly vim-introduction and intermediate-vim) had deeply nested lists and complex markdown that couldn't be converted to Solomon XML.

**Status:** These require manual review and content simplification. The patterns that fail include:
- Nested lists with inline code
- Lists with multiple levels of indentation
- Mixed bold/italic formatting in lists

---

### 9. Broken External URLs

**Issue:** Some Hugo tutorials had links to now-defunct domains:
- `calisti.app` (service discontinued)
- `automation-bootcamp` URLs
- `sandboxapicdc.cisco.com` (sandbox URLs that change)

**Fix:** Replaced broken links with archive.org versions or removed if no longer relevant.

---

## CI Workflow Improvements

### Auto-Commit Markdown Fixes

The CI workflow now automatically commits markdown fixes back to PR branches:

1. `clean_markdown.py` runs and fixes issues
2. If changes are made, they're committed with message "Auto-fix: Clean markdown formatting"
3. CI re-runs with the fixed content

This reduces manual intervention for common formatting issues.

---

## Migration Statistics

- **Total Hugo tutorials:** 110
- **Successfully migrated:** 108
- **Requiring manual review:** 2 (vim tutorials with complex nested lists)
- **Authors migrated:** 26+
- **PRs created:** 107

---

## Recommendations for Future Migrations

1. **Pre-validate content:** Run Solomon XML conversion locally before creating PRs
2. **Avoid complex markdown:** Keep list structures flat, avoid bold/italic in list items
3. **Check certifications:** Validate against the allowed list before migration
4. **Test duration parsing:** Ensure duration formats match the target schema
5. **Remove generated files:** Don't include PR_DESCRIPTION.md or other temp files in tutorial folders
6. **Avoid local file links in list items:** Use plain text references instead of markdown links to local files (e.g., `./assets/file.yaml`) in list items

---

## Issue Categories: Auto-Fix vs Human Review

### Auto-Fixable Issues (CI can fix automatically)

These issues can be automatically detected and fixed by CI without human intervention:

| Issue | Tool | Fix Strategy |
|-------|------|--------------|
| Duration mismatch | `tools/fix_sidecar.py` | Recalculate total from step durations |
| Bold in list items | `tools/clean_markdown.py` | Strip bold markers, keep text |
| Blank lines in lists | `tools/clean_markdown.py` | Remove blank lines between list items |
| Double spaces | `tools/clean_markdown.py` | Replace with single space |
| Link spacing | `tools/clean_markdown.py` | Add space before/after links |
| HTML tags | `tools/clean_markdown.py` | Convert `<br>` to newlines, strip tags |
| Local links in lists | `tools/clean_markdown.py` | Extract link after list block |
| Trailing whitespace | `tools/clean_markdown.py` | Strip trailing spaces |
| First/last step labels | CI workflow | Set "Overview" and "Congratulations" |

### Human Review Required (flag for author)

These issues require human judgment and cannot be auto-fixed:

| Issue | Reason | Action |
|-------|--------|--------|
| Broken external URLs | URL may have moved, need correct replacement | Flag in PR comment, author finds new URL |
| Missing images | Image file missing from migration | Flag in PR comment, author uploads image |
| Complex nested lists | Content restructuring needed | Flag, suggest simplification |
| Vim-style tutorials | Heavy markdown formatting requires rewrite | Manual content refactoring |
| Deprecated sandbox URLs | Need to identify replacement sandbox | Author determines if still relevant |

### Example Broken URLs Found in Migration

| URL Pattern | Count | Issue |
|-------------|-------|-------|
| `developer.cisco.com/automation-bootcamp/` | 7+ | Page removed |
| `devnetsandbox.cisco.com/RM/Diagram/...` | 3+ | Old sandbox diagram URLs |
| `content.cisco.com/chapter.sjs?...` | 2+ | Cisco docs restructured |

---

## Sidecar Auto-Fix Tool

A new tool was created to automatically fix sidecar.json issues:

**Location:** `tools/fix_sidecar.py`

**Usage:**
```bash
# Preview changes (dry run)
python tools/fix_sidecar.py tc-example --dry-run

# Apply fixes
python tools/fix_sidecar.py tc-example
```

**Fixes automatically:**
- Duration mismatch: Updates total duration to match sum of step durations

---

## CI UX Improvement Needed

**Issue:** When CI fails due to broken URLs, the error is only visible in the action logs. Authors need to click through multiple pages to find the actual issue.

**Current flow:**
1. PR shows CI failure
2. Click on failed check → GitHub Actions page
3. Click on job → Job log
4. Scroll/search for "Broken URL:" or "Broken Image:"

**Proposed improvement (Future Work):**
- Surface specific errors directly in PR comments
- Format like:
  ```
  ❌ Broken Link Detected

  **File:** step-8.md
  **URL:** https://developer.cisco.com/automation-bootcamp/

  Please replace with a working URL or remove the link.
  ```

---

## Files Modified

- `.github/workflows/tutorial-linting.yml` - YAML syntax fix and auto-commit feature
- `tools/clean_markdown.py` - Bold list item conversion, blank lines in lists fix, local file links in lists extraction, and actual file modification
- `tools/fix_sidecar.py` - NEW: Auto-fix duration mismatches in sidecar.json
- `.github/workflows/integration-tests.yml` - Added integration tests for XML conversion pipeline
