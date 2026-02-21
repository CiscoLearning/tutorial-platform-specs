# PR #183 Analysis: tc-harden-linux

**PR Title:** tc-harden-linux
**Tutorial:** Harden Your Linux Server with Open-Source Tools and Best Practices
**Editor:** jlauterb-edit (Jill)
**Commits Analyzed:** 14 commits
**Date Analyzed:** 2026-02-20

---

## Summary of Changes by Category

| Category | Count | Description |
|----------|-------|-------------|
| Heading Style | 12+ | `## Heading` converted to `**Heading**` (bold paragraph style) |
| Hyphenation | 8+ | Compound adjective hyphenation (open-source, command-line, etc.) |
| List Formatting | 15+ | Paragraphs converted to bullet lists; bold removed from bullets |
| Punctuation | 10+ | Colon removal after headings; em dash normalization |
| Article Usage | 8+ | Adding "the" before nouns (the current, the SSH, the password) |
| Acronym Expansion | 1 | CIS expanded to "Center for Internet Security" |
| Serial Comma | 5+ | Adding "and" before final list item |
| Minor Typos | 2 | "Suppor" to "Support", period after sentences |

---

## Detailed Rules Analysis

### 1. HEADING STYLE - Inline Bold vs H2/H3 Headers (NEW PATTERN)

**Status:** NEW - Not in current agent prompt

Throughout the tutorial, Jill systematically converted markdown headers (`##`) to bold text (`**...**`). This is a significant pattern not previously documented.

| Before | After |
|--------|-------|
| `## Why CIS Benchmarks Matter` | `**Why CIS Benchmarks Matter**` |
| `## Understand Your Baseline System` | `**Understand Your Baseline System**` |
| `## Install and Run Lynis Security Auditing Tool` | `**Install and Run the Lynis Security Auditing Tool**` |
| `## Analyze Current SSH Configuration` | `**Analyze the Current SSH Configuration**` |

**Note:** This appears to be a stylistic preference for subsections within steps. The tutorial already has a top-level step structure, and sub-headers become bold paragraphs.

**Query from editor:** This wasn't flagged as a query, suggesting it's an established style rule.

---

### 2. HYPHENATION - Compound Adjectives (PARTIALLY NEW)

**Status:** PARTIALLY NEW - "open-source" and "command-line" not in current rules

| Before | After | Context |
|--------|-------|---------|
| open source tools | open-source tools | Adjective before noun |
| open source security tools | open-source security tools | Adjective before noun |
| command line operations | command-line operations | Adjective before noun |
| quick scan mode | quick-scan mode | Adjective before noun |
| brute force attacks | brute-force attacks | Adjective before noun |

**Rule:** When a compound modifier (two words working together as an adjective) appears BEFORE a noun, it should be hyphenated.

**Exceptions observed:**
- "client-server model" - consistent with hyphenation rule
- "Long-Term Support" - standard LTS expansion

---

### 3. ARTICLE INSERTION - Adding "the" Before Nouns (NEW PATTERN)

**Status:** NEW - Not in current agent prompt

Jill consistently added the definite article "the" before specific nouns in procedural contexts.

| Before | After |
|--------|-------|
| Install and Run Lynis Security Auditing Tool | Install and Run **the** Lynis Security Auditing Tool |
| Analyze Current SSH Configuration | Analyze **the** Current SSH Configuration |
| Validate SSH Configuration | Validate **the** SSH Configuration |
| Test SSH Connection on New Port | Test **the** SSH Connection on the New Port |
| Verify SSH Security Improvements | Verify **the** SSH Security Improvements |
| Perform Initial Security Assessment | Perform **an** Initial Security Assessment |
| Create Configuration Backup | Create **a** Configuration Backup |

**Rule:** Procedural headings should include articles (a/an/the) for natural reading flow.

---

### 4. BOLD REMOVAL FROM LIST ITEMS (NEW PATTERN)

**Status:** NEW - Not explicitly in current agent prompt

Jill systematically removed bold formatting from category headers within bulleted lists.

