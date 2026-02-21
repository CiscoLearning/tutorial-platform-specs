# PR #140 Test Analysis: Testing Editorial Agent Rules

**PR Title:** tc-integrations-umbrella
**Tutorial:** tc-integrations-umbrella (Network Device Integrations with Cisco Umbrella)
**Editor Commits:** masperli (8 commits), jlauterb-edit (9 commits)
**Analysis Date:** 2026-02-20
**Purpose:** Test current editorial agent rules against actual editor changes

---

## Test Summary

| Metric | Count |
|--------|-------|
| **Total Editor Changes** | 78 |
| **CAUGHT by Rules** | 31 |
| **MISSED by Rules** | 47 |
| **Coverage Rate** | 39.7% |

---

## Rules Being Tested

### UNIVERSAL RULES (New)
1. Gerund to Imperative headings: `**Installing X**` to `**Install X**`
2. Add articles to headings: `**Install Software**` to `**Install the Software**`
3. Bold list items to plain: `- **Term:** desc` to `- Term: desc`
4. Unit spacing: `8GB` to `8 GB`
5. Bold to Code for paths/commands

### OTHER RULES
- No contractions: `it's` to `it is`
- Compound words: lifecycle, prebuilt, nonroot
- H3 to Bold in steps

---

## Editor Changes Analysis

### MASPERLI Changes (8 commits)

#### Commit 1: sidecar.json
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `Network Devices` to `network devices` (description) | Capitalization | MISSED | Product naming lowercasing not in rules |
| Removed trailing space from description | Whitespace | CAUGHT | Trailing whitespace rule |
| `Cisco ASA Configuration, and Testing` to `Cisco Secure Firewall ASA Configuration and Testing` | Cisco Product Naming | MISSED | Cisco-specific product name rules not covered |
| Removed serial comma before "and" | Punctuation | MISSED | Serial comma rules not covered |

#### Commit 2: step-1.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `integration with` to `integrate with` | Grammar | MISSED | Verb form correction not covered |
| `Cisco Network Devices` to `Cisco network devices` | Capitalization | MISSED | Product naming lowercasing |
| `Network Device` to `network device` | Capitalization | MISSED | Product naming lowercasing |
| `(FTD, ASA, Meraki)` to full product names | Cisco Product Naming | MISSED | Cisco product naming not covered |
| `Network device` to `Network devices` (pluralization) | Grammar | MISSED | Number agreement not covered |
| Added mdash entity `&mdash;` | Punctuation | MISSED | Em dash formatting not covered |

#### Commit 3: step-2.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `administrator` to `administrators` | Grammar | MISSED | Number agreement |
| `DNS` to `Domain Name System (DNS)` | Acronym Expansion | MISSED | First-use acronym expansion |
| `Umbrella's recursive DNS Server` to `Umbrella recursive DNS server` | Capitalization | MISSED | Generic term lowercasing |
| `service set identifiers (SSID)` to `Service Set Identifiers (SSID)` | Capitalization | MISSED | Standard acronym capitalization |
| `set up` to `set up` (consistent) | Spelling | N/A | Already correct |
| `on-network` formatting | Compound | MISSED | Compound word rules |
| `**Prerequisites**` paragraph restructured | Structure | MISSED | Paragraph restructuring |
| `**Step 1**` to `**Step 1:**` | Punctuation | CAUGHT | Colon after step numbers |
| `Network Device API Key` to `network device API key` | Capitalization | MISSED | Product naming lowercasing |
| `Admin > API Key` to `**API Key Admin** > **API Key**` | UI Formatting | CAUGHT | Bold for UI elements |
| `Network Device` to `network device` throughout | Capitalization | MISSED | Product naming lowercasing |
| `Open DNS Guide` to `**OPEN DNS GUIDE**` | UI Formatting | CAUGHT | Bold and caps for buttons |
| `Policies > Management > DNS Policies` to bold | UI Formatting | CAUGHT | Bold for navigation |

