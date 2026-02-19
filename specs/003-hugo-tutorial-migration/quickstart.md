# Quickstart: Hugo Tutorial Migration Tool

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19

## Prerequisites

- Python 3.10+
- PyYAML library (`pip install pyyaml`)
- Access to both repositories:
  - `cisco-learning-codelabs` (source)
  - `ciscou-tutorial-content` (target)

## Installation

```bash
# Clone tutorial-testing repo (contains tools)
git clone <tutorial-testing-repo>
cd tutorial-testing

# Install dependencies
pip install pyyaml pytest
```

## Quick Start

### 1. Migrate a Single Tutorial

```bash
# Basic migration
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --output ../ciscou-tutorial-content/tc-ansible-ios

# Preview changes first (recommended)
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --dry-run
```

### 2. Verify the Migration

```bash
# Check output structure
ls -la ../ciscou-tutorial-content/tc-ansible-ios/

# Validate against schema
python tools/schema_validation.py ../ciscou-tutorial-content/tc-ansible-ios

# Run full validation suite
python -m pytest tests/ -k "tc-ansible-ios"
```

### 3. Create PR with Description

```bash
# Generate PR description
python tools/migrate_hugo_tutorial.py \
    --source ../cisco-learning-codelabs/site/content/posts/ansible-ios \
    --output ../ciscou-tutorial-content/tc-ansible-ios \
    --pr-description

# The PR_DESCRIPTION.md file will be in the output folder
cat ../ciscou-tutorial-content/tc-ansible-ios/PR_DESCRIPTION.md
```

## Batch Migration Workflow

### By Author (Recommended)

```bash
# Step 1: Preview all tutorials by author
python tools/migrate_hugo_tutorial.py \
    --source-dir ../cisco-learning-codelabs/site/content/posts \
    --author "Jason Belk" \
    --dry-run

# Step 2: Migrate all (creates folders in current directory)
python tools/migrate_hugo_tutorial.py \
    --source-dir ../cisco-learning-codelabs/site/content/posts \
    --output-dir ../ciscou-tutorial-content \
    --author "Jason Belk"

# Step 3: Create PRs (one per tutorial)
for dir in ../ciscou-tutorial-content/tc-*/; do
    cd "$dir"
    git checkout -b "migrate-$(basename $dir)"
    git add .
    git commit -m "Migrate: $(basename $dir) from Hugo"
    gh pr create --title "Migrate: $(basename $dir) from Hugo" \
                 --body-file PR_DESCRIPTION.md
    cd -
done
```

## Common Scenarios

### Scenario 1: Tutorial with Images

```bash
# Migration automatically copies images/ folder
python tools/migrate_hugo_tutorial.py \
    --source ../posts/vim-introduction \
    --output ../tc-vim-introduction

# Verify images copied
ls ../tc-vim-introduction/images/
```

### Scenario 2: Tutorial Missing Skill Level

```bash
# Will default to "Intermediate"
python tools/migrate_hugo_tutorial.py \
    --source ../posts/python-pyenv \
    --dry-run

# Output shows:
#   skill-levels: null → [Intermediate]
```

### Scenario 3: Complex Category Mapping

```bash
# Preview the mapping
python tools/migrate_hugo_tutorial.py \
    --source ../posts/dnac-config-manager \
    --dry-run

# Output shows:
#   technologies: [Networking, Automation] → [Networking, Software]
```

### Scenario 4: Check Specific Tutorial in Hugo Repo

```bash
# List available tutorials
ls ../cisco-learning-codelabs/site/content/posts/

# Check if tutorial is in skip list
# Skip list: write-a-codelab, tutorial-tutorial, bombal-*, ciscou-101-*, ai-langchain-pyats, ai-python-client
```

## Troubleshooting

### "No steps found" Error

The Hugo tutorial may use non-standard shortcode format:

```bash
# Check the shortcode format
grep -n "{{<step" ../posts/problematic-tutorial/index.md
```

Expected format:
```
{{<step label="Overview" duration="1:00" xy-guid="...">}}
```

### Duration Mismatch

```bash
# Check step durations sum to total
python -c "
import yaml
with open('../posts/tutorial/index.md') as f:
    content = f.read()
    # Parse and sum durations
"
```

### Missing GUID

Only 2 tutorials lack GUIDs. The tool will generate new ones:

```bash
# Preview GUID generation
python tools/migrate_hugo_tutorial.py \
    --source ../posts/tutorial-without-guid \
    --dry-run --verbose
```

## Migration Checklist

For each tutorial migration:

- [ ] Run `--dry-run` to preview changes
- [ ] Check technology mapping is appropriate
- [ ] Verify skill level assignment
- [ ] Run migration with `--pr-description`
- [ ] Validate with `schema_validation.py`
- [ ] Run pytest validation
- [ ] Review PR_DESCRIPTION.md
- [ ] Create PR with appropriate labels
- [ ] Request editorial review

## Author Priority Order

Migrate tutorials in this order (by author volume):

1. Jason Belk (24 tutorials)
2. Quinn Snyder (13 tutorials)
3. Rafael Leiva-Ochoa (9 tutorials)
4. Alec Chamberlain (8 tutorials)
5. Robert Whitaker (6 tutorials)
6. Kareem Iskander (6 tutorials)
7. Tony Roman (5 tutorials)
8. Barry Weiss (4 tutorials)
9. Remaining authors (1-3 tutorials each)

## Skip List

Do not migrate these tutorials:

| Tutorial | Reason |
|----------|--------|
| write-a-codelab | Meta tutorial about Hugo system |
| tutorial-tutorial | Meta tutorial about Hugo system |
| bombal-packtrac-config-register | Outdated external content |
| bombal-packtrac-portfast | Outdated external content |
| ciscou-101-community | Platform-specific |
| ciscou-101-dashboard | Platform-specific |
| ciscou-101-lp | Platform-specific |
| ai-langchain-pyats | Superseded by tc-gpt-pyats-8 |
| ai-python-client | Superseded by tc-langchain-simple-chat-agent-openai |
