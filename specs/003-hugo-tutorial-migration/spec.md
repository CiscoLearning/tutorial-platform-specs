# Feature Specification: Hugo Tutorial Migration

**Feature Branch:** `003-hugo-tutorial-migration`
**Created:** 2026-02-19
**Status:** Draft
**Input:** FF-5 from requirements.md

## Problem Statement

110 tutorials exist in the legacy `cisco-learning-codelabs` repository using Hugo/Codelabs format (created 2022-2024). These tutorials are not accessible through the current Cisco U. platform workflow and represent orphaned content that should be migrated or archived.

## Scope

### In Scope
- Migration of ~96 tutorials from Hugo format to current format
- Automated conversion tooling
- Content review during migration
- Schema mapping with documentation

### Out of Scope
- Content rewriting (only formatting changes)
- New tutorial creation
- Changes to the current CI/CD pipeline

## Inventory

### Totals

| Category | Count |
|----------|-------|
| Total in Hugo repo | 110 |
| Already migrated | 3 |
| Skip (obsolete/meta) | 9 |
| **To migrate** | **~98** |

### Skip List (9 tutorials)

| Tutorial | Reason |
|----------|--------|
| write-a-codelab | Meta tutorial about Hugo system |
| tutorial-tutorial | Meta tutorial about Hugo system |
| bombal-packtrac-config-register | Outdated external content |
| bombal-packtrac-portfast | Outdated external content |
| ciscou-101-community | Platform-specific, not tutorial content |
| ciscou-101-dashboard | Platform-specific, not tutorial content |
| ciscou-101-lp | Platform-specific, not tutorial content |
| ai-langchain-pyats | Superseded by tc-gpt-pyats-8 |
| ai-python-client | Superseded by tc-langchain-simple-chat-agent-openai |

### Already Migrated (3 tutorials)
- tc-multicloud-defense-spotlight-2024
- tc-ospf-tshoot-1
- tc-spotlight-terraformer

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| MIG-001 | Convert Hugo `{{<step>}}` shortcodes to separate `step-N.md` files | P1 |
| MIG-002 | Generate `sidecar.json` from Hugo YAML frontmatter | P1 |
| MIG-003 | Add `tc-` prefix to all tutorial folder names | P1 |
| MIG-004 | Create `images/` directory (copy existing or create empty) | P1 |
| MIG-005 | Create `assets/` directory (copy existing or create empty) | P1 |
| MIG-006 | Preserve original `date` from Hugo frontmatter | P1 |
| MIG-007 | Preserve existing GUIDs (ia-guid, lesson-guid, xy-guid) | P1 |
| MIG-008 | Map Hugo categories/tags to sidecar technologies/skill-levels | P2 |
| MIG-009 | Generate 1 PR per tutorial | P1 |
| MIG-010 | PR description includes original text and migration changes | P1 |
| MIG-011 | PR description includes schema mapping rationale | P1 |
| MIG-012 | Review each tutorial for improvements during migration | P2 |

### Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-001 | Migration script completes in <30 seconds per tutorial |
| NFR-002 | All migrated tutorials pass current CI validation |
| NFR-003 | No manual steps required for basic migration |

---

## Technical Approach

### Source Format (Hugo)

```
posts/tutorial-name/
├── index.md      # Single file with YAML frontmatter + {{<step>}} shortcodes
└── images/       # Local images (optional)
```

**Hugo index.md structure:**
```markdown
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

{{<step label="Overview" duration="1:00" xy-guid="f50c3be7-02e2-4bea-9783-52c07c82455b">}}

### What You'll Learn
- Item 1
- Item 2

{{</step >}}

{{<step label="Step Title" duration="5:00" xy-guid="c803749f-6ec1-4974-aaf2-7e1aa4ff7dab">}}

Content here...

{{</step>}}
```

### Target Format (Current)

```
tc-tutorial-name/
├── sidecar.json
├── step-1.md     # "Overview"
├── step-2.md     # "Step Title"
├── ...
├── step-N.md     # "Congratulations"
├── images/       # Required (can be empty with .gitkeep)
└── assets/       # Required (can be empty with .gitkeep)
```

### Migration Script

**Input:** Path to Hugo tutorial folder
**Output:** New folder in target format

