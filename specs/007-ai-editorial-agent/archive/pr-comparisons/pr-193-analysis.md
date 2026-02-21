# PR #193 Analysis: tc-deploy-llm-openshift-cpu-vllm

**PR Title:** tc-deploy-llm-openshift-cpu-vllm
**Tutorial:** tc-deploy-llm-openshift-cpu-vllm (LLM Inference on OpenShift without GPU)
**Author:** Urek (original), Xander Stevenson (revisions), Matt Sperling (editor: masperli)
**Matt's Commits:** 14 editorial commits across sidecar.json and step-1 through step-11
**Analysis Date:** 2025-02-20

---

## Summary of Matt's Editorial Changes

This PR covers a technical tutorial about deploying LLM inference services on Red Hat OpenShift using CPU resources. Matt performed comprehensive edits across all 11 steps plus the sidecar.json metadata file.

### Change Categories Summary

| Category | Count | Percentage |
|----------|-------|------------|
| List punctuation (colon to colon-space) | ~85 | 28% |
| Sentence structure/phrasing | ~45 | 15% |
| H3 to bold conversion | ~35 | 12% |
| UI/menu formatting | ~30 | 10% |
| Terminology consistency | ~25 | 8% |
| "step" to "topic" transitions | ~20 | 7% |
| Article usage (a/an/the) | ~18 | 6% |
| Compound word handling | ~15 | 5% |
| Pronoun/subject addition | ~12 | 4% |
| Whitespace/trailing fixes | ~15 | 5% |

---

## Specific Rules with Before/After Examples

### 1. List Punctuation: Hyphen-Colon to Colon-Space

Matt consistently changed the punctuation pattern in bold list items.

| Before | After |
|--------|-------|
| `- **Container orchestration**: Automatic scaling...` | `- **Container orchestration:** Automatic scaling...` |
| `- **Model size selection**: Smaller models...` | `- **Model size selection:** Smaller models...` |
| `- **Asynchronous processing**: Non-blocking request...` | `- **Asynchronous processing:** Nonblocking request...` |
| `- **Development phase**: Create a FastAPI...` | `- **Development phase:** Create a FastAPI...` |
| `- **Label selectors**: Consistent labeling...` | `- **Label selectors:** Consistent labeling...` |

**Rule:** In bold list items with descriptions, use colon followed by space (`:**`), not colon with space-hyphen (`: `).

### 2. H3 Headings to Bold Text

Matt converted H3 headings (`###`) to bold text for subsections within tutorial steps.

| Before | After |
|--------|-------|
| `### Understand OpenShift Container Platform` | `**OpenShift Container Platform**` |
| `### CPU-Optimized LLM Architecture` | `**CPU-Optimized LLM Architecture**` |
| `### Building the Container Image` | `**Build the Container Image**` |
| `### Verify OpenShift Local Environment` | `**Verify the OpenShift Local Environment**` |
| `### Create OpenShift Project by Using Web Console` | `**Create an OpenShift Project by Using the Web Console**` |
| `### Log in to OpenShift CLI` | `**Log In to the OpenShift CLI**` |

**Rule:** Within tutorial steps, use bold text for subsections rather than H3 headings. Also note gerund-to-imperative conversion in heading titles.

### 3. "Step" to "Topic" Terminology

Matt consistently changed references from "step" to "topic" when referring to the next section.

| Before | After |
|--------|-------|
| `In the next step, you will create...` | `In the next topic, you will create...` |
| `In the next step, you will configure...` | `In the next topic, you will configure...` |
| `In the next step, you will create the container image...` | `In the next topic, you will create the container image...` |

**Rule:** Use "topic" when referring to the next logical section, not "step."

### 4. Compound Word Corrections

Matt corrected compound word styling according to standard conventions.

| Before | After |
|--------|-------|
| `Non-blocking request handling` | `Nonblocking request handling` |
| `Non-root user execution` | `Nonroot user execution` |
| `pre-trained model artifacts` | `pretrained model artifacts` |

**Rule:** "Nonblocking" and "nonroot" are written as single words (no hyphen). "Pretrained" is one word.

### 5. Article Usage (a/an/the)

Matt consistently added missing articles or corrected article usage.

