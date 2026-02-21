# PR #194 Analysis: tc-ocsf14-secdata

**PR Title:** tc-ocsf14-secdata
**Tutorial Name:** Get Started with OCSF: Standardize Security Data Across Tools
**Editor:** jlauterb-edit (Jill)
**Total Commits:** 16 (some are reverts from author pushback)
**Analysis Date:** 2026-02-20

---

## Summary of Changes by Category

| Category | Count | Auto-fixable? |
|----------|-------|---------------|
| Heading Style (gerund to imperative) | 5 | Yes |
| Acronym Expansion | 8 | Yes (with database) |
| Bold Removal (non-GUI text) | 12+ | Partial |
| Numbered List to Bullet List | 2 | No (context-dependent) |
| Product Name Expansion | 15+ | Yes (with database) |
| Code Styling (backticks) | 6 | Partial |
| Punctuation (semicolon to period) | 2 | No (context-dependent) |
| Capitalization | 3 | Yes (with rules) |
| Minor Typos | 2 | Yes |

---

## Specific Rules Found with Before/After Examples

### 1. Heading Style: Gerund to Base Infinitive (DOCUMENTED)

**Rule:** Use imperative mood for step headings, not gerund (-ing) form.

| Before | After |
|--------|-------|
| Getting Started with OCSF: Standardizing Security Data Across Tools | Get Started with OCSF: Standardize Security Data Across Tools |
| Converting Event Logs to OCSF Format | Convert Event Logs to OCSF Format |
| Validating JSON Data for OCSF Compliance | Validate JSON Data for OCSF Compliance |
| Additional Practice: Converting More Events to OCSF JSON | Additional Practice: Convert More Events to OCSF JSON |

**Agent Coverage:** Already documented. Agent should catch this.

---

### 2. Bold for GUI Elements Only (DOCUMENTED)

**Rule:** Boldfacing is for GUI elements only; use italics (sparingly) for emphasis.

| Before | After |
|--------|-------|
| `- **Event normalization:** Transforms data...` | `- Event normalization: Transforms data...` |
| `- **Log producers:** Systems, devices...` | `- Log producers: These are systems, devices...` |
| `- **Required Attributes:** Ensure that...` | `- Required attributes: These ensure that...` |

**Note:** Jill tried to remove bold from definition list terms but author pushed back, so this was reverted. The exception: "Bolding bulleted terms. It improves readability."

**Agent Coverage:** Already documented. Agent should flag but mark as context-dependent.

---

### 3. Acronym Expansion on First Use (DOCUMENTED)

**Rule:** Expand acronyms on first use in format: Full Term (ACRONYM)

| Before | After |
|--------|-------|
| FMC | Cisco Secure Firewall Management Center |
| FTD | Cisco Secure Firewall Threat Defense |
| ACL action | Access Control List (ACL) action |
| API | application programming interface (API) |
| UI | user interface |
| UTC | Coordinated Universal Time (UTC) |

**Agent Coverage:** Already documented. Agent should catch with acronym database.

---

### 4. **NEW PATTERN: Deprecated Acronyms - Full Replacement Required**

**Rule:** FTD and FMC are deprecated acronyms as of 2025. Even after first-use expansion, subsequent uses should use full product name, NOT the acronym.

| Before | After |
|--------|-------|
| Cisco FMC | Cisco Secure Firewall Management Center |
| Cisco FTD | Cisco Secure Firewall Threat Defense |
| FMC can manage multiple firewalls | Cisco Secure Firewall Management Center can manage multiple firewalls |
| the Cisco FTD DNS log | the Cisco Secure Firewall Threat Defense DNS log |

**Critical Finding:** This is NOT the standard "expand on first use, then abbreviate" pattern. FTD/FMC must ALWAYS use full names.

**Agent Coverage:** PARTIALLY documented. The editor-comments-reference.md mentions FTD/FMC are "deprecated acronyms" but does not explicitly state they must be replaced on EVERY occurrence, not just first use.

---

