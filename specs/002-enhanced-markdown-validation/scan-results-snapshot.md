# Validation Scan Results Snapshot

**Scan Date**: 2026-02-18 (updated after false positive fixes)
**Tool Version**: clean_markdown.py (FR-1 Enhanced Markdown Validation)

This document captures a point-in-time snapshot of markdown validation issues found in tutorial content. Some tutorials may have been fixed on the UAT side but the source markdown in the repo remains unchanged.

---

## Summary

### Production Tutorials (Full Scan - 138 tutorials)

| Metric | Before Fixes | After Fixes | Change |
|--------|--------------|-------------|--------|
| Total tutorials scanned | 138 | 138 | - |
| Tutorials with blocking issues | 52 | 28 | -46% |
| Total issues | 2,080 | 1,977 | -5% |
| Blocking issues | 308 | 205 | -33% |
| Warnings | 1,772 | 1,772 | - |
| **Blocking rate** | 37.7% | 20.3% | -17pp |
| Clean tutorials | 12 | 18 | +50% |

---

## Issues by Rule

### Production Tutorials (138 tutorials, after fixes)

| Rule | Before Fixes | After Fixes | Change | Severity |
|------|--------------|-------------|--------|----------|
| TRAILING_WHITESPACE | 1,418 | 1,418 | - | WARNING |
| DOUBLE_SPACE | 354 | 354 | - | WARNING |
| HTML_TAG | 125 | 125 | - | BLOCKING |
| CODE_BLOCK_IN_LIST | 145 | 42 | -71% | BLOCKING |
| LINK_NO_SPACE_AFTER | 19 | 19 | - | BLOCKING |
| LINK_NO_SPACE_BEFORE | 80 | 15 | -81% | BLOCKING |
| LINK_BROKEN | 2 | 2 | - | BLOCKING |
| LIST_INDENT_INCONSISTENT | 2 | 2 | - | BLOCKING |

---

## Analysis

### Key Finding: CODE_BLOCK_IN_LIST Dominates

The CODE_BLOCK_IN_LIST rule accounts for **96%** of blocking issues in production tutorials (848 out of 880). This indicates a systemic pattern where authors place code blocks inside numbered/bulleted lists without proper indentation.

**Pattern**: Authors write:
```markdown
1. Do this step
```bash
command here
```
```

**Should be**:
```markdown
1. Do this step

   ```bash
   command here
   ```
```

### Why These Tutorials Work in Production

Many of these tutorials are **live and functional** on Cisco U. despite having blocking issues. This happens because:

1. **UAT-side fixes**: The L&C UAT team may have manually fixed the XML after conversion
2. **Tolerant parser**: Some issues don't actually break the current XML converter
3. **Historical acceptance**: Tutorials submitted before stricter validation was added

### Recommendations

1. **Prioritize AI auto-fix for CODE_BLOCK_IN_LIST**: This single rule would fix 96% of blocking issues
2. **Consider demoting to WARNING**: If these tutorials work in production, CODE_BLOCK_IN_LIST may not actually break XML conversion
3. **Batch remediation**: A one-time cleanup pass could fix all 848 CODE_BLOCK_IN_LIST issues

---

## Tutorials with Blocking Issues

### Test Fixtures (5 tutorials)

| Tutorial | Blocking | Warnings | Issue Types |
|----------|----------|----------|-------------|
| tc-integration-test | 19 | 6 | HTML_TAG, LINK_*, CODE_BLOCK_IN_LIST, LIST_INDENT |
| tc-new | 13 | 138 | CODE_BLOCK_IN_LIST, TRAILING_WHITESPACE |
| tc-presentation-recording | 9 | 0 | CODE_BLOCK_IN_LIST |
| tc-starting-github-actions-copy | 9 | 0 | CODE_BLOCK_IN_LIST |
| tc-llm-start | 2 | 0 | CODE_BLOCK_IN_LIST |

### Production (33 of first 50 tutorials)

<details>
<summary>Click to expand full list</summary>

- tc-802-1x-ibns20
- tc-8k-add-remove-package
- tc-ai-foundation-sec-1
- tc-ai-lm-studio
- tc-ai-vulnerabilities
- tc-appd-aws-lambda-ext
- tc-appd-custom-correlation
- tc-appd-diag-session-dev-monitoring
- tc-appd-health-rules
- tc-appd-information-points
- tc-appd-smart-agents
- tc-arp-spoofing
- tc-beef-basics
- tc-benchmark-rag
- tc-c9800-wpa3-sae
- tc-constructing-an-eem-applet-for-enterprise-automation
- tc-containerize-everything
- tc-convert-config-template
- tc-customize-iot-dashboards
- tc-decoding-the-quantum-stack
- tc-demystifying-static-routing
- tc-deploy-llm-openshift-cpu-vllm
- tc-dns-cache-poisoning
- tc-duo-and-splunk
- tc-ebpf
- tc-ebpf-packet-filtering
- tc-enabling-nci-with-apic
- tc-encrypted-syslog-between-asa-and-splunk
- tc-enhance-stp-with-root-guard
- tc-etherchannel
- tc-flask-restx-rbac
- tc-fmc-rest-with-flask
- tc-ftd-rest-with-flask

</details>

---

## Clean Tutorials (Test Fixtures)

These 22 tutorials passed all validation checks:

- tc-a2
- tc-avocado-test
- tc-broken-link
- tc-cache-check, tc-cache-check2, tc-cache-check3
- tc-d2
- tc-full-demo, tc-full-test
- tc-github-action-test
- tc-image-check
- tc-jira-demo, tc-jira-new, tc-jira-test, tc-jira-test-2
- tc-new-tests
- tc-start-to-finish
- tc-tech-test-1213
- tc-template-test
- tc-whitespace-check
- tc-whole
- tc-work-check

---

## Notes

- This snapshot was taken during FR-1 implementation to establish a baseline
- Production scan was limited to first 50 tutorials (alphabetically) for performance
- Full production scan of 146+ tutorials would likely show similar patterns
- Tutorials marked as "blocking" here may still function if UAT-side fixes were applied
