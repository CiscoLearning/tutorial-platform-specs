# Tasks: AI Editorial Agent

**Input**: Design documents from `/specs/007-ai-editorial-agent/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Architecture**: Agentic approach using `anthropics/claude-code-action` with Claude Opus
**Tests**: Not explicitly requested - omitted per spec

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

This feature uses minimal code changes - primarily configuration files:
- `.github/workflows/` - GitHub Actions workflow
- `.claude/agents/` - Claude agent prompts
- `specs/007-ai-editorial-agent/` - Reference documents (already created)

## Testing Approach

**IMPORTANT**: Do NOT create PRs on production repository during testing. Current editors (Matt, Jill) follow the PR queue and should not see test PRs.

**Options for testing without visible PRs:**

1. **Add secrets to tutorial-testing repo** - preferred if possible
2. **Use `workflow_dispatch` trigger on prod** - manually trigger workflow on a branch without creating a PR
3. **Draft PRs** - create as draft (less visible in PR queue, but still shows)

Recommendation: Add `ANTHROPIC_API_KEY` and `CLAUDE_MODEL` to tutorial-testing repo, then test there with branches + manual workflow triggers.

---

## Phase 1: Setup (Repository Configuration)

**Purpose**: Configure GitHub repository secrets and variables for testing

- [x] T001 Add `ANTHROPIC_API_KEY` secret to tutorial-testing repo (Settings → Secrets and Variables → Actions → Secrets)
- [x] T002 Add `CLAUDE_MODEL` variable with value `claude-opus-4-6` to tutorial-testing repo (Settings → Secrets and Variables → Actions → Variables)
- [x] T003 Verify tutorial-testing repo has `pull-requests: write` and `contents: write` permissions for Actions

---

## Phase 2: Foundational (Agent Infrastructure)

**Purpose**: Create the core agent prompt and workflow integration - MUST complete before any user story testing

**CRITICAL**: No user story validation can begin until this phase is complete

- [x] T004 Create directory structure for agent prompt at tutorial-testing/.claude/agents/
- [x] T005 Create editorial-reviewer.md agent prompt in tutorial-testing/.claude/agents/editorial-reviewer.md with:
  - Agent persona (editorial reviewer trained on Matt/Jill patterns)
  - Reference document paths
  - Task instructions (review, edit, commit, comment)
  - PR comment format (Jill's style from data-model.md)
  - Edit type rules (AUTO-FIX, SUGGEST, QUERY)
  - Feedback response guidelines
- [x] T006 Add editorial review job to tutorial-testing/.github/workflows/tutorial-linting.yml with:
  - Trigger on `workflow_dispatch` (for manual testing without PRs)
  - Trigger on `pull_request` (opened, synchronize) - enable after testing complete
  - Trigger on `issue_comment` (created) for @claude mentions
  - `claude-code-action@v1` with configurable model via `vars.CLAUDE_MODEL`
  - `continue-on-error: true` for graceful API unavailability
  - Proper permissions (contents: write, pull-requests: write, issues: write)
- [x] T007 Copy reference documents to tutorial-testing/.claude/references/ for agent access:
  - Copy specs/007-ai-editorial-agent/editor-comments-reference.md → tutorial-testing/.claude/references/
  - Copy specs/007-ai-editorial-agent/acronym-database.json → tutorial-testing/.claude/references/
  - Copy specs/007-ai-editorial-agent/cisco-product-naming-guide.md → tutorial-testing/.claude/references/

**Checkpoint**: Agent infrastructure ready - can now test user stories

---

## Phase 3: User Story 1 - Author Receives Immediate Editorial Feedback (Priority: P1) MVP

**Goal**: When author opens PR, agent reviews, makes edits, and posts summary comment within 5 minutes

**Independent Test**: Open test PR with known editorial issues (unexpanded acronym, gerund heading, "click on") and verify:
1. Agent makes commits with fixes
2. PR comment appears with quality score
3. Comment includes Global Edits, Queries, Step-by-Step Review sections

### Implementation for User Story 1

- [ ] T008 [US1] Create test tutorial tc-editorial-test/ in a tutorial-testing (via workflow_dispatch) repo with known issues:
  - step-1.md with unexpanded "VLAN" acronym
  - step-2.md with "Configuring" gerund heading
  - step-3.md with "click on" and "Cisco ISE's" possessive
- [ ] T009 [US1] Open test PR in tutorial-testing (via workflow_dispatch) repo (NOT production) and trigger editorial review workflow
- [ ] T010 [US1] Verify agent makes editorial commits with clear commit messages
- [ ] T011 [US1] Verify PR comment appears with correct format:
  - Quality score (1-10)
  - Global Edits section
  - Queries for Author section
  - Step-by-Step Review section
- [ ] T012 [US1] Verify response time is under 5 minutes from PR open to comment
- [ ] T013 [US1] Tune agent prompt based on initial results in tutorial-testing/.claude/agents/editorial-reviewer.md

**Checkpoint**: User Story 1 complete - authors receive immediate editorial feedback

---

## Phase 4: User Story 2 - Reviewer Sees Quality Score (Priority: P2)

**Goal**: Quality score accurately reflects issue severity; reviewers can quickly assess editorial readiness

**Independent Test**: Submit PRs with varying issue counts and verify score calculation matches expected values

### Implementation for User Story 2

- [ ] T014 [US2] Add quality score calculation guidance to agent prompt in tutorial-testing/.claude/agents/editorial-reviewer.md:
  - HIGH issues: -1.0 per issue
  - MEDIUM issues: -0.5 per issue
  - LOW issues: -0.1 per issue
  - Score floor: 1.0, ceiling: 10.0
- [ ] T015 [US2] Create test PR in tutorial-testing (via workflow_dispatch) with 3 HIGH priority issues and verify score ~7/10
- [ ] T016 [US2] Create test PR in tutorial-testing (via workflow_dispatch) with only LOW priority issues and verify score 9-10/10
- [ ] T017 [US2] Verify PR comment categorizes issues correctly (High/Medium/Low Priority)
- [ ] T018 [US2] Add assessment text to agent output (Excellent/Good/Needs Work/Major Issues)

**Checkpoint**: User Story 2 complete - reviewers see accurate quality assessment

---

## Phase 5: User Story 3 - Interactive Feedback via @claude (Priority: P2)

**Goal**: Authors can request reverts, clarifications, and answer queries via @claude mentions

**Independent Test**: Post @claude comments on test PR and verify agent responds and makes requested changes

### Implementation for User Story 3

- [ ] T019 [US3] Verify `issue_comment` trigger is working for @claude mentions in tutorial-testing (via workflow_dispatch) workflow
- [ ] T020 [US3] Test revert request in tutorial-testing (via workflow_dispatch): Comment "@claude please revert the heading change in step-2"
- [ ] T021 [US3] Test clarification request in tutorial-testing (via workflow_dispatch): Comment "@claude why did you expand VLAN?"
- [ ] T022 [US3] Test query approval in tutorial-testing (via workflow_dispatch): Comment "@claude yes, expand NAS as network access server"
- [ ] T023 [US3] Verify agent makes appropriate commits or explains reasoning
- [ ] T024 [US3] Update agent prompt with collaborative response guidelines if needed

**Checkpoint**: User Story 3 complete - authors can interact with agent via @claude

---

## Phase 6: User Story 4 - Living Reference Documents (Priority: P3)

**Goal**: Editorial team can update reference docs and agent uses updated rules automatically

**Independent Test**: Update acronym-database.json, open PR, verify agent uses new rule

### Implementation for User Story 4

- [ ] T025 [US4] Add new test acronym to specs/007-ai-editorial-agent/acronym-database.json:
  - Add "TEST": {"expansion": "Test Expansion", "expand_first_use": true}
- [ ] T026 [US4] Sync updated acronym-database.json to tutorial-testing/
- [ ] T027 [US4] Create test PR in tutorial-testing (via workflow_dispatch) using "TEST" acronym without expansion
- [ ] T028 [US4] Verify agent suggests expansion per new rule
- [ ] T029 [US4] Remove test acronym and document update process for editorial team
- [ ] T030 [US4] Update quickstart.md with reference document update instructions

**Checkpoint**: User Story 4 complete - living documents work as expected

---

## Phase 7: Polish & Documentation

**Purpose**: Final cleanup and documentation for handoff

- [ ] T031 [P] Update specs/007-ai-editorial-agent/quickstart.md with lessons learned from testing
- [ ] T032 [P] Document interaction patterns in tutorial-testing/docs/editorial-agent.md
- [ ] T033 Clean up test tutorial tc-editorial-test/ (delete or mark as test)
- [ ] T034 Add editorial agent section to tutorial-testing/README.md
- [ ] T035 Collect initial feedback from first real PR review
- [ ] T036 Create backlog issue for deterministic fallback (API unavailable scenario)
- [ ] T037 Create backlog issue for analytics tracking (which rules fire, author patterns)
  - Tradeoff: Current JSON/MD files are simple and Claude reads directly; DB adds query capability but requires credentials and maintenance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - core MVP
- **User Story 2 (Phase 4)**: Depends on US1 (builds on PR comment format)
- **User Story 3 (Phase 5)**: Depends on US1 (requires working agent)
- **User Story 4 (Phase 6)**: Can start after Foundational (independent of US2/US3)
- **Polish (Phase 7)**: Depends on US1-US4 completion

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (P1) | Foundational | Phase 2 complete |
| US2 (P2) | US1 | Phase 3 complete |
| US3 (P2) | US1 | Phase 3 complete |
| US4 (P3) | Foundational | Phase 2 complete |

### Parallel Opportunities

- T001, T002, T003 can run in parallel (different GitHub settings)
- T031, T032 can run in parallel (different documentation files)
- US3 and US4 can run in parallel after US1 completes (different concerns)

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Add ANTHROPIC_API_KEY secret to repository"
Task: "Add CLAUDE_MODEL variable to repository"
Task: "Verify repository permissions for Actions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (secrets/variables)
2. Complete Phase 2: Foundational (agent prompt + workflow)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Agent reviews PR and posts comment
5. Deploy to production if ready

### Incremental Delivery

1. Setup + Foundational → Agent infrastructure ready
2. Add User Story 1 → Test independently → Agent makes edits + comments (MVP!)
3. Add User Story 2 → Test independently → Quality scores work
4. Add User Story 3 → Test independently → @claude interaction works
5. Add User Story 4 → Test independently → Living documents work
6. Polish → Documentation complete

### Critical Path

```
Setup → Foundational → US1 (MVP) → US2 → US3 → Polish
                          ↓
                         US4 (can parallel with US2/US3)
```

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 37 |
| Setup Tasks | 3 |
| Foundational Tasks | 4 |
| US1 Tasks | 6 |
| US2 Tasks | 5 |
| US3 Tasks | 6 |
| US4 Tasks | 6 |
| Polish Tasks | 7 |
| Parallel Opportunities | 8 tasks |
| MVP Scope | Phases 1-3 (T001-T013) |

---

## Notes

- [P] tasks = different files/settings, no dependencies
- [Story] label maps task to specific user story for traceability
- Most tasks are configuration/testing rather than code development
- Agent behavior controlled by prompt in `.claude/agents/editorial-reviewer.md`
- No custom Python code required - using `claude-code-action` directly
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
