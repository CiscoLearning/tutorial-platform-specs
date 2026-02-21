# PR Comparison Summary: Key Editorial Patterns

**Date:** 2026-02-20
**PRs Analyzed:** 16 (Phase 1: 156, 119, 133, 181, 195, 194, 183, 209 | Phase 2: 196, 201, 184, 189, 193, 173, 174, 191)
**Total Editor Commits:** 260+

---

## Coverage Assessment Across All PRs

### Phase 1 PRs (Original Analysis - Before Tier 1 Implementation)

| PR | Editor | Tutorial | Commits | Agent Coverage |
|----|--------|----------|---------|----------------|
| #156 | Jill | tc-radius-ise | 24 | 55-60% |
| #119 | Matt | tc-appd-information-points | 19 | 40% |
| #133 | Matt | tc-intro-umbrella | 14 | 65-70% |
| #181 | Jill | tc-train-serve | 17 | 65-70% |
| #195 | Matt | tc-sonic-bgp | 16 | 70% |
| #194 | Jill | tc-ocsf14-secdata | 16 | 55-65% |
| #183 | Jill | tc-harden-linux | 14 | 40-50% |
| #209 | Jill | UCS AI Sizer Tool | 20 | 55-60% |

**Phase 1 Average: 55-60%**

### Phase 2 PRs (With Tier 1 Rules Implemented)

| PR | Editor | Tutorial | Commits | Agent Coverage | Notes |
|----|--------|----------|---------|----------------|-------|
| #196 | Matt+Jill | tc-flask-restx-rbac | 29 | **15%** | Gerund headings biggest gap |
| #201 | Jill | tc-wifi7-iosxe | 20 | **55-60%** | Good match for existing rules |
| #184 | Jill | tc-langchain-simple-chat | 16 | **35-55%** | AI/ML tutorial, different patterns |
| #189 | Jill | tc-beef-basics | 14 | **40%** | Security tutorial |
| #193 | Matt | tc-deploy-llm-openshift | 14 | **30%** | LLM deployment, new patterns |
| #173 | Jill | tc-netconf | 13 | **37%** | Networking tutorial |
| #174 | Jill | tc-sonic-mlag | 11 | **15%** | Many bold-to-code changes |
| #191 | Jill | tc-langchain-local-ai | 10 | **20-25%** | AI tutorial, Tier 1 rules not applicable |

**Phase 2 Average: 30-35%** (lower than expected!)

---

## Critical Finding: Tier 1 Rules Not Broad Enough

The Tier 1 rules implemented were too narrowly focused on networking patterns. The **biggest coverage gaps** across all PRs are:

### TOP 5 Missing Rules (by frequency across ALL 16 PRs)

| Rank | Rule | PRs Found | Est. Occurrences | Currently Implemented? |
|------|------|-----------|------------------|------------------------|
| 1 | **Gerund → Imperative headings** | 14/16 | 200+ | NO |
| 2 | **Bold list items → Plain** | 12/16 | 150+ | NO |
| 3 | **Heading articles (add "the")** | 10/16 | 100+ | NO |
| 4 | **Unit spacing (8GB → 8 GB)** | 8/16 | 60+ | NO |
| 5 | **Bold → Code for CLI/paths** | 8/16 | 50+ | NO |

### Why Phase 2 Coverage is Lower

1. **Tutorial type mismatch**: Tier 1 rules target networking (RADIUS, iBGP). AI/ML tutorials have none of these.
2. **Gerund headings everywhere**: `**Installing Dependencies**` → `**Install Dependencies**` is THE most common edit but NOT automated.
3. **Universal patterns missing**: Unit spacing, heading articles apply to ALL tutorials but weren't in Tier 1.

---

## Updated Rule Priorities

### CRITICAL PRIORITY (Universal - Add Immediately)

These rules apply to ALL tutorials, not just networking:

