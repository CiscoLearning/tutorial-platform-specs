# PR #195 Analysis: BGP Troubleshooting in a SONiC Lab

**Tutorial:** tc-sonic-bgp
**PR Title:** init - ready for review
**Editor:** Matt (masperli)
**Total Commits:** 16
**Date Analyzed:** 2026-02-20

---

## Summary of Changes by Category

| Category | Count | Description |
|----------|-------|-------------|
| Acronym Expansion | 25+ | First-use expansion of technical acronyms |
| Title/Heading Fixes | 8 | Title case enforcement, removing colons |
| Structural Clarity | 15+ | Paragraph restructuring, sentence flow |
| Formatting Consistency | 20+ | Bold vs italic vs code style standardization |
| Grammar/Style | 30+ | "by using" vs "using", serial comma, hyphenation |
| Em Dash Usage | 10+ | Proper &mdash; with spacing context |
| Sentence Clarity | 15+ | Rewording for precision |
| Metadata Fixes | 5 | sidecar.json corrections |

---

## Specific Rules with Before/After Examples

### 1. Acronym Expansion on First Use (EXISTING RULE - Well Applied)

Multiple acronyms expanded on first appearance:

| Before | After |
|--------|-------|
| routing protocol like BGP works on SONiC (**S**oftware for **O**pen **N**etworking **i**n the **C**loud) switches | a routing protocol like Border Gateway Protocol (BGP) works on Software for Open Networking in the Cloud (SONiC) switches |
| KVM/hardware virtualization | Kernel-based Virtual Machine (KVM) hardware virtualization |
| OSPF, IS-IS, LDP | Open Shortest Path First (OSPF), Intermediate System-to-Intermediate System (IS-IS), Label Distribution Protocol (LDP) |
| QEMU | Quick Emulator (QEMU) |
| SSH | Secure Shell (SSH) |
| RHEL | Red Hat Enterprise Linux (RHEL) |
| AWS | Amazon Web Services (AWS) |
| ZTP | Zero-Touch Provisioning (ZTP) |

**NEW Pattern:** Matt removes inline bold/italic expansion syntax (like `**S**oftware for **O**pen...`) and uses standard parenthetical expansion format.

### 2. iBGP/eBGP Capitalization (NEW RULE)

Cisco standard: Use all-caps for BGP variants.

| Before | After |
|--------|-------|
| iBGP | IBGP |
| eBGP | EBGP |
| Internal BGP (iBGP or Interior Border Gateway Protocol) | Internal BGP (IBGP) |
| eBGP() | EBGP |

**Note:** Also applied to sidecar.json tags: `{ "tag": "iBGP" }` became `{ "tag": "IBGP" }`

### 3. "by using" vs "using" Construction (NEW RULE)

Matt consistently changes "using" to "by using" when describing a method.

| Before | After |
|--------|-------|
| configure it using the `vtysh` command | configure it by using the `vtysh` command |
| Save this configuration using the `config save` command | Save this configuration by using the `config save` command |
| start the lab using the `containerlab deploy` command | start the lab by using the `containerlab deploy` command |
| Verify the communication between switches using ping | Verify the communication between switches by using `ping` |
| make it permanent using the `sudo config save -y` command | make it permanent by using the `sudo config save -y` command |

### 4. Colon Placement After Introductory Lines (EXISTING RULE - Extended)

When a sentence introduces content (code block, list, image), it should end with a colon.

| Before | After |
|--------|-------|
| To view routing configuration, use the `show` command. | To view routing configuration, use the `show` command: |
| To make configuration persistent, use the `write` command. | To make configuration persistent, use the `write` command: |
| enter the `vtysh` command. | enter the `vtysh` command: |
| Perform the following commands to break iBGP session | Perform the following commands to break the IBGP session with sonic-2: |

### 5. Removing Redundant Section Headings (NEW PATTERN)

Matt removes redundant bold headings that duplicate content or are immediately followed by content.

| Before | After |
|--------|-------|
| **FRRouting**<br><br>To provide routing capabilities... | To provide routing capabilities... |
| **SONiC Configuration Management**<br><br>SONiC manages configuration... | SONiC manages configuration... |
| **Router-ID and BGP process on sonic-1**<br><br>Using the same process... | Using the same process... |
| **BGP Neighbors**<br><br>Configure the BGP neighbors. | Configure the BGP neighbors. |

