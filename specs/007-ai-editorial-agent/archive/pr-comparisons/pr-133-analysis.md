# PR #133 Analysis: tc-intro-umbrella

**PR Title:** Tc intro umbrella
**Tutorial:** tc-intro-umbrella (Introduction to Cisco Umbrella)
**Secondary Tutorial:** tc-802-1x-ibns2.0 (802.1X IBNS 2.0)
**Editor:** masperli (Matt)
**Commits Analyzed:** 14 total (6 for each tutorial + 2 sidecar updates)
**Date Analyzed:** 2026-02-20

---

## Summary of Total Changes by Category

| Category | Count | Examples |
|----------|-------|----------|
| Product naming (trademark compliance) | 15+ | "Umbrella" -> "Cisco Umbrella" |
| Acronym expansion | 12+ | MAB, SWG, DNS, AAA, EAPOL, NAT, etc. |
| Grammar/sentence construction | 20+ | Typo fixes, subject-verb agreement |
| Technical accuracy (EOL product) | 1 | Cisco Roaming Client -> Cisco Secure Client |
| Capitalization normalization | 10+ | "Switch" -> "switch", "Server" -> "server" |
| Punctuation (em dashes) | 8+ | `—` -> `&mdash;` |
| GUI element formatting | 6+ | Bold navigation paths |
| Heading style | 6 | `###` -> `**Bold**` subheadings |
| Link improvements | 3 | Raw URLs -> markdown links |
| Word choice/clarity | 15+ | "In order to" -> "To", "setup" -> "set up" |
| List formatting | 2 | Added colons after feature names |

---

## Specific Rules with Before/After Examples

### 1. Trademark Compliance: "Cisco Umbrella" Required

**Rule:** Cisco Umbrella is a registered trademark. The "Cisco" prefix must be retained in most references.

**Matt's Explicit Citation:**
> "Cisco Umbrella" (and not just "Umbrella") is a Cisco registered trademark. For legal reasons related to the trademark, we're supposed to always refer to it as Cisco Umbrella ("Cisco" included) in our learning documentation.

| Before | After |
|--------|-------|
| How to configure Umbrella on a client | How to configure Cisco Umbrella on a client |
| Umbrella DNS Layer Protection | Cisco Umbrella DNS layer protection |
| The Umbrella IPv4 addresses are: | The Cisco Umbrella IPv4 addresses are: |
| you have successfully setup Umbrella | you have successfully set up Cisco Umbrella |

**Note:** Matt allowed some "Umbrella" references to remain to avoid excessive redundancy in paragraphs with multiple mentions.

---

### 2. Generic vs. Branded Terms in Lowercase

**Rule:** Generic technical terms should be lowercase, not capitalized like proper nouns.

| Before | After |
|--------|-------|
| Cisco Switch | Cisco switch |
| RADIUS Server | RADIUS server |
| Monitor Mode | monitor mode |
| Low Impact Mode | low-impact mode |
| Public facing IP | public-facing IP |

---

### 3. "In Order To" -> "To"

**Rule:** Remove "in order to" redundancy.

| Before | After |
|--------|-------|
| In order to address this problem | To deal with this problem |
| In order for to apply DNS Polices | To apply DNS policies |
| In order to login | To log in |
| In order to prevent this | To prevent this result |

---

### 4. "Setup" vs. "Set Up"

**Rule:** "Setup" is a noun/adjective; "set up" is a verb phrase.

| Before | After |
|--------|-------|
| These DNS IP's can be setup on | These DNS IPs can be set up on |
| you have successfully setup | you have successfully set up |
| After the DNS IP address has been setup | After the DNS IP address has been set up |

---

### 5. Acronym Expansion on First Use

| Before | After |
|--------|-------|
| 802.1x using the Identity-Based Networking Services 1.0 (IBNS) | IEEE 802.1X with the Cisco Identity-Based Networking Services (IBNS) version 1.0 |
| MAB authentication failing? | MAC Authentication Bypass (MAB) failing? |
| supplicate | supplicant (typo + consistent term) |
| EAPOL packets | Extensible Authentication Protocol over LAN (EAPOL) packets |
| NAT router | Network Address Translation (NAT) router |
| SaaS based applications | software as a service (SaaS)-based applications |
| QoS | quality of service (QoS) |
| AAA server | authentication, authorization, and accounting (AAA) server |
| ACL | access control list (ACL) |

