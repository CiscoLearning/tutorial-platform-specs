# Editorial Style Guide

This style guide is derived from editorial patterns observed in Jill's commit history on tutorial PRs. These rules should be enforced by automated validation where possible.

## 1. Heading Style

### Rule: Use Imperative Mood, Not Gerunds
Headings should use imperative (command) form, not progressive (-ing) form.

| Incorrect | Correct |
|-----------|---------|
| **Accessing the Learn Tab** | **Access the Learn Tab** |
| **Taking the Interest Survey** | **Take the Interest Survey** |
| **Understanding Your Score Report** | **Understand Your Score Report** |
| **Tracking Your Progress** | **Track Your Progress** |
| **Generating Reports** | **Generate Reports** |
| **Creating Outputs and Validating Controls** | **Create Outputs and Validate Controls** |

### Rule: Title Case for Headings
Use title case capitalization for section headings.

| Incorrect | Correct |
|-----------|---------|
| Why Improvement is Necessary | Why Improvement Is Necessary |
| GET method | GET Method |

## 2. Procedural Introduction Lines

### Rule: Add "To [action]:" Before Numbered Steps
When introducing a procedure, add a lead-in line before the numbered steps.

**Incorrect:**
```markdown
## Take the Interest Survey

1. Click the Survey button.
2. Select your interests.
```

**Correct:**
```markdown
## Take the Interest Survey

To take the Interest Survey:

1. Click the Survey button.
2. Select your interests.
```

## 3. Punctuation

### Em Dashes
Use em dashes without surrounding spaces.

| Incorrect | Correct |
|-----------|---------|
| problems — they assume | problems—they assume |
| RSA and ECC — which are | RSA and ECC—which are |

### Serial Comma
Use the Oxford/serial comma before "and" in lists.

| Incorrect | Correct |
|-----------|---------|
| RSA and ECC would be broken and many | RSA and ECC would be broken, and many |

### Colons in Subheadings
Remove trailing colons from subheadings unless introducing a list.

| Incorrect | Correct |
|-----------|---------|
| **More Information on the Topic:** | **More Information on the Topic** |
| **Explore More on Cisco U.:** | **Explore More on Cisco U.** |

### End Punctuation
All sentences must end with appropriate punctuation, including in notes and bullet lists.

## 4. Code Formatting vs. Bold

### Rule: Use Code Style for Technical Terms
Use backticks for:
- Commands and CLI tools: `cURL`, `kubectl`
- Status codes: `200`, `404`
- Model names: `ietf-interfaces`
- File names and paths

### Rule: Use Bold for Concepts and UI Elements
Use bold for:
- Acronym definitions: **AAA**, **Authentication**
- UI element names: **Update Interests** button
- Key concepts being introduced

| Incorrect | Correct |
|-----------|---------|
| `IEEE 802.11be` (code style) | IEEE 802.11be (plain text for standards) |
| **200** (bold for status code) | `200` (code style for status codes) |
| `three services` (code style) | three services (plain text) |

## 5. Acronyms and Abbreviations

### Rule: Expand on First Use
Spell out acronyms on first use with the abbreviation in parentheses.

| First Use | Subsequent Uses |
|-----------|-----------------|
| Wi-Fi Protected Access 3 (WPA3) | WPA3 |
| Service Set Identifier (SSID) | SSID |
| access points (APs) | APs |
| Secure Sockets Layer (SSL) | SSL |
| Message Queuing Telemetry Transport (MQTT) | MQTT |

### Rule: Remove Redundant Expansions
After first introduction, use only the acronym.

| Incorrect | Correct |
|-----------|---------|
| "...uses Wi-Fi Protected Access 3 (WPA3) encryption. The WPA3 protocol..." | "...uses Wi-Fi Protected Access 3 (WPA3) encryption. WPA3..." |

## 6. Technical Term Formatting

### Rule: Hyphenate Compound Technical Terms
Use hyphens in compound technical specifications.

| Incorrect | Correct |
|-----------|---------|
| GCMP256 | GCMP-256 |
| AES 128 | AES-128 |
| Model Driven Programmability | Model-Driven Programmability |

### Rule: Add Space Before Units
Add space between numbers and units.

| Incorrect | Correct |
|-----------|---------|
| 160Mhz | 160 MHz |
| 5GHz | 5 GHz |

## 7. Naming Consistency

### Rule: Match UI and Documentation Names
Use exact names as they appear in the product UI or official documentation.

| Incorrect | Correct |
|-----------|---------|
| Video Series | Videos |
| Events and Webinars | Events |
| Cisco ISE box | Cisco ISE server |
| content type carousels | content carousels |

## 8. Word Choice and Clarity

### Rule: Prefer Precise Words

| Avoid | Prefer |
|-------|--------|
| making attacks meaningless | making attacks infeasible |
| In order to | To |
| the various variations | the variations |
| But (at sentence start) | However, |
| ensures | helps ensure (when hedging is appropriate) |

## 9. List Formatting

### Rule: Bold for Definition List Items
Use bold (not italic) for definition list labels, followed by colon.

| Incorrect | Correct |
|-----------|---------|
| - _CPU specifications_: Details... | - **CPU specifications:** Details... |
| - _Server memory_: The total... | - **Server memory:** The total... |

### Rule: Parallel Structure in Lists
Ensure all items in a list follow the same grammatical structure.

| Incorrect | Correct |
|-----------|---------|
| - **For You page:** Your personalized hub | - **For You page:** Visit your personalized hub |
| - **Learning Paths:** Structured learning | - **Learning Paths:** Follow structured learning |

## 10. UI Element Capitalization

### Rule: Match Exact UI Text
Capitalize UI elements exactly as they appear in the interface.

| Incorrect | Correct |
|-----------|---------|
| **Update interests** | **Update Interests** |
| click the save button | click the **Save** button |

### Rule: Lowercase General Terms
Use lowercase for general concepts (not proper nouns or UI elements).

| Incorrect | Correct |
|-----------|---------|
| Infrastructure as Code (general concept) | infrastructure as code |
| Virtual Private Clouds | virtual private clouds |

## 11. Cross-References

### Rule: Avoid Vague Forward References
Remove cross-references to later sections unless directly relevant.

| Avoid | Prefer |
|-------|--------|
| (See the next step for more details.) | [Remove if content is several steps away] |
| (see 'The Learn Tab' section for details) | [Remove unless directly actionable] |

## 12. URL Updates

### Rule: Use Current URL Patterns
Keep URLs updated to match current site structure.

| Outdated | Current |
|----------|---------|
| `/explore/tutorials` | `/tutorials` |
| `/explore/video-series` | `/videos` |
| `/explore/podcasts` | `/podcasts` |
| `/explore/events-and-webinars` | `/events` |

---

## Validation Priority

For automated enforcement, prioritize these rules:

### High Priority (Blocking)
1. Acronym expansion on first use
2. Heading style (imperative mood)
3. End punctuation
4. Technical term hyphenation

### Medium Priority (Warning)
1. Em dash spacing
2. Serial comma
3. Code vs. bold formatting
4. Procedural introduction lines

### Low Priority (Suggestion)
1. Word choice improvements
2. Cross-reference cleanup
3. Parallel structure
4. URL updates
