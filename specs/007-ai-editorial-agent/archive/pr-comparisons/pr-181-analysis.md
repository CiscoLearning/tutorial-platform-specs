# PR #181 Analysis: tc-train-serve

**PR Title:** tc-train-serve
**Tutorial:** Train and Serve ML Models with Red Hat OpenShift AI
**Editor:** jlauterb-edit (Jill)
**Commits Analyzed:** 17 commits
**Date:** 2026-02-20

---

## Summary of Changes by Category

| Category | Count | Examples |
|----------|-------|----------|
| Terminology/Word Choice | 12 | "life cycle" vs "lifecycle", "drop-down" vs "dropdown" |
| Capitalization | 8 | "Machine Learning" -> "machine learning", "Service Details" -> "Service details" |
| Code vs Bold Formatting | 7 | Notebook names, variable names in backticks |
| Acronym Expansion | 5 | ONNX, AWS, TLS, DNS, RAM |
| Article/Preposition Fixes | 5 | "the MinIO", "the Red Hat OpenShift AI" |
| Punctuation | 4 | Remove colons from subheadings, comma placement |
| Heading Style | 2 | "Disabling KServe" -> "Disable KServe" |
| Typo Fixes | 2 | "developmnet" -> "development", "platformr" -> "platform" |

---

## Specific Rules Found with Before/After Examples

### 1. Compound Words: "Life Cycle" vs "Lifecycle"

**Rule:** Use "life cycle" as two words (noun phrase), not "lifecycle"

| Before | After |
|--------|-------|
| end-to-end model lifecycle management | end-to-end model life cycle management |

**Status:** NEW RULE - Not in current style guide

---

### 2. Compound Words: "Drop-Down" vs "Dropdown"

**Rule:** Use hyphenated "drop-down" for the adjective form

| Before | After |
|--------|-------|
| From the project dropdown | From the project drop-down |

**Status:** NEW RULE - Not in current style guide

---

### 3. Compound Words: "File System" vs "Filesystem"

**Rule:** Use "file system" as two words (consistent with compound word pattern)

| Before | After |
|--------|-------|
| from local filesystems | from local file systems |

**Status:** NEW RULE - Not in current style guide

---

### 4. Lowercase Generic Concepts (Not Product Names)

**Rule:** When a term is a generic concept (not a product name or UI element), use lowercase

| Before | After |
|--------|-------|
| Machine Learning (ML) training | machine learning (ML) training |
| Data Science Projects in Red Hat | Data science projects in Red Hat |
| Service Details page | Service details page |

**Status:** DOCUMENTED - Matches "Rule: Lowercase General Terms" in style guide

---

### 5. Heading Style: Imperative Mood

**Rule:** Use imperative form for headings, not gerunds

| Before | After |
|--------|-------|
| ### Disabling KServe | ### Disable KServe |

**Status:** DOCUMENTED - Matches "Rule: Use Imperative Mood, Not Gerunds"

---

### 6. Remove Bold from Inline Subheadings in Lists

**Rule:** When a bold phrase introduces a description inline, remove the bold if it's followed by a colon

| Before | After |
|--------|-------|
| **Server Configuration:** | Server configuration: |
| **Model Settings:** | Model settings: |
| **Key steps in the loop:** | Key steps in the loop: |

**Status:** NEW PATTERN - The style guide covers list items, but not this specific inline subheading case

---

### 7. Code Style for File Names (Notebooks)

**Rule:** Use code style (backticks) for file names, including notebook names

| Before | After |
|--------|-------|
| **01_train_model.ipynb** notebook | 01_train_model.ipynb notebook |
| **02_save_to_s3.ipynb** notebook | 02_save_to_s3.ipynb notebook |
| **03_validate_rest_endpoint.ipynb** | 03_validate_rest_endpoint.ipynb |

**Status:** DOCUMENTED - Matches "Rule: Use Code Style for Technical Terms" (file names)

---

### 8. Code Style for Variable Names in Prose

**Rule:** Use backticks for variable/parameter names when referenced in prose

| Before | After |
|--------|-------|
| update the **rest_url** variable | update the `rest_url` variable |
| input name "bandwidth-input" must | input name `bandwidth-input` must |

**Status:** DOCUMENTED - Consistent with code style rules

---

### 9. Remove Bold from Library Names

**Rule:** Use plain text or code style for library names, not bold

| Before | After |
|--------|-------|
| **onnx** and **onnxscript** libraries | onnx and onnxscript libraries |

**Status:** NEW PATTERN - Style guide doesn't explicitly address library names

---

### 10. Add Article "the" Before Product Names in Some Contexts

**Rule:** When a product name is used as an object (not the subject), add "the" before it

| Before | After |
|--------|-------|
| Configure MinIO S3-compatible | Configure the MinIO S3-compatible |
| integrates perfectly with Red Hat OpenShift AI | integrates perfectly with the Red Hat OpenShift AI |

**Status:** PARTIAL - Not explicitly documented, context-dependent

---

### 11. Acronym Expansion on First Use (Technical Terms)

**Rule:** Expand acronyms on first use, even common technical ones

| Before | After |
|--------|-------|
| ONNX format | Open Neural Network Exchange (ONNX) format |
| AWS software development kit | Amazon Web Services (AWS) software development kit |
| TLS certificates | Transport Layer Security (TLS) certificates |
| DNS name | Domain Name System (DNS) name |
| 36 GB RAM | 36-GB random access memory (RAM) |

