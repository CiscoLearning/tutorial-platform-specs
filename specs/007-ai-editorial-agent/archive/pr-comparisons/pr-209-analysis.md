# PR #209 Editorial Analysis

## PR Information
- **Title:** Ready for review
- **Tutorial:** Cisco UCS AI/ML Sizer Tool
- **Editor:** jlauterb-edit (Jill)
- **Commits analyzed:** 20 commits
- **Analysis Date:** 2026-02-20

## Tutorial Description
The Cisco UCS AI Sizer Tool is an online sizing tool designed to help Cisco partners and employees size Cisco UCS servers for AI/ML workloads, particularly for inferencing with large language models (LLMs). It assists in selecting the right server, GPU, and power configurations based on workload requirements, providing performance metrics and cost estimates.

---

## Summary of Changes by Category

| Category | Count | Coverage by Agent |
|----------|-------|-------------------|
| Product Naming Consistency | 25+ | PARTIAL - needs enhancement |
| Heading Style (Gerund to Imperative) | 3 | YES - HEADING-001 |
| Definition List Formatting (Italic to Bold) | 20+ | YES - existing rule |
| Colon Formatting in Lists | 15+ | NEW RULE NEEDED |
| Sentence Restructuring | 5 | YES - AI pass |
| Email Link Formatting | 1 | NEW RULE NEEDED |
| Capitalization Fixes | 10+ | PARTIAL |
| Missing Articles | 3 | YES - AI pass |
| Punctuation (list item endings) | 10+ | YES - existing rule |

---

## Specific Rules Found with Examples

### 1. Product Naming Consistency (HIGH PRIORITY - NEW PATTERNS)

**Pattern:** Inconsistent product name usage throughout document requires standardization to match screenshots/official branding.

| Before | After |
|--------|-------|
| AI/ML Sizer Tool | Cisco UCS AI/ML Sizer Tool |
| Cisco AI/ML Sizer Tool | Cisco UCS AI/ML Sizer Tool |
| AI/ML Sizer | Cisco UCS AI/ML Sizer Tool |
| the AI/ML Sizer Tool | the Cisco UCS AI/ML Sizer Tool |

**Rule:** Product names must be consistent throughout and match official branding (screenshots, sidecar.json).

**Agent Coverage:** PARTIAL - We have PRODUCT-001/002 but they focus on possessive forms and trademark prefixes, not consistency checking across a document.

**NEW RULE NEEDED:** `PRODUCT-003` - Product name consistency check across tutorial steps.

---

### 2. Heading Style: Gerund to Imperative (COVERED)

| Before | After |
|--------|-------|
| **Getting Started** | **Get Started** |

**Agent Coverage:** YES - Rule HEADING-001 covers this pattern.

---

### 3. Definition List Formatting: Italic to Bold with Colon Style (PARTIAL)

**Pattern:** Definition lists should use bold with colon directly after (no space before colon).

| Before | After |
|--------|-------|
| `- _CPU specifications_: Details...` | `- **CPU specifications:** Details...` |
| `- _GPU type selection_: Users can...` | `- **GPU type selection:** Users can...` |
| `- _FP16/BFLOAT16 (Half-Precision)_: Offers...` | `- **FP16/BFLOAT16 (Half-Precision):** Offers...` |

**Agent Coverage:** YES for bold vs italic (existing style guide section 9).

**NEW PATTERN:** Colon placement - should be **inside** the bold formatting: `**Term:**` not `**Term**:`

---

### 4. Subsection Heading Style: Italic to Bold (NEW RULE)

**Pattern:** Subsection headers using underscore italic should be converted to bold with colon.

| Before | After |
|--------|-------|
| `_1. Workload Inputs_` | `**1. Workload Inputs**` |
| `_2. Server Inputs_` | `**2. Server Inputs**` |
| `_3. Power Inputs_` | `**3. Power Inputs**` |

**Agent Coverage:** NOT COVERED

**NEW RULE NEEDED:** `HEADING-003` - Inline subsection headers should use bold, not italic.

---

### 5. UI Element Bolding Within Prose (NEW PATTERN)

**Pattern:** UI element references within paragraph text should be bolded for clarity.

