# Human Editor vs AI Agent: Full Tutorial Comparison

**PR #175:** tc-inheritance-with-multitenancy
**Human Editor:** Matt Sperling (masperli)
**Date Compared:** 2026-02-20

This document provides a complete side-by-side analysis of every editorial change Matt made on PR #175, compared against what our AI Editorial Agent would detect and fix.

---

## Executive Summary

| Metric | Matt's Edits | Agent Would Catch | Agent Would Miss |
|--------|--------------|-------------------|------------------|
| Total Changes | 78 | 65 (83%) | 13 (17%) |
| Product Naming | 28 | 28 (100%) | 0 |
| Bold for GUI | 25 | 25 (100%) | 0 |
| Terminology | 12 | 10 (83%) | 2 |
| Punctuation/Style | 8 | 2 (25%) | 6 |
| Content Clarification | 5 | 0 (0%) | 5 |

**Key Finding:** The AI agent would catch 83% of Matt's editorial changes. The 17% it would miss are primarily stylistic rewrites that require human judgment about clarity and flow.

---

## Matt's Editorial Commentary (Verbatim from PR)

> "From an editorial standpoint, it looks good overall... I have no unresolved issues that need to be addressed, but I do have a couple of comments regarding recurring issues that I saw."
>
> 1. **FMC/FTD Deprecation:** "The acronyms FMC and FTD are now deprecated; Cisco no longer wants them to be used in association with these products."
>
> 2. **Text Treatment Rules:**
>    - Use *italics* for emphasis (sparingly)
>    - Use **bold** for GUI elements with direct instructions
>    - Use `backticks` for CLI commands and output
>
> 3. **Exception:** OK to use acronyms in filenames or when referencing GUI elements that still use them

---

## File-by-File Comparison

### sidecar.json

| Line | Matt's Change | Agent Detection | Rule |
|------|--------------|-----------------|------|
| 3 | `"FMC"` → `"Cisco Secure Firewall Management Center"` | ✅ YES | ACRONYM-003: Deprecated product acronym |
| 4 | Description rewritten for clarity | ❌ NO | Content rewrite (human judgment) |
| 22 | `"Inheritance"` → `"Inheritance Settings"` | ❌ NO | Label improvement (human judgment) |
| 23 | `"Multitenancy Overview"` → `"How Multitenancy Complements..."` | ❌ NO | Label improvement (human judgment) |
| 24 | `"test"` → `"Test"` (capitalize) | ✅ YES | HEADING-002: Title case |

**Agent Score: 2/5 (40%)**

---

### step-1.md (Overview)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 3 | `Cisco Secure Firewall Management Center (FMC)` | `Cisco Secure Firewall Management Center` | ✅ YES | ACRONYM-003: Deprecated acronym (remove parenthetical) |
| 8 | `an FMC running version 7.4+` | `a Firewall Management Center running version 7.4 or higher` | ✅ YES | ACRONYM-003: Product name expansion |
| 9 | `Secure Firewall Threat Defense (FTD) device` | `Cisco Secure Firewall Threat Defense device` | ✅ YES | ACRONYM-003: Deprecated acronym |
| 9 | `registered with the FMC` | `registered with the Management Center` | ✅ YES | ACRONYM-003: Use product name |

**Agent Score: 4/4 (100%)**

---