### 6. Em Dash Usage for Parenthetical Clauses (EXISTING RULE - Heavily Applied)

Matt uses `&mdash;` for em dashes, often converting bullets, commas, or parentheses.

| Before | After |
|--------|-------|
| - **Linux systems** (Ubuntu, Debian, RHEL, Fedora, etc.) with: | - Linux systems&mdash;Ubuntu, Debian, Red Hat Enterprise Linux (RHEL), Fedora, and so on&mdash;with: |
| (AWS EC2, Digital Ocean, Google Cloud, Azure) - native KVM support | AWS EC2, DigitalOcean, Google Cloud, and Azure; native KVM support |
| for example docker-compose, Containerlab provides | for example, Docker Compose&mdash;containerlab provides |
| using virtual machines (UTM, Parallels, VMware) or containers | using virtual machines (UTM, Parallels, and VMware) or containers |
| Once you are in the vtysh shell, execute configuration commands, for example, to configure | Once you are in the vtysh shell, execute configuration commands&mdash;for example, to configure |

### 7. List Item Formatting - Periods vs No Periods (REFINEMENT)

Lists of items that are sentence fragments use no period; full sentences use periods.

| Before | After |
|--------|-------|
| - **Software images:** redefined software versions or updates necessary for switch operation. | - **Software images:** Redefined software versions or updates that are necessary for switch operation |
| - **Configuration files:** Specific settings and parameters that tailor the switch's functionality. | - **Configuration files:** Specific settings and parameters that tailor the switch's functionality |
| - **Custom scripts:** Automated scripts to execute additional configuration tasks or customizations. | - **Custom scripts:** Automated scripts to execute additional configuration tasks or customizations |

**Note:** Period removed when items are noun phrases, not sentences.

### 8. Heading Title Case and Colon Removal (EXISTING RULES)

| Before | After |
|--------|-------|
| **NOT Compatible:** | *Not* compatible: |
| **Recommended Setup for Mac Users:** | **Recommended Setup for Mac Users** |
| **Legal Disclaimers** | **Legal Disclaimer** |
| **Device access** | **Device Access** |
| **BGP lab** | **BGP Lab** |
| **Explore More on Cisco U.:** | **Explore More on Cisco U.** |
| **Show Commands Used to Troubleshoot BGP** | **Commands Used to Troubleshoot BGP** |
| **Using Debug Command** | **Debug Command** |
| **Using FRR Log** | **FRR Log** |

### 9. Product Name Capitalization (NEW PATTERNS)

| Before | After |
|--------|-------|
| Containerlab | containerlab (lowercase for product name) |
| docker-compose | Docker Compose |
| Digital Ocean | DigitalOcean |
| sonic-vm | sonic-vm (kept lowercase, product name) |
| Apple Silicon Macs | Apple silicon Macs |
| vrnetlab | vrnetlab (kept lowercase) |

### 10. Technical Term Formatting Changes (REFINEMENTS)

| Before | After |
|--------|-------|
| **vtysh** | vtysh (no bold for command) |
| *vtysh* | `vtysh` (code style for CLI tool) |
| the **config** keyword | the `config` keyword |
| **--write-to-db** | `--write-to-db` |
| **/etc/sonic/config_db.json** | /etc/sonic/config_db.json (no bold for paths) |
| **Errors or the wrong JSON format in /etc/sonic/config_db.json may cause the system to fail** | Errors or the wrong JSON format in /etc/sonic/config_db.json *may cause the system to fail* |

### 11. Numeric Values Consistency (NEW RULE)

| Before | After |
|--------|-------|
| At least 4 CPU cores and 8GB RAM | At least four CPU cores and 8 GB of RAM |

**Rule:** Spell out small numbers (under 10), add space between value and unit.

### 12. Article and Preposition Fixes (COMMON PATTERNS)

