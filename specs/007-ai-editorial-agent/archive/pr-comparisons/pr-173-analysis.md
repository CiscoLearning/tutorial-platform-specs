# PR #173 Editorial Analysis: tc-netconf

**PR URL:** https://github.com/CiscoLearning/ciscou-tutorial-content/pull/173
**Tutorial:** tc-netconf (Introduction to NETCONF)
**Editor:** Jill Lauterborn (jlauterb-edit)
**Analysis Date:** 2026-02-20

## Summary Table of Editorial Changes

| Rule Category | Change Type | Count | Tier 1 Coverage |
|---------------|-------------|-------|-----------------|
| No contractions | `it's` -> `it is` | 2 | YES - would catch |
| Feature names lowercase | `Standard` -> `standard`, `Data` -> `data` | 8 | YES - would catch |
| Acronym expansion | `SSH` -> `Secure Shell (SSH)`, `SSID` expansion | 2 | Existing rule |
| "vs." replacement | `vs.` -> `Versus` | 1 | YES - would catch |
| Formatting changes | Bold -> Code style for XML tags | 10+ | Partial |
| Compound word: datastore | `data store` -> `datastore` | 3+ | NEW - not in Tier 1 |
| Technical standard casing | `802.1x` -> `802.1X` | 2 | NEW - not in Tier 1 |
| Redundancy removal | `YIN Notation` -> `YIN` | 1 | NEW - not in Tier 1 |
| Numbered list formatting | Numbers -> Bold numbers | 6 | NEW - not in Tier 1 |
| Sentence structure | Passive -> Active voice | 3+ | Partial |
| Informal language | `Alright, we've` -> `We've` | 1 | NEW - not in Tier 1 |
| Article fixes | Missing articles | 2 | Existing grammar |
| Hyphenation fixes | `Model Driven` -> `Model-Driven` | 1 | Existing rule |

---

## Before/After Examples by Rule Type

### 1. No Contractions (Tier 1 Rule)

**Rule:** Convert contractions to full words.

| Before | After | File |
|--------|-------|------|
| `whether it's enabled` | `whether it is enabled` | step-3.md |
| *(implicit in other changes)* | | |

**Agent Coverage:** YES - this is explicitly in Tier 1 rules

---

### 2. Feature Names Lowercase (Tier 1 Rule)

**Rule:** Feature and category names should be lowercase unless proper nouns.

| Before | After | File |
|--------|-------|------|
| `Custom Models for Services` | `Custom models for services` | step-3.md |
| `IETF Standard` | `IETF standard` | step-3.md |
| `Quality of Service (QoS)` | `quality of service (QoS)` | step-3.md |
| `Configuration Operations:` | `Configuration operations:` | step-2.md |
| `Data Retrieval Operations:` | `Data retrieval operations:` | step-2.md |
| `Locking Operations:` | `Locking operations:` | step-2.md |
| `Session Operations:` | `Session operations:` | step-2.md |
| `Running Datastore:` | `Running datastore:` | step-2.md |
| `Candidate Datastore:` | `Candidate datastore:` | step-2.md |
| `Startup Datastore:` | `Startup datastore:` | step-2.md |
| `Operational Data` | `Operational data` | step-3.md |

**Agent Coverage:** YES - this pattern is covered by Tier 1 rules

---

### 3. "vs." Replacement (Tier 1 Rule)

**Rule:** Use "Versus" instead of "vs." in headings/comparisons.

| Before | After | File |
|--------|-------|------|
| `vs. XML Notation:` | `Versus XML notation:` | step-2.md |

**Agent Coverage:** YES - "vs." in comparisons is in Tier 1 rules

---

### 4. Acronym Expansion on First Use (Existing Rule)

**Rule:** Expand acronyms on first use.

| Before | After | File |
|--------|-------|------|
| `using SSH for secure transport` | `using Secure Shell (SSH) for secure transport` | step-2.md |
| `an SSID on a wireless access point` | `a Service Set Identifier (SSID) on a wireless access point` | step-3.md |

