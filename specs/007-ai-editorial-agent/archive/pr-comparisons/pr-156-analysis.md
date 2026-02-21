# PR #156 Editorial Analysis: tc-radius-ise

## PR Overview

| Field | Value |
|-------|-------|
| **PR Title** | tc-radius-ise |
| **Tutorial** | RADIUS on ISE |
| **Description** | New RADIUS ISE tutorial ready for review |
| **Editor** | jlauterb-edit (Jill) |
| **Editor Commits** | 24 |
| **Analysis Date** | 2026-02-20 |

## Summary of Changes by Category

| Category | Count | % of Total | Agent Coverage |
|----------|-------|------------|----------------|
| Product Naming/Branding | 12 | 18% | Partial |
| Standard Formatting (802.1X) | 8 | 12% | Yes |
| Number Spelling | 3 | 5% | No |
| Code Style vs Plain Text | 15 | 23% | Partial |
| Terminology (ISE box -> server) | 10 | 15% | Yes |
| Grammar/Clarity | 8 | 12% | Partial |
| Punctuation | 5 | 8% | Yes |
| Parallel Structure | 5 | 8% | No |

**Estimated Agent Coverage: 55-60%**

---

## Detailed Rules Found

### 1. Standard Technical Formatting: 802.1x -> 802.1X

**Status:** DOCUMENTED (in editorial-style-guide.md, technical term formatting)

| Before | After |
|--------|-------|
| `802.1x` | `802.1X` |

**Occurrences:** 8+ across multiple steps

**Assessment:** Our agent should catch this. This is a standard capitalization rule.

---

### 2. Number Spelling: Digits to Words

**Status:** NEW RULE - NOT DOCUMENTED

| Before | After |
|--------|-------|
| "offer 3 AAA services" | "offer three services, commonly known as AAA" |
| "respond back in 3 different way" | "respond back in three different ways" |

**Pattern:** Single-digit numbers (1-9) should be spelled out in prose text.

**Recommendation:** Add rule TERM-003:
```yaml
- id: TERM-003
  category: TERM
  severity: LOW
  pattern: "\\b[1-9]\\b(?!\\d)"
  check_type: ai  # Needs context - not in code blocks, port numbers, etc.
  message_template: "Single-digit number should be spelled out in prose"
  fix_suggestion: "Use 'three' instead of '3' in narrative text"
  fix_type: AI
  source: Jill
```

---

### 3. Code Style for Non-Code Content

**Status:** PARTIALLY DOCUMENTED (BOLD-001 mentions context)

**Pattern:** Code backticks used for emphasis instead of bold or plain text.

| Before | After |
|--------|-------|
| `` `three services` `` | `three services` (plain text) |
| `` `AAA` `` | `**AAA**` (bold for acronym) |
| `` `A`uthentication `` | `Authentication` (plain text) |
| `` `four ports` `` | `four ports` (plain text) |
| `` `1812` `` (port number in prose) | `1812` (plain text) |

**Key Insight:** Code backticks should ONLY be used for:
- CLI commands: `aaa new-model`
- Configuration snippets: `test aaa`
- File names and paths

**Should NOT use code backticks for:**
- Numbers in prose
- Regular English words for emphasis
- Acronyms (use bold instead)
- Port numbers in prose context

**Recommendation:** Enhance rule CODE-001:
```yaml
- id: CODE-001
  category: BOLD
  severity: MEDIUM
  check_type: ai
  message_template: "Code backticks used for non-code content"
  fix_suggestion: "Use plain text or bold for emphasis; code is for CLI/config only"
  fix_type: AI
  source: Jill
```

---

### 4. Terminology: "ISE box" -> "ISE server"

**Status:** DOCUMENTED (TERM-001)

| Before | After |
|--------|-------|
| "ISE box" | "ISE server" |
| "ISE Box" | "ISE server" |

**Occurrences:** 10+ across all steps

**Assessment:** Fully covered by existing rule.

---

### 5. Terminology: "client/server" -> "client-server"

**Status:** DOCUMENTED (TERM-002)

| Before | After |
|--------|-------|
| "client/server model" | "client-server model" |

**Assessment:** Fully covered by existing rule.

---

### 6. Acronym Expansion: Expand on First Use

**Status:** DOCUMENTED (ACRONYM-001)

