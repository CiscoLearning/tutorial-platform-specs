# Expected Editorial Issues - Agent Validation Test

This document lists all known editorial issues in `test-step-1.md` and the expected agent behavior.

## Issues That SHOULD Be Caught (Based on Current Rules)

### 1. Gerund → Imperative Headings (2 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 13 | `### Understanding Network Fundamentals` | `### Understand Network Fundamentals` | GERUND_TO_IMPERATIVE |
| 17 | `### Installing Prerequisites` | `### Install Prerequisites` | GERUND_TO_IMPERATIVE |
| 40 | `## Understanding the Architecture` | `## Understand the Architecture` | GERUND_TO_IMPERATIVE |

### 2. Unit Spacing (2 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 9 | `8GB of RAM` | `8 GB of RAM` | UNIT_SPACING |
| 9 | `16GB of storage` | `16 GB of storage` | UNIT_SPACING |
| 30 | `8GB RAM` | `8 GB RAM` | UNIT_SPACING |

### 3. Bold List Items → Plain (4 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 21 | `- **Python 3.10:** The required` | `- Python 3.10: the required` | BOLD_LIST_ITEM |
| 22 | `- **Docker:** For containerization` | `- Docker: for containerization` | BOLD_LIST_ITEM |
| 23 | `- **Git:** For version control` | `- Git: for version control` | BOLD_LIST_ITEM |
| 24 | `- **Kubernetes:** For orchestration` | `- Kubernetes: for orchestration` | BOLD_LIST_ITEM |

### 4. No Contractions (5 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 7 | `you'll learn` | `you will learn` | NO_CONTRACTIONS |
| 9 | `you'll also` | `you will also` | NO_CONTRACTIONS |
| 15 | `It's important` | `It is important` | NO_CONTRACTIONS |
| 15 | `can't proceed` | `cannot proceed` | NO_CONTRACTIONS |
| 28 | `You'll need` | `You will need` | NO_CONTRACTIONS |

### 5. Deprecated Cisco Acronyms (2 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 9 | `the FMC` | `Firewall Management Center` | FMC_DEPRECATED |
| 9 | `your FTD devices` | `Firewall Threat Defense devices` | FTD_DEPRECATED |

### 6. Compound Words (3 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 42 | `lifecycle` | `life cycle` | COMPOUND_LIFECYCLE |
| 42 | `pre-installed` | `preinstalled` | COMPOUND_PREFIX |
| 42 | `non-root` | `nonroot` | COMPOUND_PREFIX |

### 7. "Click on" → "Click" (1 instance)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 46 | `Click on **Save**` | `Click **Save**` | CLICK_ON |

### 8. H3 → Bold for Subsections (2 instances)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 13 | `### Understanding Network Fundamentals` | `**Understand Network Fundamentals**` | H3_TO_BOLD |
| 17 | `### Installing Prerequisites` | `**Install Prerequisites**` | H3_TO_BOLD |

### 9. Key Takeaways → Important Takeaways (1 instance)

| Line | Original | Expected Fix | Rule |
|------|----------|--------------|------|
| 52 | `## Key Takeaways` | `**Important Takeaways**` | KEY_TAKEAWAYS |

---

## Issues That May Be MISSED (Known Gaps)

### 1. Em-dash Spacing
No instances in this test file.

### 2. Button Reference Clarity
| Line | Original | Gap |
|------|----------|-----|
| 46 | `click **Apply**` | Should be `click the **Apply** button` - NOT COVERED |

### 3. "ensures" → "helps ensure" Softening
No instances in this test file.

### 4. Acronym First-Use Expansion
| Line | Original | Gap |
|------|----------|-----|
| 32 | `CLI knowledge` | Should expand CLI on first use - NOT COVERED |
| 33 | `APIs` | Should expand API on first use - NOT COVERED |

### 5. Blockquote Note Prefix
| Line | Original | Gap |
|------|----------|-----|
| 44 | `> By following...` | Should be `> **Note:** By following...` - NOT COVERED |

### 6. Example Formatting (Inline)
| Line | Original | Gap |
|------|----------|-----|
| 48-50 | `**Example:**\n\nThis is...` | Should be inline - NOT COVERED |

---

## Summary

| Category | Expected Catches | Current Rules |
|----------|------------------|---------------|
| Gerund → Imperative | 3 | YES |
| Unit Spacing | 3 | YES |
| Bold List Items | 4 | YES |
| No Contractions | 5 | YES |
| Cisco Deprecated Acronyms | 2 | YES |
| Compound Words | 3 | YES |
| Click on | 1 | YES |
| H3 → Bold | 2 | YES |
| Key Takeaways | 1 | YES |
| **TOTAL EXPECTED CATCHES** | **24** | - |

| Category | Known Gaps | Coverage |
|----------|------------|----------|
| Button Reference Clarity | 1 | NOT COVERED |
| Acronym First-Use | 2 | NOT COVERED |
| Blockquote Note Prefix | 1 | NOT COVERED |
| Example Inline Format | 1 | NOT COVERED |
| **TOTAL EXPECTED MISSES** | **5** | - |

**Expected Coverage Rate: 24/29 = 82.8%**

This test file is designed to validate that our rules catch the expected issues.

---

## Validation Process

1. Run the editorial agent against `test-step-1.md`
2. Compare detected issues against this expected list
3. Calculate actual vs expected coverage
4. Identify any false positives or false negatives