| Before | After |
|--------|-------|
| `You should see an output similar...` | `You should see output that is similar...` |
| `Create local working directory` | `Create the local working directory` |
| `Verify Project Creation Through CLI` | `Verify Project Creation Using the CLI` |
| `modern transformer models such as Google's FLAN-T5` | `modern transformer models such as the Google FLAN-T5` |
| `FastAPI application has correct Python syntax` | `FastAPI application has the correct Python syntax` |

**Rule:** Use "the" before specific items. Remove "an" before "output" in "You should see output..."

### 6. Subject Addition in List Items

Matt added subjects to list items to make them complete sentences.

| Before | After |
|--------|-------|
| `- **Response length**: Designed for concise answers...` | `- **Response length:** FLAN-T5-small is designed for concise answers...` |
| `- **Factual focus**: Optimized for factual questions...` | `- **Factual focus:** The model is optimized for factual questions...` |
| `- **Pod network**: Container listens on port 8000...` | `- **Pod network:** The container listens on port 8000...` |
| `- **Load balancing**: OpenShift router handles...` | `- **Load balancing:** The OpenShift router handles...` |

**Rule:** List items describing properties should include a subject to form complete sentences.

### 7. Menu Navigation Formatting

Matt standardized UI navigation with proper separators and bold formatting.

| Before | After |
|--------|-------|
| `navigate to **Home / Projects**` | `navigate to **Home** > **Projects**` |
| `navigate to **Workloads > Deployments**` | `navigate to **Workloads** > **Deployments**` |
| `Navigate to **Networking > Services**` | `Navigate to **Networking** > **Services**` |
| `Navigate to **Networking > Routes**` | `Navigate to **Networking** > **Routes**` |

**Rule:** Use bold for each UI element and `>` as separator. Each element in the path should be separately bolded.

### 8. "Understand" to Simpler Headings

Matt simplified headings that started with "Understand."

| Before | After |
|--------|-------|
| `**Understand OpenShift Container Platform**` | `**OpenShift Container Platform**` |
| `**Understand Project Configuration**` | `**Understand the Project Configuration**` |
| `**Understand Registry Authentication**` | `**Understand Registry Authentication**` |

**Note:** This pattern is inconsistent - some "Understand" headings were simplified, others retained but got articles.

### 9. Word Choice: "Due to" vs "Because of"

Matt changed "due to" to "because of" in certain contexts.

| Before | After |
|--------|-------|
| `FastAPI provides the ideal framework for LLM inference APIs due to its performance characteristics` | `FastAPI provides the ideal framework for LLM inference APIs because of its performance characteristics` |

**Rule:** Prefer "because of" over "due to" when describing causation.

### 10. Parentheses vs Inline Clarity

Matt restructured parenthetical information for clarity.

| Before | After |
|--------|-------|
| `create the main application file **serve.py** that handles` | `create the main application file (serve.py) that handles` |
| `create a **Dockerfile** that defines` | `create a Dockerfile that defines` |
| `backticks for `llm-demo`` | `*llm-demo*` (italics for project name in running text) |

**Rule:** Use parentheses for file names in running prose, not bold. Use italics for project names in inline references.

### 11. Semicolon Usage

Matt changed semicolons in run-on instructions to periods or other punctuation.

| Before | After |
|--------|-------|
| `accept them, as this is expected...` | `accept them; this is expected...` |

**Note:** Matt used semicolons to join closely related independent clauses.

### 12. Range Format Standardization

Matt standardized numerical ranges.

| Before | After |
|--------|-------|
| `36 GB RAM` | `36-GB RAM` |
| `100-GB of disk space` | `100 GB of disk space` |
| `2-5 seconds` | `2 to 5 seconds` |

**Rule:** Use hyphenated compound adjectives before nouns (`36-GB RAM`), but spell out "to" for ranges in prose (`2 to 5 seconds`).

### 13. List Item Terminal Punctuation

Matt consistently ensured list items that were incomplete sentences had no periods, while complete sentences had periods.

| Before | After |
|--------|-------|
| `- Bypasses registry connectivity issues.` | `- Bypasses registry connectivity issues` |
| `- Uses OpenShift's native build system...` | `- Uses the OpenShift native build system...` |
| `- Eliminates the need for manual image pushing.` | `- Eliminates the need for manual image pushing` |

**Rule:** Omit periods from list items that are not complete sentences. Remove possessive apostrophe from product names ("OpenShift's" -> "the OpenShift").

### 14. Plural to Singular for Technical Terms

Matt adjusted plural forms for technical accuracy.

