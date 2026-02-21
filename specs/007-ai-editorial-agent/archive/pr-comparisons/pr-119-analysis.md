# PR #119 Analysis: tc-appd-information-points

**PR Title:** Tc appd information points
**Tutorial:** tc-appd-information-points (AppDynamics Information Points)
**Author:** Gurjit (original), Jason (revisions), Matt Sperling (editor)
**Matt's Commits:** 19 (highest activity PR for Matt)
**Analysis Date:** 2025-02-20

---

## Summary of Matt's Editorial Changes

This PR represents one of Matt's most comprehensive edits, covering a technical tutorial about AppDynamics Information Points. Matt performed two full editing passes after Jason's revisions to the original content.

### Change Categories Summary

| Category | Count | Percentage |
|----------|-------|------------|
| Product naming/capitalization | ~45 | 25% |
| UI element formatting | ~35 | 20% |
| Sentence structure rewriting | ~30 | 17% |
| List formatting | ~25 | 14% |
| Terminology standardization | ~20 | 11% |
| Heading style | ~10 | 6% |
| Punctuation/spacing | ~10 | 5% |
| Acronym handling | ~5 | 3% |

---

## Specific Rules with Before/After Examples

### 1. Product Naming - Lowercase Product Feature Names

Matt consistently lowercased product feature names that are not proper product names.

| Before | After |
|--------|-------|
| `Information Points` | `information points` |
| `Business Transactions` | `business transactions` |
| `Service Endpoints` | `service endpoints` |
| `Code Metrics` | `code metrics` |
| `Custom Metrics` | `custom metrics` |
| `Data Collectors` | `data collectors` |
| `Match Conditions` | `match conditions` |
| `Metric Browser` | `metric browser` (note: kept as `Metric Browser` when referring to specific UI) |

**Rule:** Generic feature/concept names should be lowercase, even if the original documentation capitalizes them. Only capitalize when referring to a specific UI element or proper product name.

### 2. UI Element Navigation Formatting

Matt changed UI navigation instructions to use bold and specific separators.

| Before | After |
|--------|-------|
| `Navigate to [Home Page] > [Application]` | `Navigate to **Application**.` |
| `select [More] > [Information Points]` | `select **More** > **Information Points**` |
| `Click [+] to create` | `Click **+ Add** to create` |
| `Click [Add Match Condition]` | `Click **Add Match Condition**` |
| `Clicking 'Save' adds the condition` | `Click **Save** to add the condition` |

**Rule:** Use **bold** for UI elements, use `>` for menu navigation, describe button labels explicitly (e.g., "+ Add" not just "+").

### 3. List Item Capitalization and Punctuation

Matt consistently changed list items to sentence case without terminal periods.

| Before | After |
|--------|-------|
| `- **Average Response Time**` | `- Average response time` |
| `- **Calls per Minute**` | `- Calls per minute` |
| `- **Errors (including exceptions...)**` | `- Errors (including exceptions...)` |
| `- What an Information Point is.` | `- Basics of information points` |
| `- An internet browser to access the tutorial.` | `- An internet browser to access the tutorial` |

**Rule:** List items use sentence case. Omit terminal periods in simple list items. Keep items parallel in structure.

### 4. Heading Style Changes

Matt changed markdown headings from H3 (`###`) to bold text for subsections within a step.

| Before | After |
|--------|-------|
| `### Code Metrics` | `**Code Metrics**` |
| `### Custom Metrics` | `**Custom Metrics**` |
| `### Navigate to the Information Point Wizard` | `**Navigate to the Information Point Wizard**` |
| `### Define Method Signature` | `In the Define the Method Signature section...` |

**Rule:** Within tutorial steps, use bold text for subsections rather than H3 headings. Reserve markdown headings for major structural divisions.

### 5. Em Dash Usage

Matt used `&mdash;` HTML entity for em dashes in certain contexts.

| Before | After |
|--------|-------|
| `These metrics—both code and custom—are` | `These metrics&mdash;both code and custom&mdash;are` |
| `Method Parameter, Return Value, or Invoked Object` | `source&mdash;Method Parameter, Return Value, or Invoked Object` |

**Note:** This is inconsistent with our current rule (em dashes without spaces). Matt used HTML entities in some places.

### 6. Comparison Section Formatting

Matt restructured comparison sections with bullet-point categories.