```python
def migrate_tutorial(hugo_path: str, output_path: str) -> MigrationResult:
    """
    1. Parse index.md frontmatter (YAML)
    2. Extract {{<step>}} blocks with regex
    3. Generate sidecar.json from frontmatter
    4. Write step-N.md files from step blocks
    5. Copy images/ folder (or create empty with .gitkeep)
    6. Create assets/ folder with .gitkeep
    7. Validate against schema
    8. Return migration report
    """
```

### Schema Mapping

| Hugo Field | Sidecar Field | Mapping Logic |
|------------|---------------|---------------|
| title | title | Direct copy |
| description | description | Direct copy |
| date | date | Format as YYYY-MM-DD |
| duration | duration | Convert MM:SS to XmXXs format |
| authors | authors[0] | Single author (first if multiple) |
| ia-guid | ia-guid | Direct copy |
| lesson-guid | lesson-guid | Direct copy |
| categories | technologies | Best-effort mapping (see table below) |
| tags | keywords (in description) | Append to description |
| skilllevels | skill-levels | Map or default to "Intermediate" |

**Category to Technology Mapping:**

| Hugo Category | Sidecar Technology |
|---------------|-------------------|
| Networking | Networking |
| Security | Security |
| Cloud | Cloud and Computing |
| Data Center | Data Center |
| Automation | Software |
| Coding | Software |
| Collaboration | Collaboration |
| Certification | (ignore - not a technology) |
| Other/Unknown | Other |

**Step Extraction:**

| Hugo Step | Sidecar Step |
|-----------|--------------|
| First step (usually "Overview") | step-1.md with label "Overview" |
| Middle steps | step-2.md through step-(N-1).md |
| Last step | step-N.md (add "Congratulations" if not present) |

---

## PR Format

Each migration PR should include:

### Title
```
Migrate: tc-{tutorial-name} from Hugo
```

### Description Template
```markdown
## Migration: {original-name} → tc-{tutorial-name}

**Source:** cisco-learning-codelabs/site/content/posts/{original-name}/
**Original Date:** {date}
**Author:** {author}

### Schema Mapping

| Field | Hugo Value | Sidecar Value | Notes |
|-------|------------|---------------|-------|
| title | "..." | "..." | Direct copy |
| technologies | [Coding, Automation] | ["Software"] | Mapped Coding→Software |
| skill-levels | null | ["Intermediate"] | Default applied |
| ... | ... | ... | ... |

### Migration Changes

1. Split index.md into {N} step files
2. Converted duration from MM:SS to XmXXs format
3. Created empty assets/ directory
4. {any other changes}

### Content Review Notes

- {Any issues found}
- {Suggestions for improvement}
- {Links that may need updating}

### Original Content

<details>
<summary>Click to expand original index.md (without frontmatter)</summary>

{original markdown content}

</details>
```

---

## Implementation Plan

### Phase 1: Tooling (1-2 days)
1. Create `migrate_hugo_tutorial.py` script
2. Implement frontmatter parsing
3. Implement step extraction
4. Implement sidecar.json generation
5. Add validation against schema
6. Create PR description generator

### Phase 2: Test Migration (1 day)
1. Run on 5 sample tutorials
2. Verify CI passes
3. Iterate on edge cases
4. Document any manual fixes needed

### Phase 3: Batch Migration (~98 PRs)
1. Run migration script on each tutorial
2. Review each PR for improvements
3. Submit PRs in batches of 5-10 per day
4. Editors review and merge

### Phase 4: Cleanup
1. Update FF-5 status in requirements.md
2. Archive cisco-learning-codelabs repo
3. Document any tutorials that couldn't be migrated

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Tutorials migrated | ~98 |
| CI pass rate | 100% |
| PRs requiring manual fixes | <10% |
| Migration time per tutorial | <5 minutes |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Some Hugo shortcodes not handled | Document edge cases, fix manually |
| Images with broken paths | Validate during migration, fix in PR |
| Outdated content | Flag in PR review notes |
| Duplicate content with main repo | Cross-check during review |

---

## Open Questions

1. Should we batch PRs by author for easier review assignment?
2. What's the preferred order - alphabetical, by date, by author?
3. Should outdated tutorials get a banner/note added?