---

### 6. Em Dash HTML Entity

**Rule:** Use `&mdash;` for em dashes in markdown (XML conversion compatibility).

| Before | After |
|--------|-------|
| — (unicode em dash) | `&mdash;` |
| Host modes — previously defined as | Host modes&mdash;previously defined as |
| restrictions — for example | restrictions&mdash;for example |

---

### 7. Feature Definition Format in Lists

**Rule:** In definition lists, format as `**Term:** Description` with colon inside bold.

| Before | After |
|--------|-------|
| `**Secure Web Gateway (SWG)** - is a full proxy` | `**Secure Web Gateway (SWG)** is a full proxy` |
| `**Service Template** Used to apply` | `**Service template:** This component is used to apply` |

---

### 8. Heading Levels (H3 -> Bold)

**Rule:** Convert H3 (`###`) subheadings within steps to bold text (`**Bold**`) for flatter hierarchy.

| Before | After |
|--------|-------|
| `### Creating a Service Template` | `**Create a Service Template**` |
| `### Defining a Identity Control Policy` | `**Define an Identity Control Policy**` |
| `### Session Initialization` | `**Session Initialization**` |

---

### 9. Article Usage: "a" vs "an"

| Before | After |
|--------|-------|
| a interface | an interface |
| a Identity Control Policy | an Identity Control Policy |

---

### 10. Verb Form Consistency in Instructions

**Rule:** Use imperative mood and present tense consistently.

| Before | After |
|--------|-------|
| "The diagram below summarizes" | "The following figure summarizes" |
| "In the example below" | "In the following example" |
| "As you can see, if a user tries" | "Notice that if a user tries" |

---

### 11. Link Format Improvements

**Rule:** Convert raw URLs to markdown links with descriptive text.

| Before | After |
|--------|-------|
| `browse to http://welcome.umbrella.com` | `browse to [welcome.umbrella.com](http://welcome.umbrella.com)` |
| `you will go to https://login.umbrella.com/` | `go to [login.umbrella.com](https://login.umbrella.com/)` |

---

### 12. Navigation Path Formatting

**Rule:** Use bold for GUI navigation with ">" separators.

| Before | After |
|--------|-------|
| `go to \`Deployment\`, and select \`Networks\`` | `navigate to **Deployments**, and then select **Networks**` |
| `click on \`Add\`` | `click **Add**` |

---

### 13. "This/That" Clarity

**Rule:** Replace vague pronouns with specific nouns.

| Before | After |
|--------|-------|
| "This allow the user to send" | "which allows the user to send" |
| "This is used to block" | "Malware protection is used to block" |

---

### 14. IP Address Formatting (Apostrophe)

| Before | After |
|--------|-------|
| DNS IP's | DNS IPs |
| Public IP's | public IPs |

---

### 15. Product EOL/Rebranding Update

**Rule:** Keep product names current; update EOL/deprecated products.

**Matt's Explicit Citation:**
> However, Cisco Roaming Client has reached EOL, and software maintenance ended last month. It has been replaced by Cisco Secure Client, so I have changed "Cisco Roaming Client" to "Cisco Secure Client."

| Before | After |
|--------|-------|
| Cisco Roaming Client | Cisco Secure Client |

---

### 16. Sentence Combining for Flow

**Rule:** Combine short, choppy sentences for better flow.

| Before | After |
|--------|-------|
| "After the interface template has been created, it can be applied to a range of interfaces using the `source template` command. This applies all the settings..." | "After the interface template has been created, it can be applied to a range of interfaces, using the `source template` command. This command applies all the settings..." |

---

### 17. Code Block Formatting

**Rule:** Add colon before code blocks.

| Before | After |
|--------|-------|
| "For example, the following template applies..." (no colon) | "For example, the following template applies...:" |

