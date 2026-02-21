# Implementation Plan: AI Editorial Agent

**Branch**: `007-ai-editorial-agent` | **Date**: 2026-02-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-ai-editorial-agent/spec.md`

## Summary

Build an AI-powered editorial agent using Claude Opus via `claude-code-action` to replace human editors (masperli and jlauterb-edit). The agent makes editorial edits directly, comments explaining changes, and responds to author feedback in PR threads - replicating the interactive editorial workflow.

## Architecture Decision

### Why Agentic (Not Regex Rules)

| Consideration | Regex Engine | Claude Code Agent |
|---------------|--------------|-------------------|
| Context awareness | None | Full tutorial + references |
| Nuanced judgment | Can't decide | "Is this bold for GUI or emphasis?" |
| Interactive feedback | One-shot | Responds to @claude mentions |
| Making edits | Separate tool | Built-in commit capability |
| Style matching | Rigid patterns | Learns from editor examples |
| Maintenance | Update Python code | Update reference markdown |

**Decision**: Use `anthropics/claude-code-action` with Claude Opus 4.6 as an interactive editorial agent.

**Research basis**: See [research.md](./research.md) for industry best practices and pitfall analysis.

## Technical Context

**AI Model**: Claude Opus (configurable via repository variable)
**Authentication**: Anthropic API key (direct)
**Platform**: GitHub Actions on ubuntu-latest
**Volume**: 5-10 PRs/month (occasional bursts during migrations)
**Fallback**: Skip editorial review if API unavailable (backlog item: deterministic fallback)

### Model Configuration

The model is configured via GitHub repository variable for easy updates:

| Setting | Location | Current Value |
|---------|----------|---------------|
| `CLAUDE_MODEL` | Repository Variables | `claude-opus-4-6` |

**To update when new Opus releases:**
1. Go to Repository Settings → Secrets and Variables → Actions → Variables
2. Update `CLAUDE_MODEL` to new model ID (e.g., `claude-opus-4-7`)
3. No code changes required

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Tutorial Quality First | ✅ PASS | Agent provides editor-quality feedback |
| II. Structured Content Organization | ✅ PASS | Validates content against style guide |
| III. Validate Early, Fail Fast | ✅ PASS | Runs at PR time, makes immediate edits |
| IV. Editorial Consistency Through Automation | ✅ PASS | **Direct implementation** of this principle |
| V. Transparent Pipeline Feedback | ✅ PASS | Comments explain every change with reasoning |

## Agent Capabilities

### Core Behaviors

1. **Review & Edit**: Agent reads all step files, makes editorial corrections directly
2. **Comment & Explain**: Posts PR comment with:
   - Quality score (1-10)
   - Summary of changes made
   - Queries requiring author decision (checkboxes)
   - Step-by-step breakdown
3. **Respond to Feedback**: Author can @claude to:
   - Ask for reverts ("@claude revert the acronym change in step-2")
   - Request clarification ("@claude why did you change this heading?")
   - Approve queries ("@claude yes, expand YANG on first use")
4. **Iterate**: Agent responds and makes additional commits as needed

### Reference Documents (Context)

The agent receives these as context for every review:

| Document | Purpose |
|----------|---------|
| `editor-comments-reference.md` | Rules extracted from Matt/Jill's PR history |
| `acronym-database.json` | Acronym expansion rules, deprecated terms |
| `cisco-product-naming-guide.md` | Product names, trademarks, branding |
| `editorial-style-guide.md` | Existing Cisco U. style guide |

### Edit Types

| Edit Type | Agent Behavior |
|-----------|----------------|
| **Auto-fix** | Makes commit directly (em dashes, "click on", possessives) |
| **Suggested** | Makes commit + explains reasoning in comment |
| **Query** | Does NOT edit; asks author via checkbox in comment |

## Project Structure

### Documentation (this feature)

```text
specs/007-ai-editorial-agent/
├── plan.md                        # This file
├── spec.md                        # Feature specification
├── research.md                    # Architecture research
├── data-model.md                  # Entity definitions
├── quickstart.md                  # Setup guide
├── contracts/
│   └── editorial-rules.yaml       # Rule definitions for agent prompt
├── checklists/requirements.md     # Quality validation
├── editor-comments-reference.md   # Rules from PR history
├── cisco-product-naming-guide.md  # Product naming reference
├── acronym-database.json          # Acronym rules
└── reference-data/                # Raw mined data
    ├── masperli_comments.jsonl
    └── jlauterb_comments.jsonl
```

### Source Code Changes

```text
tutorial-testing/
├── .github/workflows/
│   └── tutorial-linting.yml       # MODIFY: Add claude-code-action step
├── .claude/
│   └── agents/
│       └── editorial-reviewer.md  # NEW: Agent prompt/persona
└── tools/
    └── (existing tools unchanged)
