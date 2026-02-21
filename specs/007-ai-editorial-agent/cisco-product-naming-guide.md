# Cisco Product Naming and Acronym Guide

**Purpose:** Living reference document for the AI editorial agent. Update this document as Cisco products, acronyms, and standards change.

**Last Updated:** 2026-02-20
**Maintainers:** Editorial Team (Jill, Matt), Technical Advocates

---

## How to Use This Document

The AI editorial agent references this document to:
1. Validate product name usage
2. Suggest acronym expansions
3. Flag deprecated terminology
4. Ensure trademark compliance

**To Update:** Edit this file directly or provide a PDF version. Changes will be picked up by the agent on next run.

---

## Product Naming Standards

### Security Products

| Short Form | Full Official Name | First Use | Subsequent |
|------------|-------------------|-----------|------------|
| ASA | Cisco Secure Firewall Adaptive Security Appliance | Cisco Secure Firewall Adaptive Security Appliance (ASA) | Secure Firewall ASA, ASA |
| FTD | **DEPRECATED** | Cisco Secure Firewall Threat Defense | Secure Firewall Threat Defense |
| FMC | **DEPRECATED** | Cisco Secure Firewall Management Center | Secure Firewall Management Center |
| ISE | Cisco Identity Services Engine | Cisco Identity Services Engine (ISE) | ISE |
| Umbrella | Cisco Umbrella | Cisco Umbrella | Cisco Umbrella (keep "Cisco" - trademark) |
| Duo | Cisco Duo | Cisco Duo | Duo (after first use) |

### Networking Products

| Short Form | Full Official Name | First Use | Subsequent |
|------------|-------------------|-----------|------------|
| ACI | Cisco Application Centric Infrastructure | Cisco Application Centric Infrastructure (Cisco ACI) | Cisco ACI |
| NX-OS | Cisco Nexus Operating System | Cisco Nexus Operating System (Cisco NX-OS) | Cisco NX-OS |
| NSO | Cisco Network Services Orchestrator | Cisco Network Services Orchestrator (NSO) | NSO |
| DNA Center | Cisco DNA Center | Cisco DNA Center | DNA Center |
| Meraki | Cisco Meraki | Cisco Meraki | Meraki (both are registered trademarks) |

### Collaboration Products

| Short Form | Full Official Name | First Use | Subsequent |
|------------|-------------------|-----------|------------|
| Webex | Cisco Webex | Cisco Webex | Webex |

### AI Products

| Short Form | Full Official Name | Notes |
|------------|-------------------|-------|
| AI Assistant | Cisco AI Assistant | Use "AI Assistant models" not "AI Assistants" for plural |

---

## Deprecated Acronyms

These acronyms should NOT be used. Use full product names instead:

| Deprecated | Replacement |
|------------|-------------|
| FTD | Cisco Secure Firewall Threat Defense |
| FMC | Cisco Secure Firewall Management Center |
| CCO | Cisco Connection Online |
| UCS (in general text) | Cisco Unified Computing System |

**Exception:** UCS can be used in GUI element references (e.g., "**UCS Domain**" button)

---

## Trademark Rules

### Must Keep "Cisco"

These products MUST include "Cisco" even in subsequent references (registered trademarks):

- Cisco Umbrella (not just "Umbrella")
- Cisco AI Assistant

### Can Drop "Cisco" After First Use

- Cisco Meraki → Meraki
- Cisco ISE → ISE
- Cisco Duo → Duo

### Possessive Form

**Never use Cisco product names in possessive form:**

| Incorrect | Correct |
|-----------|---------|
| Cisco Hypershield's technology | the Cisco Hypershield technology |
| ISE's configuration | the ISE configuration |

---

## Common Acronyms

### Networking Acronyms (Expand on First Use)

| Acronym | Expansion |
|---------|-----------|
| VLAN | virtual LAN |
| VRF | virtual routing and forwarding |
| BGP | Border Gateway Protocol |
| OSPF | Open Shortest Path First |
| MPLS | Multiprotocol Label Switching |
| QoS | quality of service |
| SNMP | Simple Network Management Protocol |
| DNS | Domain Name System |
| DHCP | Dynamic Host Configuration Protocol |
| NAT | Network Address Translation |
| ACL | access control list |
| STP | Spanning Tree Protocol |
| LACP | Link Aggregation Control Protocol |
| L3VPN | Layer 3 VPN |
| ECMP | Equal Cost Multi-Path |

### Security Acronyms

| Acronym | Expansion |
|---------|-----------|
| AAA | authentication, authorization, and accounting |
| TACACS+ | Terminal Access Controller Access-Control System Plus |
| RADIUS | Remote Authentication Dial-In User Service |
| MFA | multifactor authentication |
| SSO | single sign-on |
| SAML | Security Assertion Markup Language |
| PKI | public key infrastructure |
| TLS | Transport Layer Security |
| SSL | Secure Sockets Layer |

### General Technical Acronyms (Well-Known - Skip Expansion)

These are well-established and typically don't need expansion:
- API, URL, HTTP, HTTPS, HTML, CSS, JSON, XML, SQL
- CLI, GUI, OS, VM, IP, TCP, UDP

### Certification Acronyms (Don't Expand)

Cisco certifications are used as-is:
- CCIE, CCNP, CCNA, CCDA
- DevNet Associate, DevNet Professional, DevNet Expert

---

## Third-Party Product Updates

Track rebranding of non-Cisco products referenced in tutorials:

| Old Name | New Name | Effective Date |
|----------|----------|----------------|
| Azure AD | Microsoft Entra ID | 2023 |
| - | - | - |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-02-20 | Initial document creation | Claude Code |
| - | - | - |

---

## How to Request Updates

1. **Editorial Team:** Edit this file directly and commit to main
2. **Authors:** Open an issue with tag `editorial-update`
3. **Automated:** Pipeline will flag unknown products/acronyms for review

---

*This document is the source of truth for product naming in the AI editorial agent.*