---

### 18. "Click On" -> "Click"

| Before | After |
|--------|-------|
| From the top right click on `Add` | At the top right, click **Add** |

---

## NEW Rules Not in Current Agent Prompt

### NEW 1: Trademark-Specific Redundancy Exception

The agent prompt mentions trademark compliance but does not capture Matt's nuance:

> "However, to avoid too much redundancy, I left some occurrences of 'Umbrella' as is in sentences where there were two or more references and in paragraphs with multiple references."

**Recommendation:** Add rule allowing occasional omission of "Cisco" prefix after 2+ uses in same paragraph to avoid excessive repetition.

---

### NEW 2: H3 to Bold Subheading Conversion

Not currently in agent prompt. Matt consistently converts `###` subheadings to `**Bold**` text within tutorial steps.

| Pattern | Reason |
|---------|--------|
| `### Title` -> `**Title**` | Flatter hierarchy, better XML conversion |

---

### NEW 3: Product EOL Awareness

The agent prompt mentions rebranding but not the specific Cisco Roaming Client -> Cisco Secure Client change. This is a **domain-specific knowledge gap**.

**Recommendation:** Add to product naming reference:
- Cisco Roaming Client (EOL 2025) -> Cisco Secure Client
- Cisco AnyConnect -> Cisco Secure Client

---

### NEW 4: IEEE Prefix for Standards

| Before | After |
|--------|-------|
| 802.1x | IEEE 802.1X |

Not currently enforced. The "IEEE" prefix is proper for standards references.

---

### NEW 5: "following" vs "below"

Matt consistently changes:
- "below" -> "following"
- "above" -> "preceding"

This matches progressive disclosure reading patterns.

---

### NEW 6: Feature List Punctuation Pattern

When defining features in a bullet list:
- Remove dash/hyphen separator between term and definition
- Keep colon inside bold: `**Term:** Definition`

---

### NEW 7: Note Block Formatting

| Before | After |
|--------|-------|
| `> The \`always\` class is a built-in...` | `> **Note:** The \`always\` class is a built-in...` |

Add explicit "Note:" prefix to blockquote callouts.

---

## Agent Coverage Assessment

### Rules Agent Would Catch (Estimated 65-70%)

| Rule | Coverage | Confidence |
|------|----------|------------|
| Acronym expansion | Full | High |
| "Click on" -> "Click" | Full | High |
| GUI bold formatting | Full | High |
| Em dash usage | Full | High |
| Product naming (Cisco prefix) | Partial | Medium |
| Article usage (a/an) | Full | High |
| "In order to" -> "To" | Full | High |
| "setup" vs "set up" | Full | High |
| Possessive IP plurals | Full | High |

### Rules Agent Would Miss (Estimated 30-35%)

| Rule | Gap | Reason |
|------|-----|--------|
| Trademark redundancy balance | Major | Requires judgment on "too much" |
| H3 -> Bold conversion | Major | Not in current prompt |
| Product EOL updates | Major | Requires external knowledge |
| IEEE prefix for standards | Minor | Not currently enforced |
| "below" -> "following" | Minor | Not explicitly stated |
| Feature list punctuation | Minor | Pattern not documented |

### Overall Agent Effectiveness Estimate

**Estimated catch rate: 65-70%** of Matt's editorial changes

The agent would handle mechanical transformations well but would miss:
1. **Judgment calls** (trademark redundancy balancing)
2. **External knowledge** (product EOL, rebranding)
3. **Structural changes** (heading level adjustments)
4. **Content accuracy** (technical corrections like Cisco Roaming Client)

---

## Matt's Explicit Rule Citations in This PR

1. **Trademark Rule:** "Cisco Umbrella" is a registered trademark requiring "Cisco" prefix
2. **Product EOL:** Cisco Roaming Client replaced by Cisco Secure Client (with URL reference)
3. **Redundancy Allowance:** Some trademark references can be omitted to avoid repetition

---

*Analysis based on 14 commits across tc-intro-umbrella and tc-802-1x-ibns2.0 tutorials*
