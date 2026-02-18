# Tutorial Pipeline Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CONTENT CREATION                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                               │
│  │ Tech     │    │ Learn w/ │    │  TMEs    │                               │
│  │ Advocates│    │ Cisco    │    │          │                               │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘                               │
│       │               │               │                                      │
│       └───────────────┴───────────────┘                                      │
│                       │                                                      │
│                       ▼                                                      │
│              ┌────────────────┐                                              │
│              │  tc-* branch   │                                              │
│              │  with tutorial │                                              │
│              └────────┬───────┘                                              │
└───────────────────────┼─────────────────────────────────────────────────────┘
                        │
                        ▼ Pull Request
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CI VALIDATION PIPELINE                                │
│                     (tutorial-linting.yml)                                   │
│                                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │  Structure  │──▶│   Schema    │──▶│   Pytest    │──▶│  Markdown   │     │
│  │  Validation │   │  Validation │   │  Validation │   │   Cleanup   │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│         │                │                 │                  │              │
│         ▼                ▼                 ▼                  ▼              │
│  • tc-* naming     • sidecar.json    • skill-levels     • whitespace        │
│  • images/ folder  • GUID format     • technologies     • formatting        │
│  • assets/ (opt)   • duration regex  • duration sum                         │
│                    • required fields • step naming                          │
│                                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                        │
│  │  MD → XML   │──▶│   Solomon   │──▶│ AI Analysis │                        │
│  │ Conversion  │   │  Transform  │   │  (advice)   │                        │
│  └─────────────┘   └─────────────┘   └─────────────┘                        │
│         │                │                  │                                │
│         ▼                ▼                  ▼                                │
│  • tutorial_md2xml  • XML linting    • Editorial feedback                   │
│  • raw XML output   • libxml2-utils  • Cisco Chat-AI LLM                    │
│                                                                              │
│                          │                                                   │
│                          ▼                                                   │
│                 ┌────────────────┐                                           │
│                 │   PR Comment   │                                           │
│                 │  with results  │                                           │
│                 └────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                        │
                        ▼ Human Review
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REVIEW PROCESS                                      │
│                                                                              │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐             │
│  │  Editorial  │───────▶│  Technical  │───────▶│   Merge     │             │
│  │   Review    │        │   Review    │        │  Approval   │             │
│  │ (Jill/Matt) │        │    (TAs)    │        │             │             │
│  └─────────────┘        └─────────────┘        └─────────────┘             │
│         │                                                                    │
│         ▼                                                                    │
│  • Grammar/spelling                                                          │
│  • Style consistency                                                         │
│  • Heading format                                                            │
│  • Acronym expansion                                                         │
│  • Punctuation                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                        │
                        ▼ Merge to main
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DEPLOYMENT PIPELINE                                    │
│                    (tutorial-automation.yml)                                 │
│                                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                        │
│  │  Validate   │──▶│  Detect     │──▶│  REST API   │                        │
│  │  One Folder │   │  NEW/EXIST  │   │    Push     │                        │
│  └─────────────┘   └─────────────┘   └─────────────┘                        │
│                                             │                                │
│                                             ▼                                │
│                                    ┌────────────────┐                        │
│                                    │   Publishing   │                        │
│                                    │     Team       │                        │
│                                    └────────┬───────┘                        │
│                                             │                                │
│                                             ▼                                │
│                          ┌─────────────────────────────────┐                │
│                          │         Cisco U. Platform        │                │
│                          │   ┌─────────┐    ┌──────────┐   │                │
│                          │   │ Staging │───▶│Production│   │                │
│                          │   └─────────┘    └──────────┘   │                │
│                          │        │              ▲         │                │
│                          │        └── UAT ───────┘         │                │
│                          └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Validation Tools (`tutorial-testing/tools/`)

