# PR #174 Editorial Analysis - tc-sonic-mlag

**PR URL:** https://github.com/CiscoLearning/ciscou-tutorial-content/pull/174
**Editor:** jlauterb-edit (Jill Lauterborn)
**Tutorial:** tc-sonic-mlag (Dual-Homing with SONiC Using LAG and MCLAG)
**Analysis Date:** 2026-02-20

## Summary

PR #174 contains 11 editorial commits from jlauterb-edit, covering all 9 steps plus sidecar.json. This analysis documents all editorial changes and assesses how well the proposed Tier 1 rules would catch these patterns.

---

## 1. Summary Table of Changes

| Rule Category | Occurrences | Auto-Fixable | Agent Would Catch |
|--------------|-------------|--------------|-------------------|
| No contractions | 2 | Yes | Yes |
| Article corrections (a/an/the) | 25+ | Maybe | Partial |
| Acronym expansion on first use | 3 | No | No (needs context) |
| Compound word hyphenation | 1 | Yes | Yes |
| Cisco branding compliance | 3 | Yes | Yes |
| Bold to code formatting | 8 | Maybe | Partial |
| Feature names lowercase | 1 | Yes | Yes |
| List formatting consistency | 12 | Yes | Yes |
| Remove bold from list markers | 12 | Yes | Yes |
| Remove trailing colons in headings | 1 | Yes | Yes |
| Em-dash usage | 1 | Maybe | Partial |
| Important to Note formatting | 1 | Yes | Yes |
| Title case in titles | 1 | Yes | Yes |
| Typo fixes | 1 | Maybe | Partial |

---

## 2. Before/After Examples by Rule Type

### 2.1 No Contractions (TIER 1 - DETECTED)

| Before | After | File |
|--------|-------|------|
| `It's important to verify` | `It is important to verify` | step-4.md |
| `it's crucial to configure` | `it is crucial to configure` | step-6.md |

**Agent Assessment:** The current Tier 1 rules include contractions. These would be caught.

---

### 2.2 Cisco Branding Compliance (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `Cisco IOS-based switch` | `Cisco IOS software-based switch` | step-1.md, step-4.md |
| `IOS-based switch` | `Cisco IOS software-based switch` | step-4.md |

**Editor Note:** "Based on Cisco branding guidelines"

**Agent Assessment:** NOT in current Tier 1 rules. Should be added as a Cisco-specific branding rule.

---

### 2.3 Acronym Expansion on First Use (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `MCLAG in SONiC` | `Multi-Chassis Link Aggregation Group (MCLAG) in Software for Open Networking in the Cloud (SONiC)` | sidecar.json |
| `Multichassis Link Aggregation Group` | `Multi-Chassis Link Aggregation Group` | sidecar.json, step-1.md |
| `using SSH` | `using Secure Shell (SSH)` | step-5.md |

**Agent Assessment:** NOT in current rules. Requires acronym database lookup and first-use tracking.

---

### 2.4 Compound Word Hyphenation (TIER 1 - DETECTED)

| Before | After | File |
|--------|-------|------|
| `Multichassis` | `Multi-Chassis` | sidecar.json, step-1.md, step-2.md |

**Agent Assessment:** The Tier 1 rules should include compound words. "Multi-Chassis" is the correct hyphenated form.

---

### 2.5 Bold to Code Formatting (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `**/etc/sonic/config_db.json` | `` `/etc/sonic/config_db.json` `` | step-3.md |
| `**config** keyword` | `` `config` keyword`` | step-3.md |
| `**show** keyword` | `` `show` keyword`` | step-3.md |
| `**sudo config load *file_name.json***` | `` `sudo config load file_name.json` `` | step-3.md |
| `**/etc/network/interfaces**` | `` `/etc/network/interfaces` `` | step-4.md |
| `**sudo config interface startup *interface_name***` | `` `sudo config interface startup interface_name` `` | step-5.md |
| `**--write-to-db**` | `` `--write-to-db` `` | step-3.md |
| `**sudo config vlan add *vlan_id***` | `` `sudo config vlan add vlan_id` `` | step-6.md |

**Agent Assessment:** NOT in current Tier 1 rules. Pattern: file paths and CLI commands should use code formatting, not bold.

---

### 2.6 Feature Names Lowercase (TIER 1 - DETECTED)

| Before | After | File |
|--------|-------|------|
| `Known Unicast, Broadcast, Unknown Unicast, and Multicast (BUM)` | `known unicast, broadcast, unknown unicast, and multicast (BUM)` | step-2.md |
| `Internet routing protocol` | `internet routing protocol` | step-3.md |

**Agent Assessment:** Tier 1 rules should include feature names lowercase. However, this is context-dependent.

