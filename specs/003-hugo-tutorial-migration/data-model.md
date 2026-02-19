# Data Model: Hugo Tutorial Migration

**Branch**: `003-hugo-tutorial-migration` | **Date**: 2026-02-19

## Entity Definitions

### HugoTutorial (Input)

Represents a tutorial in the legacy Hugo/Codelabs format.

```python
@dataclass
class HugoFrontmatter:
    """YAML frontmatter from Hugo index.md"""
    title: str
    description: str
    date: datetime.date
    duration: str                    # Format: "MM:SS" or "H:MM:SS"
    authors: str                     # Single author name
    draft: bool
    ia_guid: Optional[str]           # UUID
    lesson_guid: Optional[str]       # UUID
    categories: List[str]            # e.g., ["Coding", "Automation"]
    tags: List[str]                  # e.g., ["Python", "pyATS"]
    keywords: Optional[str]          # Semicolon-separated
    certifications: Optional[str]    # Usually null
    technologies: Optional[str]      # Usually null
    skilllevels: Optional[str]       # Usually null

@dataclass
class HugoStep:
    """Single step extracted from {{<step>}} shortcode"""
    label: str                       # Step title
    duration: str                    # Format: "M:SS"
    xy_guid: Optional[str]           # UUID for tracking
    content: str                     # Markdown content

@dataclass
class HugoTutorial:
    """Complete Hugo tutorial structure"""
    folder_name: str                 # e.g., "ansible-ios"
    frontmatter: HugoFrontmatter
    steps: List[HugoStep]
    images_path: Optional[Path]      # Path to images/ folder
    raw_content: str                 # Original index.md content
```

### SidecarTutorial (Output)

Represents a tutorial in the target sidecar.json format.

```python
@dataclass
class SidecarFile:
    """Single step file in sidecar format"""
    name: str                        # e.g., "step-1.md"
    label: str                       # Step title
    duration: str                    # Format: "M:SS"
    xy_guid: Optional[str]           # UUID

@dataclass
class SidecarAuthor:
    """Author in sidecar format"""
    name: str

@dataclass
class SidecarJson:
    """Complete sidecar.json structure"""
    title: str
    id: str                          # e.g., "tc-ansible-ios"
    description: str
    date: str                        # Format: "YYYY-MM-DD"
    duration: str                    # Format: "XmXXs" or "XhXXmXXs"
    ia_guid: str                     # UUID
    lesson_guid: str                 # UUID
    authors: List[SidecarAuthor]
    skill_levels: List[str]          # Valid: Beginner, Intermediate, Advanced, Expert
    technologies: List[str]          # Valid: see schema
    certifications: List[str]        # Valid: see schema
    active: bool                     # Always True for migration
    files: List[SidecarFile]
```

### MigrationResult

Represents the output of a migration operation.

```python
@dataclass
class MigrationChange:
    """Single change made during migration"""
    field: str                       # Field that was changed
    original: str                    # Original value
    migrated: str                    # New value
    reason: str                      # Why the change was made

@dataclass
class MigrationWarning:
    """Warning or issue found during migration"""
    severity: str                    # "info", "warning", "error"
    message: str
    suggestion: Optional[str]

@dataclass
class MigrationResult:
    """Complete migration result"""
    source_path: Path
    target_path: Path
    tutorial_id: str                 # e.g., "tc-ansible-ios"
    success: bool
    changes: List[MigrationChange]
    warnings: List[MigrationWarning]
    sidecar: SidecarJson
    step_files: Dict[str, str]       # filename -> content
    pr_description: str              # Generated PR body
```

---

## State Transitions

### Migration Pipeline States

```
┌─────────────┐
│   PENDING   │  Tutorial identified for migration
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PARSING   │  Reading Hugo index.md
└──────┬──────┘
       │
       ├──── Error ────► FAILED (parse error)
       │
       ▼
┌─────────────┐
│  CONVERTING │  Mapping fields, generating sidecar
└──────┬──────┘
       │
       ├──── Error ────► FAILED (conversion error)
       │
       ▼
┌─────────────┐
│  VALIDATING │  Schema validation, CI checks
└──────┬──────┘
       │
       ├──── Error ────► FAILED (validation error)
       │
       ▼
┌─────────────┐
│   READY     │  PR can be created
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MIGRATED   │  PR merged, tutorial in new system
└─────────────┘
```

---

## Relationships

```
HugoTutorial (1) ──────► (1) SidecarJson
     │                        │
     │ has                    │ has
     │                        │
     ▼                        ▼
HugoStep (N) ─────────► SidecarFile (N)
     │                        │
     │ content                │ content
     │                        │
     ▼                        ▼
  String ──────────────►  step-N.md
```

---

## Validation Rules

### Input Validation (Hugo)

| Field | Rule | Error |
|-------|------|-------|
| title | Non-empty string | "Title is required" |
| date | Valid date | "Invalid date format" |
| duration | Matches `\d+:\d{2}` | "Invalid duration format" |
| steps | At least 1 step | "No steps found" |
| step.label | Non-empty string | "Step label required" |
| step.duration | Matches `\d+:\d{2}` | "Invalid step duration" |

### Output Validation (Sidecar)

| Field | Rule | Error |
|-------|------|-------|
| id | Matches `^tc-[a-z0-9-]+$` | "Invalid tutorial ID format" |
| duration | Matches `^\d+m\d{2}s$` or `^\d+h\d{2}m\d{2}s$` | "Invalid duration format" |
| date | Matches `^\d{4}-\d{2}-\d{2}$` | "Invalid date format" |
| files | Length >= 3 | "Minimum 3 steps required" |
| files[0].label | Equals "Overview" | "First step must be Overview" |
| files[-1].label | Equals "Congratulations" | "Last step must be Congratulations" |
| skill_levels | All in valid set | "Invalid skill level" |
| technologies | All in valid set | "Invalid technology" |
| ia_guid | Valid UUID | "Invalid ia-guid format" |
| lesson_guid | Valid UUID | "Invalid lesson-guid format" |

---

## Mapping Tables

### Duration Conversion Examples

| Hugo Input | Sidecar Output |
|------------|----------------|
| "5:00" | "5m00s" |
| "30:00" | "30m00s" |
| "60:00" | "1h00m00s" |
| "90:30" | "1h30m30s" |

### Category Mapping

| Hugo Category | Sidecar Technology |
|---------------|-------------------|
| Networking | Networking |
| Security | Security |
| Cloud | Cloud and Computing |
| Data Center | Data Center |
| Automation | Software |
| Coding | Software |
| Collaboration | Collaboration |
| Other | Other |