| Before | After |
|--------|-------|
| While Edit and Delete actions... | While **Edit** and **Delete** actions... |
| the Build action triggers | the **Build** action triggers |
| click the Next button | click the **Next** button |
| click the _Create Configuration_ link | click the **Create Configuration** link |

**Agent Coverage:** PARTIAL - We have guidelines about bold for UI elements but no detection pattern.

**NEW RULE NEEDED:** `BOLD-003` - UI action references (buttons, links, menu items) should be bolded.

---

### 6. Title Case for Subheadings (PARTIAL COVERAGE)

**Pattern:** Section headings should use title case.

| Before | After |
|--------|-------|
| **Integration with Cisco quoting tools** | **Integration with Cisco Quoting Tools** |
| **Concurrent Users (Requests)** | **Concurrent users (requests)** |

**Note:** This is context-dependent - some terms should be lowercased if not proper nouns.

**Agent Coverage:** PARTIAL - HEADING-002 exists but doesn't cover title case validation.

---

### 7. Email Link Formatting (NEW RULE)

**Pattern:** Email addresses should use angle bracket syntax for proper linking.

| Before | After |
|--------|-------|
| `` `ucstools-help@cisco.com` `` | `<ucstools-help@cisco.com>` |

**Agent Coverage:** NOT COVERED

**NEW RULE NEEDED:** `FORMAT-001` - Email addresses should use `<email@domain.com>` format for automatic linking.

---

### 8. Acronym Parenthetical Style (NEW PATTERN)

**Pattern:** When introducing multiple related acronyms, use semicolons and "or" for clarity.

| Before | After |
|--------|-------|
| time to first token (TTFT), latency, and throughput | time to first token, or TTFT; latency; and throughput |

**Agent Coverage:** NOT COVERED - This is a stylistic refinement for complex parentheticals.

---

### 9. List Item Capitalization (NEW RULE)

**Pattern:** List items continuing from a previous sentence should be capitalized when they are full sentences, but lowercase if they complete a sentence fragment.

| Before | After |
|--------|-------|
| - requiring 41 GB GPU memory | - Requiring 41 GB GPU memory |
| - sized for 1x Nvidia L40S GPU | - Sized for 1x NVIDIA L40S GPU |
| - UCS X-Series | - Cisco UCS X-Series |

**Agent Coverage:** NOT COVERED

**NEW RULE NEEDED:** `LIST-001` - List items that are standalone statements should begin with capital letter.

---

### 10. Vendor Name Capitalization (NEW RULE)

**Pattern:** Vendor/brand names must use official capitalization.

| Before | After |
|--------|-------|
| Nvidia | NVIDIA |
| fabric interconnect (generic) | Fabric Interconnect (Cisco term) |

**Agent Coverage:** NOT COVERED - needs brand name database.

**NEW RULE NEEDED:** `TERM-003` - Vendor name capitalization must match official branding.

---

### 11. Sentence Restructuring for Clarity (AI PASS)

**Pattern:** Remove wordy constructions like "The purpose of X is to..."

| Before | After |
|--------|-------|
| The purpose of the Cisco UCS AI Sizer Tool is to accurately estimate... | The Cisco UCS AI Sizer Tool accurately estimates... |
| Here's a detailed breakdown of each input category: | A detailed breakdown of each input category follows. |
| Below is a detailed breakdown of each configurable element: | A detailed breakdown of each configurable element follows. |

**Agent Coverage:** YES - This would be caught by AI analysis pass for wordiness.

---

### 12. List Item Punctuation Consistency (PARTIAL)

**Pattern:** All list items should end with periods if they are complete sentences.

| Before | After |
|--------|-------|
| - Select the PSU to be used for each compute selection | - Select the PSU to be used for each compute selection. |
| The GPUs will be shown based on server selections | The GPUs will be shown based on server selections. |

**Agent Coverage:** YES - Existing end punctuation rule covers this.

---

### 13. Missing Articles (AI PASS)

**Pattern:** Add appropriate articles ("the", "a", "an") where grammatically required.

| Before | After |
|--------|-------|
| working knowledge of Cisco UCS portfolio | working knowledge of the Cisco UCS portfolio |
| generate bill of materials (BOM) | generate a bill of materials (BOM) |

