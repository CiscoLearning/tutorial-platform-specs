# PR #189 Editorial Analysis: tc-beef-basics

**PR URL:** https://github.com/CiscoLearning/ciscou-tutorial-content/pull/189
**Editor:** Jill Lauterborn (jlauterb-edit)
**Tutorial:** Browser Exploitation Basics with BeEF
**Date:** October 7-8, 2025
**Editor Commits:** 14 commits

---

## Summary Table of Editorial Changes

| Rule Type | Count | Tier 1 Match | Agent Would Catch |
|-----------|-------|--------------|-------------------|
| No contractions | 5 | Yes | Yes |
| Protocol/acronym caps (ReST -> REST) | 1 | Yes | Yes |
| Acronym expansion in titles - Remove | 2 | No | No |
| Acronym first use expansion | 7+ | Partial | Partial |
| List item punctuation (add periods) | 6 | No | Possible |
| Hyphenation (compound modifiers) | 15+ | Partial | Partial |
| Bold list items to plain text | 4 | Partial | Partial |
| "web site" -> "website" | 1 | No | Possible |
| H3 to bold conversion | 2 | Yes | Yes |
| UI references (backticks to bold/quotes) | 10+ | No | No |
| Keyboard shortcuts formatting | 1 | No | No |
| Serial comma additions | 5+ | No | Possible |
| Sentence restructuring/clarity | 20+ | No | No |
| Redundant heading removal | 2 | No | No |
| Missing newline at EOF | 3 | No | Possible |
| Duplicate word removal | 1 | No | Possible |

---

## Before/After Examples by Rule Type

### 1. No Contractions (Tier 1 - MATCHED)

| Before | After |
|--------|-------|
| `It's a relatively basic HTTP interface` | `It is a relatively basic HTTP interface` |
| `Although it's intuitive` | `Although it is intuitive` |
| `it's a good idea` | `it is a good idea` |
| `It's important to note` | `It is important to note` |

**Agent Coverage:** YES - This is a Tier 1 rule

---

### 2. Protocol/Acronym Caps (Tier 1 - MATCHED)

| Before | After |
|--------|-------|
| `ReST API` | `REST API` |
| `Github` | `GitHub` (proper casing) |

**Agent Coverage:** YES - Protocol names caps rule

---

### 3. H3 to Bold Conversion (Tier 1 - MATCHED)

| Before | After |
|--------|-------|
| `### Use Built-In BeEF Modules...` | (removed - heading provided by label) |
| `**Use BeEF ReST API...**` | (removed - heading provided by label) |

**Editor Note:** "Label provides step's heading, so I removed the bold heading"

**Agent Coverage:** YES - H3 to bold within steps rule

---

### 4. Hyphenation - Compound Modifiers (Tier 1 - PARTIAL MATCH)

| Before | After |
|--------|-------|
| `command and control` | `command-and-control` |
| `web related` | `web-related` |
| `session expired` | `session-expiration` |
| `browser hooking process` | `browser-hooking process` |
| `real world impact` | `real-world impact` |
| `right bottom` | `bottom right` |

**Agent Coverage:** PARTIAL - Some compound modifiers covered, but context-dependent

---

### 5. Acronym Handling in Titles - NEW RULE

| Before | After |
|--------|-------|
| `Browser Exploitation Basics with BeEF (Browser Exploitation Framework)` | `Browser Exploitation Basics with BeEF` |
| `Introduction to Browser Exploitation Framework (BeEF)` | `Introduction to BeEF` |

**Editor Note:** "Typically, we don't expand acronyms in titles or headings"

**Agent Coverage:** NO - This is a NEW rule not in Tier 1

---

### 6. Acronym Expansion - CML -> Cisco Modeling Labs

| Before | After |
|--------|-------|
| `CML Ubuntu image` | `Cisco Modeling Labs Ubuntu image` |
| `your CML server` | `your Cisco Modeling Labs server` |
| `CML console` | `Cisco Modeling Labs console` |
| `CML environment` | `Cisco Modeling Labs environment` |
| `CML nodes` | `Cisco Modeling Labs nodes` |

**Editor Note:** "CML should be Cisco Modeling Labs (no acronym)"
**Count:** 7+ instances

**Agent Coverage:** PARTIAL - First-use expansion is covered, but avoiding acronyms entirely is new

---

### 7. UI Element Formatting - NEW RULE

| Before | After |
|--------|-------|
| `` `Hook Me!` `` | `"Hook Me!"` or `**Hook Me!**` |
| `` `Edit...` `` | `**Edit...**` |
| `` `Save` `` | `**Save** button` |
| `` `View page source` `` | `**View page source**` |
| `CTRL+SHIFT+B` | `Ctrl+Shift+B` |

**Agent Coverage:** NO - UI element formatting rules not in Tier 1

---

### 8. List Item Punctuation - NEW RULE

| Before | After |
|--------|-------|
| `- Discover the concepts of browser exploits...` | `- Discover the concepts of browser exploits...` + `.` |
| `- Explore the ways to inject...` | `- Explore the ways to inject...` + `.` |

All list items under "What You'll Learn" had periods added.

**Agent Coverage:** NO - Not explicitly in Tier 1 rules

---

### 9. Bold List Items to Plain Text - PARTIAL MATCH

| Before | After |
|--------|-------|
| `- **Ethics and safety**: Use BeEF...` | `- Ethics and safety: Use BeEF...` |
| `- **Lab setup**: Create...` | `- Lab setup: Create...` |
| `- **Behavioral Protection**: Detects...` | `- Behavioral protection: Detects...` |
| `- **DNS Security**: Blocks...` | `- DNS security: Blocks...` |

**Agent Coverage:** YES for bold removal, but also involves lowercasing feature names

---