| Rule ID | Rule | Example | PRs Found |
|---------|------|---------|-----------|
| **GERUND-001** | Gerund → Imperative in headings | `**Installing X**` → `**Install X**` | 14/16 |
| **LIST-BOLD-001** | Remove bold from list item terms | `- **Term:** desc` → `- Term: desc` | 12/16 |
| **ARTICLE-HEAD-001** | Add articles to headings | `**Install Software**` → `**Install the Software**` | 10/16 |
| **UNIT-SPACE-001** | Space between number and unit | `8GB` → `8 GB` | 8/16 |
| **BOLD-CODE-001** | Code font for paths/CLI | `**/etc/sonic/**` → `` `/etc/sonic/` `` | 8/16 |

### HIGH PRIORITY (Existing Tier 1 - Keep)

| Rule ID | Rule | Example | PRs Found |
|---------|------|---------|-----------|
| COMPOUND-001 | life cycle (two words) | `lifecycle` → `life cycle` | 4/16 |
| CONTRACT-001 | No contractions | `it's` → `it is` | 6/16 |
| PROTOCOL-001 | Protocol names caps | `Radius` → `RADIUS` | 3/16 |
| FEAT-001 | Feature names lowercase | `Business Transactions` → `business transactions` | 5/16 |
| H3-BOLD-001 | H3 → Bold in steps | `### Title` → `**Title**` | 8/16 |

### MEDIUM PRIORITY (Tier 2 - Add Soon)

| Rule ID | Rule | Example | PRs Found |
|---------|------|---------|-----------|
| COMPOUND-PREFIX-001 | Prefix compounds closed | `pre-built` → `prebuilt`, `non-root` → `nonroot` | 6/16 |
| COMPOUND-LY-001 | No hyphen after -ly | `highly-optimized` → `highly optimized` | 4/16 |
| BOLD-ITALIC-001 | Italics for status text | `**Error**` → `*Error*` (display text) | 3/16 |
| DATASTORE-001 | datastore (one word) | `data store` → `datastore` | 2/16 |
| IEEE-001 | IEEE standard casing | `802.1x` → `802.1X` | 2/16 |

### NETWORKING-SPECIFIC (Apply Conditionally)

| Rule ID | Rule | Example | When to Apply |
|---------|------|---------|---------------|
| BGP-001 | iBGP/eBGP caps | `iBGP` → `IBGP` | BGP tutorials only |
| USING-001 | "by using" construction | `configure using` → `configure by using` | All |
| RFC-001 | RFC formatting | `RFC-8212` → `IETF RFC 8212` | Networking |
| ROUTER-ID-001 | router ID (two words) | `router-ID` → `router ID` | BGP/OSPF |

---

## Updated Coverage Projection

| Stage | Coverage | Notes |
|-------|----------|-------|
| Current (Tier 1 only) | 30-35% | Too networking-focused |
| + CRITICAL rules | **55-65%** | Universal rules add most value |
| + HIGH rules | **65-75%** | Combined with existing |
| + MEDIUM rules | **75-85%** | Comprehensive coverage |
| + Networking-specific | **80-90%** | Full coverage for tech domain |

---

## Pattern Frequency Analysis (All 16 PRs)

| Pattern | PRs Found | Total Occurrences | Category |
|---------|-----------|-------------------|----------|
| Gerund → Imperative headings | 14/16 | 200+ | CRITICAL |
| Acronym expansion | 16/16 | 150+ | Existing |
| Bold list items → Plain | 12/16 | 150+ | CRITICAL |
| Heading articles | 10/16 | 100+ | CRITICAL |
| Bold for GUI elements | 12/16 | 80+ | Existing |
| Unit spacing | 8/16 | 60+ | CRITICAL |
| Bold → Code for paths | 8/16 | 50+ | CRITICAL |
| Compound words | 8/16 | 40+ | HIGH |
| H3 → Bold conversion | 8/16 | 35+ | HIGH |
| Contractions | 6/16 | 25+ | HIGH |
| "by using" construction | 4/16 | 25+ | MEDIUM |
| Protocol caps | 3/16 | 15+ | NETWORKING |