**Agent Coverage:** YES - AI analysis pass should catch these.

---

### 14. Comma Before "and" in Compound Predicates (NEW PATTERN)

**Pattern:** Oxford comma should be used, and also comma before "and" in certain compound constructions.

| Before | After |
|--------|-------|
| context length, and concurrency level determine | context length, and concurrency level, determine |

**Agent Coverage:** PARTIAL - Serial comma rule exists but this is a refinement.

---

### 15. Acronym Expansion in Headings (COVERED)

**Pattern:** First use expansion applies even to titles/headings.

| Before | After |
|--------|-------|
| Artificial Intelligence and Machine Learning (AI/ML) Sizer Tool | Cisco Unified Computing System (UCS) Artificial Intelligence (AI) and Machine Learning (ML) Sizer Tool |

**Agent Coverage:** YES - ACRONYM-001 covers this.

---

## New Rules NOT in Current Agent

Based on this PR analysis, the following NEW rules should be added:

### HIGH PRIORITY

1. **PRODUCT-003: Product Name Consistency**
   - Check that product names are used consistently throughout all steps
   - Match against sidecar.json title/description
   - Severity: HIGH

2. **BOLD-003: UI Element References**
   - UI actions (Click, Select, Enter) should reference bolded element names
   - Pattern: `click the X button` should become `click the **X** button`
   - Severity: MEDIUM

3. **FORMAT-001: Email Link Formatting**
   - Email addresses should use `<email@domain.com>` format
   - Pattern: backtick-wrapped emails or plain text emails
   - Severity: LOW

### MEDIUM PRIORITY

4. **HEADING-003: Subsection Header Style**
   - Numbered subsections like `_1. Topic_` should use bold: `**1. Topic**`
   - Pattern: `_\d+\.\s+.*_`
   - Severity: MEDIUM

5. **LIST-001: List Item Capitalization**
   - List items that are statements should begin with capital letters
   - Context-dependent check
   - Severity: LOW

6. **TERM-003: Vendor Name Capitalization**
   - Database of vendor names with official capitalization (NVIDIA, AMD, Intel, Cisco)
   - Severity: MEDIUM

---

## Agent Coverage Assessment

### Rules That Would Be Caught (Estimated 55-60%)

| Rule | Pattern | Coverage |
|------|---------|----------|
| Gerund headings | `**Getting Started** -> **Get Started**` | FULL |
| Italic to bold definitions | `_term_: -> **term:**` | FULL |
| End punctuation | Missing periods | FULL |
| Wordy constructions | "The purpose of X is..." | AI PASS |
| Missing articles | "working knowledge of Cisco" | AI PASS |
| Acronym expansion | First use | FULL |

### Rules That Would Be MISSED (Estimated 40-45%)

| Rule | Pattern | Gap |
|------|---------|-----|
| Product name consistency | Multiple variations | No cross-file check |
| UI element bolding in prose | `click the Next button` | No detection |
| Email formatting | backticks vs angle brackets | No rule |
| Vendor capitalization | Nvidia vs NVIDIA | No database |
| List item capitalization | lowercase starts | No rule |
| Colon inside bold | `**Term**:` vs `**Term:**` | No pattern |

---

## Recommendations

1. **Add Product Consistency Checker**
   - Extract product name from sidecar.json
   - Scan all step files for variations
   - Report inconsistencies

2. **Enhance UI Element Detection**
   - Pattern: `(click|select|enter|choose|press)\s+the\s+(\w+)\s+(button|link|tab|menu|field)`
   - Suggest bolding the element name

3. **Add Brand Name Database**
   - Similar to acronym-database.json
   - Include: NVIDIA, AMD, Intel, Cisco products
   - Case-sensitive matching

4. **Colon Placement Rule**
   - Pattern: `\*\*[^*]+\*\*:`
   - Should be: `**term:**` not `**term**:`

---

## Editor Queries (Non-automatable)

Jill raised several queries that require human judgment:

1. Should we remove extra "tc-" in URL parameters?
2. Should we blur names in screenshots?
3. Should we match list order to screenshot order?
4. Should short sentences be converted to bullet lists?

These represent judgment calls that cannot be automated but could be flagged for author attention.