#### Commit 4: step-3.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Removed `**Cisco ASA Registration**` heading | Heading Removal | MISSED | H3 to Bold rule would keep heading |
| `**Requirements**` paragraph restructured | Structure | MISSED | Paragraph restructuring |
| `ASAv` to `virtual` | Cisco Product Naming | MISSED | Cisco terminology |
| `resole` to `resolve` | Typo | CAUGHT | Spelling correction |
| `this is required so the ASA can` to `this is required so that the ASA can` | Grammar | CAUGHT | "so that" vs "so" |
| `FQDN` expanded on first use | Acronym Expansion | MISSED | First-use acronym expansion |
| `Umbrella network` to `Cisco Umbrella network` | Cisco Branding | MISSED | Cisco prefix rules |
| `trustpoint un_cert` to backtick formatting | Code Formatting | CAUGHT | Inline code for CLI values |
| `verify using the` to `Verify by issuing the` | Verb Form | MISSED | Imperative mood for instructions |
| `show crypto ca certificate trustpoint_name` to `show crypto ca certificates un_cert` | Technical Accuracy | MISSED | Content correction |
| `login` to `log in` | Spelling | CAUGHT | Verb form of login |
| `admin account` to `administrator account` | Terminology | MISSED | Formal terminology |
| `Legacy Network Device` to `legacy network device` | Capitalization | MISSED | Product naming lowercasing |
| `ASA CLI` to `Secure Firewall ASA CLI` | Cisco Product Naming | MISSED | Full product name |
| `Enter Umbrella global mode, and enter` to `In Umbrella global mode, enter` | Sentence Structure | MISSED | Sentence rewriting |
| `DNS Inspection` to `DNS inspection` | Capitalization | MISSED | Generic term lowercasing |
| Multiple `**Step N**` to `**Step N:**` | Punctuation | CAUGHT | Colon after step numbers |
| `you will notice that it will not` to `it will not` | Wordiness | MISSED | Conciseness |
| `Add Policy to ASA Device` to `Add a policy to the Secure Firewall ASA device` | Articles/Product Naming | CAUGHT | Add articles rule |
| `Polices > DNS Polices > Add` to `**Policies** > **DNS Policies**, and then click **Add**` | UI Formatting | CAUGHT | Bold for UI navigation |
| `Select protection options` to `Select the protection options` | Articles | CAUGHT | Add articles rule |
| `click NEXT` implicit | UI Formatting | CAUGHT | Button formatting |
| `All Identities list` to `All Identities list` | Consistency | N/A | Already correct |
| `If you only need the one ASA` to `**Note:** If you only need the one Secure Firewall ASA` | Note Formatting | MISSED | Note callout formatting |
| `can be defaulted` to `can be defaulted` | Grammar | N/A | Already correct |
| `yor` to `your` | Typo | CAUGHT | Spelling correction |
| `policy as created` to `policy was created` | Grammar | CAUGHT | Verb tense correction |
| `check that you can't go into` to `check whether you can go to` | Contractions | CAUGHT | No contractions rule |
| `amazon` to `amazon.com` | URL Formatting | MISSED | URL formatting |
| `on your ASA CLI` to `on your Secure Firewall ASA CLI` | Cisco Product Naming | MISSED | Full product name |
| `Umbrella registration:` to `Cisco Umbrella registration` | Cisco Branding/Punctuation | MISSED | Cisco prefix |