---

### 2.7 List Formatting - Remove Bold from List Markers (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `- **Upstream switch:** Cisco IOS switch.` | `- Upstream switch: Cisco IOS switch` | step-4.md |
| `- **SONiC switches:** These might be...` | `- SONiC switches: These might be...` | step-4.md |
| `- **Host:** Alpine Linux...` | `- Host: Alpine Linux...` | step-4.md |
| `- **Software images:** Predefined...` | `- Software images: predefined...` | step-5.md |
| `- **Configuration files:** Specific...` | `- Configuration files: specific...` | step-5.md |
| `- **Custom scripts:** Automated...` | `- Custom scripts: automated...` | step-5.md |
| `- **PortChannel01:** Port-channel...` | `- PortChannel01: port-channel...` | step-6.md |
| `- **PortChannel02:** Port-channel...` | `- PortChannel02: port-channel...` | step-6.md |
| `- **PortChannel99:** Port-channel...` | `- PortChannel99: port-channel...` | step-6.md |
| `- **VLAN 100:** Used for...` | `- VLAN 100: used for...` | step-6.md |
| `- **VLAN 99:** Used for...` | `- VLAN 99: used for...` | step-6.md |

**Agent Assessment:** NOT in current Tier 1 rules. Pattern: List items should not start with bold terms followed by colon.

---

### 2.8 Remove Trailing Colons from Headings (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `**Explore More on Cisco U.:**` | `**Explore More on Cisco U.**` | step-9.md |

**Agent Assessment:** NOT in current rules. Pattern: Headings should not end with colons.

---

### 2.9 Important to Note Formatting (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `**Important:** When configuring VLANs...` | `> Note: When configuring VLANs...` | step-6.md |

**Agent Assessment:** NOT in current rules. Pattern: Important callouts should use blockquote Note format.

---

### 2.10 Title Case in Titles (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `Dual-Homing with SONiC using LAG and MCLAG` | `Dual-Homing with SONiC Using LAG and MCLAG` | sidecar.json |

**Agent Assessment:** NOT in current rules. Pattern: Title case requires capitalizing significant words.

---

### 2.11 Video Series to Videos (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `Video Series` | `Videos` | step-9.md |

**Agent Assessment:** Likely a Cisco U. platform-specific terminology update. NOT detectable without terminology dictionary.

---

### 2.12 Article Corrections (Partial in Tier 1)

| Before | After | Context |
|--------|-------|---------|
| `with editor` | `with an editor` | step-3.md |
| `port-channel uses` | `the port-channel uses` | step-4.md |
| `port-channel on the switch` | `the port-channel on the switch` | step-4.md |
| `Lab environment is` | `The lab environment is` | step-4.md |
| `log in to device` | `log in to the device` | step-5.md |
| `initial behavior of device` | `initial behavior of the device` | step-5.md |
| `How was the SONiC image built` | `how the SONiC image was built` | step-5.md |

**Agent Assessment:** Partial - basic a/an rules exist, but definite article ("the") insertion is complex and context-dependent.

---

### 2.13 Bold Formatting Changes for Credentials (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `username **admin** with password **YourPaSsWoRd**` | `username _admin_ with password _YourPaSsWoRd_` | step-5.md |
| `a \"non-ZTP\" image` | `a _non-ZTP_ image` | step-5.md |
| `**-i 1** represents` | `_-i 1_ represents` | step-8.md |

**Agent Assessment:** NOT in current rules. Pattern: Use italics for placeholder values and inline terms, not bold.

---

### 2.14 Typo Fixes

| Before | After | File |
|--------|-------|------|
| `FRRuting (FRR)` | `FRRouting (FRR)` | step-3.md |
| `upstram-1 device` | `upstream-1 device` | step-8.md |

**Agent Assessment:** Typos require spell-check capability, which is partially available.

---

### 2.15 Em-dash Usage (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `at the moment of interface failure, for example` | `at the moment of the interface failure--for example` | step-8.md |

**Agent Assessment:** NOT in current rules. Em-dash usage for parenthetical expressions.

---

### 2.16 "On Linux Alpine" Word Order (NEW - NOT IN TIER 1)

| Before | After | File |
|--------|-------|------|
| `On Linux Alpine` | `On the Alpine Linux host` | step-4.md |

**Agent Assessment:** NOT in current rules. This is a product name word order fix.

---

## 3. NEW Rules Found Not in Tier 1

Based on this PR analysis, the following rules should be added:

### High Priority (Multiple Occurrences)

1. **Bold list items to plain** - Remove bold formatting from list item terms (`- **Term:** Description` to `- Term: description`)

2. **File paths and commands in code** - Use backtick code formatting for file paths and CLI commands, not bold

