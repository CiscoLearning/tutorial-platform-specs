# CLI Interface Contract: migrate_hugo_tutorial.py

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19

## Command Overview

```bash
python tools/migrate_hugo_tutorial.py [OPTIONS]
```

## Arguments

### Required Arguments (one of)

| Argument | Type | Description |
|----------|------|-------------|
| `--source` | PATH | Path to single Hugo tutorial folder |
| `--source-dir` | PATH | Path to Hugo posts directory for batch mode |

### Optional Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--output` | PATH | Auto-generated | Output folder path (single mode) |
| `--output-dir` | PATH | Current dir | Output directory (batch mode) |
| `--author` | STRING | None | Filter batch by author name |
| `--dry-run` | FLAG | False | Preview changes without writing files |
| `--pr-description` | FLAG | False | Generate PR description file |
| `--pr-only` | FLAG | False | Only generate PR description (no migration) |
| `--skip-validation` | FLAG | False | Skip schema validation |
| `--verbose` | FLAG | False | Enable verbose logging |

---

## Usage Patterns

### Single Tutorial Migration

```bash
# Basic migration
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --output ../ciscou-tutorial-content/tc-ansible-ios

# With PR description
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --output ../ciscou-tutorial-content/tc-ansible-ios \
    --pr-description

# Dry run preview
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --dry-run --verbose
```

### Batch Migration

```bash
# Migrate all tutorials by author
python tools/migrate_hugo_tutorial.py \
    --source-dir ../cisco-learning-codelabs/site/content/posts \
    --output-dir ../ciscou-tutorial-content \
    --author "Jason Belk"

# Dry run all tutorials
python tools/migrate_hugo_tutorial.py \
    --source-dir ../cisco-learning-codelabs/site/content/posts \
    --output-dir ../ciscou-tutorial-content \
    --dry-run
```

### PR Description Only

```bash
# Generate PR description without migration
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --pr-only
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Parse error (invalid Hugo format) |
| 2 | Conversion error (mapping failed) |
| 3 | Validation error (schema mismatch) |
| 4 | File system error (read/write failed) |
| 5 | Invalid arguments |

---

## Output Structure

### Single Migration Output

```
tc-ansible-ios/
├── sidecar.json          # Generated metadata
├── step-1.md             # Overview step
├── step-2.md             # Content steps
├── ...
├── step-N.md             # Congratulations step
├── images/               # Copied from source (or .gitkeep)
├── assets/               # Empty with .gitkeep
└── PR_DESCRIPTION.md     # If --pr-description flag used
```

### Console Output (Normal)

```
Migrating: ansible-ios → tc-ansible-ios
  ✓ Parsed frontmatter (12 fields)
  ✓ Extracted 5 steps
  ✓ Generated sidecar.json
  ✓ Created step files
  ✓ Copied images/ (3 files)
  ✓ Created assets/ directory
  ✓ Schema validation passed

Migration complete: /path/to/tc-ansible-ios
```

### Console Output (Dry Run)

```
[DRY RUN] Would migrate: ansible-ios → tc-ansible-ios

Schema Mapping:
  title: "Ansible IOS Configuration" (unchanged)
  technologies: [Coding, Automation] → [Software]
  skill-levels: null → [Intermediate]
  duration: 30:00 → 30m00s

Changes:
  1. Split index.md into 5 step files
  2. Convert duration format
  3. Map categories to technologies
  4. Apply default skill level

Warnings:
  - No images found in source

No files written (dry run mode)
```

### Console Output (Verbose)

```
[DEBUG] Reading: ../cisco-learning-codelabs/site/content/posts/ansible-ios/index.md
[DEBUG] Frontmatter fields: title, description, date, duration, authors, ...
[DEBUG] Step 1: "Overview" (1:00)
[DEBUG] Step 2: "Prerequisites" (2:00)
...
[DEBUG] Writing: /path/to/tc-ansible-ios/sidecar.json
[DEBUG] Writing: /path/to/tc-ansible-ios/step-1.md
...
```

---

## Error Messages

### Parse Errors

```
ERROR: Failed to parse frontmatter in index.md
  File: ../posts/ansible-ios/index.md
  Line: 5
  Details: Invalid YAML syntax - unexpected key

ERROR: No {{<step>}} shortcodes found
  File: ../posts/ansible-ios/index.md
  Details: Expected at least one step block
```

### Conversion Errors

```
ERROR: Invalid duration format
  Field: duration
  Value: "thirty minutes"
  Expected: "MM:SS" format (e.g., "30:00")

ERROR: Unknown category mapping
  Field: categories
  Value: ["Quantum Computing"]
  Details: No mapping defined for "Quantum Computing"
```

### Validation Errors

```
ERROR: Schema validation failed
  Field: id
  Value: "Ansible-IOS"
  Expected: lowercase alphanumeric with hyphens only

ERROR: Duration mismatch
  Top-level: 30m00s
  Sum of steps: 25m00s
  Details: Step durations must sum to total duration
```

---

## JSON Output Mode

For programmatic use, add `--json` flag:

```bash
python tools/migrate_hugo_tutorial.py \
    --source ../posts/ansible-ios \
    --output ../tc-ansible-ios \
    --json
```

Output:
```json
{
  "success": true,
  "source": "../posts/ansible-ios",
  "target": "../tc-ansible-ios",
  "tutorial_id": "tc-ansible-ios",
  "changes": [
    {"field": "technologies", "from": ["Coding"], "to": ["Software"]},
    {"field": "skill-levels", "from": null, "to": ["Intermediate"]}
  ],
  "warnings": [],
  "files_created": [
    "sidecar.json",
    "step-1.md",
    "step-2.md",
    "step-3.md",
    "images/.gitkeep",
    "assets/.gitkeep"
  ]
}
```