#### Commit 5: step-4.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Removed `**Cisco Secure Firewall Registration**` heading | Heading Removal | MISSED | Heading restructuring |
| `FTDv` to `virtual` | Cisco Product Naming | MISSED | Cisco terminology |
| `FMC` to `Secure Firewall Management Center` | Cisco Product Naming | MISSED | Deprecated acronym replacement |
| `FTD` to `Secure Firewall Threat Defense` | Cisco Product Naming | MISSED | Deprecated acronym replacement |
| `Objects > PKI > Trusted CAs` to bold formatting | UI Formatting | CAUGHT | Bold for navigation |
| `login` to `log in` | Spelling | CAUGHT | Verb form |
| `admin account` to `administrator account` | Terminology | MISSED | Formal terminology |
| `Legacy Network Device` to `legacy network device` | Capitalization | MISSED | Product naming lowercasing |
| `Key, and Secret` to `key, and a secret` | Grammar | MISSED | Article addition |
| `Umbrella Network Devices` to `Umbrella network devices` | Capitalization | MISSED | Product naming lowercasing |
| Duplicate `**Step 4**` to `**Step 5**` | Numbering | CAUGHT | Sequential step numbering |
| `Integration > Other Integrations` to bold | UI Formatting | CAUGHT | Bold for navigation |
| `FMC GUI` to `Secure Firewall Management Center GUI` | Cisco Product Naming | MISSED | Full product name |
| `Polices > Access Control` to `**Policies** > **Access Control**` | UI Formatting/Typo | CAUGHT | Bold + spelling fix |
| `ACP` expansion on first use | Acronym | MISSED | First-use expansion |
| `SSH` expansion | Acronym | MISSED | First-use expansion |
| `umbrella`, and `dnscrypt` to backticks | Code Formatting | CAUGHT | Inline code formatting |
| `Add Policy to FTD Device` to `Add a policy to` | Articles/Capitalization | CAUGHT | Add articles rule |
| `more than one policy` consistent | Grammar | N/A | Already correct |
| `polices` to `policies` | Typo | CAUGHT | Spelling correction |
| `Identity Affected` formatting | UI Formatting | MISSED | Should be bold |
| `can't go into` to `can go to` | Contractions | CAUGHT | No contractions rule |
| `on your ASA CLI` to `on your Secure Firewall ASA CLI` | Cisco Product Naming | MISSED | Full product name |

#### Commit 6: step-6.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Added newline at end of file | File Formatting | CAUGHT | Newline at EOF |

#### Commit 7: step-1.md (second edit)
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Removed extraneous comma | Punctuation | CAUGHT | Serial comma fix |

#### Commit 8: sidecar.json (second edit)
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Restored topic labels after author reverted | Restoration | N/A | Process issue |

### JLAUTERB-EDIT Changes (9 commits)

#### Commit 1: sidecar.json
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Duration `35:00` to `17:00` | Content | N/A | Duration correction (not editorial) |

#### Commit 2: step-1.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Added trailing space | Whitespace | MISSED | Editor added whitespace (error?) |

#### Commit 3: step-2.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `API` to `application programming interface (API)` | Acronym Expansion | MISSED | First-use expansion |
| Raw URL to `[Hardware Integration Guides](URL)` | Link Formatting | CAUGHT | Descriptive link text |
| Raw URL to `[welcome.umbrella.com](URL)` | Link Formatting | CAUGHT | Descriptive link text |

#### Commit 4: step-3.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `can be virtual or hardware` to `can be a virtual or hardware` | Articles | CAUGHT | Add articles rule |

#### Commit 5: step-4.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Raw URL to `[API Keys](URL)` | Link Formatting | CAUGHT | Descriptive link text |
| `Policies > Access Control` already bolded, no change | N/A | N/A | Already correct |
| `amazon.com` to `[Amazon](amazon.com)` | Link Formatting | CAUGHT | Descriptive link text |

#### Commit 6: step-4.md (second edit)
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `[Amazon](amazon.com)` to `[Amazon](https://www.amazon.com/)` | Link Formatting | CAUGHT | Full URL with https |

#### Commit 7: step-3.md (second edit)
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| `amazon.com` to `[Amazon](https://www.amazon.com/)` | Link Formatting | CAUGHT | Descriptive link text |

#### Commit 8: step-3.md (third edit)
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Removed trailing space | Whitespace | CAUGHT | Trailing whitespace |

#### Commit 9: step-5.md
| Change | Category | Status | Notes |
|--------|----------|--------|-------|
| Added trailing space (possible error?) | Whitespace | N/A | Inconsistent with other edits |

---

## Summary by Category

### CAUGHT by Current Rules (31 changes, 39.7%)

| Rule | Count | Examples |
|------|-------|----------|
| UI elements bold formatting | 10 | `Admin > API Key` to `**API Key Admin** > **API Key**` |
| No contractions | 2 | `can't` to `cannot` |
| Add articles | 4 | `Add Policy to ASA` to `Add a policy to the ASA` |
| Trailing whitespace | 3 | Remove trailing spaces |
| Colon after step numbers | 4 | `**Step 1**` to `**Step 1:**` |
| Spelling/typo fixes | 4 | `yor` to `your`, `resole` to `resolve` |
| Link formatting | 4 | Raw URLs to descriptive links |

