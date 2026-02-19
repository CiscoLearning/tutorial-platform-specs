# Reference Code - FR-1 Enhanced Markdown Validation

This directory contains snapshots of the key implementation files for reference.
The canonical source is in the `tutorial-testing` repository.

## Files

| File | Description |
|------|-------------|
| `clean_markdown.py` | Main validation tool with detection rules and auto-fix |
| `test_detection_rules.py` | Comprehensive unit tests (38 tests covering edge cases) |
| `integration_test.py` | Integration test runner for full validation pipeline |
| `integration-tests.yml` | GitHub Actions workflow for CI testing |

## Key Functions in clean_markdown.py

### Detection Rules

- `check_html_tags()` - Detects `<br>`, `<p>`, `<div>` etc.
- `check_link_spacing_before()` - Missing space before `[link](url)`
- `check_link_spacing_after()` - Missing space after `[link](url)`
- `check_link_broken()` - Line breaks inside link syntax
- `check_list_indent()` - Inconsistent nested list indentation
- `check_code_block_in_list()` - Code blocks not properly separated from lists
- `check_trailing_whitespace()` - Trailing spaces/tabs
- `check_double_space()` - Double spaces outside code blocks

### Auto-Fix

- `fix_html_tags()` - Replace `<br>` with blank lines
- `fix_link_spacing()` - Add missing spaces around links
- `ai_reformat_markdown()` - AI-powered fix for complex structures

### AI Integration

- OAuth2 authentication with Cisco Chat-AI
- Exponential backoff retry (3 attempts)
- Response validation (URL preservation, content length, code blocks)

## Snapshot Date

2026-02-18 (includes CODE_BLOCK_IN_LIST false positive fix)