3. **Cisco IOS branding** - "Cisco IOS-based" should be "Cisco IOS software-based"

4. **Important to Note** - `**Important:**` callouts should become `> Note:` blockquotes

5. **Italics for placeholders** - Use italics (`_placeholder_`) not bold for credential placeholders and inline terms

6. **Acronym expansion** - Expand acronyms on first use (requires acronym database)

### Medium Priority (Few Occurrences)

7. **Title case in titles** - Capitalize significant words in tutorial titles

8. **No trailing colons in headings** - Remove `:` from end of bold headings

9. **Word order corrections** - "Linux Alpine" to "Alpine Linux"

10. **Em-dash for parentheticals** - Use em-dash for parenthetical expressions

---

## 4. Coverage Assessment

### Current Tier 1 Rules Coverage

| Rule | Would Catch | Notes |
|------|-------------|-------|
| Contractions (`it's` -> `it is`) | **YES** | 2 occurrences found |
| Compound words (Multi-Chassis) | **YES** | 1 pattern type found |
| Feature names lowercase | **PARTIAL** | Context-dependent |
| Protocol names caps | **NO** | None found in this PR |
| H3 to bold | **NO** | None found in this PR |
| "by using" construction | **NO** | None found in this PR |
| "vs." usage | **NO** | None found in this PR |

### Estimated Coverage

Based on the 80+ editorial changes in this PR:

| Category | Count | Agent Would Catch | Percentage |
|----------|-------|-------------------|------------|
| Contractions | 2 | 2 | 100% |
| Compound words | 3 | 3 | 100% |
| Feature lowercase | 2 | 1 | 50% |
| Bold to code | 8 | 0 | 0% |
| List bold removal | 12 | 0 | 0% |
| Article corrections | 25+ | 5 | ~20% |
| Cisco branding | 3 | 0 | 0% |
| Acronym expansion | 3 | 0 | 0% |
| Important to Note | 1 | 0 | 0% |
| Other formatting | 20+ | 2 | ~10% |

### Overall Coverage Estimate

**Current Tier 1 Rules: ~15% of editorial changes would be caught**

### Coverage with Proposed New Rules

If the NEW rules identified above were added to Tier 1:

| Additional Rules | Estimated Catch |
|-----------------|-----------------|
| Bold list to plain | +12 |
| File paths/commands in code | +8 |
| Cisco IOS branding | +3 |
| Important to Note | +1 |
| Italics for placeholders | +3 |

**Estimated Coverage with New Rules: ~45-50% of editorial changes would be caught**

---

## 5. Recommendations

### Immediate Additions to Tier 1

1. **Rule: Bold list items** - Detect `- **Term:**` pattern and suggest removing bold
2. **Rule: File paths in code** - Detect file paths in bold and suggest code formatting
3. **Rule: CLI commands in code** - Detect commands starting with common prefixes (sudo, show, config) in bold
4. **Rule: Important callouts** - Detect `**Important:**` and suggest `> Note:` format
5. **Rule: Cisco IOS branding** - Detect "Cisco IOS-based" and correct to "Cisco IOS software-based"

### Future Tier 2 Additions

1. Acronym first-use expansion (requires dictionary)
2. Title case validation
3. Comprehensive article correction (a/an/the)
4. Em-dash formatting
5. Product name word order

---

## 6. Editor Comments Analysis

The editor included valuable QUERY comments in commit messages asking about:

1. Expanding acronyms (VTY, FRR, oC)
2. Formatting Notes vs inline text
3. Rewording unclear sentences
4. Consistency of "persistent" vs "permanent"
5. "Finishing Up" section in final steps

These queries indicate areas where the agent could flag for human review rather than auto-fix.

---

## Appendix: All Editor Commits Analyzed

| SHA | File | Changes |
|-----|------|---------|
| 93f0f58 | step-9.md | Removed trailing colon from heading, Video Series to Videos |
| 33edd6e | sidecar.json | Acronym expansion, title case, Multi-Chassis hyphenation |
| 9afca42 | step-1.md | Multi-Chassis, Cisco IOS branding |
| 7c56110 | step-2.md | Need for MCLAG heading, lowercase traffic types |
| fbccd76 | step-3.md | Bold to code formatting (8 instances), FRRouting typo |
| 234071d | step-4.md | Cisco IOS branding, Alpine Linux word order, bold to code |
| 19eab46 | step-5.md | SSH expansion, bold to italics, articles |
| e504a7e | step-6.md | List bold removal, Important to Note, articles |
| 1a6309c | step-7.md | Articles, formatting consistency |
| 6615462 | step-8.md | Articles, em-dash, typo fix |
| f6b2f64 | step-9.md | Trailing space fix |
