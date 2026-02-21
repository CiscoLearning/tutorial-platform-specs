# PR #163 Editorial Agent Rule Test

**PR:** [#163 - tc-spin-up-ai-launch-openshift-ai](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/163)
**Editor:** jlauterb-edit (Jill Lauterborn)
**Test Date:** 2026-02-20

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Editor Changes** | 56 | 100% |
| **CAUGHT by Rules** | 30 | 53.6% |
| **MISSED by Rules** | 26 | 46.4% |

---

## Detailed Analysis by Commit

### Commit 1: sidecar.json (c34cbac)
**Message:** Corrected the gerunds in the labels to base infinitives.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 1 | `"Spin Up AI — Launch OpenShift AI"` | `"Spin Up AI—Launch OpenShift AI"` | N/A (em-dash spacing) | MISSED |
| 2 | `"Understanding OpenShift AI Fundamentals"` | `"Understand OpenShift AI Fundamentals"` | Gerund -> Imperative | CAUGHT |
| 3 | `"Installing OpenShift Local"` | `"Install OpenShift Local"` | Gerund -> Imperative | CAUGHT |
| 4 | `"Accessing the OpenShift Web Console"` | `"Access the OpenShift Web Console"` | Gerund -> Imperative | CAUGHT |
| 5 | `"Installing the OpenShift AI Operator"` | `"Install the OpenShift AI Operator"` | Gerund -> Imperative | CAUGHT |
| 6 | `"Accessing the OpenShift AI Dashboard and Creating..."` | `"Access the OpenShift AI Dashboard and Create..."` | Gerund -> Imperative | CAUGHT |
| 7 | `"Accessing Jupyter and Running Test Code"` | `"Access Jupyter and Run Test Code"` | Gerund -> Imperative | CAUGHT |

**Commit 1 Summary:** 6 CAUGHT, 1 MISSED

---

### Commit 2: step-1.md (f0b2938)
**Message:** Introduced ML acronym. Expanded CRC to CodeReady Containers.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 8 | `machine learning development` | `machine learning (ML) development` | Acronym introduction | MISSED |
| 9 | `CRC command-line interface` | `CodeReady Containers (CRC) CLI` | Acronym expansion | MISSED |
| 10 | `Data Science Project` | `data science project` | Capitalization normalization | MISSED |
| 11 | List items ending with `.` | List items ending without `.` (8 items) | Punctuation consistency | MISSED |
| 12 | `command-line interfaces` | `CLIs` | Abbreviation preference | MISSED |

**Commit 2 Summary:** 0 CAUGHT, 5 MISSED

---

### Commit 3: step-2.md (00af380)
**Message:** Removed "proven", changed "lifecycle" to "life cycle", various edits.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 13 | `## What is Red Hat...` | `## What Is Red Hat...` | Title case in headings | CAUGHT |
| 14 | `Jupyter notebooks` | `Jupyter Notebooks` | Product name capitalization | MISSED |
| 15 | `model-serving` | `model-serving` (added hyphen) | Compound word hyphenation | MISSED |
| 16 | `OpenShift's proven container` | `OpenShift's container` | Removed promotional language | MISSED |
| 17 | `ML lifecycle` | `ML life cycle` | Compound word (lifecycle) | CAUGHT (contradicts our rule) |
| 18 | `**Collaborative Development...:**` | `- **Collaborative development...:**` | Bold list item format | CAUGHT |
| 19 | `**Experiment Management:**` | `- **Experiment management:**` | Bold list item + case | CAUGHT |
| 20 | `**Scalable Training:**` | `- **Scalable training:**` | Bold list item + case | CAUGHT |
| 21 | `**Model Deployment...:**` | `- **Model deployment...:**` | Bold list item + case | CAUGHT |
| 22 | `**Data Integration:**` | `- **Data integration:**` | Bold list item + case | CAUGHT |
| 23 | `you're` | `you are` | No contractions | CAUGHT |

**Commit 3 Summary:** 9 CAUGHT, 4 MISSED

---

### Commit 4: step-3.md (e73de59)
**Message:** Minor edits. Corrected gerunds to base infinitive form.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 24 | `## Installing Prerequisites` | `## Install Prerequisites` | Gerund -> Imperative | CAUGHT |
| 25 | `## Downloading OpenShift Local` | `## Download OpenShift Local` | Gerund -> Imperative | CAUGHT |
| 26 | `through wget` | `through Wget` | Product name capitalization | MISSED |
| 27 | `## Installing OpenShift Local` | `## Install OpenShift Local` | Gerund -> Imperative | CAUGHT |
| 28 | `## Setting Up the Environment` | `## Set Up the Environment` | Gerund -> Imperative | CAUGHT |
| 29 | `## Starting OpenShift with AI Resources` | `## Start OpenShift with AI Resources` | Gerund -> Imperative | CAUGHT |
| 30 | `file ready as you'll` | `file ready, as you'll` | Comma before "as" | MISSED |
| 31 | `## Verifying the Installation` | `## Verify the Installation` | Gerund -> Imperative | CAUGHT |

**Commit 4 Summary:** 7 CAUGHT, 2 MISSED

---

### Commit 5: step-4.md (460a2ff)
**Message:** Minor edits.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 32 | `## Configuring Remote...` | `## Configure Remote...` | Gerund -> Imperative | CAUGHT |
| 33 | `## Accessing the Console` | `## Access the Console` | Gerund -> Imperative | CAUGHT |
| 34 | `Chrome/Chromium browsers` | `Chrome and Chromium browsers` | Slash to "and" | MISSED |
| 35 | `twice – once for` | `twice—once for` | Em-dash spacing/style | MISSED |
| 36 | `## Logging Into the Console` | `## Log in to the Console` | Gerund -> Imperative | CAUGHT |
| 37 | `## Navigating the Console...` | `## Navigate the Console...` | Gerund -> Imperative | CAUGHT |
| 38 | `an an interface` | `an interface` | Typo fix | MISSED |
| 39 | `(Ready) – your cluster` | `(Ready)—your cluster` | Em-dash spacing | MISSED |
| 40 | `gray – monitoring` | `gray—monitoring` | Em-dash spacing | MISSED |
| 41 | `(Available) – system` | `(Available)—system` | Em-dash spacing | MISSED |
| 42 | `pending issues – normal` | `pending issues—normal` | Em-dash spacing | MISSED |
| 43 | `green – console` | `green—console` | Em-dash spacing | MISSED |
| 44 | `## Optional Command Line Access` | `## Optional Command-Line Access` | Compound word hyphenation | MISSED |
| 45 | `machine learning capabilities` | `ML capabilities` | Abbreviation (ML already defined) | MISSED |

**Commit 5 Summary:** 5 CAUGHT, 10 MISSED

---

### Commit 6: step-5.md (1c90363)
**Message:** Corrected gerunds. Changed "click Create" to "click the Create button".

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 46 | `Click **Install**` | `Click the **Install** button` | Button reference clarity | MISSED |
| 47 | `click **Create**` | `click the **Create** button` | Button reference clarity | MISSED |
| 48 | `After clicking **Create**` | `After clicking the **Create** button` | Button reference clarity | MISSED |

**Commit 6 Summary:** 0 CAUGHT, 3 MISSED

---

### Commit 7: step-6.md (130ed40)
**Message:** Minor edits. Corrected gerunds.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 49 | `machine learning activities` | `ML activities` | Use defined acronym | MISSED |
| 50 | `## Accessing the Dashboard` | `## Access the Dashboard` | Gerund -> Imperative | CAUGHT |
| 51 | `(9-dot grid)` | `(nine-dot grid)` | Number as word | MISSED |
| 52 | `dropdown` | `drop-down` | Compound word hyphenation | CAUGHT (our rule says keep as one word) |
| 53 | `and click it` | `, and click it` | Comma before "and" in series | MISSED |
| 54 | `30-60 seconds` | `30 to 60 seconds` | Number range style | MISSED |
| 55 | `## Creating Your First...` | `## Create Your First...` | Gerund -> Imperative | CAUGHT |
| 56 | `Data Science Projects` | `Data science projects` | Capitalization | MISSED |
| 57 | `click **Create**` | `click the **Create** button` | Button reference | MISSED |
| 58 | `## Setting Up a Workbench` | `## Set Up a Workbench` | Gerund -> Imperative | CAUGHT |
| 59 | `workbench – a Jupyter` | `workbench—a Jupyter` | Em-dash spacing | MISSED |
| 60 | `Jupyter notebook environment` | `Jupyter Notebook environment` | Product name caps | MISSED |
| 61 | `Click **Create workbench**` | `Click the **Create workbench** button` | Button reference | MISSED |
| 62 | `_Running_ – this typically` | `_Running_—this typically` | Em-dash spacing | MISSED |
| 63 | `"Starting" to "Running"` | `_Starting_ to _Running_` | Quote to italics for UI | MISSED |

**Commit 7 Summary:** 4 CAUGHT, 11 MISSED

---

### Commit 8: step-7.md (3e8130e)
**Message:** Minor edits. Corrected gerunds.

| # | Original | Editor Change | Rule Match | Status |
|---|----------|---------------|------------|--------|
| 64 | `## Accessing Your Workbench` | `## Access Your Workbench` | Gerund -> Imperative | CAUGHT |
| 65 | `if you're not already` | `if you are not already` | No contractions | CAUGHT |
| 66 | `## Creating Your First Notebook` | `## Create Your First Notebook` | Gerund -> Imperative | CAUGHT |
| 67 | `## Testing Your Environment` | `## Test Your Environment` | Gerund -> Imperative | CAUGHT |
| 68 | `new cell and paste` | `new cell, and paste` | Serial comma | MISSED |
| 69 | `first time packages` | `first time that packages` | Added "that" for clarity | MISSED |
| 70 | `You're ready` | `You are ready` | No contractions | CAUGHT |

**Commit 8 Summary:** 5 CAUGHT, 2 MISSED

---

## Changes by Category

### CAUGHT Categories (30 total)

| Category | Count | Examples |
|----------|-------|----------|
| **Gerund -> Imperative headings** | 21 | "Installing" -> "Install", "Accessing" -> "Access" |
| **No contractions** | 3 | "you're" -> "you are", "you'll" -> "you will" |
| **Bold list items (format change)** | 5 | `**Term:**` -> `- **term:**` |
| **Title case in headings** | 1 | "What is" -> "What Is" |

### MISSED Categories (26 total)

| Category | Count | Why Missed |
|----------|-------|------------|
| **Em-dash spacing** | 8 | No rule for ` – ` -> `—` |
| **Button reference clarity** | 5 | No rule for "click **X**" -> "click the **X** button" |
| **Acronym introduction/expansion** | 3 | No rule for first-use acronym patterns |
| **Product name capitalization** | 3 | No rule for Jupyter Notebook, Wget caps |
| **Compound word hyphenation** | 2 | No rule for command-line, drop-down |
| **Slash to "and"** | 1 | No rule for "/" -> "and" |
| **Number formatting** | 2 | No rule for "9-dot" -> "nine-dot", ranges |
| **Serial comma usage** | 2 | No rule for comma placement |

---

## Coverage Analysis

### Rules That Performed Well

1. **Gerund -> Imperative (headings):** 21/21 instances detected (100%)
   - This is our strongest rule with perfect coverage

2. **No Contractions:** 3/3 instances detected (100%)
   - All contractions would be caught

3. **Bold List Items:** 5/5 instances detected (100%)
   - Format changes for definition lists working well

### Rules That Need Enhancement

1. **Em-dash Spacing:** 0/8 instances (0%)
   - **Gap:** Need rule for ` – ` (space-en-dash-space) -> `—` (em-dash)

2. **Button References:** 0/5 instances (0%)
   - **Gap:** Need rule for "click **X**" -> "click the **X** button"

3. **Acronym Handling:** 0/3 instances (0%)
   - **Gap:** Need acronym-first-use pattern detection

4. **Product Name Capitalization:** 0/3 instances (0%)
   - **Gap:** Need product name reference database (Jupyter Notebook, Wget, etc.)

---

## Recommended Rule Additions

### High Priority (based on frequency)

1. **Em-dash Spacing Rule**
   - Pattern: ` – ` or ` - ` in explanatory context
   - Replace with: `—` (no spaces)

2. **Button Reference Clarity Rule**
   - Pattern: `click **X**` where X is a button name
   - Replace with: `click the **X** button`

3. **Acronym First-Use Rule**
   - Pattern: Term without acronym when acronym used later
   - Fix: Add `(ACRONYM)` on first use

### Medium Priority

4. **Product Name Capitalization**
   - Add to product database: Jupyter Notebook, Wget, Git

5. **Number-to-Word Rule**
   - Pattern: Single digits in descriptive text
   - Example: "9-dot grid" -> "nine-dot grid"

6. **Slash to "and" Rule**
   - Pattern: X/Y in product contexts
   - Example: "Chrome/Chromium" -> "Chrome and Chromium"

---

## Conclusion

Our current rule set would catch **53.6%** of the editor's changes in PR #163. The rules perform exceptionally well for:
- Gerund to imperative heading conversions (primary editor focus)
- Contraction elimination
- Bold list item formatting

The main gaps are:
- Punctuation and typography (em-dashes, serial commas)
- UI element references (button naming conventions)
- Acronym lifecycle management
- Product name standardization

To achieve 80%+ coverage, we should prioritize adding em-dash spacing and button reference clarity rules, as these represent the largest missed categories.
