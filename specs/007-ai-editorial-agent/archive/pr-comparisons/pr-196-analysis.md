# PR #196 Editorial Analysis

**PR:** [#196](https://github.com/CiscoLearning/ciscou-tutorial-content/pull/196)
**Tutorial:** tc-flask-restx-rbac (Flask-RESTX API with RBAC and Token Authentication)
**Editors:** masperli (13 commits), jlauterb-edit (13 commits)
**Analysis Date:** 2026-02-20

## Summary Table of Editorial Changes

| Rule Category | Count | Agent Coverage | Notes |
|---------------|-------|----------------|-------|
| Gerund to base infinitive in headings | 20+ | **NO** | Consistent pattern across all steps |
| Compound word: "life cycle" (two words) | 6 | **NO** | Changed "lifecycle" to "life cycle" |
| Acronym expansion (first use) | 15+ | Partial | REST, API, RBAC, CRUD, HMAC, ORM, NIST, LDAP |
| H2/H3 to bold text | 10+ | **YES** | `## Section` to `**Section**` |
| List capitalization | 8+ | **NO** | Sentence case after bullets |
| UI element formatting | 12+ | **NO** | `**"Try it out"**` to `**Try it out**` |
| Compound word: "multistrategy" | 3 | **NO** | "multi-strategy" to "multistrategy" |
| Compound word: "multiregional" | 2 | **NO** | "multi-region" to "multiregional" |
| Ampersand to "and" | 4 | **NO** | "Security & Validation" to "Security and Validation" |
| Sentence-ending periods in lists | 30+ | **NO** | Added periods at end of bullet items |
| Bold to italic for emphasis | 2 | **NO** | Specific phrases changed to italics |
| Missing article "the" | 5+ | **NO** | Grammar corrections |
| No contractions (partial) | 2 | **YES** | Some contractions retained (common in tutorials) |

---

## Before/After Examples by Rule Type

### 1. Gerund to Base Infinitive in Headings (NEW - High Priority)

The editors consistently changed gerund forms (-ing) to base infinitive forms in headings and step labels.

**sidecar.json labels:**
```
BEFORE: "Building the Foundation"
AFTER:  "Build the Foundation"

BEFORE: "Implementing Token Authentication"
AFTER:  "Implement Token Authentication"

BEFORE: "Creating Protected Endpoints"
AFTER:  "Create Protected Endpoints"

BEFORE: "Testing Your API"
AFTER:  "Test Your API"
```

**step-3.md headings:**
```
BEFORE: **Installing Dependencies**
AFTER:  **Install Dependencies**

BEFORE: **Creating a Virtual Environment**
AFTER:  **Create a Virtual Environment**
```

**step-5.md headings:**
```
BEFORE: **Understanding JWT Architecture**
AFTER:  **Understand JWT Architecture**

BEFORE: **Implementing Token Management**
AFTER:  **Implement Token Management**

BEFORE: **Configuring JWT Callbacks**
AFTER:  **Configure JWT Callbacks**
```

**step-7.md headings:**
```
BEFORE: **Implementing User List Endpoint**
AFTER:  **Implement User List Endpoint**

BEFORE: **Creating Role Management Endpoints**
AFTER:  **Create Role Management Endpoints**

BEFORE: **Registering API Namespaces**
AFTER:  **Register API Namespaces**
```

**step-9.md headings:**
```
BEFORE: **Setting Up the Testing Environment**
AFTER:  **Set Up the Testing Environment**

BEFORE: **Running Your Tests**
AFTER:  **Run Your Tests**

BEFORE: **Creating the Application Entry Point**
AFTER:  **Create the Application Entry Point**

BEFORE: **Starting the Application**
AFTER:  **Start the Application**

BEFORE: **Accessing the Interactive Documentation**
AFTER:  **Access the Interactive Documentation**

BEFORE: **Testing Authentication Flow**
AFTER:  **Test Authentication Flow**

BEFORE: **Verifying RBAC Enforcement**
AFTER:  **Verify RBAC Enforcement**

BEFORE: **Protecting Your Project with .gitignore**
AFTER:  **Protect Your Project with .gitignore**
```

---

### 2. Compound Word: "life cycle" (Two Words) - NEW

Consistent change from "lifecycle" to "life cycle".

**step-1.md:**
```
BEFORE: access/refresh tokens and secure lifecycle management
AFTER:  access and refresh tokens and secure life cycle management
```

**step-2.md:**
```
BEFORE: rejected early in the request lifecycle
AFTER:  rejected early in the request life cycle

BEFORE: refresh token lifecycle management
AFTER:  refresh token life cycle management
```

**step-5.md:**
```
BEFORE: Authentication routes handle the complete token lifecycle.
AFTER:  Authentication routes handle the complete token life cycle.

BEFORE: token lifecycle management
AFTER:  token life cycle management
```

**step-9.md:**
```
BEFORE: the complete authentication lifecycle
AFTER:  the complete authentication life cycle
```

---

### 3. Acronym Expansion on First Use

Editors expanded acronyms on first occurrence with the full form followed by the acronym in parentheses.

**step-1.md:**
```
BEFORE: In this tutorial, you will develop an enterprise-grade REST API
AFTER:  In this tutorial, you will develop an enterprise-grade Representational State Transfer (REST) application programming interface (API)

BEFORE: comprehensive Role-Based Access Control (RBAC)
AFTER:  comprehensive role-based access control (RBAC)
```

**step-2.md:**
```
BEFORE: using SQLAlchemy ORM patterns
AFTER:  using SQLAlchemy Object Relational Mapper (ORM) patterns
```

**step-3.md:**
```
BEFORE: prevent XSS attacks
AFTER:  prevent cross-site scripting (XSS) attacks
```

**step-7.md:**
```
BEFORE: comprehensive CRUD operations
AFTER:  comprehensive create, read, update, and delete (CRUD) operations
```

**step-11.md:**
```
BEFORE: Add LDAP/Active Directory integration
AFTER:  Add Lightweight Directory Access Protocol (LDAP)/Active Directory integration
```

**step-12.md:**
```
BEFORE: NIST guidelines for role-based access control
AFTER:  The National Institute of Standards and Technology (NIST) guidelines for RBAC implementation
```

---

### 4. H2/H3 Headings to Bold Text (Existing Rule - Confirmed)

Markdown headings converted to bold text within tutorial steps.

**step-1.md (masperli):**
```
BEFORE: ## What You'll Learn
AFTER:  **What You'll Learn**

BEFORE: ## What You'll Need
AFTER:  **What You'll Need**

BEFORE: ### Prerequisite Knowledge
AFTER:  Prerequisite knowledge:

BEFORE: ### Development Environment
AFTER:  Development environment:
```

**step-2.md (masperli):**
```
BEFORE: ## Why Flask-RESTX?
AFTER:  **Why Flask-RESTX?**

BEFORE: ## Architecture Overview
AFTER:  **Architecture Overview**

BEFORE: ### Design Principles
AFTER:  **Design Principles**
```

---

### 5. UI Element Formatting (No Quotes Inside Bold) - NEW

Editors removed quotation marks from UI elements that were already bolded.

**step-9.md:**
```
BEFORE: click **"Try it out"**
AFTER:  click **Try it out**

BEFORE: Click **"Execute"**
AFTER:  Click **Execute**

BEFORE: Click the **"Authorize"** button
AFTER:  Click the **Authorize** button

BEFORE: Click **"Authorize"**, then **"Close"**
AFTER:  Click **Authorize**, then **Close**
```

---

### 6. Compound Words: "multi-" Prefix (Closed Form) - NEW

The "multi-" prefix is joined without hyphen.

**step-1.md:**
```
BEFORE: Build a multi-strategy token validation system
AFTER:  Build a multistrategy token validation system
```

**step-11.md:**
```
BEFORE: Multi-layered Flask-RESTX architecture
AFTER:  Multilayered Flask-RESTX architecture

BEFORE: Multi-factor authentication
AFTER:  Multifactor authentication

BEFORE: multi-region architecture
AFTER:  multiregional architecture

BEFORE: multi-tenant authorization
AFTER:  multitenant authorization

BEFORE: multi-service automation workflows
AFTER:  multiservice automation workflows
```

---

### 7. Ampersand to "and" - NEW

Ampersands replaced with "and" in prose and diagrams.

**step-2.md (from masperli commit message):**
```
BEFORE: Security & Validation
AFTER:  Security and Validation

BEFORE: Retrieval & Analytics
AFTER:  Retrieval and Analytics
```

---

### 8. Sentence-Ending Periods in Lists - NEW

Editors added periods at the end of bullet point items that form complete sentences.

**step-3.md:**
```
BEFORE: - `flask`: The core web framework foundation for handling HTTP requests and responses
AFTER:  - `flask`: is the core web framework foundation for handling HTTP requests and responses

BEFORE: - `flask-restx`: Adds automatic API documentation
AFTER:  - `flask-restx`: adds automatic API documentation
```

**step-11.md:**
```
BEFORE: - Implement JWT-based authentication for network device management APIs
AFTER:  - Implement JWT-based authentication for network device management APIs.

BEFORE: - Build rate limiting mechanisms for high-volume automation request processing
AFTER:  - Build rate limiting mechanisms for high-volume automation request processing.
```

**step-9.md:**
```
BEFORE: - **auth** - Authentication endpoints (login, logout, refresh)
AFTER:  - **auth** - authentication endpoints (login, logout, refresh)
```

---

### 9. Case Sensitivity: Architecture/System Names - NEW

Section names that are not proper nouns use sentence case.

**step-2.md:**
```
BEFORE: - **Authentication System:** Handles user registration...
AFTER:  - **Authentication system:** Handles user registration...

BEFORE: - **RBAC System:** Manages roles...
AFTER:  - **RBAC system:** Manages roles...

BEFORE: - **API Resources:** The actual endpoints...
AFTER:  - **API resources:** The actual endpoints...

BEFORE: - **Security Middleware:** Decorators and utilities...
AFTER:  - **Security middleware:** Consists of decorators and utilities...

BEFORE: - **Models Layer:** Database models...
AFTER:  - **Models layer:** Database models...
```

**step-11.md:**
```
BEFORE: ***Enterprise API Architecture (35% of professional focus):***
AFTER:  ***Enterprise API architecture (35% of professional focus):***

BEFORE: ***Security and Compliance (35% of professional focus):***
AFTER:  ***Security and compliance (35% of professional focus):***
```

---

### 10. Bold to Italic for Specific Emphasis - NEW

Certain instructional notes changed from bold to italic.

**step-11.md:**
```
BEFORE: This is an **example pattern for future practice**
AFTER:  This is an _example pattern for future practice_

BEFORE: It is a **conceptual example for learning**
AFTER:  It is a _conceptual example for learning_
```

---

### 11. "Login/Logout" as Verbs - NEW

When used as verbs (actions), written as two words.

**step-9.md:**
```
BEFORE: - **Login to get your access token:**
AFTER:  1. **Log in to get your access token:**

BEFORE: Logout by clicking...
AFTER:  Log out by clicking...

BEFORE: Login as the new user
AFTER:  Log in as the new user
```

---

### 12. Grammar: Missing Articles and Clarity

**step-2.md:**
```
BEFORE: JWTs contain all necessary user verification information
AFTER:  JWTs contain all the necessary user verification information

BEFORE: Server validates tokens without database queries
AFTER:  The server validates tokens without database queries
```

---

### 13. Em Dashes for Parenthetical Phrases

Editors used em dashes appropriately.

**step-3.md (masperli):**
```
BEFORE: We'll use environment variables for sensitive information - never hardcode secrets!
AFTER:  We'll use environment variables for sensitive information&mdash;never hardcode secrets!
```

**step-9.md:**
```
BEFORE: should fail with 403 (Insufficient permissions)
AFTER:  should fail with 403 (insufficient permissions)

BEFORE: Try to access **GET /users/** - should fail
AFTER:  Try to access **GET /users/**—it should fail
```

---

## NEW Rules Not in Current Tier 1 (Candidates for Addition)

| Rule | Priority | Frequency | Automatable |
|------|----------|-----------|-------------|
| **Gerund to base infinitive in headings** | HIGH | Very High | Yes (regex + context) |
| **"life cycle" as two words** | HIGH | High | Yes (dictionary lookup) |
| **"multi-" prefix closed form** | MEDIUM | Medium | Yes (dictionary lookup) |
| **Ampersand to "and"** | MEDIUM | Medium | Yes (simple regex) |
| **UI elements: no quotes inside bold** | MEDIUM | Medium | Yes (regex) |
| **Sentence case for system/layer names** | LOW | Medium | Context-dependent |
| **"Log in/Log out" as verbs** | LOW | Low | Context-dependent |
| **Bold to italic for instructional notes** | LOW | Low | Context-dependent |

---

## Coverage Assessment

### Rules the Current Agent Would Catch

| Rule | Status | Notes |
|------|--------|-------|
| H3 to bold formatting | YES | Already in Tier 1 |
| No contractions | PARTIAL | Rule exists but not consistently applied |
| Trailing whitespace | YES | Clean markdown handles |
| Missing newline at EOF | YES | Clean markdown handles |

### Rules the Agent Would Miss

| Rule | Priority to Add | Implementation Complexity |
|------|-----------------|---------------------------|
| Gerund to base infinitive | **HIGH** | Medium - needs heading detection + verb identification |
| "life cycle" (two words) | **HIGH** | Low - dictionary lookup |
| "multistrategy/multiregional" (no hyphen) | MEDIUM | Low - dictionary lookup |
| Ampersand to "and" | MEDIUM | Low - simple regex |
| UI element quote removal | MEDIUM | Low - regex pattern |
| Acronym expansion tracking | LOW | High - requires document context |
| Sentence case for descriptors | LOW | High - requires semantic understanding |

### Estimated Current Coverage

Based on this PR analysis:

- **Changes Agent Would Catch:** ~15%
- **Changes Agent Would Miss:** ~85%

The most significant gap is the **gerund to base infinitive** rule for headings, which appears in almost every step and accounts for a large portion of editorial changes. Adding this single rule would dramatically improve coverage.

---

## Recommended Tier 1 Rule Additions

### Priority 1 (Add Immediately)

1. **Gerund to Base Infinitive in Headings**
   - Pattern: Detect headings (bold or H2/H3) starting with gerund verbs
   - Change: "Installing" to "Install", "Creating" to "Create", etc.
   - Complexity: Medium (verb conjugation needed)

2. **Compound Word: "life cycle"**
   - Pattern: `/lifecycle/gi`
   - Change: "lifecycle" to "life cycle"
   - Complexity: Low

3. **Compound Word: "multi-" prefix**
   - Pattern: `/multi-(\w+)/gi`
   - Change: Most "multi-X" to "multiX" (multistrategy, multilayered, etc.)
   - Exception: "multi-factor" may vary by style guide
   - Complexity: Low

### Priority 2 (Add Soon)

4. **Ampersand to "and"**
   - Pattern: `/\s&\s/g`
   - Change: " & " to " and "
   - Complexity: Low

5. **UI Element Quote Removal**
   - Pattern: `/\*\*"([^"]+)"\*\*/g`
   - Change: `**"Text"**` to `**Text**`
   - Complexity: Low

6. **Log in/Log out as Verbs**
   - Pattern: Context-aware detection
   - Change: "Login" (verb) to "Log in", "Logout" (verb) to "Log out"
   - Complexity: Medium

---

## Conclusion

PR #196 reveals a consistent editorial pattern focused heavily on:

1. **Heading verb forms** - Converting gerunds to base infinitives (most common change)
2. **Compound words** - Cisco style prefers "life cycle" (two words) and closed "multi-" compounds
3. **Formatting consistency** - UI elements without quotes, sentence case for descriptors

The current AI agent would catch approximately 15% of the editorial changes seen in this PR. Adding the gerund-to-infinitive rule alone would significantly improve coverage, as it represents the single most frequent editorial change across all tutorial steps.