### 5. **NEW PATTERN: Numbered List to Bullet List for Non-Sequential Items**

**Rule:** Change numbered lists to bullet lists when items are not sequential/procedural.

| Before | After |
|--------|-------|
| `1. Category` | `- Category` |
| `2. Event Class` | `- Event class` |
| `3. Data Types, Attributes, and Arrays` | `- Data types, attributes, and arrays` |
| `4. Profile` | `- Profile` |
| `5. Extension` | `- Extension` |

**Context from commit:** "Lines 14-18: Changed the numbered list to a bullet list."

**Why:** The OCSF taxonomy constructs are not steps or a sequence - they are components that exist in parallel.

**Agent Coverage:** NOT DOCUMENTED. This is a new pattern requiring semantic understanding.

---

### 6. Code Styling for Technical Terms (DOCUMENTED)

**Rule:** Use backticks for field names, variables, log patterns, and technical identifiers.

| Before | After |
|--------|-------|
| `src_ip, ip_address, and source_ip` | `` `src_ip`, `ip_address`, and `source_ip` `` |
| `%FTD type in the event log` | `` `%FTD` type in the event log `` |

**Agent Coverage:** Already documented for commands/filenames. Should extend to field names and log patterns.

---

### 7. **NEW PATTERN: List Item Sentence Structure Improvement**

**Rule:** Add introductory phrasing ("These are...", "These...") to make list items complete sentences.

| Before | After |
|--------|-------|
| `- **Log producers:** Systems, devices, applications...` | `- Log producers: These are systems, devices, applications...` |
| `- **Security solutions:** Comprehensive tools designed to...` | `- Security solutions: These comprehensive tools are designed to...` |
| `- **Required Attributes:** Ensure that each event...` | `- Required attributes: These ensure that each event...` |

**Agent Coverage:** NOT DOCUMENTED. This pattern makes list items grammatically complete sentences.

---

### 8. **NEW PATTERN: Capitalization in List Items (Sentence Case)**

**Rule:** Use sentence case for list items, not title case.

| Before | After |
|--------|-------|
| Event Class | Event class |
| Data Types, Attributes, and Arrays | Data types, attributes, and arrays |
| Required Attributes | Required attributes |
| Security Controls profile | Security Control profile |

**Agent Coverage:** PARTIALLY documented (general capitalization rules exist, but not specific to list items).

---

### 9. Typo/Error Corrections (DOCUMENTED)

**Rule:** Fix typos and grammatical errors.

| Before | After |
|--------|-------|
| unfied format | unified format |
| OSCF is designed for | OCSF is designed for |
| recreate | re-create |

**Agent Coverage:** Standard spell-check/grammar capability.

---

### 10. **NEW PATTERN: Subheading Style Consistency**

**Rule:** Subheadings within a step should also use imperative mood.

| Before | After |
|--------|-------|
| **Mapping Raw Event Fields to OCSF Attributes** | **Map the Raw Event Fields to OCSF Attributes** |
| **Automating Log Parsing for Cisco Secure Firewalls** | **Automate Log Parsing for Cisco Secure Firewalls** |

**Agent Coverage:** NOT explicitly documented for subheadings. The gerund-to-imperative rule is documented for step labels but should extend to all headings.

---

### 11. Punctuation: Semicolon to Period (DOCUMENTED)

**Rule:** Avoid run-on sentences with semicolons when a period and new sentence is clearer.

| Before | After |
|--------|-------|
| `...which are optional; recommended attributes are not mandatory...` | `...which are optional. Recommended attributes are not mandatory...` |

**Agent Coverage:** Already documented as a general principle.

---

### 12. **NEW PATTERN: Serial Comma with Semicolons for Complex Lists**

**Rule:** Use semicolons to separate complex list items that contain commas.

| Before | After |
|--------|-------|
| `Extended Detection and Response (XDR), Security Orchestration, Automation, and Response (SOAR), and other` | `Extended Detection and Response (XDR); Security Orchestration, Automation, and Response (SOAR); and other` |