**Before:**
```markdown
**Port Change Benefits:**

- **Significantly reduces automated attacks** since most bots target default port 22.
- **Eliminates script kiddie attempts** using common vulnerability scanners.
```

**After:**
```markdown
Port change benefits:

- Significantly reduces automated attacks since most bots target default port 22.
- Eliminates script kiddie attempts using common vulnerability scanners.
```

**Rule:** List items should not have bold text for emphasis. Bold is reserved for GUI elements with direct instructions.

---

### 5. COLON AFTER HEADINGS - Removal Pattern (NEW PATTERN)

**Status:** NEW - Not in current agent prompt

Colons were removed from the end of headings/subheadings.

| Before | After |
|--------|-------|
| `**Baseline Requirements:**` | `**Baseline Requirements**` |
| `**Port Change Benefits:**` | `Port change benefits:` (converted to intro line) |
| `**Authentication Hardening:**` | `Authentication hardening:` |

**Rule:** Bold headings/subheadings should not end with colons. However, when converted to intro lines for lists, they can end with colons.

---

### 6. PARAGRAPH TO LIST CONVERSION (ENHANCEMENT)

**Status:** PARTIALLY DOCUMENTED - "procedural introduction" is documented, but conversion pattern is new

Jill converted paragraph-style content into bulleted lists for better scannability.

**Before:**
```markdown
**Lynis** provides comprehensive security auditing capabilities...

**Fail2Ban** offers dynamic intrusion prevention...

**Uncomplicated Firewall (UFW)** simplifies iptables management...
```

**After:**
```markdown
- **Lynis** provides comprehensive security auditing capabilities...

- **Fail2Ban** offers dynamic intrusion prevention...

- **Uncomplicated Firewall (UFW)** simplifies iptables management...
```

**Rule:** When content presents a series of related concepts (especially tools or features), convert to a bulleted list format.

---

### 7. EM DASH USAGE (DOCUMENTED, BUT NEW CONTEXT)

**Status:** DOCUMENTED - Em dash without spaces is in current rules

| Before | After |
|--------|-------|
| `This is normal behavior - logs are created` | `This is normal behavior—logs are created` |

Additional context: Hyphens used as dashes should be converted to proper em dashes without spaces.

---

### 8. PERIOD AFTER SENTENCES INTRODUCING LISTS (NEW PATTERN)

**Status:** NEW - Not in current agent prompt

| Before | After |
|--------|-------|
| `...baseline configuration:` | `...baseline configuration.` |
| `...security baseline:` | `...security baseline.` |
| `...attack vectors:` | `...attack vectors.` |

**Rule:** When a sentence introduces a list or subsequent content, end with a period (not a colon) if the sentence is complete on its own.

---

### 9. SERIAL COMMA / LIST ITEM CONNECTOR (DOCUMENTED)

**Status:** DOCUMENTED

| Before | After |
|--------|-------|
| `curl, wget, vim, git, htop, tree, unzip, bash-completion` | `curl, wget, vim, git, htop, tree, unzip, and bash-completion` |

**Rule:** Add "and" before the final item in a list.

---

### 10. NUMBER FORMATTING (DOCUMENTED)

**Status:** DOCUMENTED in editorial style

| Before | After |
|--------|-------|
| `3 months` | `three months` |

**Rule:** Spell out numbers under 10 in prose (not in code/technical contexts).

---

### 11. LIST ITEM PUNCTUATION (NEW PATTERN)

**Status:** NEW - Not in current agent prompt

Jill added periods to the end of list items that are complete sentences.

| Before | After |
|--------|-------|
| `- Complete audit trail of all authentication attempts and successes` | `- Complete audit trail of all authentication attempts and successes.` |
| `- Privilege escalation tracking through dedicated sudo and su logging` | `- Privilege escalation tracking through dedicated sudo and su logging.` |

**Rule:** List items that are complete sentences should end with periods.

---

## Queries Raised by Editor

Jill raised multiple queries in commit messages asking for author input:

1. **Code Styling Queries:**
   - Should "rsyslog", "sudo", "iptables", "syslog", "setfacl", "umask", "auditd" be styled as code?
   - Should configuration terms in lists be styled as code?

