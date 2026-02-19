# Migration Learnings

**Document Created:** 2026-02-19
**Status:** Active - Updated during migration process

This document captures learnings from the Hugo tutorial migration process to inform future migrations and CI improvements.

---

## Summary

Migrating Quinn Snyder's 11 tutorials revealed systematic content quality issues in the original Hugo content that CI validation catches. These issues require either programmatic fixes or manual editorial attention.

**Results:** 9/11 PRs passing, 2/11 requiring manual review (complex Solomon XML edge cases)

---

## Content Quality Issues

### 1. Duration Mismatches (High Frequency)

**Problem:** Original Hugo tutorials have total duration that doesn't match sum of step durations.

**Examples:**
- tc-calisti-sdm-intro: `1h00m00s` total but steps sum to `1h01m00s`
- tc-panoptica-introduction: `50m00s` total but steps sum to `1h13m00s`
- tc-terraform-introduction: `25m00s` total but steps sum to `27m00s`

**Fix:** Recalculate total duration from step durations in sidecar.json:
```python
def fix_duration(sidecar):
    total_seconds = sum(parse_step_duration(f["duration"]) for f in sidecar["files"])
    sidecar["duration"] = format_total_duration(total_seconds)
```

**Prevention:** Migration tool should auto-recalculate totals during conversion.

---

### 2. Invalid Certifications (Medium Frequency)

**Problem:** Hugo tutorials have certification values not in the approved list.

**Invalid Values Found:**
- `ENCC` (not a valid certification)
- `ENNA` (not a valid certification)
- `SCAZT` (not a valid certification)

**Valid Certifications:**
- CCNA, CCNP (various), CCIE (various)
- Cisco Certified DevNet Associate/Professional/Expert
- Cisco Certified Cybersecurity Associate/Professional
- Cisco Certified Design Expert

**Fix:** Set `certifications: null` when original value is invalid.

**Prevention:** Add certification validation to migration tool.

---

### 3. Broken URLs (Medium Frequency)

**Problem:** Original Hugo tutorials contain links to sites that no longer exist.

**Broken URLs Found:**
| URL | Status | Replacement |
|-----|--------|-------------|
| https://www.calisti.app | Dead (service discontinued) | Remove link, keep text |
| https://cloud.calisti.app/download | Dead | Remove link |
| https://developer.cisco.com/automation-bootcamp/ | 404 | https://developer.cisco.com/learning/ |
| https://sandboxapicdc.cisco.com | 404 | https://devnetsandbox.cisco.com/RM/Topology |
| https://td4a.codethenetwork.com/ | Dead | Remove link |
| https://nornir.tech/nornir/plugins/ | Dead | https://nornir.readthedocs.io/ |

**Fix:** CI's pytest_validation.py `test_broken_links` catches these. Requires manual or scripted URL replacement.

**Prevention:**
1. CI already validates URLs
2. Migration tool could pre-check URLs and flag in PR description

---

### 4. Broken Image References (Low Frequency)

**Problem:** Image filenames in markdown don't match actual files in images/ folder.

**Examples:**
- tc-panoptica-introduction: `sock-shop-deployment.gif` → `sock-shop-deploy.gif` (typo)
- tc-enna-cat-center: `step-28-bste.png` → `step-28-b.png` (typo)

**Fix:** Manual correction or fuzzy matching to find close image names.

**Prevention:** Migration tool should validate image references exist.

---

## Solomon XML Conversion Issues

### 5. Malformed Image Tags (High Frequency)

**Problem:** Hugo content has space between `!` and `[` in image markdown.

**Wrong:** `! [image alt](./images/file.png)`
**Correct:** `![image alt](./images/file.png)`

**Impact:** XML converter can't parse malformed image syntax.

**Fix:** Simple regex: `s/! \[/![/g`

**Status:** `clean_markdown.py` does NOT currently check for this pattern.

**Action Item:** Add rule to `clean_markdown.py` for malformed image tags.

---

### 6. Nested List Structures (Medium Frequency)

**Problem:** 3-level nested lists don't convert properly to Solomon XML.

**Example:**
```markdown
- Access to a Linux workstation
  - Docker option
    - Details about Docker images  ← 3rd level causes XML errors
```

**Impact:** XML parser error: `Opening and ending tag mismatch: ItemPara and ParaBlock`

**Fix Options:**
1. Flatten to 2-level lists
2. Restructure using headings instead of nested lists
3. Use numbered lists instead of bullets

**Example Fix:**
```markdown
- Access to a Linux workstation

Options for accessing Linux:
1. Docker - Use the provided Dockerfile
2. DevNet Sandbox - Any sandbox with DevBox
```

**Action Item:** Add nested list depth check to `clean_markdown.py`.

---

### 7. Inline Code + Links in Lists (Low Frequency)