---

## Editor-Specific Patterns

### Matt (masperli) - PRs #119, #133, #195, #193, #196

**Distinctive patterns:**
1. Detailed PR comments citing specific Cisco style rules with dates ("since 2008")
2. Product EOL/rebranding awareness (Cisco Roaming Client → Cisco Secure Client)
3. Legal/trademark considerations
4. "by using" construction preference
5. iBGP/eBGP → IBGP/EBGP enforcement
6. RFC formatting (IETF prefix, space not hyphen)
7. Content sensitivity notes (avoid political questions in examples)

### Jill (jlauterb-edit) - PRs #156, #181, #194, #183, #209, #201, #184, #189, #173, #174, #191

**Distinctive patterns:**
1. Step-by-step commit format with line-by-line changes
2. QUERY sections for author decisions
3. H2/H3 → Bold subsection conversion
4. Compound word enforcement
5. List formatting consistency (bold removal, punctuation)
6. Definition list formatting
7. Duration verification (step times vs total)
8. Unit spacing enforcement
9. Heading article insertion

---

## Files in This Directory

### Phase 1 Analyses
| File | PR | Editor | Focus |
|------|-----|--------|-------|
| pr-119-analysis.md | #119 | Matt | AppDynamics, feature lowercase |
| pr-133-analysis.md | #133 | Matt | Umbrella trademark, EOL |
| pr-156-analysis.md | #156 | Jill | RADIUS, compound numbers |
| pr-181-analysis.md | #181 | Jill | OpenShift AI, compound words |
| pr-183-analysis.md | #183 | Jill | Linux hardening, H3→Bold |
| pr-194-analysis.md | #194 | Jill | OCSF, FTD/FMC full replacement |
| pr-195-analysis.md | #195 | Matt | SONiC BGP, "by using" |
| pr-209-analysis.md | #209 | Jill | UCS AI Sizer, product consistency |

### Phase 2 Analyses
| File | PR | Editor | Focus |
|------|-----|--------|-------|
| pr-173-analysis.md | #173 | Jill | NETCONF, datastore compound |
| pr-174-analysis.md | #174 | Jill | SONiC MLAG, bold→code |
| pr-184-analysis.md | #184 | Jill | LangChain chat, bold→italic |
| pr-189-analysis.md | #189 | Jill | BeEF basics, UI formatting |
| pr-191-analysis.md | #191 | Jill | LangChain local AI, unit spacing |
| pr-193-analysis.md | #193 | Matt | LLM OpenShift, step→topic |
| pr-196-analysis.md | #196 | Both | Flask RESTX, gerund headings |
| pr-201-analysis.md | #201 | Jill | Wi-Fi 7, tech hyphenation |

---

## Recommendations

### Immediate Action (This Week)

1. **Add gerund → imperative heading rule** - Single biggest impact
2. **Add bold list item removal** - Very common pattern
3. **Add heading article insertion** - Universal pattern
4. **Add unit spacing rule** - Easy to implement, common

### Short-Term (Next Sprint)

5. **Add bold → code for paths/CLI** - Technical accuracy
6. **Expand compound word rules** - prebuilt, nonroot, systemwide
7. **Add -ly adverb rule** - No hyphen after -ly adverbs

### Medium-Term (Future Iteration)

8. **Add italic for display text** - Bold vs italic distinction
9. **Add IEEE standard casing** - 802.1X, 802.11ac
10. **Add datastore compound** - Network tutorials

---

## Key Insight

**The original Tier 1 rules were too narrowly focused on networking patterns (RADIUS, iBGP, "by using").**

The rules that would provide the MOST value are **universal patterns** that apply to ALL tutorials:
- Gerund headings
- Bold list removal
- Heading articles
- Unit spacing

These should be implemented BEFORE the networking-specific rules.

---

*Updated 2026-02-20 after Phase 2 analysis (8 additional PRs)*