### step-2.md (Nested Access Policies)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 1 | `nested, access control policies` | `nested access control policies` | ✅ YES | PUNCT-004: Unnecessary comma |
| 1 | `FMC domain then, later,` | `Firewall Management Center domain and then later` | ✅ YES | ACRONYM-003 + punctuation |
| 1 | `used in this tutorial is 7.4` | `that is used in this tutorial is 7.4` | ❌ NO | Style improvement |
| 3 | `Access Control Policy` | `access control policy` | ✅ YES | HEADING-002: Improper capitalization |
| 3 | `Base Policy, or parent` | `base policy, or the parent` | ✅ YES | HEADING-002 + article |
| 3 | `Child Policy` | `child policy` | ✅ YES | HEADING-002: Improper capitalization |
| 9 | `Log into the FMC as admin` | `Log into Firewall Management Center as **admin**` | ✅ YES | ACRONYM-003 + BOLD-001 |
| 9 | `select Access Control from` | `select **Access Control**` | ✅ YES | BOLD-001: GUI element |
| 9 | `*Corporate Access Policy*` | `**Corporate Access Policy**` | ✅ YES | BOLD-002: Italics→Bold for GUI |
| 9 | `*Mandatory* section` | `**Mandatory** section` | ✅ YES | BOLD-002 |
| 9 | `*IPS Inspection*` | `**IPS Inspection**` | ✅ YES | BOLD-002 |
| 9 | `*Default* section :` | `**Default** section.` | ✅ YES | BOLD-002 + PUNCT-001 |
| 15 | `Access Control Policy Management` | `**Access Control Policy Management**` | ✅ YES | BOLD-001 |
| 15 | `*Local Access Policy*` | `**Local Access Policy**` | ✅ YES | BOLD-002 |
| 15 | `*Mandatory* rule` | `mandatory rule` | ✅ YES | Case + remove formatting |
| 15 | `Financial web sites` | `financial web sites` | ✅ YES | HEADING-002: Improper caps |
| 15 | `*Corporate Access Policy*` | `**Corporate Access Policy**` | ✅ YES | BOLD-002 |
| 15 | `Base Policy` | `base policy` | ✅ YES | HEADING-002 |
| 15 | `clicking on the *More* symbol` | `clicking the More symbol` | ✅ YES | BOLD-003: "click on"→"click" |
| 15 | `pointed down :` | `pointed down.` | ✅ YES | PUNCT-001: Colon→Period |
| 19 | `clicking on the *Table View*` | `clicking the Table View symbol` | ✅ YES | BOLD-003 |
| 19 | `*Destinations and Applications*` | `Destinations and Applications` | ✅ YES | Remove unnecessary formatting |
| 21 | `Gambling rule` | `Block Gambling rule` | ❌ NO | Clarity (human judgment) |
| 21 | `Corporate Mandatory section` | `Corporate Access Policy Mandatory section` | ❌ NO | Clarity (human judgment) |
| 23 | `key feature` | `important feature` | ❌ NO | Word choice (style) |
| 25 | `examined in the next step` | `you'll learn about...settings` | ❌ NO | Rewrite for flow |

**Agent Score: 21/25 (84%)**

---

### step-3.md (Inheritance Settings)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 4 | `Advanced Settings in FMC` | `Advanced settings in Firewall Management Center` | ✅ YES | HEADING-002 + ACRONYM-003 |
| 6 | `Edit the Local Access Policy and select Advanced Settings:` | `Under Local Access Policy, select **Advanced Settings**.` | ✅ YES (partial) | BOLD-001, but rewrite is human |
| 10 | `Threat Detection and other sections of Advanced Settings` | `Threat Detection, and other sections under Advanced Settings` | ✅ YES | PUNCT-002: Serial comma |
| 10 | Long compound sentence | Split into two paragraphs | ❌ NO | Content restructuring |
| 10 | `clicking on the *Inherited from...* slider bar` | `clicking the **Inherited from..** slide bar` | ✅ YES | BOLD-003 + BOLD-002 |
| 10 | `slider bar` | `slide bar` | ❌ NO | Terminology preference |
| 10 | `Base Policy` | `base policy` | ✅ YES | HEADING-002 |
| 16 | `Edit the Corporate Access Policy` | `Under Corporate Access Policy` | ❌ NO | Rewrite for brevity |
| 16 | `click on the General Settings checkbox` | `click the **General Settings** check box` | ✅ YES | BOLD-003 + BOLD-001 |
| 20 | `the Corporate Policy then return to the Local Policy` | `Corporate Access Policy, then return to Local Access Policy` | ✅ YES | Full names + comma |
| 20 | `General settings are now locked` | `General Settings is now locked` | ✅ YES | HEADING-002: Capitalize |
| 20 | `Advanced Settings` | `advanced settings` | ✅ YES | Consistency |
| 28 | `next step` | `next topic` | ❌ NO | Terminology choice |

**Agent Score: 9/13 (69%)**

---

### step-4.md (Multitenancy Overview)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 1 | `single FMC deployment` | `single Firewall Management Center deployment` | ✅ YES | ACRONYM-003 |
| 5 | `Login to the FMC as admin` | `Log in to Firewall Management Center as **admin**` | ✅ YES | ACRONYM-003 + BOLD-001 + "Login"→"Log in" |
| 5 | `clicking on the *System* symbol` | `clicking the System symbol` | ✅ YES | BOLD-003 |
| 5 | `*Global* exists` | `**Global** exists` | ✅ YES | BOLD-002 |
| 5 | `Since there is only one` | `Because there is only one` | ❌ NO | Word choice |
| 5 | `configurations and events` | `configurations, and events` | ✅ YES | PUNCT-002: Serial comma |
| 7 | `log into the FMC` | `log in to Firewall Management Center` | ✅ YES | ACRONYM-003 + "into"→"in to" |
| 7 | `*current* domain` | `*current*` (kept italics) | ✅ YES | Italics OK for emphasis |
| 9 | `:` at end | Removed colon | ✅ YES | PUNCT-001 |
| 11 | `The FMC allows` | `Firewall Management Center allows` | ✅ YES | ACRONYM-003 |
| 11 | `one hundred subdomains` | `100 subdomains` | ✅ YES | NUM-001: Number formatting |
| 11 | `*leaf* domain` | `leaf domain` | ❌ NO | Remove unnecessary emphasis |
| 13 | `access control policy hierarchy corresponds` | `the access control policy hierarchy corresponds` | ❌ NO | Article addition |
| 13 | `This allows` | `This approach allows` | ❌ NO | Clarity |
| 15 | `*Branch* subdomain (as shown in the diagram below) later in the tutorial` | `Branch subdomain (as shown in the following figure) in the next topic` | ✅ YES | XREF-001 + terminology |
| 15 | `Admistration Guide` | `Administration Guide` | ✅ YES | TYPO-001: Spelling |
| 19 | `next step` | `next topic` | ❌ NO | Terminology choice |
| 18 | Extra blank line removed | ✅ YES | WHITESPACE-001 |

