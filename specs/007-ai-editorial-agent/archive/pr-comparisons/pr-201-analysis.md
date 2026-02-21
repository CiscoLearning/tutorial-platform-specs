# PR #201 Editorial Analysis

**PR:** [#201](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/201) - Wi-Fi 7 on Cisco IOS XE Tutorial
**Editor:** Jill Lauterborn (jlauterb-edit)
**Date:** November 15-17, 2025
**Tutorial:** tc-wifi7-iosxe

---

## Summary Table of Editorial Changes

| Rule Category | Count | Agent Would Catch | Notes |
|---------------|-------|-------------------|-------|
| Colon vs Period in Lists | 12 | Yes (Tier 1) | `:` after bold terms in lists |
| Acronym Management | 15+ | Partial | Remove expansion after first use |
| Technical Format Consistency | 10+ | Yes (New Rule) | GCMP256 → GCMP-256, AES 128 → AES-128 |
| Sentence End Punctuation | 8 | Yes (Tier 1) | Missing periods in list items |
| Title Case in Labels | 5 | Yes (Tier 2) | "Enabling Wi-Fi 7 globally" → "Enable Wi-Fi 7 Globally" |
| Code to Bold Conversion | 8 | Partial | UI elements: code → bold |
| "by using" Construction | 0 | N/A | Not found in this PR |
| Contractions | 0 | N/A | None found to correct |
| Protocol Name Caps | 0 | N/A | No Radius/iBGP issues |
| H3 to Bold | 1 | Yes (Tier 1) | Subhead formatting |
| Feature Names Lowercase | 0 | N/A | Not applicable here |
| Compound Words | 0 | N/A | No lifecycle/dropdown instances |
| Removing "Cisco" | 5 | New Rule | "Cisco IOS XE" → "IOS XE" after first use |
| "access points" → "APs" | 4 | Yes (Acronym) | Abbreviation after introduction |
| Comma Before "and" | 3 | No | Serial comma preference |
| Word Choice Improvements | 6+ | No | "lots of" → "many", etc. |

---

## Before/After Examples by Rule Type

### 1. Colon Style in Bold List Items

**Rule:** Use colon after bold terms in definition-style lists, followed by lowercase.

| Before | After |
|--------|-------|
| `- **Higher data rates**: up to 30 Gbps` | `- **Higher data rates:** up to 30 Gbps` |
| `- **Wider channel bandwidth**: Wi-Fi 7 can utilize...` | `- **Wider channel bandwidth:** Wi-Fi 7 can utilize...` |
| `- **Multi-link operation (MLO)**: this feature enables...` | `- **Multi-link operation (MLO):** This feature enables...` |
| `- **WPA Parameters**: WPA3 Policy...` | `- **WPA Parameters:** WPA3 Policy...` |

**Agent Coverage:** Yes - Tier 1 rule for colon outside bold and capitalization after colon.

---

### 2. Technical Hyphenation Consistency

**Rule:** Hyphenate technical terms consistently (e.g., GCMP-256, AES-128).

| Before | After |
|--------|-------|
| `GCMP256` | `GCMP-256` |
| `AES 128` | `AES-128` |
| `AES(CCMP128)` | `AES (CCMP128)` |
| `GCMP256 cipher suite` | `GCMP-256 cipher suite` |
| `Enhanced Open / OWE` | `Enhanced Open/OWE` |

**Agent Coverage:** Partial - Need new rule for technical term hyphenation patterns.

---

### 3. Acronym Management (After First Use)

**Rule:** Remove expanded form after acronym is introduced.

| Before | After |
|--------|-------|
| `Target wake time (TWT) enhancements: TWT allows devices...` | `TWT enhancements: TWT allows devices...` |
| `Enhanced multi-user, multiple input, multiple output (MU-MIMO) and orthogonal frequency-division multiple access (OFDMA)` | `Enhanced MU-MIMO and OFDMA` |
| `Wi-Fi Protected Access 3 (WPA3)` [after first use] | `WPA3` |
| `Multi-Link Operations (MLO)` [after first use] | `MLO` |
| `Opportunistic Wireless Encryption (OWE)` [after first use] | `OWE` |

**Agent Coverage:** No - Requires document-level context tracking, not single-pass regex.

---

### 4. Removing "Cisco" Before Product Names (After First Use)

**Rule:** Drop "Cisco" before trademarked terms after first instance in document.

| Before | After |
|--------|-------|
| `Cisco IOS XE 17.18.1` [second+ use] | `IOS XE 17.18.1` |
| `Cisco IOS XE version` [after first use] | `IOS XE version` |
| `the access points` | `the APs` |
| `Wi-Fi 7 access points` | `Wi-Fi 7 APs` |

**Agent Coverage:** No - Requires document-level context; new rule needed.

---

### 5. Title Case in Step Labels (sidecar.json)

**Rule:** Use title case for step labels, verb form for action steps.

| Before | After |
|--------|-------|
| `"Wi-Fi 7 and 6 Ghz Operations"` | `"Wi-Fi 7 and 6-Ghz Operations"` |
| `"Enabling Wi-Fi 7 globally"` | `"Enable Wi-Fi 7 Globally"` |
| `"Verify the configuration using..."` | `"Verify the Configuration Using..."` |

**Agent Coverage:** Yes - Tier 2 rule for title case in labels.

---

### 6. Sentence-Ending Punctuation in Lists

**Rule:** List items that are complete sentences must end with periods.

| Before | After |
|--------|-------|
| `- Enable 802.11be radios globally` | `- Enable 802.11be radios globally.` |
| `- Verify configuration using Cisco WCAE` | `- Verify the configuration using WCAE.` |
| `Congratulations, you have enabled Wi-Fi 7...!` | `Congratulations, you have enabled Wi-Fi 7...` |

**Agent Coverage:** Yes - Tier 1 rule for list item punctuation.

---

### 7. Bold vs Code Formatting for UI Elements

**Rule:** Use bold (not code) for UI elements that are not literal input; use code for CLI commands.

| Before | After |
|--------|-------|
| `` `WLANs Summary` `` (table name) | `**WLANs Summary**` |
| `` `Download Debug Bundle` `` (button) | `**Download Debug Bundle** button` |
| `` `Open file` `` (option) | `**Open file to process**` |
| `` `WiFi-7` `` (column name) | `**WiFi-7**` |

**Agent Coverage:** Partial - Need rule to distinguish input commands from UI labels.

---

### 8. Word Choice and Formality

**Rule:** Use formal word choices.

| Before | After |
|--------|-------|
| `lots of access points` | `many APs` |
| `based on learnings over years` | `based on knowledge gleaned from years` |
| `4-way handshake` | `four-way handshake` |
| `This is especially useful` | `This is particularly useful` |
| `Controller will process` | `The controller will process` |

**Agent Coverage:** No - Requires NLP/style analysis beyond pattern matching.

---

### 9. H3/Subhead to Bold Formatting

**Rule:** First-level headings within step content use bold, not H3.

| Before | After |
|--------|-------|
| `**You have successfully configured Wi-Fi 7 on Cisco IOS XE through the Dashboard**` (with bold) | `You have successfully configured Wi-Fi 7 on IOS XE through the dashboard.` (plain with period) |
| Section markers in body | Kept as bold (appropriate) |

**Agent Coverage:** Yes - Tier 1 rule for H3 to bold conversion within steps.

---

### 10. Removing Redundant "IEEE" References

**Rule:** After first IEEE reference, use just the standard number.

| Before | After |
|--------|-------|
| `IEEE 802.11be` [after first use] | `802.11be` |
| `extension to IEEE 802.11` | `extension to 802.11` |

**Agent Coverage:** No - Requires document-level context tracking.

---

### 11. Layer 2 Tab Formatting

**Rule:** Tab/menu names follow specific formatting.

| Before | After |
|--------|-------|
| `**Layer2**` | `Layer 2` |
| `the **Layer2** tab` | `the Layer 2 tab` |

**Agent Coverage:** No - Need domain-specific rule for "Layer 2" spacing.

---

### 12. Code Formatting for Input Values

**Rule:** Use code formatting for literal input shown in screenshots.

| Before | After |
|--------|-------|
| `**WPA3 Policy**` (in input context) | `` `WPA3 Policy` `` |
| `**Disabled**` (toggle value) | `` `Disabled` `` |
| `**OWE**` (dropdown value) | `` `OWE` `` |

**Agent Coverage:** No - Context-dependent; same text may be bold or code depending on usage.

---

## NEW Rules Found (Not in Current Tier 1)

### 1. Technical Term Hyphenation
**Pattern:** `GCMP256` → `GCMP-256`, `AES 128` → `AES-128`
**Regex:** `\b(GCMP|AES|SHA)[\s]?(\d+)\b` → `$1-$2`

### 2. Cisco Trademark Abbreviation (After First Use)
**Pattern:** Remove "Cisco" before product names after first instance
**Complexity:** Requires document-level tracking (not automatable with regex)

### 3. Acronym Expansion Removal (After First Use)
**Pattern:** Don't re-expand acronyms already introduced
**Complexity:** Requires document-level tracking (not automatable with regex)

### 4. "Layer2" → "Layer 2"
**Pattern:** Space between "Layer" and number
**Regex:** `\bLayer(\d+)\b` → `Layer $1`

### 5. Numbers in Technical Context
**Pattern:** Numerals for measurements, spelled out for ordinals
**Example:** `4-way handshake` → `four-way handshake`

### 6. Article Addition
**Pattern:** Add missing "the" before specific nouns
**Example:** `Controller will process` → `The controller will process`

### 7. Slash Spacing Consistency
**Pattern:** No spaces around slashes in compound terms
**Example:** `Enhanced Open / OWE` → `Enhanced Open/OWE`

### 8. GUI Value Code Formatting
**Pattern:** Use code blocks for exact GUI input values
**Example:** `**Disabled**` → `` `Disabled` ``

---

## Coverage Assessment

### Rules Agent Would Catch (Updated Tier 1)

| Rule | Pattern Matchable | Confidence |
|------|-------------------|------------|
| Colon after bold in lists | Yes | 100% |
| Period at end of list items | Yes | 95% |
| Title case in labels | Yes | 90% |
| H3 to bold in steps | Yes | 100% |
| Technical hyphenation (GCMP-256) | Yes | 95% |
| Layer 2 spacing | Yes | 100% |
| Slash spacing | Yes | 100% |

### Rules Requiring Document Context (Cannot Automate with Regex)

| Rule | Why Not Automatable |
|------|---------------------|
| Acronym expansion removal | Need to track first definition |
| Cisco trademark abbreviation | Need to track first full usage |
| IEEE reference removal | Need to track first usage |
| Bold vs code for UI elements | Context-dependent (input vs label) |

### Rules Requiring NLP/Style Analysis

| Rule | Why Not Automatable |
|------|---------------------|
| Word choice ("lots of" → "many") | Semantic understanding |
| Formality improvements | Style analysis |
| Missing article detection | Grammar analysis |
| Numeral vs spelled-out numbers | Context-dependent |

---

## Overall Coverage Estimate

| Category | Estimated % Caught |
|----------|-------------------|
| **Punctuation & Formatting** | 95% |
| **Capitalization** | 90% |
| **Technical Term Consistency** | 85% |
| **Document-Level Rules** | 0% (requires enhancement) |
| **Style/Word Choice** | 10% |

### **Overall: ~55-60% of editorial changes would be caught by updated Tier 1 agent**

### Recommendations for Agent Enhancement

1. **Add Technical Hyphenation Rule:**
   ```
   Pattern: (GCMP|AES|SHA|WPA)[\s]?(\d+)
   Fix: $1-$2
   ```

2. **Add Layer Spacing Rule:**
   ```
   Pattern: \bLayer(\d+)\b
   Fix: Layer $1
   ```

3. **Add Slash Spacing Rule:**
   ```
   Pattern: (\w+)\s+/\s+(\w+)
   Fix: $1/$2
   ```

4. **Consider Document-Level Enhancement:**
   - Track first occurrences of acronyms
   - Track first "Cisco" product references
   - Implement "no re-expansion" warnings

5. **Add to Checklist (Human Review):**
   - Bold vs code for UI elements
   - Word choice formality
   - Article usage