| Before | After |
|--------|-------|
| `Purpose` (standalone subheading) | `- **Purpose:** Service endpoints provide...` |
| `Data Capture` (standalone subheading) | `- **Data capture:** Data collectors will...` |
| `Data Format` (standalone subheading) | `- **Data format:** Data collectors capture...` |

**Rule:** When comparing two items, use a bulleted list with bold category labels followed by colons, rather than separate subheadings.

### 7. Sentence Structure Improvements

Matt rewrote passive and awkward constructions.

| Before | After |
|--------|-------|
| `In this tutorial, Information Points within AppDynamics will be discussed` | `This tutorial will provide you with an understanding of the capabilities of information points` |
| `The Information Point gathers metrics for every call` | `Information points in AppDynamics gather metrics for every call` |
| `Hence, the scope of an Information Point and a Service Endpoint are the same` | `Therefore, the scope of an information point and a service endpoint is the same` |
| `for example; a return value, within a method, may capture` | `For example, a return value within a method may capture` |

**Rule:** Prefer active voice. Avoid semicolons in mid-sentence. Use "Therefore" instead of "Hence."

### 8. Figure/Image References

Matt standardized how images are referenced.

| Before | After |
|--------|-------|
| `Figure 1 displays an example of two Business Transactions` | `The figure shows an example of two business transaction` |
| `The four images in the above diagram show` | `The four images in the figure above show` |
| `The configuration to match the condition:` | `The configuration to match the condition is shown here:` |

**Rule:** Use "the figure" or "the figure above/below" rather than figure numbers. Add contextual phrases before images.

### 9. "vs." in Headings

Matt used "vs." for comparison section headings.

| Before | After |
|--------|-------|
| `**Information Point and Data Collectors**` | `**Information Points vs. Data Collectors**` |
| `**Information Point and Service Endpoints**` | `**Information Points vs. Service Endpoints**` |

**Rule:** Use "vs." for comparison headings, not "and."

### 10. Acronym Clarification with Expanded Form

Matt added an interesting clarification for ambiguous acronyms.

| Before | After |
|--------|-------|
| `PHP` | `Penultimate hop popping (PHP)` |

**Matt's note in commit:** "OK to leave the first occurrence of 'PHP' as is without an expanded term if it is (as seems very likely here) referring to the scripting language that uses the recursive acronym 'PHP: Hypertext Preprocessor.' However, in the highly unlikely case that it is referring to 'penultimate hop popping,' please use the expanded term."

**Rule:** When an acronym could have multiple meanings, clarify based on context. In networking contexts, PHP could mean penultimate hop popping (MPLS), not just the programming language.

### 11. "It's" to "It is" in Technical Writing

| Before | After |
|--------|-------|
| `it's essential to understand` | `it is essential to understand` |
| `the data type, it's not available` | `it is not available` |

**Rule:** Avoid contractions in formal technical documentation.

### 12. Table Formatting Standardization

Matt reformatted tables for consistency.

| Before | After |
|--------|-------|
| `Purpose \| Troubleshooting Business Transactions` | `Purpose \| Troubleshoot business transactions` |
| `Data range \| Individual data values captured` | `Data range \| Individual data values captured` |
| `SUM or AVERAGE` | `summation or average` |

**Rule:** Use sentence case in table cells. Spell out abbreviations like SUM/AVG in prose contexts.

### 13. Branding Updates

| Before | After |
|--------|-------|
| `Cisco AppDynamics` | `Splunk AppDynamics` (in step-1, final edit) |
| `cybersecurity as a service (cSaaS)` | `cybersecurity as a service (cSaaS)` (expanded) |

**Rule:** Keep product naming current (AppDynamics is now part of Splunk). Expand unfamiliar acronyms.

---

## NEW Rules Not in Current Agent Prompt

### HIGH VALUE - Add to Agent

1. **Product feature lowercase rule**
   - Current prompt has no rule about lowercasing generic feature names like "Business Transactions" or "Information Points"
   - Matt consistently lowercases these unless they're specific UI element names
   - **Add:** "Lowercase generic product feature names (business transactions, information points, data collectors) unless referring to a specific UI element"

2. **H3 vs Bold for subsections**
   - Current prompt doesn't address when to use `###` vs `**bold**`
   - Matt converts H3 subsections to bold text within tutorial steps
   - **Add:** "Use bold text for subsections within tutorial steps, reserve H3+ headings for major structural divisions"