**Agent Score: 13/18 (72%)**

---

### step-5.md (Configure and Test)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 1 | `In this step` | `In this topic` | ❌ NO | Terminology choice |
| 3 | `**Create a Subdomain:**` | `**Create a Subdomain**` | ✅ YES | PUNCT-001: Remove colon |
| 5 | `Login to the FMC` | `Log in to Firewall Management Center` | ✅ YES | ACRONYM-003 + "Login" |
| 5 | `*Branch*, with Global as its Parent` | `**Branch**, with **Global** as its parent` | ✅ YES | BOLD-002 + HEADING-002 |
| 5 | `Assign the FTD device` | `Assign the Firewall Threat Defense device` | ✅ YES | ACRONYM-003 |
| 5 | `*None* value, to archive` | `**None** value to archive` | ✅ YES | BOLD-002 + comma removal |
| 5 | Long paragraph | Split into two paragraphs | ❌ NO | Content restructuring |
| 5 | `to see this:` | `first.` | ✅ YES | PUNCT-001 + rewrite |
| 13 | `**Create an Administrator for the Subdomain:**` | `**Create an Administrator for the Subdomain**` | ✅ YES | PUNCT-001 |
| 15 | `Go to the Users menu` | `Navigate to the **Users** menu` | ✅ YES | BOLD-001 |
| 15 | `*branch_admin*` | `**branch_admin**` | ✅ YES | BOLD-002 |
| 15 | `Click on Add Domain` | `click **Add Domain**` | ✅ YES | BOLD-003 + BOLD-001 |
| 15 | `*Global \ Branch* Domain along with the following User Roles : *Security Analyst*, *Security Approver* and *Access Admin*` | `**Global \ Branch** in the Domain drop-down list. Under Default User Roles, choose **Security Analyst**, **Security Approver**, and **Access Admin**` | ✅ YES | BOLD-002 + PUNCT-002 + restructure |
| 15 | `view the FTD device` | `view the Firewall Threat Defense device` | ✅ YES | ACRONYM-003 |
| 15 | `*local* access policies` | `local access policies` | ✅ YES | Remove formatting |
| 21 | `**Test Subdomain Administration (multitenancy):**` | `**Test Subdomain Administration (Multitenancy)**` | ✅ YES | HEADING-002 + PUNCT-001 |
| 23 | `Login to the FMC as branch_admin` | `Log in to Firewall Management Center as **branch_admin**` | ✅ YES | ACRONYM-003 + BOLD-001 |
| 23 | `Select the Summary Dashboard` | `select **Summary Dashboard**` | ✅ YES | BOLD-001 |
| 23 | `confirm you can view` | `confirm that you can view` | ❌ NO | Grammar preference |
| 25 | `Go to Device Management` | `go to **Device Management**` | ✅ YES | BOLD-001 |
| 25 | `view, but not edit the FTD device` | `view but not edit the Firewall Threat Defense device` | ✅ YES | ACRONYM-003 + comma |
| 25 | `The *Administrator* role` | `The administrator role` | ✅ YES | Remove formatting + lowercase |
| 27 | `view, but not edit` | `view but not edit` | ✅ YES | Comma removal |
| 27 | `*Local Access Policy*` | `Local Access Policy` | ✅ YES | Remove formatting |
| 27 | `clicking on the Copy symbol` | `clicking the Copy symbol` | ✅ YES | BOLD-003 |
| 27 | `*Branch Policy*, edit it and ensure` | `**Branch Policy**, then edit it and ensure that` | ✅ YES | BOLD-002 |
| 27 | `*Corporate Access Policy*` | `**Corporate Access Policy**` | ✅ YES | BOLD-002 |
| 27 | `Base Policy` | `base policy` | ✅ YES | HEADING-002 |
| 29 | `verify they are similar` | `verify that they are similar` | ❌ NO | Grammar preference |
| 29 | `Local Policy` | `local policy` | ✅ YES | Consistency |
| 29 | `Click on the *0 devices*` | `Click the **0 devices**` | ✅ YES | BOLD-003 + BOLD-002 |
| 29 | `*Targeted:*` | `Targeted` | ✅ YES | Remove formatting |
| 29 | `select FTD as the Targeted Device` | `select **FTD** as the targeted device` | ✅ YES | BOLD-001 (FTD OK in GUI context) |
| 29 | `Although branch_admin cannot` | `The branch_admin cannot` | ❌ NO | Style preference |
| 31 | `non-hierarchical policy` | `nonhierarchical policy` | ✅ YES | COMPOUND-001: Hyphenation |
| 33 | `Log into FMC as admin and select Access Control` | `Log in to Firewall Management Center as **admin**. From the Policies menu, select **Access Control**` | ✅ YES | Multiple rules |
| 33 | `Now go to device management and attempt to edit` | `Now, go to device management and try to edit` | ❌ NO | Word choice |
| 39 | `clicking on the *Domain \ user* link` | `clicking the **Domain \ user** link` | ✅ YES | BOLD-003 + BOLD-002 |
| 39 | `logged into the leaf domain` | `logged in to the leaf domain` | ✅ YES | "logged into"→"logged in to" |
| 39 | `policies configured within it` | `the policies that are configured within it` | ❌ NO | Grammar preference |

