# Editor Comments Reference

This document compiles editorial rules and patterns extracted from PR comments and commits by the human editors (masperli/Matt Sperling and jlauterb-edit/Jill).

**Data Sources:**
- GitHub PR comments (issues endpoint)
- Commit messages with detailed edit notes
- Git diffs showing actual changes

---

## Editor Profiles

### jlauterb-edit (Jill)

**Comment Style:**
- Comprehensive step-by-step review format
- Global edits → Global queries → Step-by-step changes
- Notable edits called out with line numbers
- QUERYs section for author decisions
- Before/after examples in commit messages

**Active Period:** 2025-07 through present

### masperli (Matt)

**Comment Style:**
- Detailed summary at end of tutorial edit
- Comments often reference long-standing Cisco style rules
- Cites specific dates ("since at least 2008")
- References Cisco Branding guidelines
- Includes trademark and legal considerations

**Active Period:** 2024-03 through present

---

## Rules by Category

### 1. Product Naming and Branding

#### Rule: Full Product Names on First Use

**Priority:** High | **Source:** Matt (PR #140, PR #116)

Products must use full official names on first use, then can abbreviate.

| Product | First Use | Subsequent |
|---------|-----------|------------|
| ASA | Cisco Secure Firewall Adaptive Security Appliance (ASA) | Secure Firewall ASA, ASA |
| FTD | Cisco Secure Firewall Threat Defense | Secure Firewall Threat Defense |
| ISE | Cisco Identity Services Engine (ISE) | ISE |
| NSO | Cisco Network Services Orchestrator (NSO) | NSO |
| ACI | Cisco Application Centric Infrastructure (Cisco ACI) | Cisco ACI |
| NX-OS | Cisco Nexus Operating System (Cisco NX-OS) | Cisco NX-OS |

**Note:** "FTD" and "FMC" are now **deprecated acronyms** (as of 2025). Use full names.

#### Rule: Cisco Possessive Form

**Priority:** High | **Source:** Matt (PR #116)

> "Cisco corporate style is to avoid using the name Cisco and its associated products in the form of a possessive."

| Incorrect | Correct |
|-----------|---------|
| Cisco Hypershield's technology | the Cisco Hypershield technology |
| Cisco's ISE | Cisco ISE |

#### Rule: Trademark Considerations

**Priority:** High | **Source:** Matt (PR #140)

| Product | Trademark Status | Usage |
|---------|-----------------|-------|
| Cisco Umbrella | Registered trademark | Must keep "Cisco" in most references |
| Cisco Meraki / Meraki | Both registered | Can use either form |
| Cisco AI Assistant | Correct form | Use "AI Assistant models" not "AI Assistants" |

**Product Pluralization:**
> "When referring to two or more units or models, use a descriptor noun after the name in plural form ('AI Assistant models,' 'AI Assistant types'), but leave 'Assistant' in singular form."

#### Rule: Cisco Before Product Names

**Priority:** Medium | **Source:** Jill (multiple PRs)

Add "Cisco" before product names on first reference in keeping with brand guidelines.

**Examples from commits:**
- "Added 'Cisco' before 'Nexus Dashboard' in tag in keeping with brand guidelines"
- "Added 'Cisco' to title: 'Introduction to TACACS+ on Cisco ISE'"
- "Changed {tag: 'ISE'} to {tag: 'Cisco ISE'}"

---

### 2. Acronym Handling

#### Rule: Expand on First Use

**Priority:** High | **Sources:** Both editors (multiple PRs)

**Standard Pattern:**
- First use: Full term (ACRONYM)
- Subsequent: ACRONYM only

**Examples from edits:**
| Before | After |
|--------|-------|
| ACI and NXOS | Cisco Application Centric Infrastructure (Cisco ACI) and Cisco Nexus Operating System (Cisco NX-OS) |
| SSH | Secure Shell (SSH) |
| VRF | virtual routing and forwarding (VRF) |
| AV pairs | attribute-value pair (AV pair) |
| ECMP paths | Equal Cost Multi-Paths (ECMPs) |

#### Rule: Certification Acronyms

**Priority:** Medium | **Source:** Matt (PR #73)

> "Do not use acronyms in which the 'C' stands for 'Cisco,' unless referring to Cisco certifications (CCIE, CCNA, and so on)."

| Incorrect | Correct |
|-----------|---------|
| CCO | Cisco Connection Online |
| CCIE | CCIE (OK as certification) |

**Query from Jill (PR #160):**
> "Should I expand the first instance of CCIE (Cisco Certified Internetwork Expert)? Or are certifications not expanded?"

**Answer:** Certifications typically do NOT need expansion.

#### Rule: Well-Established Acronyms

**Priority:** Low | **Source:** Matt (PR #75)

These don't need expansion:
- API, URL, HTTP, HTTPS, HTML, CSS, JSON, XML, SQL, CLI, GUI, OS
- SNMP, DNS (expand on first use per standard style)
- VLAN (typically not expanded per Jill's query confirmation)

#### Rule: Title Acronym Rule

**Priority:** High | **Source:** Matt (PR #116)

> "The long-standing Cisco rule (since at least 2008) is that the titles of all Cisco learning content should include either an acronym or its expanded term, but NOT both."

| Incorrect | Correct Options |
|-----------|-----------------|
| Introduction to Extended Berkeley Packet Filter (eBPF) | "Introduction to eBPF" OR "Introduction to Extended Berkeley Packet Filter" |

---

### 3. Terminology and Clarity

#### Rule: Cisco ISE Server (not Box)

**Priority:** Medium | **Source:** Jill (PR #166)

| Incorrect | Correct |
|-----------|---------|
| Cisco ISE box | Cisco ISE server |

#### Rule: Client-Server Hyphenation

**Priority:** Low | **Source:** Jill (diff)

| Incorrect | Correct |
|-----------|---------|
| client/server model | client-server model |

#### Rule: Word Choice Improvements

**Priority:** Medium | **Sources:** Both editors

| Avoid | Prefer | Reason |
|-------|--------|--------|
| meaningless | infeasible | More precise |
| a lot of boilerplate | repetitive boilerplate | More specific |
| is NOT going to format | does not format | Cleaner prose |
| resole | resolve | Typo fix |

#### Rule: Proper Capitalization

**Priority:** Medium | **Source:** Jill (diffs)

| Incorrect | Correct |
|-----------|---------|
| Radius | RADIUS |
| ssh | SSH |
| nano services | nano services (lowercase confirmed) |

---

### 4. GUI Elements and Formatting

#### Rule: Bold for GUI Elements with Direct Instructions

**Priority:** High | **Source:** Matt (PR #73)

> "The longstanding rule on Cisco learning content, dating back to at least 2008, is to boldface the name of a GUI element if it is associated with a direct instruction -- a direct command in the imperative voice to do something."

**Use bold:**
- "Navigate to **Users** > **Rules**."
- "Expand the **Configure** menu."
- "Click the **Save** button."

**Don't use bold:**
- "From the Operate tab, click the **Save** button." (Operate not bolded - not a direct instruction to navigate there)
- "Copy and save the information in the Device ID field" (information not bolded - not specific)

#### Rule: Italics for Emphasis (Not Bold)

**Priority:** High | **Source:** Jill (PR #221)

> "Cisco style is to use italics (sparingly) instead of boldfacing for emphasis. Boldfacing is for GUI elements."

**Exception:** "Bolding bulleted terms. It improves readability and aligns with our Congratulations step format."

#### Rule: "Click" Not "Click On"

**Priority:** Medium | **Source:** Matt (PR #73)

| Incorrect | Correct |
|-----------|---------|
| Click on the **Save** button | Click the **Save** button |

#### Rule: Code Style for Commands

**Priority:** Medium | **Source:** Jill (PR #166)

Use backticks (code style) for:
- Commands: `server name`, `ip tacacs source-interface`, `aaa`
- File names: `l3vpn-template.xml`
- Directories: `templates` directory
- Configuration values: `service = shell`

**From commit:**
> "Corrected commands in bold by styling as code: server name, ip tacacs source-interface, aaa, test aaa, etc."

---

### 5. Content Structure

#### Rule: Procedural Introduction Lines

**Priority:** High | **Source:** Jill (multiple PRs)

Before numbered steps, add an introduction line.

**Before:**
```markdown
## Configure the Service

1. Click **Settings**.
2. Enter the value.
```

**After:**
```markdown
## Configure the Service

To configure the service:

1. Click **Settings**.
2. Enter the value.
```

**Examples from commits:**
- "Added 'To configure the service:' to introduce the bullet list."
- "Added 'Additional features include:' to introduce bullets"
- "Added 'Traffic Analytics offers several key advantages:' to introduce the bullet list"

#### Rule: Cross-Reference Cleanup

**Priority:** Medium | **Source:** Jill (PR #221)

> "I removed '(See the next step for more details.)' at the end of Learning Paths because Bookmarking is covered in step-5 (next step) and Learning Paths are covered in step-6."

Remove vague forward references when:
- The referenced content is several steps away
- The reference doesn't add immediate value

#### Rule: Parallel Structure in Lists

**Priority:** Medium | **Source:** Jill (PR #221)

Lists should follow consistent grammatical structure.

**Example from PR #221:**
- "Added 'How to ...' to the two bullets under 'What You'll Learn'"

#### Rule: Duration Verification

**Priority:** High | **Source:** Jill (PR #153)

> "Corrected the duration time to match steps' total time stamps."

Step durations in sidecar.json must sum to the total duration.

---

### 6. Punctuation

#### Rule: Em Dash Without Spaces

**Priority:** Medium | **Source:** Jill (PR #154)

> "Removed spaces around em dashes throughout tutorial."

| Incorrect | Correct |
|-----------|---------|
| problems — they assume | problems—they assume |

#### Rule: Excessive Exclamation Points

**Priority:** Medium | **Source:** Jill (multiple PRs)

> "Removed extraneous exclamation points in content."

Limit use of "!" - remove excessive instances.

---

### 7. URL and Link Handling

#### Rule: URL Title Matching

**Priority:** Medium | **Source:** Jill (PR #221)

Match link text to actual page titles.

| Incorrect | Correct |
|-----------|---------|
| Video Series: | Videos: (matches URL page title) |
| Events and Webinars: | Events: (matches URL page title) |

#### Rule: URL Verification

**Priority:** High | **Source:** Matt (PR #147)

> "The URL link to the Secure Firewall Management Center Software Download page did not work, so I changed it to this link..."

Always verify that URLs:
1. Are not broken (404)
2. Lead to appropriate content
3. Are the most direct link (not a link that redirects)

---

### 8. Image Guidelines

#### Rule: Image Accessibility

**Priority:** Medium | **Source:** Matt (PR #146)

> "The figure appears to have a transparent background. In GitHub, I can only see the text by right-clicking the Open Image in New Tab option."

Check that images:
- Don't have transparent backgrounds that make content invisible
- Are high resolution (not blurry)
- Have appropriate sizing

#### Rule: Figure Text Standards

**Priority:** Medium | **Source:** Matt (PR #147)

Text within figures (diagrams, tables) should follow same style rules as body text:
- Proper capitalization
- Acronym expansion where space permits
- Correct product names

---

### 9. Rebranding Awareness

#### Rule: Keep Product Names Current

**Priority:** High | **Source:** Matt (PR #146)

> "Microsoft has rebranded Azure AD as Microsoft Entra ID... Consequently, I have renamed it accordingly in all occurrences."

Stay aware of product rebranding:
- Azure AD → Microsoft Entra ID
- FTD/FMC → Cisco Secure Firewall Threat Defense / Management Center

---

## Query Patterns (Require Human Decision)

Editors often flag items as QUERYs requiring author input:

1. **Acronym Expansion Ambiguity**
   - "Should we expand L3VPN as Layer 3 VPN?"
   - "Is 'network-attached storage' correct for NAS, or 'network access server'?"

2. **Content Structure Decisions**
   - "Should we create a new step for this content?"
   - "Should steps 4 and 7 be similarly structured?"

3. **Image Issues**
   - "Can we replace with hi-res versions?"
   - "Should we add annotations?"

4. **Missing Content**
   - "Is the step 5 topic missing?"
   - "There is no subsequent content that mentions troubleshooting"

---

## Appendix: Sample Commit Messages

### Jill's Format
```
Update step-3.md

step-3.md

Notable edits:
1. Changed "Cisco ISE box" to "Cisco ISE server"
2. Added "attribute-value pair (AV pair)" expansion

QUERIES:
1. Should we style "START" as code?
2. Should we expand L3VPN?
```

### Matt's Format
```
Update step-6.md

tc-integrations-umbrella step 6 edited.

Hi @jabelk, @kyle-winters, and @qsnyder -- Dakotah and I have finished editing Rafael's tutorial...

Overall comments:
--For the network devices, use the full product names per Cisco style...
--"Cisco Umbrella" is a registered trademark, so "Cisco" technically should not be dropped...

Please let me know if you have any questions.
Thanks! --Matt
```

---

## Data Files

The following JSON files contain the raw extracted data:

- `reference-data/jlauterb-commits.json` - Jill's commits with messages
- `reference-data/masperli-commits.json` - Matt's commits with messages
- `reference-data/pr-comments.json` - PR issue comments from both editors
- `reference-data/sample-diffs.json` - Actual before/after diffs

---

*Generated from PR history analysis of CiscoLearning/ciscou-tutorial-content repository*
*Last updated: 2026-02-20*