### 10. Feature Names Lowercase (Tier 1 - MATCHED)

| Before | After |
|--------|-------|
| `Behavioral Protection` | `Behavioral protection` |
| `Script Protection` | `Script protection` |
| `Exploit Prevention` | `Exploit prevention` |
| `Retrospective Security` | `Retrospective security` |
| `Real-Time Detection` | `Real-time detection` |
| `Immediate Response` | `Immediate response` |
| `DNS Security` | `DNS security` |
| `Threat Intelligence Integration` | `Threat intelligence integration` |
| `Visibility and Control` | `Visibility and control` |

**Agent Coverage:** YES - Feature names lowercase rule in Tier 1

---

### 11. Serial Comma - NEW RULE

| Before | After |
|--------|-------|
| `IP routing and switching` | `IP routing, and switching` |
| (various compound lists) | (serial comma added) |

**Agent Coverage:** NO - Not explicitly in Tier 1

---

### 12. Website Spelling - NEW RULE

| Before | After |
|--------|-------|
| `Cisco Networking Academy web site` | `Cisco Networking Academy website` |

**Agent Coverage:** NO - Not in Tier 1 rules

---

### 13. Duplicate Word Removal

| Before | After |
|--------|-------|
| `uses the the client-side approach` | `uses the client-side approach` |

**Agent Coverage:** POSSIBLE - Basic grammar check

---

### 14. "Internet" Capitalization

| Before | After |
|--------|-------|
| `Internet access` | `internet access` |

**Editor Query:** "Has Cisco formally adopted lowercasing 'Internet' yet?"

**Agent Coverage:** NO - Not in Tier 1, and appears to be evolving standard

---

### 15. Sentence Clarity Improvements

| Before | After |
|--------|-------|
| `for example an instance of Chrome` | `for example, open an instance of Chrome` |
| `testing Windows PC` | `test Windows PC` |
| `respond with the user cisco password` | `respond with the username and password` |
| `It is therefore crucial` | `Therefore, it is crucial` |

**Agent Coverage:** NO - Requires contextual understanding

---

### 16. Description Rewording

| Before | After |
|--------|-------|
| `Understand how BeEF works` | `Learn how BeEF works` |
| `perform basic actions` | `perform basic tasks` |
| `simulating social engineering attacks` | `running social-engineering exercises` |
| `gathering system info` | `gathering system information` |

**Agent Coverage:** NO - Style preference requiring judgment

---

### 17. UI Expansion

| Before | After |
|--------|-------|
| `BeEF UI` | `BeEF user interface` |
| `web UI` | `web user interface` |

**Count:** 10+ instances

**Agent Coverage:** PARTIAL - Could be added as specific rule

---

## NEW Rules Found (Not in Tier 1)

1. **No acronyms in titles/headings** - Remove parenthetical expansions from titles
2. **Avoid acronyms when not necessary** - Some product names should be spelled out fully (CML -> Cisco Modeling Labs)
3. **UI element formatting** - Use bold for UI elements, quotes for displayed text
4. **Keyboard shortcut casing** - `CTRL+SHIFT+B` -> `Ctrl+Shift+B`
5. **List item punctuation** - Add periods to list items that are complete sentences
6. **Serial comma** - Oxford comma usage
7. **"website" vs "web site"** - One word preferred
8. **"Internet" lowercase** - Evolving standard (editor queried this)
9. **Redundant heading removal** - When step label provides heading, remove bold heading from content
10. **"UI" expansion** - Spell out "user interface"

---

## Coverage Assessment

### Tier 1 Rules Performance

| Rule | Examples in PR | Agent Would Catch |
|------|----------------|-------------------|
| Compound words (life cycle, drop-down, file system) | None found | N/A |
| "by using" construction | None found | N/A |
| No contractions | 5 instances | YES (100%) |
| Protocol names caps (RADIUS, IBGP) | 1 instance (REST) | YES (100%) |
| H3 to bold | 2 instances | YES (100%) |
| Feature names lowercase | 12+ instances | YES (100%) |
| "vs." in comparisons | None found | N/A |

### Overall Coverage Estimate

**Changes the agent WOULD catch:** ~40%
- No contractions (5)
- Protocol caps (1)
- H3 to bold (2)
- Feature names lowercase (12)
- Duplicate words (1)
- Some hyphenation (5-7)

**Changes the agent would NOT catch:** ~60%
- Acronym in titles rule (2)
- Full acronym avoidance - CML (7)
- UI element formatting (10+)
- Keyboard shortcut formatting (1)
- List punctuation (6)
- Serial comma (5+)
- Sentence restructuring (20+)
- Style improvements (10+)
- Website spelling (1)
- UI expansion (10+)

### Recommendations for Tier 1 Expansion

Based on PR #189 analysis, consider adding these high-frequency rules:

1. **UI Element Formatting** (10+ instances)
   - Bold for clickable UI elements
   - Quotes for displayed text

2. **Acronym in Titles** (2 instances)
   - Do not expand acronyms in titles/headings

3. **"UI" Expansion** (10+ instances)
   - `UI` -> `user interface` in body text

4. **Keyboard Shortcut Casing** (1 instance)
   - `CTRL+SHIFT+B` -> `Ctrl+Shift+B`

5. **List Item Punctuation** (6 instances)
   - Complete sentence list items need periods

---

## Editor Queries from This PR

The editor raised these questions for author/team discussion:

1. "Has Cisco formally adopted lowercasing 'Internet' yet?"
2. "We have two notes stacked. If permitted, I recommend using different callout labels, such as Note and Tip"
3. "Should [image.png] have a frame around the image?"
4. "May we change 'respond with the user cisco password' to 'respond with the username and password'?"

These queries indicate areas where editorial guidelines may need clarification.