| Tool | Purpose | Lines |
|------|---------|-------|
| `pytest_validation.py` | Main pytest-based validation suite | 608 |
| `schema_validation.py` | JSON schema validation | 157 |
| `clean_markdown.py` | Whitespace/formatting checks | 106 |
| `ai_analysis.py` | AI-powered editorial feedback | 542 |
| `jira_update.py` | Jira ticket integration | 301 |
| `guid_update.py` | GUID cache management | 79 |
| `template_bootstrap.py` | New tutorial scaffolding | 165 |

### Data Flow

```
Tutorial Folder (tc-*)
        │
        ├── sidecar.json ──────▶ schema_validation.py ──▶ schema.json
        │                              │
        │                              ▼
        │                       pytest_validation.py
        │                              │
        │                              ├── skill-levels check
        │                              ├── technologies check
        │                              ├── duration sum check
        │                              ├── step naming check
        │                              └── GUID uniqueness ──▶ guid_cache.json
        │
        ├── step-*.md ─────────▶ clean_markdown.py
        │                              │
        │                              ▼
        │                       tutorial_md2xml
        │                              │
        │                              ▼
        │                       Solomon XML transform
        │                              │
        │                              ▼
        │                       ai_analysis.py ──────▶ Cisco Chat-AI API
        │
        └── images/ ───────────▶ Image reference validation
```

### External Integrations

| System | Purpose | Authentication |
|--------|---------|----------------|
| Cisco Chat-AI | LLM for editorial analysis | OAuth2 (CLIENT_ID, CLIENT_SECRET, APP_KEY) |
| Jira | Ticket status tracking | API Token (EMAIL, API_TOKEN) |
| Cisco U. API | Tutorial publishing | AUTOMATION_SECRET |
| GitHub | PR comments, workflow triggers | GITHUB_TOKEN (automatic) |

### Tutorial File Structure

```
tc-example/
├── sidecar.json          # Required: Metadata and step definitions
│   ├── id                # Must match folder name, lowercase alphanumeric + hyphens
│   ├── title             # <60 characters
│   ├── description       # 1-2 sentences
│   ├── date              # YYYY-MM-DD
│   ├── duration          # XXmXXs or XhXXmXXs (must equal sum of step durations)
│   ├── ia-guid           # Unique UUID
│   ├── lesson-guid       # Unique UUID
│   ├── certifications    # Array of {cert: "..."} or null
│   ├── skill-levels      # Beginner|Intermediate|Advanced|Expert
│   ├── tags              # Array of {tag: "..."}
│   ├── technologies      # Array of {tech: "..."} from allowed list
│   ├── files             # Array of step definitions
│   │   └── {label, duration (MM:SS), xy-guid, file}
│   ├── authors           # Single author {name, email}
│   └── active            # Must be true
│
├── step-1.md             # Required: Overview
│   ├── What you'll learn
│   └── What you'll need
│
├── step-2.md ... step-N-1.md  # Content steps
│
├── step-N.md             # Required: Congratulations
│   └── Call to action with resources
│
├── images/               # Required folder (can be empty)
│   └── *.png, *.gif, *.jpg
│
└── assets/               # Optional: configs, manifests, etc.
    └── *.yaml, *.json, etc.
```

## XML Conversion Pipeline

The markdown to XML conversion is a critical path where errors often occur:

```
step-*.md
    │
    ▼
tutorial_md2xml (Go binary)
    │
    ├── Parses markdown
    ├── Converts to raw XML
    └── Sensitive to:
        • Whitespace around links
        • Newlines in inline elements
        • Special characters in code blocks
    │
    ▼
Solomon XML Transform
    │
    ├── Applies Cisco U. specific transformations
    └── Validates against platform schema
    │
    ▼
libxml2-utils validation
    │
    └── Final XML lint check
```

### Common XML Conversion Errors

| Issue | Cause | Fix |
|-------|-------|-----|
| Unexpected whitespace | Newline before/after `[link](url)` | Remove extra newlines |
| Invalid entity | Unescaped `&` in text | Use `&amp;` |
| Malformed element | Incomplete markdown syntax | Fix markdown formatting |
| Missing closing tag | Nested formatting issues | Simplify nested formatting |