2. **Heading Style Queries:**
   - Should lines 177, 183, 188, etc. remove heading style or colon?

3. **Symbol Handling:**
   - Should we remove or replace the bullet symbol before "ssh.service"?

4. **Acronym Consistency:**
   - Should "dccp, sctp, rds, tipc" be "DCCP, SCTP, RDS and TIPC"?
   - Should "Auditd" be "auditd" and styled as code?

5. **Acronym Expansion:**
   - UFW: Is it "Uncomplicated Firewall" or "Ubuntu Firewall"?

---

## NEW Rules Not in Current Agent Prompt

| Rule ID | Rule Description | Priority | Examples |
|---------|------------------|----------|----------|
| HEADING-002 | Convert `## Heading` to `**Heading**` for subsections within steps | Medium | `## Install Tool` -> `**Install the Tool**` |
| ARTICLE-001 | Add articles (a/an/the) to procedural headings | Medium | "Analyze Configuration" -> "Analyze the Configuration" |
| BOLD-002 | Remove bold from list items; bold is for GUI elements only | High | `- **Item**` -> `- Item` |
| HYPHEN-002 | Hyphenate compound adjectives before nouns (open-source, command-line) | Medium | "open source tools" -> "open-source tools" |
| COLON-001 | Remove colons from bold headings | Low | `**Title:**` -> `**Title**` |
| PERIOD-001 | End complete sentences introducing lists with periods, not colons | Low | "...configuration:" -> "...configuration." |
| LIST-PUNCT-001 | Complete sentence list items should end with periods | Medium | "- Item text" -> "- Item text." |
| PARAGRAPH-LIST-001 | Convert parallel paragraphs about related items into bullet lists | Low | Tool descriptions -> bulleted list |

---

## Agent Coverage Assessment

### Rules the Agent WOULD Catch (~40%)

| Rule | Coverage | Notes |
|------|----------|-------|
| Acronym expansion (CIS) | Full | Already in agent prompt |
| Em dash spacing | Full | Already documented |
| Serial comma | Full | Already documented |
| "click on" usage | Full | Already documented |
| Cisco product naming | Full | Not applicable to this tutorial |

### Rules the Agent WOULD PARTIALLY Catch (~25%)

| Rule | Coverage | Notes |
|------|----------|-------|
| Hyphenation | Partial | "client-server" documented; "open-source" not |
| List introduction | Partial | Intro lines documented; period vs colon not |
| Bold for emphasis | Partial | General rule exists; list item context new |

### Rules the Agent WOULD NOT Catch (~35%)

| Rule | Coverage | Notes |
|------|----------|-------|
| Heading to bold conversion | None | New pattern |
| Article insertion in headings | None | New pattern |
| List item punctuation | None | New pattern |
| Paragraph to list conversion | None | Requires judgment |
| Code styling decisions | None | Requires author input (queries) |

---

## Recommendations

1. **Add HEADING-002 rule**: Document the pattern of converting `## Heading` to `**Heading**` for in-step subsections.

2. **Add ARTICLE-001 rule**: Procedural headings should include articles for natural flow.

3. **Add BOLD-002 rule**: Clarify that bold in list items is incorrect except for GUI elements.

4. **Add HYPHEN-002 rule**: Add "open-source" and "command-line" to the hyphenation examples.

5. **Add LIST-PUNCT-001 rule**: Complete sentence list items require ending punctuation.

6. **Add to Query Patterns**: Code styling for technical terms (commands, config files, daemons) should be flagged as queries requiring author input.

---

## Summary Statistics

- **Total distinct patterns observed:** 11
- **Patterns already documented:** 4 (36%)
- **Patterns partially documented:** 3 (27%)
- **NEW patterns not documented:** 4 (36%)
- **Estimated agent catch rate:** 40-50%

The agent would catch basic issues but miss the more nuanced structural edits (heading conversion, article insertion, list formatting). These structural changes represent a significant portion of editorial work.

---

*Analysis generated from PR #183 commit history*
