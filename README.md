# Cisco U. Tutorial Platform - Development Workspace

This repository serves as the planning and specification workspace for improving the Cisco U. tutorial content pipeline. It uses [Spec-Kit](https://github.com/github/spec-kit) for spec-driven development.

## Repository Structure

```
tutorial-platform-specs/
├── .specify/                    # Spec-Kit templates and project memory
│   ├── memory/constitution.md   # Project principles and governance
│   └── specs/                   # Requirements, architecture docs
├── specs/                       # Feature specifications
│   ├── 001-tutorial-testing-sync/     # Completed: Production sync
│   ├── 002-enhanced-markdown-validation/  # Completed: 7 detection rules
│   ├── 003-hugo-tutorial-migration/   # Completed: 108 tutorials migrated
│   ├── 004-pr-comment-enhancements/   # In Progress: Better CI error surfacing
│   ├── 005-pre-commit-validation/     # Completed: GUID auto-generation
│   └── 006-tutorial-creation-workflows/  # Completed: Issue form + Codespace
├── CLAUDE.md                    # Claude Code instructions
├── tutorial-testing/            # Cloned repo (tools development)
└── ciscou-tutorial-content/     # Cloned repo (production reference)
```

## Setup

To replicate this workspace:

```bash
# Clone this specs repo
git clone git@github.com:CiscoLearning/tutorial-platform-specs.git
cd tutorial-platform-specs

# Clone the sub-repositories
git clone git@github.com:CiscoLearning/tutorial-testing.git
git clone git@github.com:CiscoLearning/ciscou-tutorial-content.git
```

**Note:** `ciscou-tutorial-content` is a private org repository. You need CiscoLearning org membership to access it.

## Feature Backlog

See [.specify/specs/requirements.md](.specify/specs/requirements.md) for the full backlog.

### Completed

| Feature | Description | Spec |
|---------|-------------|------|
| FR-0: Tutorial-Testing Sync | Daily sync of production tutorials to testing repo | [spec](specs/001-tutorial-testing-sync/spec.md) |
| FR-1: Enhanced Markdown Validation | 7 detection rules, 41% false positive reduction | [spec](specs/002-enhanced-markdown-validation/spec.md) |
| FF-5: Hugo Tutorial Migration | 108 tutorials migrated, 92% auto-fix rate | [spec](specs/003-hugo-tutorial-migration/spec.md) |
| FR-4: Pre-commit Validation | GUID auto-generation on PR, local validation CLI, 29 unit tests | [spec](specs/005-pre-commit-validation/spec.md) |
| FF-2: Tutorial Creation Workflows | Issue form + auto-PR, Codespace, CLI wizard, 40 unit tests | [spec](specs/006-tutorial-creation-workflows/spec.md) |
| FR-5: PR Comment Enhancements | CI errors surfaced in PR comments with fix guidance | [spec](specs/004-pr-comment-enhancements/spec.md) |

### Backlog

| Feature | Description | Priority |
|---------|-------------|----------|
| FR-2 | Editorial Style Validation | High |
| FR-3 | AI-Powered Editorial Feedback | High |
| FF-1 | AI-Powered Sidecar Generation | Future |
| FF-3 | Tutorial Preview Rendering | Future |

## Workflow

1. **Plan**: Use `/speckit.specify` to create feature specs
2. **Design**: Use `/speckit.plan` to create implementation plans
3. **Tasks**: Use `/speckit.tasks` to generate task lists
4. **Implement**: Use `/speckit.implement` to execute tasks
5. **Analyze**: Use `/speckit.analyze` to check consistency

## Related Repositories

| Repository | Purpose |
|------------|---------|
| [tutorial-testing](https://github.com/CiscoLearning/tutorial-testing) | Tools development, validation scripts, CI/CD testing |
| [ciscou-tutorial-content](https://github.com/CiscoLearning/ciscou-tutorial-content) | Production tutorials (private, 146+ tutorials) |

## Maintenance

- Keep this README updated as features are completed
- Update the backlog table when starting/completing features
- Sub-repositories are independent - changes go directly to them

## License

This repository is licensed under the [Apache License 2.0](LICENSE).

**Note:** This repo contains specifications, tooling documentation, and planning artifacts. The actual tutorial content lives in separate repositories:
- `tutorial-testing` - Public, contains validation tools and synced tutorials
- `ciscou-tutorial-content` - Private, production tutorial content (Cisco proprietary)