| Before | After |
|--------|-------|
| "ISE" (first use) | "Identity Services Engine (ISE)" |
| "SD-Access" (first use) | "Software-Defined Access (SD-Access)" |
| "UDP" (first use) | "User Datagram Protocol (UDP)" |
| "NAS" (first use) | "Network Access Server (NAS)" |
| "MFA" (first use) | "multifactor authentication (MFA)" |
| "ACL" (first use) | "access control lists (ACLs)" |
| "VLAN" (first use) | "VLANs" (plural noted) |
| "SGT" (first use) | "Security Group Tags (SGTs)" |

**Assessment:** Fully covered. Note that Jill expands many networking acronyms that technical audiences might know.

---

### 7. Case Sensitivity: "Radius" -> "RADIUS"

**Status:** PARTIALLY DOCUMENTED (product naming)

| Before | After |
|--------|-------|
| "Radius" | "RADIUS" |
| "Radius protocol" | "RADIUS protocol" |

**Occurrences:** 20+ across tutorial

**Pattern:** Protocol acronyms must be ALL CAPS consistently.

**Recommendation:** Add rule TERM-004:
```yaml
- id: TERM-004
  category: TERM
  severity: HIGH
  pattern: "\\b(Radius|radius)\\b(?! server)"
  message_template: "RADIUS should be all caps"
  fix_suggestion: "Change 'Radius' to 'RADIUS'"
  fix_type: AUTO
  source: Jill
```

---

### 8. Hyphenation Rules

**Status:** NEW RULES - NOT FULLY DOCUMENTED

| Before | After |
|--------|-------|
| "Dial In User Service" | "Dial-In User Service" |
| "dial-up" | "dial-up" (correct) |
| "widely-used" | "widely used" (adverb+adj) |
| "dotcom boom" / "Dot-com boom" | "dot-com boom" |
| "Clear-Text" | "cleartext" |
| "ease dropper" | "eavesdropper" |

**Pattern 1:** Compound modifiers before nouns get hyphens (Dial-In)
**Pattern 2:** Adverb-adjective combinations after verb don't get hyphens ("widely used")
**Pattern 3:** "cleartext" is one word, lowercase

**Recommendation:** Add rule TERM-005:
```yaml
- id: TERM-005
  category: TERM
  severity: LOW
  pattern: "\\b(Clear-Text|clear-text)\\b"
  message_template: "Use 'cleartext' as one word"
  fix_suggestion: "Change 'Clear-Text' to 'cleartext'"
  fix_type: AUTO
  source: Jill
```

---

### 9. Word Choice Improvements

**Status:** PARTIALLY DOCUMENTED

| Before | After |
|--------|-------|
| "go between" | "intermediary" |
| "As your can see" | "As you can see" (typo) |
| "ease dropper" | "eavesdropper" |
| "image before this" | "prior image" |
| "looking at" | "In the list of" |
| "and so forth" | (varies - sometimes removed) |

**Assessment:** These are grammar/word choice that AI should catch but require contextual analysis.

---

### 10. Parallel Structure in Lists

**Status:** NEW RULE - NOT DOCUMENTED

**Before:**
```markdown
- Console, Secure Shell (SSH), or Telnet access to the switch:
- Enable password:
- 802.1X authentication:
- EXEC shell control from RADIUS:
- VLAN assignment from RADIUS, and other service controls:
```

**After:**
```markdown
- To configure authentication for the console, Secure Shell (SSH), or Telnet access to the switch:
- To enable the password for authentication:
- To configure for 802.1X authentication:
- To configure for authorization of EXEC shell control from RADIUS:
- To enable VLAN assignment from RADIUS and other service controls:
```

**Pattern:** When list items are introductions to code blocks/procedures, they should all start with "To [verb]..." for parallel structure.

**Recommendation:** Add rule PROC-002:
```yaml
- id: PROC-002
  category: PROC
  severity: MEDIUM
  check_type: ai
  message_template: "List items not parallel in structure"
  fix_suggestion: "Make list items start with consistent grammatical structure"
  fix_type: AI
  source: Jill
```

---

### 11. RFC and Standard Formatting

**Status:** NEW RULE - NOT DOCUMENTED

| Before | After |
|--------|-------|
| "RFC 6614 titled **Transport Layer Security (TLS) Encryption for RADIUS**" | "RFC 6614, titled _**Transport Layer Security (TLS) Encryption for RADIUS**_" |
| "RFC 6614, also known as RADSEC" | "RFC 6614, also known as RadSec" |