**Problem:** List items with both inline code and links can cause XML parsing issues.

**Problematic Pattern:**
```markdown
- `set bg=dark`: Tweaks the [color palette](link) to look better
```

**Impact:** Complex inline formatting in list items generates malformed XML.

**Fix:** Simplify formatting - either remove code fences or remove links.

---

### 8. Orphan Nested Lists (Low Frequency)

**Problem:** List items with incorrect indentation (nested without parent).

**Wrong:**
```markdown
Some text

  - Item 1 (incorrectly indented)
  - Item 2
```

**Correct:**
```markdown
Some text

- Item 1
- Item 2
```

**Fix:** Remove leading whitespace from orphan list items.

**Action Item:** Add orphan list detection to `clean_markdown.py`.

---

## CI Workflow Issues

### 9. clean_markdown.py Doesn't Commit Fixes

**Problem:** CI runs `clean_markdown.py` which auto-fixes issues, but doesn't commit the fixes back to the PR. Authors must manually apply fixes or push again.

**Current Behavior:**
1. clean_markdown.py runs and fixes files
2. Changes are lost (not committed)
3. PR comments report what was fixed
4. Author must re-run locally and push

**Desired Behavior:**
1. clean_markdown.py runs and fixes files
2. Changes committed back to PR branch
3. CI re-runs with fixed content
4. Author sees fixes applied automatically

**Action Item:** Update CI workflow to commit clean_markdown fixes.

---

## Recommended CI Workflow Updates

### Update 1: Auto-commit clean_markdown fixes

Add to `tutorial-linting.yml` after the clean_markdown step:

```yaml
- name: Commit markdown cleanup fixes
  if: success()
  run: |
    git config user.name "github-actions"
    git config user.email "actions@github.com"

    git add "${{ steps.folder-check.outputs.FOLDER_NAME }}/"

    if git diff --staged --quiet; then
      echo "No markdown fixes to commit"
    else
      git commit -m "Auto-fix: Clean markdown formatting

Automated fixes applied by clean_markdown.py:
- Double space removal
- Link spacing fixes
- Other formatting corrections

Co-Authored-By: GitHub Actions <actions@github.com>"
      git push origin HEAD:${{ github.event.pull_request.head.ref }}
      echo "Committed and pushed markdown fixes"
    fi
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Update 2: Add malformed image tag check

Add to `clean_markdown.py` validation rules:

```python
MALFORMED_IMAGE_TAG = ValidationRule(
    id="T024",
    name="MALFORMED_IMAGE",
    severity=Severity.BLOCKING,
    fix_type=FixType.REGEX,
    pattern=re.compile(r'!\s+\['),
    message_template="Line {line}: Malformed image tag `! [` should be `![`",
    fix_suggestion="Remove space between ! and [",
    fix_pattern=(r'!\s+\[', '!['),
)
```

### Update 3: Add nested list depth check

Add to `clean_markdown.py`:

```python
def check_nested_list_depth(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for 3+ level nested lists that break XML conversion"""
    issues = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Check for 3-level nesting (6+ spaces or 3+ tabs before list marker)
        if re.match(r'^(\s{6,}|\t{3,})[-*+]', line):
            issues.append(ValidationIssue(
                rule_id="T025",
                rule_name="NESTED_LIST_DEPTH",
                severity=Severity.WARNING,
                file=file_path,
                line=line_num,
                message="3+ level nested list may break XML conversion",
                fix_type=FixType.MANUAL,
            ))

    return issues
```

---

## Migration Statistics

### Jason Belk Batch (24 tutorials)
- PRs Created: 24
- Passing: 23/24 (96%)
- Manual Review: 1 (tc-appd-apis - Solomon XML `unknown element` warnings)

### Quinn Snyder Batch (11 tutorials)
- PRs Created: 11
- Passing: 9/11 (82%)
- Manual Review: 2 (tc-vim-introduction, tc-intermediate-vim - nested lists/formatting)

### Common Fix Categories
| Fix Type | Jason Belk | Quinn Snyder |
|----------|------------|--------------|
| Duration recalculation | 8 | 9 |
| Invalid certification | 3 | 3 (ENCC) |
| Broken URLs | 4 | 6 |
| Malformed image tags | 0 | 17 |
| Nested list flattening | 0 | 2 |
| Link spacing (clean_markdown) | Many | Many |

---

## Next Steps

1. **Implement CI auto-commit** for clean_markdown fixes
2. **Add malformed image tag rule** to clean_markdown.py
3. **Add nested list depth warning** to clean_markdown.py
4. **Update migration tool** to pre-validate:
   - Duration totals
   - Certification values
   - URL accessibility
   - Image file existence
5. **Continue migrations** with Rafael Leiva-Ochoa batch (9 tutorials)