**Agent Coverage:** NOT DOCUMENTED. This is an advanced punctuation rule.

---

### 13. **NEW PATTERN: Minor Grammar Preference - "the" Article Addition**

**Rule:** Add articles before GUI element references for clarity.

| Before | After |
|--------|-------|
| `click **Execute**` | `click the **Execute** button` |

**Agent Coverage:** NOT DOCUMENTED. This is a style preference that adds clarity.

---

## NEW Rules Not in Current Agent Prompt

1. **Deprecated Acronym Full Replacement:** FTD/FMC must use full names on EVERY occurrence, not just first use. This is stronger than the standard "expand then abbreviate" rule.

2. **Numbered vs. Bullet List Selection:** Change numbered lists to bullet lists when items are non-sequential (components, features, concepts rather than steps).

3. **List Item Sentence Completeness:** Add introductory phrases ("These are...", "These...") to make list items grammatically complete.

4. **Subheading Imperative Mood:** The gerund-to-imperative rule applies to ALL headings, including subheadings within steps (not just step labels).

5. **Serial Comma with Semicolons:** Use semicolons between complex list items containing internal commas.

6. **Article Addition for GUI Elements:** Add "the ... button" phrasing for clarity when referencing GUI elements.

---

## Agent Coverage Assessment

| Issue Type | Count | Agent Would Catch? | Confidence |
|------------|-------|-------------------|------------|
| Heading style (gerund to imperative) | 5 | Yes | High |
| Acronym expansion | 8 | Yes | High |
| Bold removal (non-GUI) | 12+ | Partial | Medium |
| Product name expansion (FTD/FMC) | 15+ | Partial (first use only) | Medium |
| Code styling for field names | 6 | Maybe | Low |
| Typo fixes | 2 | Yes | High |
| Numbered to bullet list | 2 | No | Low |
| List sentence structure | 6+ | No | Low |
| List item capitalization | 4 | Maybe | Medium |
| Subheading style | 2 | Maybe | Medium |
| Semicolon for complex lists | 1 | No | Low |

### Estimated Coverage: 55-65%

**High Confidence (would catch):**
- Gerund headings in step labels: 5 issues
- Acronym first-use expansion: 8 issues
- Typo/spelling: 2 issues

**Medium Confidence (might catch):**
- Bold removal (depends on context detection): ~6 issues
- FTD/FMC first occurrence: ~3 issues
- Capitalization issues: 4 issues

**Low Confidence (would miss):**
- FTD/FMC subsequent occurrences: ~12 issues
- Numbered to bullet list: 2 issues
- List sentence structure: 6 issues
- Subheading style: 2 issues
- Semicolon punctuation: 1 issue

---

## Recommendations for Agent Enhancement

1. **Update Acronym Database:** Add a `replacement_required: true` flag for deprecated acronyms like FTD/FMC that must be replaced on ALL occurrences.

2. **Add List Type Rule:** Detect numbered lists that contain non-sequential concepts and suggest conversion to bullet lists.

3. **Extend Heading Rule:** Apply gerund-to-imperative detection to ALL markdown headings (# through ####), not just step labels.

4. **Add List Completeness Check:** Flag list items that are noun phrases without verbs and suggest adding introductory phrases.

5. **Add Complex List Punctuation:** Detect list items with internal commas and suggest semicolon separation.

---

## Author Pushback Notes

Jill made edits to remove bold from definition list terms (e.g., `- **Event normalization:**`) but the author (Alexander) pushed back:

> "P.S. as regards the Cisco style for using italics (sparingly) instead of boldfacing for emphasis. I respect that and will comply, but I feel boldfacing terms, like on lines 17 and 18 in step-2.md, would improve the readability."

**Result:** Jill reverted the bold removal for definition list terms.

**Implication for Agent:** The agent should flag bold on definition terms but categorize as "Query for Author" rather than "High Priority," since there is documented author preference that may override.

---

*Analysis generated from PR #194 diff examination*