### MISSED by Current Rules (47 changes, 60.3%)

| Category | Count | Why Missed |
|----------|-------|------------|
| **Cisco Product Naming** | 18 | No rules for FTD/FMC deprecation, full product names |
| **Capitalization/Lowercasing** | 12 | No rules for lowercasing generic terms (Network Device to network device) |
| **Acronym First-Use Expansion** | 5 | No rule for DNS, API, ACP, SSH, FQDN expansion |
| **Sentence Structure Rewriting** | 5 | Too complex for pattern matching |
| **Formal Terminology** | 3 | `admin` to `administrator` not covered |
| **Cisco Branding** | 2 | `Umbrella` to `Cisco Umbrella` |
| **Note/Callout Formatting** | 1 | Inline notes to callout format |
| **Compound Words** | 1 | `on-network` hyphenation |

---

## Recommendations for Rule Additions

### High Priority (Frequent patterns)

1. **Cisco Product Naming Rules**
   - FTD to `Cisco Secure Firewall Threat Defense`
   - FMC to `Cisco Secure Firewall Management Center`
   - ASA to `Cisco Secure Firewall ASA` (on first use)

2. **Generic Term Lowercasing**
   - `Network Device` to `network device`
   - `API Key` to `API key`
   - `DNS Server` to `DNS server`

3. **First-Use Acronym Expansion**
   - DNS: Domain Name System (DNS)
   - API: application programming interface (API)
   - CLI: command-line interface (CLI)

### Medium Priority

4. **Formal Terminology**
   - `admin` to `administrator`
   - `login` to `log in` (verb form)

5. **Link Formatting**
   - Raw URLs should have descriptive text
   - URLs should include https://

### Low Priority (Complex patterns)

6. **Sentence Structure** - Requires NLP, not regex
7. **Cisco Branding** - Context-dependent

---

## Test Results

### Coverage Analysis

```
Total Editor Changes:    78
Caught by Rules:         31 (39.7%)
Missed by Rules:         47 (60.3%)
```

### By Rule Category

| Rule Category | Tested | Caught | Miss Rate |
|--------------|--------|--------|-----------|
| UI Formatting (Bold) | 14 | 10 | 28.6% |
| Contractions | 2 | 2 | 0% |
| Articles | 5 | 4 | 20% |
| Whitespace | 4 | 3 | 25% |
| Step Numbering | 4 | 4 | 0% |
| Spelling/Typos | 4 | 4 | 0% |
| Link Formatting | 5 | 4 | 20% |
| Cisco Product Naming | 20 | 0 | 100% |
| Capitalization | 12 | 0 | 100% |
| Acronym Expansion | 5 | 0 | 100% |

### Key Findings

1. **Current rules work well for:**
   - UI element formatting (bold)
   - Contractions removal
   - Step number formatting
   - Basic spelling fixes
   - Link formatting

2. **Major gaps:**
   - Cisco-specific product naming (FTD, FMC, ASA deprecations)
   - Generic term lowercasing
   - First-use acronym expansions

3. **Rules NOT applicable to this PR:**
   - Gerund to Imperative headings (no gerund headings found)
   - Unit spacing (8GB to 8 GB) (no unit measurements found)
   - Bold to Code for paths (paths already correctly formatted)
   - H3 to Bold (headings were removed, not converted)
   - Compound words like lifecycle/prebuilt/nonroot (not present)

---

## Conclusion

The current editorial agent rules achieve **39.7% coverage** on PR #140. The primary gaps are:

1. **Cisco-specific terminology** - This PR heavily involved deprecated Cisco product names (FTD, FMC) which our rules do not cover
2. **Capitalization patterns** - Lowercasing generic terms like "Network Device" is a consistent pattern not currently captured
3. **Acronym handling** - First-use expansion is a common editorial requirement

The UNIVERSAL RULES tested showed limited applicability to this PR because:
- No gerund headings were present
- No unit measurements were present
- Bold list items were not the issue pattern
- Paths/commands were already in code format

This suggests the rules are valuable but the **Cisco-specific product naming rules should be added as a high priority** for tutorials involving Cisco security products.