| Before | After |
|--------|-------|
| on a SONiC switches | on SONiC switches |
| the routing information will be used | The network's routing information will be used |
| the SONiC switch to have the appropriate software configuration options | the SONiC switch to have the appropriate software configuration options |
| that you intend to use | that you intend to use |
| attached to you SONiC devices | attached to your SONiC devices |

### 13. RFC Formatting (NEW RULE)

| Before | After |
|--------|-------|
| RFC-8212 | RFC 8212 |
| the [RFC-8212](url) policy requirement | the [IETF RFC 8212](url) policy requirement |

### 14. "Autonomous System" Spelling (NEW RULE)

| Before | After |
|--------|-------|
| Autonomous System (AS) | autonomous system |
| AS value | autonomous system value |

**Note:** Lowercase unless starting a sentence; "AS" abbreviation avoided in favor of full term or "autonomous system."

### 15. Router-ID vs Router ID (NEW RULE)

| Before | After |
|--------|-------|
| router-ID | router ID |
| single router-ID | single router ID |

---

## Notes from Matt's Commit Messages

Matt flagged image transparency issues in his commits:

> "In step 4, the topology figure (topo2.png) appears to have a transparent background. In GitHub, I cannot see the image unless I use the Open Image in New Tab feature to open a separate window. Please make sure that readers of this tutorial will be able to see the image on the Cisco U. platform."

This is a **visual accessibility** concern not covered by text-based validation.

---

## NEW Rules Not in Current Agent Prompt

Based on this analysis, the following patterns are NEW or need clarification:

### HIGH PRIORITY (Add to Agent)

1. **iBGP/eBGP Capitalization:** Always use IBGP and EBGP (all caps), not iBGP/eBGP
2. **"by using" Construction:** Prefer "by using the X command" over "using the X command"
3. **RFC Formatting:** Use "RFC 8212" (space, no hyphen) and prefix with "IETF" on first use
4. **Router ID:** Two words, not hyphenated (router ID, not router-ID)
5. **Autonomous System:** Lowercase unless at sentence start
6. **Remove Redundant Headings:** Bold headings that merely restate the following content should be removed

### MEDIUM PRIORITY (Refine Existing Rules)

7. **Small Numbers:** Spell out numbers under 10 (four CPU cores, not 4 CPU cores)
8. **Product Names:** Document correct casing for common tools:
   - containerlab (lowercase)
   - Docker Compose (title case)
   - DigitalOcean (one word)
   - sonic-vm (lowercase)
   - vrnetlab (lowercase)
9. **Em Dash in Lists:** When converting bullet-style explanations, em dashes can replace hyphens
10. **Code Style for CLI Options:** Use backticks for flags like `--write-to-db`

### LOW PRIORITY (Good to Have)

11. **List Period Consistency:** Noun phrases in lists omit final periods; full sentences include them
12. **Image Accessibility:** Flag images with transparency issues (requires image analysis)

---

## Agent Coverage Assessment

### Rules Our Agent Would Catch (~70%)

- Acronym expansion on first use
- Title case for headings
- Colon removal from headings
- Em dash spacing
- Serial comma usage
- Code vs bold formatting (partially)
- "In order to" -> "To"

### Rules Our Agent Would MISS (~30%)

- iBGP/eBGP -> IBGP/EBGP conversion
- "by using" construction preference
- RFC formatting (space instead of hyphen)
- Redundant heading removal
- Product name casing (containerlab, Docker Compose)
- Small number spelling
- Router ID spacing
- Autonomous system capitalization
- Context-aware list period decisions
- Removal of creative/inline acronym expansions

---

## Recommendations for Agent Improvement

1. **Add networking-specific terminology rules** - This tutorial reveals many BGP/networking conventions
2. **Create a product naming reference** - Document correct casing for 50+ common products
3. **Add "by using" transformation** - Simple regex pattern to suggest
4. **Handle RFC references** - Standardize to "IETF RFC XXXX" format
5. **Flag redundant headings** - Detect when heading text matches first sentence of section

---

## Raw Statistics

- **Total lines changed:** ~500+
- **Acronym expansions:** 25+
- **"by using" fixes:** 15+
- **Heading fixes:** 8
- **Em dash insertions:** 10+
- **Code style corrections:** 20+
- **Sentence restructures:** 30+
