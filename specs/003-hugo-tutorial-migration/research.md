# Research: Hugo Tutorial Migration

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19
**Input**: Phase 0 research findings from plan.md

## R1: Hugo Shortcode Parsing

**Decision**: Regex-based extraction for `{{<step>}}` shortcodes

**Rationale**:
- Hugo shortcodes follow predictable patterns
- No need for full Hugo parser dependency
- Matches approach used in `clean_markdown.py`

**Pattern**:
```python
STEP_PATTERN = re.compile(
    r'\{\{<step\s+label="([^"]+)"\s+duration="([^"]+)"(?:\s+xy-guid="([^"]+)")?\s*>\}\}'
    r'(.*?)'
    r'\{\{</step\s*>\}\}',
    re.DOTALL
)
```

**Alternative Rejected**: Full Hugo parser library - adds dependency for no benefit

**Edge Cases Identified**:
- Inconsistent spacing in shortcode attributes
- Optional `xy-guid` attribute (present in 108/110 tutorials)
- Inconsistent closing tag spacing (`{{</step>}}` vs `{{</step >}}`)

---

## R2: YAML Frontmatter Parsing

**Decision**: Use PyYAML library

**Rationale**:
- Already used in other Python projects
- Handles all YAML edge cases (multiline, arrays, nulls)
- Standard library `yaml` module not available

**Alternative Rejected**: Regex parsing - too fragile for complex YAML

**Sample Frontmatter Structure**:
```yaml
---
title: "Tutorial Title"
description: "Description text"
date: 2022-10-17
categories: [ Coding, Automation ]
tags: [ Python, pyATS, Automation ]
duration: 60:00
authors: John Doe
draft: false
ia-guid: 88385837-dd43-475d-b2d2-9d736f039599
lesson-guid: 7742a0d1-44c3-41ea-9416-ce7104f8f499
keywords: python; pyATS; Automation
certifications: null
technologies: null
skilllevels: null
---
```

---

## R3: Duration Format Conversion

**Decision**: Convert Hugo `MM:SS` to sidecar `XmXXs` format

**Rationale**: Required by sidecar.json schema

**Conversion Logic**:
```python
def convert_duration(hugo_duration: str) -> str:
    """Convert '60:00' to '1h00m00s' or '5:00' to '5m00s'"""
    parts = hugo_duration.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1]) if len(parts) > 1 else 0

    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h{minutes:02d}m{seconds:02d}s"
    return f"{minutes}m{seconds:02d}s"
```

**Step Duration**: Kept in original `MM:SS` format per sidecar schema

---

## R4: Category to Technology Mapping

**Decision**: Best-effort mapping with documentation in PR

| Hugo Category | Sidecar Technology |
|---------------|-------------------|
| Networking | Networking |
| Security | Security |
| Cloud | Cloud and Computing |
| Data Center | Data Center |
| Automation | Software |
| Coding | Software |
| Collaboration | Collaboration |
| Certification | (skip - not a technology) |
| Other/Unknown | Other |

**Rationale**:
- Sidecar schema has fixed technology values
- Best match based on content domain
- Document mapping decision in PR for editorial review

---

## R5: Skill Level Mapping

**Decision**: Map explicit values, default to "Intermediate"

| Hugo Value | Sidecar Value |
|------------|---------------|
| Beginner | Beginner |
| Intermediate | Intermediate |
| Advanced | Advanced |
| Expert | Expert |
| null/missing | Intermediate |

**Rationale**: Most Hugo tutorials don't have skill levels set; Intermediate is safest default for technical content

---

## R6: GUID Preservation

**Decision**: Preserve existing GUIDs from Hugo frontmatter

**Fields to Preserve**:
- `ia-guid` → `ia-guid`
- `lesson-guid` → `lesson-guid`
- `xy-guid` (per step) → `xy-guid` in files array

**Rationale**: 108/110 tutorials already have GUIDs; reusing prevents duplicate content issues in Cisco U. platform

---

## R7: Image Path Handling

**Decision**: Copy images/ folder as-is, update relative paths if needed

**Hugo Format**: `./images/screenshot.png` or `images/screenshot.png`
**Target Format**: `./images/screenshot.png`

**Implementation**:
1. Copy entire `images/` folder to target
2. Scan step content for image references
3. Normalize paths to `./images/` prefix if not present

---

## R8: Author Format Normalization

**Decision**: Convert string to single-element array with object

**Hugo Format**: `authors: John Doe` (string)
**Sidecar Format**: `"authors": [{"name": "John Doe"}]` (array of objects)

**Edge Cases**:
- Multiple authors in Hugo (rare): Take first only per sidecar schema constraint
- Missing author: Flag in PR for editorial review

---

## R9: Tutorial ID Generation

**Decision**: Derive from folder name with `tc-` prefix

**Examples**:
- `ansible-ios` → `tc-ansible-ios`
- `vim-introduction` → `tc-vim-introduction`
- `python-pyenv` → `tc-python-pyenv`

**Validation**: Must match regex `^tc-[a-z0-9-]+$`

---

## R10: Hugo Tags Handling

**Decision**: Discard Hugo tags

**Rationale**:
- Hugo `tags` field contains free-form keywords (e.g., `[ Python, pyATS, Automation ]`)
- Sidecar.json has no `tags` field - uses `technologies` (fixed list) and `skill-levels`
- Hugo tags are not equivalent to sidecar technologies
- Discarding is cleaner than attempting to map arbitrary keywords

---

## R11: Congratulations Step Standardization

**Decision**: Replace/augment final step with standard boilerplate

**Rationale**:
- Original Hugo tutorials had inconsistent Congratulations pages
- Standard boilerplate improves user journey to Cisco U. resources
- Preserving custom links maintains tutorial-specific value

**Implementation**:
1. Extract any custom links from original Congratulations step
2. Generate standard boilerplate with tutorial-id UTM parameters
3. Insert custom links in "Related Content" section if present
4. Append standard boilerplate

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| What about outdated content? | All content 2+ years old; no special banner needed |
| How to handle open PRs? | Incorporate updates during migration review |
| Migration order? | By author, highest volume first |
| Skip criteria? | 9 tutorials identified as meta/obsolete/superseded |
| Hugo tags? | Discarded - not equivalent to sidecar technologies |
| PR #198? | ai-python-client - already in skip list (superseded) |
| PR #201? | ccna-top-commands - incorporate during that tutorial's migration |