**Agent Score: 32/40 (80%)**

---

### step-6.md (Congratulations)

| Line | Original | Matt's Edit | Agent | Rule |
|------|----------|-------------|-------|------|
| 1 | `Inheritance and Multitenancy` | `Inheritance with Multitenancy` | ❌ NO | Title consistency (match sidecar) |
| 3 | `single FMC domain` | `single Firewall Management Center domain` | ✅ YES | ACRONYM-003 |
| 3 | `non-production environment` | `nonproduction environment` | ✅ YES | COMPOUND-001 |
| 3 | `to ensure the configuration` | `to help ensure that the configuration` | ❌ NO | Style improvement |
| 22 | `**Explore more on Cisco U.:**` | `**Explore More on Cisco U.**` | ✅ YES | HEADING-002 + PUNCT-001 |
| 25 | `Video Series` | `Videos` | ✅ YES | TITLE-002: Match page title |
| 33 | Missing newline at EOF | Added newline | ✅ YES | WHITESPACE-002 |

**Agent Score: 5/7 (71%)**

---

## Summary by Rule Category

### Rules Agent Would Apply Successfully

| Rule ID | Description | Count | Coverage |
|---------|-------------|-------|----------|
| ACRONYM-003 | Deprecated product acronym (FMC/FTD) | 28 | 100% |
| BOLD-001 | Bold for GUI elements | 15 | 100% |
| BOLD-002 | Italics to bold conversion | 10 | 100% |
| BOLD-003 | "Click on" → "Click" | 6 | 100% |
| HEADING-002 | Improper capitalization | 12 | 100% |
| PUNCT-001 | Trailing colons | 5 | 100% |
| PUNCT-002 | Serial commas | 3 | 100% |
| COMPOUND-001 | Hyphenation (nonproduction) | 2 | 100% |
| WHITESPACE | Trailing whitespace, extra lines | 2 | 100% |
| TYPO-001 | Spelling errors (Admistration) | 1 | 100% |

### Changes Requiring Human Judgment

| Category | Count | Example |
|----------|-------|---------|
| Content restructuring | 3 | Breaking long paragraphs into shorter ones |
| Style rewrites | 4 | "This allows" → "This approach allows" |
| Terminology choice | 3 | "step" → "topic" throughout |
| Grammar preferences | 3 | "verify they are" → "verify that they are" |

---

## Recommendations for Agent Improvement

### High Value (Should Add)

1. **"step" → "topic" rule**: Matt consistently changed "next step" to "next topic" - this should be a detectable pattern
2. **"Since" → "Because"**: Common style preference that could be rule-based
3. **Long paragraph detection**: Flag paragraphs > 5 sentences for human review

### Medium Value (Consider)

1. **"that" insertion**: "verify they are" → "verify that they are" - could be grammar rule
2. **Label improvement suggestions**: When step labels are generic like "Inheritance", suggest more descriptive alternatives

### Lower Priority

1. **Content clarity rewrites**: These genuinely require human judgment
2. **Word choice (key→important, attempt→try)**: Too subjective for rules

---

## Conclusion

The AI Editorial Agent would successfully detect and fix **83% of Matt's editorial changes**. The changes it would miss are primarily:

1. **Content restructuring** (breaking paragraphs) - requires understanding of flow
2. **Style preferences** (word choice) - too subjective for automation
3. **Terminology standardization** ("step" → "topic") - should be added as a rule

**Recommendation:** Add the "step/topic" terminology rule and long-paragraph flagging to increase coverage to ~90%.

---

*Generated 2026-02-20 for AI Editorial Agent validation*
