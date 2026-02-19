# FF-5: Legacy Hugo Tutorial Migration

## Overview

Migrate 110+ tutorials from the legacy Hugo-based `cisco-learning-codelabs` repository to the production `ciscou-tutorial-content` repository with full CI/CD validation compatibility.

## Problem Statement

The Cisco Learning team maintains tutorials in two systems:
1. **Legacy Hugo system** (`cisco-learning-codelabs`): 110+ tutorials using Hugo static site generator
2. **Production system** (`ciscou-tutorial-content`): Modern CI/CD pipeline with Solomon XML conversion

Tutorials in the Hugo system cannot be deployed to Cisco U. without migration. The migration requires:
- Converting Hugo `codelabs.json` metadata to `sidecar.json` format
- Ensuring markdown content passes Solomon XML conversion
- Handling format differences (durations, certifications, step labels)
- Fixing broken/outdated URLs and images

## Goals

1. Migrate all 110+ Hugo tutorials to production format
2. Automate detection and fixing of common migration issues
3. Document patterns that require manual intervention
4. Create reusable tools for future migrations

## Non-Goals

- Rewriting tutorial content
- Updating deprecated technologies covered in tutorials
- Creating new tutorials

## Stakeholders

- **Content Authors**: Tutorial creators who need their content migrated
- **Platform Team**: Responsible for CI/CD pipeline compatibility
- **Editors**: Review migrated content for quality

## Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Tutorials migrated | 110 | 108 |
| Auto-fix success rate | >80% | 92% |
| Manual review required | <10 | 7 |
| CI pipeline passing | 100% after fixes | 93% (7 pending human review) |

## Technical Approach

### Migration Pipeline

```
Hugo Repo (codelabs.json) → Migration Script → PR Creation
                                    ↓
                            CI Validation
                                    ↓
                    Auto-Fix (clean_markdown.py, fix_sidecar.py)
                                    ↓
                            Solomon XML Conversion
                                    ↓
                        Ready for Merge / Human Review
```

### Key Challenges Solved

1. **Solomon XML Compatibility**: Identified and auto-fixed markdown patterns that break XML conversion
2. **Metadata Format Conversion**: Automated `codelabs.json` → `sidecar.json` transformation
3. **Duplicate GUID Detection**: Regenerated all GUIDs to avoid conflicts with existing tutorials
4. **Broken URL Detection**: Integrated URL validation into CI pipeline

## Implementation Summary

### Tools Created

| Tool | Purpose | Location |
|------|---------|----------|
| `fix_sidecar.py` | Auto-fix duration mismatches | `ciscou-tutorial-content/tools/` |
| `clean_markdown.py` enhancements | Fix Solomon XML issues | `ciscou-tutorial-content/tools/` |
| Integration tests | Validate fix pipeline | `ciscou-tutorial-content/tests/` |

### CI Workflow Improvements

- Auto-commit markdown fixes back to PR branches
- HEREDOC syntax for multi-line commit messages
- Better error surfacing in PR comments

### Issues Discovered

See [learnings.md](learnings.md) for detailed documentation of:
- 9 issue types discovered and fixed
- Auto-fix vs human-review categorization
- Recommendations for future migrations

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Initial migration script | 1 session | Complete |
| CI integration | 1 session | Complete |
| Issue discovery & fixes | 3 sessions | Complete |
| Final cleanup | 1 session | Complete |

## Dependencies

- Solomon XML converter (`tutorial_md2xml`)
- GitHub Actions CI/CD
- `ciscou-tutorial-content` repository access

## Related Features

- **FR-1**: Enhanced Markdown Validation (provides detection rules)
- **FR-5**: PR Comment Enhancements (future: better error surfacing)