3. **Comparison formatting pattern**
   - No rule for how to format comparison sections
   - Matt uses `- **Category:** Description` pattern consistently
   - **Add:** "For feature comparisons, use bulleted list with bold category labels: `- **Purpose:** Description...`"

4. **"vs." in comparison headings**
   - Current prompt doesn't address this
   - **Add:** "Use 'vs.' for comparison headings, not 'and' (e.g., 'Information Points vs. Data Collectors')"

5. **Avoid contractions in technical docs**
   - Current prompt doesn't mention contractions
   - **Add:** "Avoid contractions (it's, don't, can't) in formal technical documentation"

6. **Figure/image reference standardization**
   - Current prompt doesn't address how to reference images
   - **Add:** "Use 'the figure' or 'the figure above/below' rather than 'Figure 1'. Add contextual lead-in before images"

7. **Hence vs Therefore**
   - Current prompt has "Since vs Because" but not this
   - **Add:** "'Hence' -> 'Therefore' for logical conclusions"

### MEDIUM VALUE - Consider Adding

8. **Table cell capitalization**
   - Use sentence case in table cells
   - Spell out abbreviations in table prose

9. **List item terminal punctuation**
   - Omit terminal periods in simple list items
   - Keep punctuation in complex list items or full sentences

10. **UI button label specificity**
    - Describe buttons explicitly (`**+ Add**` not just `+`)

---

## Agent Coverage Assessment

### What Current Agent WOULD Catch (~40%)

| Pattern | Coverage |
|---------|----------|
| Em dash spacing | Partial (format differs) |
| Heading style (gerund to imperative) | Yes |
| Bold for GUI elements | Yes |
| Acronym expansion | Yes |
| "Click on" to "Click" | Yes |
| Serial comma | Yes |
| Trailing whitespace | Yes |

### What Current Agent Would MISS (~60%)

| Pattern | Gap |
|---------|-----|
| Product feature lowercase | No rule |
| H3 to bold subsections | No rule |
| Comparison formatting | No rule |
| "vs." in headings | No rule |
| Contractions | No rule |
| Figure references | No rule |
| Hence/Therefore | No rule |
| List item punctuation | Incomplete |
| Table formatting | No rule |
| Sentence structure rewrites | Complex - requires judgment |

---

## Matt's Explicit Style Citations

From commit messages, Matt explicitly cited:

1. **Legal disclaimer requirement:** "Does step 1 of this post need a Cisco legal disclaimer?" (recurring concern)

2. **Acronym disambiguation:** "OK to leave the first occurrence of 'PHP' as is without an expanded term if it is (as seems very likely here) referring to the scripting language..."

3. **Screenshot recommendations:** "Step 5 could use a couple of additional screenshots to better illustrate some of the configuration steps"

4. **UI instruction clarity:** "Is this referring to the button with the circle icon that appears at the top right...? If so, for the sake of clarity, you may want to change the sentence to..."

5. **Step restructuring:** "I merged all the content from the step 2 file (Background) into step 1 (Overview). The step 2 file should be deleted..."

---

## Recommendations for Agent Improvement

### Priority 1: Add New Rules

1. Product feature lowercase rule (high impact, easy to implement)
2. Contractions rule (high impact, easy to implement)
3. "vs." in comparison headings (easy to implement)
4. Hence/Therefore substitution (easy to implement)

### Priority 2: Query Patterns

1. Legal disclaimer presence check
2. Ambiguous acronym detection (PHP, NAS, etc.)
3. Screenshot sufficiency suggestions

### Priority 3: Complex Patterns (Future)

1. H3 to bold conversion for subsections
2. Comparison section restructuring
3. Figure reference standardization
4. Sentence structure improvements

---

## Quality Assessment

**Estimated Agent Coverage:** 40%

This PR shows Matt's most thorough editing patterns. The tutorial had significant issues requiring restructuring and reformatting beyond simple find-replace rules. The 60% gap primarily consists of:

- Structural changes (heading levels, section organization)
- Judgment calls about capitalization of product terms
- Sentence-level rewrites for clarity
- Content reorganization suggestions

Improving agent coverage to ~65% is achievable by adding the Priority 1 and 2 rules above.
