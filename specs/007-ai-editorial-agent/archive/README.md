# Archive - AI Editorial Agent

This directory contains intermediate work products from the FR-7 AI Editorial Agent development.

## Contents

### pr-comparisons/

Individual PR analysis files comparing human editor changes vs AI agent detection.

**Superseded by:** `tutorial-testing/analysis/v2-official-rules/`

The v2 analysis uses official Cisco Style Guide rules (75+ terms) instead of inferred rules, providing more accurate coverage estimates (~75% vs ~52%).

### reference-data/

Raw JSON lines files containing editor comments:
- `jlauterb_comments.jsonl` - Jill's comments
- `masperli_comments.jsonl` - Matt's comments

**Summarized in:** `../editor-comments-reference.md`

### test-tutorial/

Test fixtures used during development:
- `test-step-1.md` - Sample tutorial step with intentional issues
- `expected-issues.md` - Expected detection results

### human-vs-agent-comparison.md

Early comparison analysis using inferred rules.

**Superseded by:** `tutorial-testing/analysis/v2-official-rules/COMPARISON-REPORT.md`

### validation-report.md

Intermediate validation report from testing.

**Superseded by:** `tutorial-testing/analysis/v2-official-rules/summary.json`

---

## Why Keep This?

These files document the development journey:
1. Started with mining editor comments (reference-data/)
2. Tested against PRs with inferred rules (pr-comparisons/)
3. Discovered ~52% coverage was insufficient
4. Parsed official Cisco Style Guide
5. Achieved ~75% coverage with official rules

The final, authoritative analysis is in `tutorial-testing/analysis/v2-official-rules/`.