| Before | After |
|--------|-------|
| `OpenShift Routes provide several advantages` | `OpenShift Route provides several advantages` |
| `OpenShift Image Streams provide several advantages` | `OpenShift image streams provide several advantages` |
| `Legal Disclaimers` | `Legal Disclaimer` |

**Rule:** When describing a Kubernetes/OpenShift resource type conceptually, use singular form. Lowercase generic references.

### 15. "By Using" Construction

Matt did NOT enforce the "by using" construction in this PR - the original text already used it correctly:

| Existing (kept) |
|-----------------|
| `deploy a high-performance LLM inference server...by using standard CPU resources` |
| `Confirm that your project was created successfully by using the OpenShift CLI` |

**Observation:** The "by using" construction was already present in this tutorial; no corrections needed.

---

## NEW Rules Not in Current Tier 1

### HIGH VALUE - Add to Agent

1. **List punctuation pattern**
   - Bold label followed by colon-space, not colon-space with hyphen formatting
   - Pattern: `- **Label:** Description...` (note space after colon)
   - **Add:** "In bold list items, use format `- **Label:** Description` with colon immediately after bold"

2. **"Step" to "topic" terminology**
   - Current prompt has no rule about this
   - Matt consistently changes "step" to "topic" for section transitions
   - **Add:** "Use 'topic' when referring to the next section within a tutorial, not 'step'"

3. **Compound words: nonblocking, nonroot, pretrained**
   - Current prompt mentions "lifecycle" but not these
   - **Add:** "Compound words: 'nonblocking' (one word), 'nonroot' (one word), 'pretrained' (one word)"

4. **"Output similar" pattern**
   - Matt consistently changes `You should see an output similar to` -> `You should see output that is similar to`
   - **Add:** "Use 'You should see output that is similar to' (no 'an' before 'output')"

5. **Possessive form removal for products**
   - `OpenShift's native build system` -> `the OpenShift native build system`
   - **Add:** "Do not use possessive form for product names; use 'the' + product name instead"

6. **Subject addition in list items**
   - List items describing properties need explicit subjects
   - **Add:** "List item descriptions should include subjects (e.g., 'The model is optimized...' not 'Optimized...')"

7. **Menu navigation formatting**
   - Each element in navigation path should be separately bolded
   - **Add:** "Menu navigation: bold each element separately with > separator: `**Home** > **Projects**`"

8. **Range formatting**
   - Hyphenated compound adjectives before nouns, spelled-out ranges in prose
   - **Add:** "Hyphenate measurements before nouns (36-GB RAM), but use 'to' for ranges in prose (2 to 5 seconds)"

### MEDIUM VALUE - Consider Adding

9. **H3 to bold for subsections within steps**
   - Already identified in other PRs
   - Strong confirmation of pattern here

10. **Resource name capitalization**
    - Kubernetes Deployment, Service (initial caps)
    - But "service" and "route" when generic
    - Complex rule requiring context

---

## Assessment Against New Tier 1 Rules

### Compound Words

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `life cycle` (two words) | Not found | N/A |
| `drop-down` (hyphenated) | Not found | N/A |
| `file system` (two words) | Not found | N/A |
| `nonblocking` (one word) | Yes - Matt changed `Non-blocking` -> `Nonblocking` | NO - not in current rules |
| `nonroot` (one word) | Yes - Matt changed `Non-root` -> `Nonroot` | NO - not in current rules |
| `pretrained` (one word) | Yes - Matt changed `pre-trained` -> `pretrained` | NO - not in current rules |

### "By Using" Construction

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `configure using X` -> `configure by using X` | Already correct in original | YES - would not flag (correct) |

### No Contractions

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `it's` -> `it is` | Not found in this PR | N/A |
| Other contractions | `you're logged in` kept in troubleshooting note | Partial - depends on context |

### Protocol Names Caps

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `Radius` -> `RADIUS` | Not found | N/A |
| `iBGP` -> `IBGP` | Not found | N/A |
| `HTTP/HTTPS` | Correctly capped throughout | YES |
| `SSL/TLS` | Spelled out: `SSL and TLS` | Handled differently |

### H3 to Bold

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `### Subsection` -> `**Subsection**` | Yes - 35+ instances converted | NO - not in current rules |

