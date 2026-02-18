# Cisco U. Tutorial Platform Requirements

## System Context

### Current State
The Cisco U. tutorial platform enables technical content creation through a GitHub-based workflow:

1. **Authors** create tutorials as markdown files with metadata in `sidecar.json`
2. **CI Pipeline** validates structure, schema, and converts markdown to Cisco U. XML format
3. **Editors** manually review PRs for style, grammar, and consistency
4. **Technical Advocates** approve and merge PRs
5. **Automation** pushes XML to publishing team via REST API
6. **Publishing Team** deploys to staging, then production after UAT approval

### Pain Points
- **XML Conversion Errors**: Whitespace issues around links and file references cause XML parsing failures; authors must manually fix based on pipeline error messages
- **Manual Editorial Review**: Two part-time editors review English quality on every PR
- **Inconsistent Style**: Authors don't always follow style conventions (heading format, acronym expansion, punctuation)
- **Validation Feedback Loop**: Authors discover issues late in the process

## Stakeholder Requirements

### Tutorial Authors (Technical Advocates, Instructors, TMEs)

| ID | Requirement | Priority |
|----|-------------|----------|
| AUTH-1 | Get clear, actionable feedback on validation errors before merge | High |
| AUTH-2 | Receive AI-powered editorial suggestions during PR review | High |
| AUTH-3 | Scaffold new tutorials with correct structure automatically | Medium |
| AUTH-4 | Preview how tutorial will render in Cisco U. format | Low |

### Editorial Team (Jill, Matt Sperling)

| ID | Requirement | Priority |
|----|-------------|----------|
| EDIT-1 | AI should catch common style issues before human review | High |
| EDIT-2 | Style guide violations should be flagged automatically | High |
| EDIT-3 | Reduce volume of PRs requiring manual corrections | High |

### Technical Advocates (Reviewers/Approvers)

| ID | Requirement | Priority |
|----|-------------|----------|
| TA-1 | Trust that merged PRs will convert to valid XML | High |
| TA-2 | See editorial quality score/summary before approving | Medium |
| TA-3 | One tutorial per PR enforced automatically | Medium |

### Publishing Team

| ID | Requirement | Priority |
|----|-------------|----------|
| PUB-1 | Receive valid XML that doesn't require manual fixes | High |
| PUB-2 | Clear differentiation between NEW and EXISTING tutorials | Medium |

## Functional Requirements

### FR-1: Enhanced Markdown Validation
Validate markdown files for issues that cause XML conversion failures:
- Whitespace before/after links
- Improper newlines around inline elements
- Invalid image/file references
- Code block formatting issues

### FR-2: Editorial Style Validation
Automatically check for style guide compliance based on editorial patterns:
- Heading format (imperative mood, not gerund)
- Acronym expansion on first use
- Punctuation standards (em-dash spacing, serial comma)
- Technical term formatting (hyphenation, code vs. bold)
- Parallel structure in lists

### FR-3: AI-Powered Editorial Feedback
Enhance existing `ai_analysis.py` to provide:
- Style guide violation detection
- Suggested corrections for common issues
- Quality score with breakdown by category
- Comparison to editorial patterns from historical commits

### FR-4: Pre-commit Validation
Provide local validation before pushing:
- Schema validation
- Duration sum check
- GUID uniqueness check
- Basic style checks

### FR-5: PR Comment Enhancements
Improve automated PR comments to include:
- Categorized issues (blocking vs. suggestions)
- Specific line references for fixes
- Style guide references for violations
- Before/after examples for corrections

## Non-Functional Requirements

### NFR-1: Performance
- Validation pipeline should complete within 5 minutes
- AI analysis should complete within 2 minutes

### NFR-2: Accuracy
- Style suggestions should have <10% false positive rate
- XML conversion predictions should be >95% accurate

### NFR-3: Maintainability
- Style rules should be configurable, not hardcoded
- New validation rules should be addable without code changes

## Constraints

- Must integrate with existing GitHub Actions workflows
- Must use Cisco Chat-AI LLM API for AI features
- Cannot change the XML format required by publishing team
- Must maintain backward compatibility with existing tutorials

## Success Criteria

1. Reduce manual editorial corrections by 50%
2. Eliminate XML conversion errors at merge time
3. Authors receive actionable feedback within 5 minutes of PR creation
4. Style guide compliance rate increases to >90%