**Pattern 1:** RFC titles should be italicized (with or without bold)
**Pattern 2:** "RadSec" uses camelCase, not "RADSEC"

**Recommendation:** Add rule TERM-006:
```yaml
- id: TERM-006
  category: TERM
  severity: LOW
  check_type: ai
  message_template: "RFC title formatting"
  fix_suggestion: "RFC titles should be italicized: _RFC 6614: Title_"
  fix_type: AI
  source: Jill
```

---

### 12. Attribute-Value Pair Terminology

**Status:** NEW RULE - DOMAIN SPECIFIC

| Before | After |
|--------|-------|
| "AV Pairs" | "Attribute-Value Pairs (AVPs)" on first use, then "AVPs" |
| "AV Pair format" | "AVP format" |
| "number 2" / "number 3" | "Attribute 2" / "Attribute 3" |

**Pattern:** Use consistent terminology for RADIUS attributes.

---

### 13. List Formatting in Technical Context

**Status:** NEW INSIGHT

| Before | After |
|--------|-------|
| `Username = sam` (plain) | `- \`Username = sam\`` (bullet + code) |
| Inline list | Bullet list with code formatting |

**Pattern:** Example values that resemble key=value pairs should be in code blocks within bulleted lists.

---

### 14. Duration Mismatch Flagging

**Status:** DOCUMENTED (DUR-001)

Jill flagged: "Steps' time stamps (22 min) do not add up to the 35-min duration."

**Assessment:** Fully covered by existing rule.

---

## NEW Rules to Add (Not Currently Documented)

| Rule ID | Pattern | Priority | Description |
|---------|---------|----------|-------------|
| TERM-003 | Single-digit numbers | LOW | Spell out 1-9 in prose |
| TERM-004 | Radius -> RADIUS | HIGH | Protocol acronyms all caps |
| TERM-005 | Clear-Text -> cleartext | LOW | Single word, lowercase |
| TERM-006 | RFC title formatting | LOW | Italicize RFC titles |
| PROC-002 | Parallel list structure | MEDIUM | "To [verb]..." consistency |
| CODE-001 | Code backticks for non-code | MEDIUM | Backticks only for CLI/config |

---

## Agent Coverage Assessment

### Rules Our Agent WILL Catch (55%):
1. 802.1x -> 802.1X (documented)
2. ISE box -> ISE server (TERM-001)
3. client/server -> client-server (TERM-002)
4. Acronym expansion (ACRONYM-001)
5. Em dash spacing (PUNCT-001)
6. Duration mismatch (DUR-001)
7. Procedural introduction lines (PROC-001)

### Rules Our Agent MIGHT Catch with Enhancement (25%):
1. Code backticks for emphasis (needs CODE-001 rule)
2. Parallel structure (needs PROC-002 rule)
3. Word choice improvements (general AI capability)
4. Grammar errors like "your" vs "you" (general AI capability)

### Rules Our Agent Will NOT Catch Without New Rules (20%):
1. Number spelling (3 -> three)
2. Radius -> RADIUS case sensitivity
3. cleartext vs Clear-Text
4. RFC title formatting
5. Domain-specific terminology (AVP, attribute numbering)

---

## Recommendations

### High Priority
1. **Add TERM-004:** Enforce RADIUS (all caps) consistently
2. **Add CODE-001:** Flag code backticks on non-code content
3. **Add PROC-002:** Check for parallel structure in lists

### Medium Priority
4. **Add TERM-003:** Spell out single-digit numbers
5. **Add TERM-005:** cleartext as one word
6. Enhance AI prompts to catch basic grammar (your/you)

### Low Priority
7. **Add TERM-006:** RFC title italicization
8. Domain-specific RADIUS terminology guidance

---

## Sample Editor Query Patterns

Jill frequently uses "QUERY:" in commit messages to ask the author questions:

1. "Should it be 'Cisco RADIUS' or 'RADIUS'?"
2. "Should we change all instances of 'ISE box' to 'ISE server'?"
3. "Should the following list be set in a table?"
4. "Should we change the boldfaced headings into numbered steps?"
5. "Duration mismatch - steps (22 min) vs sidecar (35 min)"

**Insight:** Our agent could flag these as queries for author consideration rather than automatic fixes.