**Agent Coverage:** YES - existing editorial-style-guide.md rule

---

### 5. Bold to Code Style for XML Tags

**Rule:** Use code style (backticks) for XML/code elements, not bold.

| Before | After | File |
|--------|-------|------|
| `**\<get-config\>**` | `` `\<get-config\>` `` | step-2.md, step-5.md |
| `**\<edit-config\>**` | `` `\<edit-config\>` `` | step-2.md |
| `**\<copy-config\>**` | `` `\<copy-config\>` `` | step-2.md |
| `**\<delete-config\>**` | `` `\<delete-config\>` `` | step-2.md |
| `**\<get\>**` | `` `\<get\>` `` | step-2.md |
| `**\<lock\>**` | `` `\<unlock\>` `` | step-2.md |
| `**netconf_iosxe.py**` | `` `netconf_iosxe.py` `` | step-5.md |

**Agent Coverage:** PARTIAL - existing rule for code vs. bold, but may need refinement for XML tag detection

---

### 6. Product/Device Name Casing

**Rule:** Use lowercase for generic device types.

| Before | After | File |
|--------|-------|------|
| `Cisco Router or Switch running Cisco IOS XE` | `Cisco router or switch running Cisco IOS XE` | step-1.md |
| `wireless AccessPoint` | `wireless access point` | step-3.md |

**Agent Coverage:** PARTIAL - some product naming rules exist but need expansion

---

## NEW Rules Discovered (Not in Current Tier 1)

### NEW-1: Compound Word "datastore" (No Space)

**Pattern:** `data store` -> `datastore` (compound word, no space)

| Before | After | File |
|--------|-------|------|
| `configuration data store` | `configuration datastore` | step-2.md |
| `three main data stores` | `three main datastores` | step-2.md |
| (multiple occurrences) | | |

**Recommendation:** Add to compound words list: `datastore` (one word, no space)

---

### NEW-2: Technical Standard Casing (802.1X)

**Pattern:** `802.1x` -> `802.1X` (uppercase letter suffix)

| Before | After | File |
|--------|-------|------|
| `configure 802.1x on a switch` | `configure 802.1X on a switch` | step-3.md |
| `enable on 802.1x` | `enable on 802.1X` | step-3.md |

**Recommendation:** Add rule for IEEE standard suffixes: the letter portion should be uppercase (802.1X, 802.11ac, etc.)

---

### NEW-3: Redundancy Removal (Acronym within Acronym)

**Pattern:** Remove redundant words when the word is part of the acronym itself.

| Before | After | File |
|--------|-------|------|
| `YIN Notation` | `YIN` | step-2.md |

**Note:** "N" in YIN stands for "Notation," making "YIN Notation" redundant (similar to "ATM Machine").

**Recommendation:** Add common redundant acronym patterns:
- `YIN Notation` -> `YIN`
- `PIN Number` -> `PIN`
- `ATM Machine` -> `ATM`

---

### NEW-4: Numbered List Step Formatting (Bold Numbers)

**Pattern:** In procedural steps, format numbered items with bold.

| Before | After | File |
|--------|-------|------|
| `1. Set up the management interface` | `**1. Set up the management interface:**` | step-4.md |
| `2. Configure the hostname` | `**2. Configure the hostname:**` | step-4.md |
| `3. Generate an RSA key` | `**3. Generate an RSA key:**` | step-4.md |
| `4. Create a username` | `**4. Create a username:**` | step-4.md |
| `5. Enable NETCONF` | `**5. Enable NETCONF:**` | step-4.md |
| `6. Verify that NETCONF is running` | `**6. Verify that NETCONF is running:**` | step-4.md |

**Recommendation:** Consider adding rule for procedural steps with code blocks: bold the step text when followed by a code block.

---

### NEW-5: Remove Informal Language

**Pattern:** Remove casual/informal expressions at sentence starts.

| Before | After | File |
|--------|-------|------|
| `Alright, we've just finished` | `We've just finished` | step-4.md |