```

**Note**: Minimal code changes required. The agent's behavior is defined by:
1. The workflow YAML configuration
2. The agent prompt in `.claude/agents/editorial-reviewer.md`
3. The reference documents it receives as context

## Workflow Integration

### GitHub Actions Configuration

```yaml
name: Editorial Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  editorial-review:
    # Only run on PRs to tutorial folders
    if: |
      (github.event_name == 'pull_request') ||
      (github.event_name == 'issue_comment' &&
       contains(github.event.comment.body, '@claude'))

    runs-on: ubuntu-latest
    permissions:
      contents: write      # For making commits
      pull-requests: write # For PR comments
      issues: write        # For responding to comments

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.ref }}
          fetch-depth: 0

      - name: Run Editorial Agent
        uses: anthropics/claude-code-action@v1
        with:
          model: ${{ vars.CLAUDE_MODEL || 'claude-opus-4-6' }}  # Configurable, defaults to Opus 4.6
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          allowed_tools: |
            Read
            Edit
            Write
            Bash(git status)
            Bash(git diff)
            Bash(git add)
            Bash(git commit)
          prompt_file: .claude/agents/editorial-reviewer.md
        continue-on-error: true  # Don't block if API unavailable
```

### Agent Prompt Structure

The `.claude/agents/editorial-reviewer.md` file defines the agent's persona and instructions:

```markdown
# Editorial Reviewer Agent

You are an editorial reviewer for Cisco U. tutorials, trained on feedback
patterns from editors Matt Sperling (masperli) and Jill Lauterbach (jlauterb-edit).

## Your Reference Documents

Read these files for editorial rules:
- specs/007-ai-editorial-agent/editor-comments-reference.md
- specs/007-ai-editorial-agent/acronym-database.json
- specs/007-ai-editorial-agent/cisco-product-naming-guide.md

## Your Task

1. Review all step-*.md files in the tutorial folder
2. Make editorial corrections following the reference documents
3. Commit your changes with clear commit messages
4. Post a PR comment summarizing your review

## PR Comment Format (Jill's Style)

[Format specification from data-model.md]

## Rules for Making Edits

- AUTO-FIX: Em dashes, "click on", Cisco possessives, obvious typos
- SUGGEST + EXPLAIN: Heading style, acronym expansion, product names
- QUERY (don't edit): Ambiguous acronyms, content restructuring, tone

## Responding to Feedback

When author replies with @claude:
- Acknowledge the request
- Make requested changes or explain why not
- Be collaborative, not defensive
```

## Implementation Phases

### Phase 1: Basic Agent Setup
- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Create `.claude/agents/editorial-reviewer.md` prompt
- [ ] Add editorial review job to `tutorial-linting.yml`
- [ ] Test on a sample PR

### Phase 2: Reference Document Integration
- [ ] Copy reference docs to location agent can access
- [ ] Tune prompt based on initial test results
- [ ] Verify agent correctly applies rules from documents

### Phase 3: Interactive Feedback
- [ ] Enable `issue_comment` trigger for @claude mentions
- [ ] Test revert/clarification requests
- [ ] Document interaction patterns for authors

### Phase 4: Refinement
- [ ] Collect feedback from first 10 PRs
- [ ] Update reference documents based on agent performance
- [ ] Tune quality score calculation

## Testing Approach

**IMPORTANT**: Do NOT create test PRs on the production repository - current editors (Matt, Jill) follow the PR queue and should not see test activity until the agent is ready for handoff.

**Testing strategy:**
1. Add `ANTHROPIC_API_KEY` and `CLAUDE_MODEL` secrets to tutorial-testing repo
2. Use `workflow_dispatch` trigger to manually test on branches (no PR needed)
3. Validate agent behavior before enabling PR-triggered workflow on production

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection rate | >70% of issues editors would catch | Compare to historical editor comments |
| False positive rate | <15% for auto-edits | Track reverts requested by authors |
| Author satisfaction | 80% find feedback actionable | Optional survey in PR comment |
| Response time | <5 minutes | Time from PR open to comment |

## Backlog Items

| Item | Priority | Notes |
|------|----------|-------|
| Deterministic fallback | Medium | If API unavailable, run basic regex checks |
| Analytics tracking | Medium | Track which rules fire, author correction patterns. Tradeoff: Current JSON/MD files are simple (Claude reads directly, no credentials, version controlled); DB adds query capability but requires infrastructure |
| Quality score refinement | Low | Tune weights based on real usage |
| Multi-tutorial PR handling | Low | Current: one tutorial per PR (existing rule) |
| Editor training mode | Low | Let Matt/Jill review agent suggestions to improve |

## Cost Estimate

| Component | Estimate |
|-----------|----------|
| Claude Opus API | ~$50-100/month at 5-10 PRs |
| GitHub Actions | Included in existing plan |
| **Total** | **~$50-100/month** |

Compared to part-time editor costs (~$2-3K/month), this is a significant cost reduction while maintaining quality.