### Feature Names Lowercase

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| `Business Transactions` -> `business transactions` | Not applicable (different domain) | N/A |
| `Service` vs `service` | Matt kept Kubernetes Service caps, lowercase generic | Partial - context-dependent |
| `Route` vs `route` | Matt kept OpenShift Route caps, lowercase generic | Partial - context-dependent |

### "vs." in Comparisons

| Rule | Found in PR | Agent Would Catch |
|------|-------------|-------------------|
| Use of "vs." | Not found in this PR | N/A |

---

## Agent Coverage Assessment

### What Current Agent WOULD Catch (~30%)

| Pattern | Coverage |
|---------|----------|
| Bold for GUI elements | Yes |
| Heading gerund to imperative | Yes |
| Serial comma | Yes |
| Trailing whitespace | Yes |
| "Click on" to "Click" | Yes |
| HTTP/HTTPS capitalization | Yes |
| Double spaces | Yes |

### What Current Agent Would MISS (~70%)

| Pattern | Gap |
|---------|-----|
| List punctuation (colon-space format) | No rule |
| H3 to bold subsections | No rule |
| "Step" to "topic" terminology | No rule |
| Compound words (nonblocking, nonroot, pretrained) | Incomplete |
| "Output similar" article removal | No rule |
| Possessive form removal for products | No rule |
| Subject addition in list items | No rule |
| Menu navigation multi-bold format | Incomplete |
| Range formatting rules | No rule |
| Resource name capitalization (context-dependent) | Too complex |
| "Due to" vs "because of" | No rule |

---

## Quality Assessment

**Estimated Agent Coverage:** 30%

This PR shows extensive editorial patterns focused on:

1. **Structural formatting** - H3 to bold conversions, list punctuation standardization
2. **Compound word styling** - nonblocking, nonroot, pretrained
3. **Technical precision** - Kubernetes resource naming, article usage
4. **Consistency patterns** - "step" to "topic", output phrasing

The 70% gap is significant because this tutorial is technical and well-written to begin with. Matt's edits are largely about:

- Style consistency (list punctuation patterns)
- Terminology precision (step vs topic)
- Structural formatting (H3 to bold)
- Compound word conventions

### Priority Additions to Improve Coverage

**Would increase coverage to ~55%:**

1. Add list punctuation pattern rule (`- **Label:** Description`)
2. Add "step" -> "topic" rule
3. Add compound words: nonblocking, nonroot, pretrained
4. Add "output similar" pattern
5. Add possessive form removal for products
6. Add H3 to bold subsection rule

**Would increase to ~65%:**

7. Add menu navigation multi-bold format
8. Add range formatting rules
9. Add subject addition in list items rule
10. Add "due to" -> "because of" rule

---

## Matt's Editorial Notes (from commit messages)

1. **Terminology clarification:** "I changed 'Kubernetes Deployments, Services, and Routes' to 'Kubernetes Deployment, Service, and Ingress (for routes).' Ingress (not 'Route' or 'Routes') is the proper Kubernetes name..."

2. **Product naming precision:** "In step 2, I changed 'OpenShift Route to expose the Service' to 'OpenShift Route to expose the Kubernetes Service' to distinguish between OpenShift and Kubernetes."

3. **Screenshot consistency:** "In step 4, I changed the Display name setting from 'LLM Demo' to 'llm-demo' in order to match the Display name shown in the accompanying screenshot..."

4. **Content sensitivity:** "In step 10, the 'Test Current Events and General Knowledge' subtopic asks the user to test the model's performance with a political knowledge question... I would recommend using a general knowledge question here instead that avoids any connection to politics..."

---

## Comparison with Tier 1 Rules Focus

| Tier 1 Rule | Evidence in PR #193 | Agent Detection |
|-------------|---------------------|-----------------|
| Compound words (life cycle, drop-down, file system) | Not found | N/A |
| Compound words (nonblocking, nonroot, pretrained) | Found and corrected | NO |
| "by using" construction | Already correct | N/A |
| No contractions | Not found | N/A |
| Protocol names caps | Correctly used | YES |
| H3 to bold | 35+ instances | NO |
| Feature names lowercase | Context-dependent | Partial |
| "vs." in comparisons | Not found | N/A |

**Conclusion:** Of the NEW Tier 1 rules being assessed, only the H3-to-bold pattern and compound word corrections are strongly evidenced in this PR. The agent would NOT catch either of these currently. Adding these rules would significantly improve coverage for this type of technical tutorial.
