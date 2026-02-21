# Quickstart: AI Editorial Agent

**Branch**: `007-ai-editorial-agent` | **Date**: 2026-02-20

## Overview

The AI Editorial Agent is a Claude Opus-powered reviewer that replaces human editors for Cisco U. tutorial PRs. It makes edits directly, explains changes, and responds to author feedback via @claude mentions.

## How It Works

```
Author opens PR
       │
       ▼
┌─────────────────────────────┐
│  Claude Opus Editorial Agent │
│  - Reads all step-*.md files │
│  - Applies editorial rules   │
│  - Makes commits with fixes  │
│  - Posts summary comment     │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│    Author reviews changes    │
│    - Approves or requests    │
│      changes via @claude     │
└─────────────┬───────────────┘
              │
              ▼
       Agent responds
       (iterates as needed)
```

## Setup

### 1. Repository Secrets

Add to **Settings → Secrets and Variables → Actions → Secrets**:

| Secret | Value |
|--------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 2. Repository Variables

Add to **Settings → Secrets and Variables → Actions → Variables**:

| Variable | Value | Notes |
|----------|-------|-------|
| `CLAUDE_MODEL` | `claude-opus-4-6` | Update when new Opus releases |

### 3. Agent Prompt

Create `.claude/agents/editorial-reviewer.md` in your repository (see plan.md for template).

### 4. Workflow

The editorial review job is added to `tutorial-linting.yml`. It runs:
- On PR open/update
- When someone comments with @claude

## Interacting with the Agent

### Initial Review

When you open a PR, the agent automatically:
1. Reviews all step files
2. Makes editorial corrections (commits)
3. Posts a summary comment with quality score

### Asking for Changes

Comment on the PR with @claude:

```
@claude please revert the heading change in step-3
```

```
@claude why did you expand VLAN? I think it's well-known enough
```

```
@claude yes, go ahead and expand NAS as "network access server"
```

The agent will respond and make additional commits as needed.

## What Gets Auto-Fixed

| Issue | Example | Agent Action |
|-------|---------|--------------|
| Em dash spacing | `problems — they` | Auto-fix: `problems—they` |
| "Click on" | `Click on Save` | Auto-fix: `Click Save` |
| Cisco possessive | `Cisco ISE's` | Auto-fix: `the Cisco ISE` |
| Gerund headings | `Configuring` | Suggest: `Configure` |
| Acronym expansion | `VLAN` first use | Suggest: `virtual LAN (VLAN)` |
| Deprecated acronym | `FTD` | Query: Flag for author decision |

## What Triggers a Query

The agent won't auto-fix these - it asks in the PR comment:

- Ambiguous acronyms (NAS = storage or access server?)
- Content restructuring suggestions
- Unclear product name context
- Tone/voice recommendations

## Updating the Rules

### Add New Acronym

Edit `specs/007-ai-editorial-agent/acronym-database.json`:

```json
"NEW_ACRONYM": {
  "expansion": "Full Name Here",
  "expand_first_use": true
}
```

### Add Product Name Rule

Edit `specs/007-ai-editorial-agent/cisco-product-naming-guide.md` and add entry.

### Update Editorial Rules

Edit `specs/007-ai-editorial-agent/editor-comments-reference.md` with new patterns.

The agent reads these files on every run - no code changes needed.

## Updating the Model

When Anthropic releases a new Opus version:

1. Go to **Settings → Secrets and Variables → Actions → Variables**
2. Update `CLAUDE_MODEL` to new model ID (e.g., `claude-opus-4-7`)
3. Done - next PR will use new model

## Troubleshooting

### Agent Didn't Run

- Check if API key is set correctly in secrets
- Check GitHub Actions logs for errors
- Verify workflow trigger conditions

### Agent Made Wrong Edit

Comment: `@claude please revert [specific change]`

The agent will acknowledge and revert.

### API Unavailable

The workflow uses `continue-on-error: true`, so the pipeline continues. Editorial review is skipped, but other validations still run.

### Want Different Behavior

Edit `.claude/agents/editorial-reviewer.md` to adjust the agent's instructions.

## Cost

| Volume | Estimated Cost |
|--------|----------------|
| 5-10 PRs/month | ~$50-100/month |
| Burst (migration) | ~$200-300/month |

Compared to part-time editor costs (~$2-3K/month), this is significant savings.

## Reference Documents

| Document | Purpose |
|----------|---------|
| [editor-comments-reference.md](./editor-comments-reference.md) | Rules from Matt/Jill's PR history |
| [acronym-database.json](./acronym-database.json) | Acronym expansion rules |
| [cisco-product-naming-guide.md](./cisco-product-naming-guide.md) | Product naming standards |
| [plan.md](./plan.md) | Full implementation plan |
