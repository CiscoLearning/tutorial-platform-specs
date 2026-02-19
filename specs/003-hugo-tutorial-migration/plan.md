# Implementation Plan: Hugo Tutorial Migration

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-hugo-tutorial-migration/spec.md`

## Summary

Migrate ~98 tutorials from the legacy `cisco-learning-codelabs` Hugo/Codelabs repository to the current `ciscou-tutorial-content` format. Create automated tooling to convert Hugo `{{<step>}}` shortcodes to separate `step-N.md` files, generate `sidecar.json` from YAML frontmatter, and produce PRs with documented changes for editorial review.

## Technical Context

**Language/Version**: Python 3.10+ (matches existing tools in tutorial-testing)
**Primary Dependencies**: PyYAML, standard library (re, json, os, argparse, pathlib)
**Storage**: File-based (markdown input/output, JSON sidecar)
**Testing**: pytest (matches existing test suite)
**Target Platform**: CLI tool (macOS/Linux)
**Project Type**: Single CLI tool
**Performance Goals**: <30 seconds per tutorial migration
**Constraints**: Migrated tutorials MUST pass current CI validation (schema + markdown checks)
**Scale/Scope**: ~98 tutorials, 27 authors, ~110 total step files to generate

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Tutorial Quality First | ✅ PASS | Content preserved; review during migration identifies improvements |
| II. Structured Content Organization | ✅ PASS | Converting TO standardized format (step-N.md, sidecar.json) |
| III. Validate Early, Fail Fast | ✅ PASS | Each migrated tutorial goes through CI validation |
| IV. Editorial Consistency | ✅ PASS | Opportunity to fix issues during migration review |
| V. Transparent Pipeline Feedback | ✅ PASS | PRs document all changes and mapping decisions |

**Gate Status**: PASS - No violations, no justification needed

## Project Structure

### Documentation (this feature)

```text
specs/003-hugo-tutorial-migration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
tutorial-testing/
└── tools/
    ├── migrate_hugo_tutorial.py    # Main migration script
    ├── hugo_parser.py              # Hugo frontmatter + step extraction
    ├── sidecar_generator.py        # Generate sidecar.json from Hugo metadata
    └── pr_generator.py             # Generate PR description with changes

tests/
├── test_hugo_parser.py
├── test_sidecar_generator.py
├── test_migration_e2e.py
└── fixtures/
    └── sample_hugo_tutorial/       # Sample Hugo tutorial for testing
```

**Structure Decision**: Single CLI tool in existing `tools/` directory, following established patterns from `clean_markdown.py`. Tests in existing `tests/` directory.

## Complexity Tracking

> No violations - section not applicable.

---

## Phase 0: Research Summary

### R1: Hugo Shortcode Parsing

**Decision**: Use regex-based extraction for `{{<step>}}` shortcodes
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

### R2: YAML Frontmatter Parsing

**Decision**: Use PyYAML library
**Rationale**:
- Already used in other Python projects
- Handles all YAML edge cases (multiline, arrays, nulls)
- Standard library `yaml` module not available

**Alternative Rejected**: Regex parsing - too fragile for complex YAML

### R3: Duration Format Conversion

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

### R4: Category to Technology Mapping

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

### R5: Skill Level Mapping

**Decision**: Map explicit values, default to "Intermediate"
**Rationale**: Most Hugo tutorials don't have skill levels set; Intermediate is safest default

### R6: GUID Preservation

**Decision**: Preserve existing GUIDs from Hugo frontmatter
**Rationale**: 108/110 tutorials already have GUIDs; reusing prevents duplicate content issues

---

## Phase 1: Design

### Data Flow

```
┌─────────────────────┐
│ Hugo Tutorial       │
│ posts/name/index.md │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ hugo_parser.py      │
│ - Parse YAML        │
│ - Extract steps     │
│ - Extract metadata  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ sidecar_generator   │
│ - Map fields        │
│ - Convert formats   │
│ - Validate schema   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Output: tc-name/    │
│ - sidecar.json      │
│ - step-1.md ...     │
│ - images/           │
│ - assets/           │
└─────────────────────┘
```

### CLI Interface

```bash
# Migrate single tutorial
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --output ../ciscou-tutorial-content/tc-ansible-ios \
    --pr-description

# Batch migrate by author
python tools/migrate_hugo_tutorial.py \
    --source-dir ../cisco-learning-codelabs/site/content/posts \
    --output-dir ../ciscou-tutorial-content \
    --author "Jason Belk" \
    --dry-run

# Generate PR description only
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --pr-only
```

### Output Files

**sidecar.json** (generated):
```json
{
  "title": "...",
  "id": "tc-ansible-ios",
  "description": "...",
  "date": "2022-03-16",
  "duration": "30m00s",
  "ia-guid": "...",
  "lesson-guid": "...",
  "authors": [{"name": "Jason Belk"}],
  "skill-levels": ["Intermediate"],
  "technologies": ["Software"],
  "certifications": [],
  "active": true,
  "files": [
    {"name": "step-1.md", "label": "Overview", "duration": "1:00", "xy-guid": "..."},
    {"name": "step-2.md", "label": "...", "duration": "5:00", "xy-guid": "..."}
  ]
}
```

**step-N.md** (generated):
```markdown
[Step content extracted from {{<step>}} block]
[Image paths updated from ./images/ to ./images/]
```

**Final step (Congratulations)**: Uses standardized boilerplate with:
- Opening congratulations message
- Cisco U. account CTA with tutorial-specific UTM tracking
- Learning resources links (YouTube, Tutorials, Video Series, Podcasts, Events)
- Community and support links
- Any custom links from original preserved in "Related Content" section

---

## Artifacts Generated

| File | Purpose | Status |
|------|---------|--------|
| `research.md` | Research decisions and alternatives considered | ✅ Complete |
| `data-model.md` | Data structures for migration (HugoTutorial, SidecarJson, MigrationResult) | ✅ Complete |
| `contracts/cli-interface.md` | CLI argument specification with usage examples | ✅ Complete |
| `contracts/pr-template.md` | PR description format and reviewer checklist | ✅ Complete |
| `quickstart.md` | How to run the migration tool with common scenarios | ✅ Complete |
| `tasks.md` | Implementation tasks (63 tasks across 8 phases) | ✅ Complete |