**Status:** DOCUMENTED - Matches "Rule: Expand on First Use"

---

### 12. Remove Trailing Colons from Subheadings

**Rule:** Remove colons at end of bold subheadings when not introducing an immediate list

| Before | After |
|--------|-------|
| **Explore More on Cisco U.:** | **Explore More on Cisco U.** |

**Status:** DOCUMENTED - Matches "Colons in Subheadings"

---

### 13. Comma Before Introductory Phrases

**Rule:** Add comma after introductory clauses/phrases

| Before | After |
|--------|-------|
| as shown in the following figure: | , as shown in the following figure: |
| After the bucket is connected you | After the bucket is connected, you |

**Status:** NEW RULE - Standard grammar, not explicitly documented

---

### 14. URL/UI Element Name Consistency

**Rule:** Match link text to actual UI or page names

| Before | After |
|--------|-------|
| Video Series | Videos |

**Status:** DOCUMENTED - Matches "Rule: URL Title Matching"

---

### 15. Sentence Structure: Remove Line Breaks

**Rule:** Fix sentences that were incorrectly split across lines

| Before | After |
|--------|-------|
| You can compare them to the initialized parameters and<br>see how your neural network | You can compare them to the initialized parameters and see how your neural network |

**Status:** NEW PATTERN - Line break/sentence continuity issue

---

### 16. Trailing Whitespace Cleanup

**Rule:** Remove trailing whitespace at end of files/paragraphs

Multiple instances of trailing whitespace removal observed.

**Status:** DOCUMENTED - "TRAILING_WHITESPACE" in markdown validation

---

## NEW Rules Not in Current Agent Prompt

### High Priority (Should Add)

1. **Compound Word: "life cycle"** - Use "life cycle" (two words) not "lifecycle"
2. **Compound Word: "drop-down"** - Use hyphenated "drop-down" as adjective
3. **Compound Word: "file system"** - Use "file system" (two words) not "filesystem"
4. **Inline Subheadings** - Remove bold from inline subheading phrases like "**Key steps:**" when they're not bulleted list items

### Medium Priority (Consider Adding)

5. **Library Names** - Use plain text or code style for library/package names, not bold
6. **Comma After Introductory Clauses** - Standard grammar rule for introductory phrases
7. **Article "the" Before Products** - Add "the" before product names when used as object of preposition

---

## Agent Catch Rate Assessment

### Rules Our Agent Would Catch

| Rule | Confidence | Notes |
|------|------------|-------|
| Heading imperative mood | 95% | Well documented |
| Acronym expansion | 90% | Well documented |
| Code style for files/commands | 85% | Well documented |
| Remove trailing colons | 85% | Documented |
| Lowercase generic terms | 80% | Partially documented |
| URL name consistency | 75% | Documented |
| Trailing whitespace | 100% | Automated tool |
| Typo fixes | 70% | Depends on AI model |

### Rules Our Agent Would Miss

| Rule | Confidence Miss | Notes |
|------|-----------------|-------|
| "life cycle" vs "lifecycle" | 95% miss | NOT documented |
| "drop-down" vs "dropdown" | 95% miss | NOT documented |
| "file system" vs "filesystem" | 95% miss | NOT documented |
| Inline subheading bold removal | 80% miss | Edge case not covered |
| Library name formatting | 70% miss | Not explicitly covered |
| Article "the" placement | 60% miss | Context-dependent |
| Comma after intro clauses | 50% miss | Basic grammar, may catch |

### Overall Estimated Catch Rate

**Estimated: 65-70%**

The agent would catch most acronym, formatting, and structural issues but would miss the compound word consistency rules which appeared frequently in this PR. The compound word rules (life cycle, drop-down, file system) represent a significant pattern that should be added to the style guide.

---

## Recommendations

1. **Add Compound Word Rules** - Create a new section "Compound Words" in the style guide with:
   - "life cycle" (noun, two words)
   - "drop-down" (adjective, hyphenated)
   - "file system" (noun, two words)
   - Other common variations to watch for

2. **Clarify Bold vs Code for Libraries** - Add explicit guidance that library/package names use code style or plain text, never bold

3. **Add Inline Subheading Rule** - Clarify that bold inline subheadings (not in bulleted lists) should not be bold, just capitalized with colon

4. **Consider Acronym Query Patterns** - Jill flagged multiple acronyms as QUERYs (YAML, DevOps, CSV). These suggest common acronyms that may not need expansion. Consider adding a "well-known acronyms" exception list.

---

## Editor Query Patterns (For Human Decision)

From Jill's commit messages, these items were flagged for author decision:

1. "Should we expand YAML (YAML Ain't Markup Language)? Or is it common?"
2. "Should we expand DevOps (development and IT operations)? Or is it common?"
3. "Should we expand CRDs (custom resource definitions)?"
4. "Should we expand CSV (comma-separated values)?"
5. "Should the image have a thin rule (frame) around it?"
6. "Should we move this line before the image?"
7. "Should we add a screenshot that covers the following?"

These QUERYs represent editorial decisions that require author input and cannot be automated.

---

*Analysis generated: 2026-02-20*
*PR: CiscoLearning/ciscou-tutorial-content#181*
