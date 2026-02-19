# PR Template Contract: Hugo Migration

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19

## PR Title Format

```
Migrate: tc-{tutorial-name} from Hugo
```

Examples:
- `Migrate: tc-ansible-ios from Hugo`
- `Migrate: tc-vim-introduction from Hugo`
- `Migrate: tc-python-pyenv from Hugo`

---

## PR Description Template

```markdown
## Migration: {original-name} → tc-{tutorial-name}

**Source:** cisco-learning-codelabs/site/content/posts/{original-name}/
**Original Date:** {YYYY-MM-DD}
**Author:** {author-name}

### Schema Mapping

| Field | Hugo Value | Sidecar Value | Notes |
|-------|------------|---------------|-------|
| title | "{title}" | "{title}" | Direct copy |
| id | (none) | "tc-{name}" | Generated from folder |
| description | "{description}" | "{description}" | Direct copy |
| date | {date} | "{date}" | Format preserved |
| duration | {MM:SS} | "{Xm00s}" | Format converted |
| ia-guid | {guid} | "{guid}" | Preserved |
| lesson-guid | {guid} | "{guid}" | Preserved |
| authors | {author} | [{"name": "{author}"}] | Array format |
| technologies | [{categories}] | ["{technology}"] | Mapped (see below) |
| skill-levels | {level/null} | ["{level}"] | Default if null |
| certifications | null | [] | No change |
| active | (none) | true | Default |

### Technology Mapping Applied

| Hugo Category | → | Sidecar Technology |
|---------------|---|-------------------|
| {category1} | → | {technology1} |
| {category2} | → | {technology2} |

### Migration Changes

1. Split `index.md` into {N} step files
2. Converted duration from `{MM:SS}` to `{XmXXs}` format
3. {Additional change if any}
4. {Additional change if any}

### Step Files Generated

| File | Label | Duration |
|------|-------|----------|
| step-1.md | Overview | {M:SS} |
| step-2.md | {label} | {M:SS} |
| ... | ... | ... |
| step-{N}.md | Congratulations | {M:SS} |

### Content Review Notes

- [ ] Technical accuracy verified
- [ ] Links checked and working
- [ ] Images display correctly
- [ ] No outdated references

**Issues Found:**
- {Any issues identified during migration}
- {Suggestions for improvement}
- {Links that may need updating}

### Original Content

<details>
<summary>Click to expand original index.md (without frontmatter)</summary>

```markdown
{original-content}
```

</details>

---

🤖 Generated with [Hugo Migration Tool](../tools/migrate_hugo_tutorial.py)
```

---

## Example PR Description

```markdown
## Migration: ansible-ios → tc-ansible-ios

**Source:** cisco-learning-codelabs/site/content/posts/ansible-ios/
**Original Date:** 2022-06-15
**Author:** Jason Belk

### Schema Mapping

| Field | Hugo Value | Sidecar Value | Notes |
|-------|------------|---------------|-------|
| title | "Ansible IOS Configuration" | "Ansible IOS Configuration" | Direct copy |
| id | (none) | "tc-ansible-ios" | Generated from folder |
| description | "Learn to configure IOS devices with Ansible" | "Learn to configure IOS devices with Ansible" | Direct copy |
| date | 2022-06-15 | "2022-06-15" | Format preserved |
| duration | 30:00 | "30m00s" | Format converted |
| ia-guid | 88385837-dd43-475d-b2d2-9d736f039599 | "88385837-dd43-475d-b2d2-9d736f039599" | Preserved |
| lesson-guid | 7742a0d1-44c3-41ea-9416-ce7104f8f499 | "7742a0d1-44c3-41ea-9416-ce7104f8f499" | Preserved |
| authors | Jason Belk | [{"name": "Jason Belk"}] | Array format |
| technologies | [Coding, Automation] | ["Software"] | Mapped (see below) |
| skill-levels | null | ["Intermediate"] | Default applied |
| certifications | null | [] | No change |
| active | (none) | true | Default |

### Technology Mapping Applied

| Hugo Category | → | Sidecar Technology |
|---------------|---|-------------------|
| Coding | → | Software |
| Automation | → | Software |

### Migration Changes

1. Split `index.md` into 5 step files
2. Converted duration from `30:00` to `30m00s` format
3. Created empty `assets/` directory with `.gitkeep`
4. Normalized image paths to `./images/` prefix

### Step Files Generated

| File | Label | Duration |
|------|-------|----------|
| step-1.md | Overview | 1:00 |
| step-2.md | Prerequisites | 3:00 |
| step-3.md | Configure Ansible Inventory | 10:00 |
| step-4.md | Create Playbook | 10:00 |
| step-5.md | Congratulations | 1:00 |

### Content Review Notes

- [ ] Technical accuracy verified
- [ ] Links checked and working
- [ ] Images display correctly
- [ ] No outdated references

**Issues Found:**
- External link to Ansible docs may need version update
- Screenshot shows older Ansible version (2.9)

### Original Content

<details>
<summary>Click to expand original index.md (without frontmatter)</summary>

```markdown
{{<step label="Overview" duration="1:00" xy-guid="f50c3be7-02e2-4bea-9783-52c07c82455b">}}

### What You'll Learn

In this tutorial, you will learn how to:

- Install and configure Ansible for network automation
- Create an inventory file for IOS devices
- Write a basic playbook to configure interfaces

{{</step >}}

{{<step label="Prerequisites" duration="3:00" xy-guid="a1b2c3d4-...">}}
...
{{</step>}}
```

</details>

---

🤖 Generated with [Hugo Migration Tool](../tools/migrate_hugo_tutorial.py)
```

---

## PR Labels

Apply these labels to migration PRs:

| Label | Description |
|-------|-------------|
| `migration` | Hugo to sidecar migration |
| `author:{name}` | Author of original tutorial |
| `needs-review` | Requires editorial review |
| `auto-generated` | PR description auto-generated |

---

## PR Checklist (for Reviewers)

```markdown
### Reviewer Checklist

- [ ] Schema mapping is correct
- [ ] All steps extracted properly
- [ ] Images copied and display correctly
- [ ] No content was lost during migration
- [ ] Duration sum matches total
- [ ] Technology mapping is appropriate
- [ ] Tutorial passes CI validation
```