**Recommendation:** Add rule to flag/remove informal interjections: "Alright,", "OK,", "So,", "Well,", "Now then,"

---

### NEW-6: Phrase Improvements for Clarity

**Pattern:** Improve verbose or awkward phrases.

| Before | After | File |
|--------|-------|------|
| `the various variations` | `the variations` | step-5.md |
| `more easily-readable formats` | `formats that are more easily readable` | step-5.md |
| `output after change:` | `output after the change:` | step-5.md |

**Note:** "the various variations" is redundant; article "the" was missing before "change"

---

### NEW-7: Trailing Colon Removal from Bold Headings

**Pattern:** Remove colons from bold section headers (subheadings).

| Before | After | File |
|--------|-------|------|
| `**Explore more on Cisco U.:**` | `**Explore More on Cisco U.**` | step-6.md |

**Note:** This already exists in editorial-style-guide.md but combined with title case fix.

---

### NEW-8: Link Text Hyphenation

**Pattern:** Hyphenate compound modifiers in link text.

| Before | After | File |
|--------|-------|------|
| `Model Driven Programmability` | `Model-Driven Programmability` | step-5.md |

**Agent Coverage:** YES - hyphenation rules exist but need link text application

---

## Coverage Assessment

### Rules the AI Agent Would Catch (Current Tier 1)

| Rule | Occurrences in PR | Would Catch? |
|------|-------------------|--------------|
| No contractions (`it's` -> `it is`) | 2 | YES |
| Feature names lowercase | 8+ | YES |
| "vs." -> "Versus" | 1 | YES |
| Hyphenation (compound modifiers) | 1 | YES |
| Colon removal from subheadings | 1 | YES |

**Tier 1 Coverage: 13 of 35+ changes (~37%)**

### Rules Partially Covered

| Rule | Coverage Gap |
|------|--------------|
| Bold vs. Code for XML tags | Need XML/code element detection |
| Product name casing | Need Cisco product database |

**Partial Coverage: ~8 changes (~23%)**

### NEW Rules Needed

| Rule | Priority | Frequency |
|------|----------|-----------|
| Compound words: `datastore` (no space) | High | Common in network tutorials |
| IEEE standard casing: `802.1x` -> `802.1X` | Medium | Technical tutorials |
| Redundant acronym patterns | Low | Occasional |
| Bold numbered steps with code blocks | Low | Style preference |
| Remove informal interjections | Medium | Common in drafts |
| Article corrections | Medium | Existing grammar tools |

---

## Summary Statistics

- **Total editorial changes identified:** ~35
- **Changes current Tier 1 would catch:** ~13 (37%)
- **Changes partially covered:** ~8 (23%)
- **Changes requiring NEW rules:** ~14 (40%)

### Recommendations for Tier 1 Expansion

1. **Add to compound words list:**
   - `datastore` (one word)
   - `filesystem` (one word) - already in Tier 1
   - `lifecycle` (one word) - check usage

2. **Add IEEE standard casing rule:**
   - Pattern: `802.1[a-z]` -> `802.1[A-Z]`
   - Apply to common standards: 802.1X, 802.11ac, 802.11be

3. **Add redundant acronym detection:**
   - Common patterns: YIN Notation, PIN Number, ATM Machine, VIN Number

4. **Add informal language removal:**
   - Flag: "Alright,", "OK,", "So," at sentence start

5. **Enhance code vs. bold detection:**
   - XML tags should always use code style
   - File names should always use code style

---

## Editor Notes from Commit Messages

Jill's commit messages included valuable editorial reasoning:

1. **YIN Notation fix:** "to avoid redundancy, as 'N' in 'YIN' stands for 'Notation'"
2. **IETF standard lowercase:** "I could not confirm the following were proper nouns. Also, on IETF's site, IETF 'standard model' is lower case."
3. **802.1X casing:** Changed from `802.1x` to `802.1X`
4. **Datastore compound:** Changed "data store" to "datastore" throughout

These notes provide excellent training data for rule refinement.
