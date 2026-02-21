# PR #159 Editorial Rules Test Results

**PR:** [#159 - tc-infrastructure-as-code-for-security-architects](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/159)
**Editor:** jlauterb-edit (Jill Lauterborn)
**Test Date:** 2026-02-20

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Editor Changes | 89 | 100% |
| **CAUGHT by Rules** | 49 | **55%** |
| **MISSED by Rules** | 40 | **45%** |

---

## Detailed Analysis

### CAUGHT: Changes Our Rules Would Detect (49 total)

#### 1. Gerund to Imperative Headings (12 changes) - UNIVERSAL RULE

| Original | Editor Change | Rule |
|----------|---------------|------|
| `Understanding Infrastructure as Code Fundamentals` | `Understand Infrastructure as Code Fundamentals` | GERUND_TO_IMPERATIVE |
| `Installing Terraform` | `Install Terraform` | GERUND_TO_IMPERATIVE |
| `Setting Up AWS CLI for Secure Credential Management` | `Set Up AWS CLI for Secure Credential Management` | GERUND_TO_IMPERATIVE |
| `Creating Your Secure VPC Foundation` | `Create Your Secure VPC Foundation` | GERUND_TO_IMPERATIVE |
| `Configuring Network Routing and Internet Access` | `Configure Network Routing and Internet Access` | GERUND_TO_IMPERATIVE |
| `Implementing Identity and Access Management` | `Implement Identity and Access Management` | GERUND_TO_IMPERATIVE |
| `Setting Up Comprehensive Security Logging` | `Set Up Comprehensive Security Logging` | GERUND_TO_IMPERATIVE |
| `Implementing Web Application Firewall Protection` | `Implement Web Application Firewall Protection` | GERUND_TO_IMPERATIVE |
| `Implementing Network Security with Security Groups` | `Implement Network Security with Security Groups` | GERUND_TO_IMPERATIVE |
| `Defining the Application Infrastructure` | `Define the Application Infrastructure` | GERUND_TO_IMPERATIVE |
| `Create Outputs and Validating Security Controls` | `Create Outputs and Validate Security Controls` | GERUND_TO_IMPERATIVE |
| `Deploying Your Secure Infrastructure` | `Deploy Your Secure Infrastructure` | GERUND_TO_IMPERATIVE |

#### 2. H3 to Bold/H2 Headings (31 changes) - OTHER RULE

All `## Section Name` headings in steps were converted from gerunds to imperatives. Examples:
- `## Preparing Your System` -> `## Prepare Your System`
- `## Installing the HashiCorp GPG Key` -> `## Install the HashiCorp GPG Key`
- `## Creating Internet Gateway` -> `## Create an Internet Gateway`
- `## Configuring Public Route Tables` -> `## Configure Public Route Tables`

#### 3. Add Articles to Headings (6 changes) - UNIVERSAL RULE

| Original | Editor Change |
|----------|---------------|
| `## Create Variables Configuration` | `## Create a Variables Configuration` |
| `## Create Internet Gateway` | `## Create an Internet Gateway` |
| `## Set Up NAT Gateway for Private Subnet Access` | `## Set Up a NAT Gateway for Private Subnet Access` |
| `## Create IAM Role for EC2 Instances` | `## Create an IAM Role for EC2 Instances` |
| `## Create WAF Web ACL with Security Rules` | `## Create a WAF Web ACL with Security Rules` |
| `## Create Load Balancer Security Group` | `## Create a Load Balancer Security Group` |

---

### MISSED: Changes Our Rules Would NOT Detect (40 total)

#### 1. Acronym First-Use Expansions (7 changes)

| Original | Editor Change | Why Missed |
|----------|---------------|------------|
| `AWS CLI` | `Amazon Web Services (AWS) CLI` | Acronym expansion not in our rules |
| `Virtual Private Clouds (VPCs)` | `virtual private clouds (VPCs)` | Case normalization for non-proper nouns |
| `GPG` | `GNU Privacy Guard (GPG)` | Acronym expansion |
| `NAT gateways` | `Network Address Translation (NAT) gateways` | Acronym expansion |
| `URI paths` | `uniform resource identifier (URI) paths` | Acronym expansion |
| `CI/CD` | `continuous integration and continuous delivery (CI/CD)` | Acronym expansion |
| `Web ACL` | `web access control list (ACL)` | Combined case + expansion |

**Why not caught:** We have no ACRONYM_EXPAND rule for first-use expansions.

#### 2. Punctuation and Comma Usage (8 changes)

| Original | Editor Change | Why Missed |
|----------|---------------|------------|
| `time-consuming, and prone to errors. ... can increase operational costs as` | `can increase operational costs, as` | Oxford comma addition |
| `is crucial for security as it` | `is crucial for security, as it` | Comma before "as" clause |
| `APIs calls, and so on` | `updates, API calls, and similar tasks` | "and so on" -> "and similar tasks" |
| `and optionally, a default` | `and, optionally, a default` | Comma pair around "optionally" |
| `multi-line blocks` | `multiline blocks` | Compound word (covered partially) |
| List items ending with `.` removed | List items without periods | List punctuation normalization |

**Why not caught:** Subtle punctuation rules (comma placement) not in our ruleset.

#### 3. Word Choice / Style Preferences (12 changes)

| Original | Editor Change | Why Missed |
|----------|---------------|------------|
| `recreate` | `re-create` | Hyphenation preference |
| `upfront` | `up front` | Two-word vs one-word |
| `And by storing` | `Also, by storing` | Sentence starter preference |
| `lifecycle` | `life cycle` | Two-word preference (conflicts with our compound word rule!) |
| `multi-factor` | `multifactor` | Hyphen removal |
| `minimal` | `minimum` | Word choice |
| `utilizing` | `using` | Plain language |
| `5-10 minutes` | `5 to 10 minutes` | Number range format |
| `automatically identify` | `identify automatically` | Word order |
| `your go-to resource` | (kept but pattern shows preference) | Informal language |

**Why not caught:** These are style preferences without consistent patterns.

#### 4. Sentence Structure / Rewrites (5 changes)

| Original | Editor Change | Why Missed |
|----------|---------------|------------|
| `They define...` (sentence fragment after colon) | Full sentence with `They` subject | Parallelism fix |
| `**Load Balancing Layer:**` | `**Load balancing layer:**` | Case normalization in bold headings |
| `Follow these steps to deploy your secure infrastructure:` | `Follow these steps to deploy your secure infrastructure.` | Colon to period before numbered list |
| Numbered list items `**1. X:**` | `**1. X.**` | Period vs colon in numbered headings |

**Why not caught:** Complex sentence restructuring is beyond pattern matching.

#### 5. Bold Heading Case Normalization (8 changes)

| Original | Editor Change | Why Missed |
|----------|---------------|------------|
| `**Ownership Tags:**` | `**Ownership tags:**` | Title case -> Sentence case |
| `**Lifecycle Management:**` | `**Life cycle management:**` | Title case -> Sentence case |
| `**Operational Control:**` | `**Operational control:**` | Title case -> Sentence case |
| `**Load Balancing Layer:**` | `**Load balancing layer:**` | Title case -> Sentence case |
| `**Compute Layer:**` | `**Compute layer:**` | Title case -> Sentence case |
| `**Security Integration:**` | `**Security integration:**` | Title case -> Sentence case |
| `**Information Access:**` | `**Information access:**` | Title case -> Sentence case |
| `**Reference Documentation:**` | `**Reference documentation:**` | Title case -> Sentence case |

**Why not caught:** We don't have a BOLD_HEADING_CASE rule for sentence case in bold headings.

---

## Rule Effectiveness Analysis

### Rules That Worked Well

| Rule | Matches Found | Notes |
|------|---------------|-------|
| GERUND_TO_IMPERATIVE | 43 (12 sidecar + 31 H2) | **Highest impact rule** - caught all heading conversions |
| ADD_ARTICLES | 6 | Caught article additions to headings |

### Rules Not Tested (no instances in PR)

| Rule | Notes |
|------|-------|
| BOLD_LIST_ITEM | No `- **Term:**` patterns in this PR |
| UNIT_SPACING | No `8GB` style issues in this PR |
| BOLD_TO_CODE | No path/command bold issues in this PR |
| NO_CONTRACTIONS | No contractions found in original |

### Gaps Identified

| Missing Rule | Priority | Frequency in PR |
|--------------|----------|-----------------|
| **ACRONYM_FIRST_USE** | High | 7 instances |
| **BOLD_HEADING_CASE** | High | 8 instances |
| **COMMA_CLAUSE** | Medium | 8 instances |
| **LIFECYCLE_TWO_WORDS** | Low | 2 instances (conflicts with our compound word rule) |
| **NUMBER_RANGE_WORDS** | Low | 1 instance |

---

## Recommendations

### 1. Add New Universal Rules

```
ACRONYM_FIRST_USE: Flag common tech acronyms (AWS, VPC, IAM, NAT, etc.) that appear
                   without prior expansion in the document.

BOLD_HEADING_CASE: Bold headings should use sentence case, not title case.
                   Example: `**Load balancing layer:**` not `**Load Balancing Layer:**`
```

### 2. Clarify Existing Rules

```
COMPOUND_WORDS: "lifecycle" vs "life cycle" - Editor prefers TWO words.
                This CONFLICTS with our current rule recommending one word.
                Need to verify Cisco style guide preference.
```

### 3. Consider Low-Priority Rules

```
COMMA_AS_CLAUSE: Add comma before "as" when introducing a reason clause.
NUMBER_RANGE_WORDS: "5-10" -> "5 to 10" for readability.
PLAIN_LANGUAGE: "utilizing" -> "using"
```

---

## Conclusion

Our current rules would catch **55% of editor changes** in this PR. The gerund-to-imperative rule is highly effective for headings. The main gaps are:

1. **Acronym handling** (7 changes missed) - Would require document-level context
2. **Bold heading case normalization** (8 changes missed) - Simple regex rule to add
3. **Punctuation nuances** (8 changes missed) - Complex rules, may require AI

**Recommended next step:** Add `BOLD_HEADING_CASE` rule as it's high-frequency and simple to implement.
