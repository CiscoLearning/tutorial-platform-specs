"""
Enhanced Markdown Validation Tool

Detects markdown patterns that break XML conversion and optionally auto-fixes them.
Part of the CI/CD pipeline for Cisco U. tutorial validation.

Usage:
    python clean_markdown.py [OPTIONS] <folder_path>

Options:
    --no-fix        Disable auto-fix; report issues only
    --json-output   Output results as JSON instead of text
    --verbose       Show detailed processing information
    --strict        Fail on warnings (not just blockers)
"""
import os
import re
import json
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Pattern, Callable
from enum import Enum


# =============================================================================
# Data Classes (T003)
# =============================================================================

class Severity(Enum):
    """Issue severity levels"""
    BLOCKING = "BLOCKING"  # Will definitely break XML conversion
    WARNING = "WARNING"    # May cause issues; recommended to fix


class FixType(Enum):
    """How the issue can be fixed"""
    REGEX = "REGEX"  # Simple regex replacement
    AI = "AI"        # Requires AI reformatting
    MANUAL = "MANUAL"  # Cannot be auto-fixed


@dataclass
class ValidationRule:
    """Defines a single validation rule"""
    id: str
    pattern: Optional[Pattern] = None  # None for stateful checks
    severity: Severity = Severity.BLOCKING
    message_template: str = ""
    fix_suggestion: str = ""
    auto_fixable: bool = False
    fix_type: FixType = FixType.MANUAL
    check_function: Optional[Callable] = None  # For stateful checks


@dataclass
class ValidationIssue:
    """Represents a single issue found during validation"""
    rule_id: str
    file_path: str
    line_number: int
    message: str
    severity: Severity
    match: str = ""
    column: int = 0
    fixed: bool = False
    original_text: str = ""
    fixed_text: str = ""
    fix_suggestion: str = ""


@dataclass
class ValidationResult:
    """Aggregated result from validating one or more files"""
    issues: List[ValidationIssue] = field(default_factory=list)
    blocking_count: int = 0
    warning_count: int = 0
    files_scanned: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    auto_fix_enabled: bool = True
    summary: str = ""

    def add_issue(self, issue: ValidationIssue):
        """Add an issue and update counts"""
        self.issues.append(issue)
        if issue.severity == Severity.BLOCKING:
            self.blocking_count += 1
        else:
            self.warning_count += 1

    def has_blocking_issues(self) -> bool:
        """Check if there are any unfixed blocking issues"""
        return any(
            i.severity == Severity.BLOCKING and not i.fixed
            for i in self.issues
        )


# =============================================================================
# Validation Rules Registry
# =============================================================================

# Regex patterns for detection
HTML_TAG_PATTERN = re.compile(r'<(br|p|div|span|hr|img)([^>]*)/?>', re.IGNORECASE)
# Exclude images (!) from "missing space before link" detection
# Exclude: whitespace, ! (images), ( (parenthetical links), * (bold links)
LINK_NO_SPACE_BEFORE_PATTERN = re.compile(r'[^\s!(*]\[[^\]]+\]\([^)]+\)')
# Exclude: whitespace, punctuation, ), ], }, *, _ (markdown), ' (possessive)
LINK_NO_SPACE_AFTER_PATTERN = re.compile(r'\[[^\]]+\]\([^)]+\)[^\s\.\,\!\?\;\:\)\]\}\*\_\']')
LINK_BROKEN_PATTERN = re.compile(r'\[[^\]]*\n[^\]]*\]\([^)]*\)', re.MULTILINE)
TRAILING_WHITESPACE_PATTERN = re.compile(r'[ \t]+$', re.MULTILINE)
DOUBLE_SPACE_PATTERN = re.compile(r'(?<=\S) {2,}(?=\S)')

# Rule definitions
RULES: List[ValidationRule] = [
    ValidationRule(
        id="HTML_TAG",
        pattern=HTML_TAG_PATTERN,
        severity=Severity.BLOCKING,
        message_template="Line {line}: HTML tag `{match}` will break XML conversion.",
        fix_suggestion="Use blank line for paragraph breaks instead of <br>. Remove HTML tags.",
        auto_fixable=True,
        fix_type=FixType.REGEX,
    ),
    ValidationRule(
        id="LINK_NO_SPACE_BEFORE",
        pattern=LINK_NO_SPACE_BEFORE_PATTERN,
        severity=Severity.BLOCKING,
        message_template="Line {line}: Link is missing space before it: `{match}`",
        fix_suggestion="Add a space before the opening bracket [.",
        auto_fixable=True,
        fix_type=FixType.REGEX,
    ),
    ValidationRule(
        id="LINK_NO_SPACE_AFTER",
        pattern=LINK_NO_SPACE_AFTER_PATTERN,
        severity=Severity.BLOCKING,
        message_template="Line {line}: Link is missing space after it: `{match}`",
        fix_suggestion="Add a space after the closing parenthesis ).",
        auto_fixable=True,
        fix_type=FixType.REGEX,
    ),
    ValidationRule(
        id="LINK_BROKEN",
        pattern=LINK_BROKEN_PATTERN,
        severity=Severity.BLOCKING,
        message_template="Lines {line}: Link syntax broken by line break: `{match}`",
        fix_suggestion="Remove the line break inside the link text.",
        auto_fixable=True,
        fix_type=FixType.AI,
    ),
    ValidationRule(
        id="LIST_INDENT_INCONSISTENT",
        pattern=None,  # Stateful check
        severity=Severity.BLOCKING,
        message_template="Lines {line}: Nested list has inconsistent indentation.",
        fix_suggestion="Use consistent 2 or 4 space indentation for nested list items.",
        auto_fixable=True,
        fix_type=FixType.AI,
    ),
    ValidationRule(
        id="CODE_BLOCK_IN_LIST",
        pattern=None,  # Stateful check
        severity=Severity.BLOCKING,
        message_template="Line {line}: Code block in list not properly indented.",
        fix_suggestion="Indent the code block to align with the list item content.",
        auto_fixable=True,
        fix_type=FixType.AI,
    ),
    ValidationRule(
        id="TRAILING_WHITESPACE",
        pattern=TRAILING_WHITESPACE_PATTERN,
        severity=Severity.WARNING,
        message_template="Line {line}: Trailing whitespace detected.",
        fix_suggestion="Remove trailing spaces and tabs.",
        auto_fixable=True,
        fix_type=FixType.REGEX,
    ),
    ValidationRule(
        id="DOUBLE_SPACE",
        pattern=DOUBLE_SPACE_PATTERN,
        severity=Severity.WARNING,
        message_template="Line {line}: Double space detected: `{match}`",
        fix_suggestion="Replace multiple spaces with a single space.",
        auto_fixable=True,
        fix_type=FixType.REGEX,
    ),
]

# Build lookup dictionary
RULES_BY_ID = {rule.id: rule for rule in RULES}


# =============================================================================
# Detection Functions
# =============================================================================

def is_in_code_block(lines: List[str], line_idx: int) -> bool:
    """Check if a line is inside a code block"""
    in_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_block = not in_block
        if i == line_idx:
            return in_block
    return False


def is_in_inline_code(line: str, match_start: int) -> bool:
    """Check if a position is inside inline code (backticks)"""
    # Count backticks before the position
    backtick_count = line[:match_start].count('`')
    return backtick_count % 2 == 1


def check_html_tags(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for HTML tags that break XML conversion (T014)"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["HTML_TAG"]

    for line_num, line in enumerate(lines, 1):
        # Skip if in code block
        if is_in_code_block(lines, line_num - 1):
            continue

        for match in rule.pattern.finditer(line):
            # Skip if in inline code
            if is_in_inline_code(line, match.start()):
                continue

            issues.append(ValidationIssue(
                rule_id=rule.id,
                file_path=file_path,
                line_number=line_num,
                message=rule.message_template.format(line=line_num, match=match.group()),
                severity=rule.severity,
                match=match.group(),
                column=match.start(),
                original_text=line,
                fix_suggestion=rule.fix_suggestion,
            ))

    return issues


def check_link_spacing_before(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for links missing space before them (T015)"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["LINK_NO_SPACE_BEFORE"]

    for line_num, line in enumerate(lines, 1):
        if is_in_code_block(lines, line_num - 1):
            continue

        for match in rule.pattern.finditer(line):
            # Skip if at start of line
            if match.start() == 0:
                continue
            # The pattern includes the char before [, so check if it's not whitespace
            char_before = line[match.start()]
            if not char_before.isspace():
                issues.append(ValidationIssue(
                    rule_id=rule.id,
                    file_path=file_path,
                    line_number=line_num,
                    message=rule.message_template.format(line=line_num, match=match.group()),
                    severity=rule.severity,
                    match=match.group(),
                    column=match.start(),
                    original_text=line,
                    fix_suggestion=rule.fix_suggestion,
                ))

    return issues


def check_link_spacing_after(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for links missing space after them (T016)"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["LINK_NO_SPACE_AFTER"]

    for line_num, line in enumerate(lines, 1):
        if is_in_code_block(lines, line_num - 1):
            continue

        for match in rule.pattern.finditer(line):
            issues.append(ValidationIssue(
                rule_id=rule.id,
                file_path=file_path,
                line_number=line_num,
                message=rule.message_template.format(line=line_num, match=match.group()),
                severity=rule.severity,
                match=match.group(),
                column=match.start(),
                original_text=line,
                fix_suggestion=rule.fix_suggestion,
            ))

    return issues


def check_link_broken(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for broken links (line breaks inside link syntax) (T017)"""
    issues = []
    rule = RULES_BY_ID["LINK_BROKEN"]

    for match in rule.pattern.finditer(content):
        # Find line number of the match
        line_num = content[:match.start()].count('\n') + 1

        issues.append(ValidationIssue(
            rule_id=rule.id,
            file_path=file_path,
            line_number=line_num,
            message=rule.message_template.format(line=line_num, match=match.group()[:50] + "..."),
            severity=rule.severity,
            match=match.group(),
            original_text=match.group(),
            fix_suggestion=rule.fix_suggestion,
        ))

    return issues


def check_list_indent(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for inconsistent nested list indentation (T018)"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["LIST_INDENT_INCONSISTENT"]

    # Track indentation levels within a list
    list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s')
    indent_stack = []
    in_list = False
    list_start_line = 0
    issue_detected = False
    issue_line = 0

    for line_num, line in enumerate(lines, 1):
        if is_in_code_block(lines, line_num - 1):
            continue

        match = list_pattern.match(line)
        if match:
            indent = len(match.group(1))

            if not in_list:
                in_list = True
                list_start_line = line_num
                indent_stack = [indent]
                issue_detected = False
            else:
                # Check for inconsistent indentation
                if indent > indent_stack[-1]:
                    # Going deeper - check increment consistency
                    increment = indent - indent_stack[-1]
                    if len(indent_stack) > 1:
                        prev_increment = indent_stack[-1] - indent_stack[-2] if len(indent_stack) > 1 else increment
                        if increment != prev_increment and increment not in [2, 4]:
                            issue_detected = True
                            issue_line = line_num
                    indent_stack.append(indent)
                elif indent < indent_stack[-1]:
                    # Going back up
                    while indent_stack and indent_stack[-1] > indent:
                        indent_stack.pop()
                    if indent not in indent_stack:
                        indent_stack.append(indent)
        else:
            # Non-list line - if blank, end list and capture full block if issue found
            if not line.strip():
                if in_list and issue_detected:
                    # Capture the entire list block for AI to fix
                    list_end_line = line_num - 1
                    list_block = '\n'.join(lines[list_start_line - 1:list_end_line])
                    issues.append(ValidationIssue(
                        rule_id=rule.id,
                        file_path=file_path,
                        line_number=issue_line,
                        message=rule.message_template.format(line=f"{list_start_line}-{list_end_line}"),
                        severity=rule.severity,
                        match=lines[issue_line - 1].strip() if issue_line > 0 else "",
                        original_text=list_block,
                        fix_suggestion=rule.fix_suggestion,
                    ))
                in_list = False
                indent_stack = []
                issue_detected = False

    # Handle list at end of file
    if in_list and issue_detected:
        list_block = '\n'.join(lines[list_start_line - 1:])
        issues.append(ValidationIssue(
            rule_id=rule.id,
            file_path=file_path,
            line_number=issue_line,
            message=rule.message_template.format(line=f"{list_start_line}-{len(lines)}"),
            severity=rule.severity,
            match=lines[issue_line - 1].strip() if issue_line > 0 else "",
            original_text=list_block,
            fix_suggestion=rule.fix_suggestion,
        ))

    return issues


def check_code_block_in_list(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for improperly indented code blocks in lists (T019)

    Only flags code blocks that appear WITHIN a list context without proper
    blank line separation. A blank line after a list item "breaks" the list
    context in standard markdown.
    """
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["CODE_BLOCK_IN_LIST"]

    list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s')
    in_list = False
    list_indent = 0
    list_item_start = 0
    blank_line_seen = False  # Track if we've seen a blank line after list content

    for line_num, line in enumerate(lines, 1):
        # Skip lines inside code blocks - they may contain list-like syntax
        if is_in_code_block(lines, line_num - 1):
            continue

        list_match = list_pattern.match(line)
        if list_match:
            in_list = True
            list_indent = len(list_match.group(1))
            list_item_start = line_num
            blank_line_seen = False  # Reset - we're in active list content
        elif not line.strip():
            # Blank line - if we're in a list, this might end the list context
            if in_list:
                blank_line_seen = True
        elif in_list and blank_line_seen and not line.startswith(' '):
            # Non-indented content after blank line = list has ended
            in_list = False
            blank_line_seen = False
        elif line.strip().startswith('```') and in_list and not blank_line_seen:
            # Code block marker - check if properly indented
            code_indent = len(line) - len(line.lstrip())
            if code_indent <= list_indent:
                # Find the end of this code block
                code_block_end = line_num
                for i in range(line_num, len(lines)):
                    if i > line_num - 1 and lines[i].strip().startswith('```'):
                        code_block_end = i + 1
                        break

                # Capture list item + entire code block for AI to fix
                block_start = list_item_start - 1
                block_end = code_block_end
                original_block = '\n'.join(lines[block_start:block_end])

                issues.append(ValidationIssue(
                    rule_id=rule.id,
                    file_path=file_path,
                    line_number=line_num,
                    message=rule.message_template.format(line=line_num),
                    severity=rule.severity,
                    match=line.strip(),
                    original_text=original_block,
                    fix_suggestion=rule.fix_suggestion,
                ))

    return issues


def check_trailing_whitespace(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for trailing whitespace"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["TRAILING_WHITESPACE"]

    for line_num, line in enumerate(lines, 1):
        if is_in_code_block(lines, line_num - 1):
            continue

        if rule.pattern.search(line):
            issues.append(ValidationIssue(
                rule_id=rule.id,
                file_path=file_path,
                line_number=line_num,
                message=rule.message_template.format(line=line_num),
                severity=rule.severity,
                original_text=line,
                fix_suggestion=rule.fix_suggestion,
            ))

    return issues


def check_double_space(content: str, file_path: str = "") -> List[ValidationIssue]:
    """Check for double spaces"""
    issues = []
    lines = content.split('\n')
    rule = RULES_BY_ID["DOUBLE_SPACE"]

    for line_num, line in enumerate(lines, 1):
        if is_in_code_block(lines, line_num - 1):
            continue

        for match in rule.pattern.finditer(line):
            issues.append(ValidationIssue(
                rule_id=rule.id,
                file_path=file_path,
                line_number=line_num,
                message=rule.message_template.format(line=line_num, match=match.group()),
                severity=rule.severity,
                match=match.group(),
                column=match.start(),
                original_text=line,
                fix_suggestion=rule.fix_suggestion,
            ))

    return issues


# =============================================================================
# Auto-Fix Functions (T030-T033)
# =============================================================================

def fix_trailing_whitespace(content: str) -> tuple[str, int]:
    """
    Remove trailing whitespace from all lines (T030).

    Returns:
        Tuple of (fixed_content, number_of_fixes)
    """
    lines = content.split('\n')
    fixed_lines = []
    fix_count = 0

    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        if not in_code_block and line != line.rstrip():
            fixed_lines.append(line.rstrip())
            fix_count += 1
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), fix_count


def fix_double_space(content: str) -> tuple[str, int]:
    """
    Replace double/multiple spaces with single space (T031).
    Only fixes spaces in middle of text, not leading whitespace.

    Returns:
        Tuple of (fixed_content, number_of_fixes)
    """
    lines = content.split('\n')
    fixed_lines = []
    fix_count = 0

    in_code_block = False
    double_space_pattern = re.compile(r'(?<=\S) {2,}(?=\S)')

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        if not in_code_block:
            matches = list(double_space_pattern.finditer(line))
            if matches:
                fix_count += len(matches)
                line = double_space_pattern.sub(' ', line)

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fix_count


def fix_html_tags(content: str) -> tuple[str, int]:
    """
    Fix HTML tags that break XML conversion (T032).
    - Replace <br> and <br/> with blank line
    - Remove other common HTML tags

    Returns:
        Tuple of (fixed_content, number_of_fixes)
    """
    lines = content.split('\n')
    fixed_lines = []
    fix_count = 0

    in_code_block = False
    br_pattern = re.compile(r'<br\s*/?>', re.IGNORECASE)
    other_html_pattern = re.compile(r'<(p|div|span|hr)([^>]*)/?>', re.IGNORECASE)
    closing_tag_pattern = re.compile(r'</(p|div|span)>', re.IGNORECASE)
    img_pattern = re.compile(r'<img[^>]*/?>', re.IGNORECASE)

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        if not in_code_block:
            original_line = line

            # Replace <br> with newline marker (will become blank line)
            if br_pattern.search(line):
                line = br_pattern.sub('\n', line)
                fix_count += 1

            # Remove other HTML tags
            for pattern in [other_html_pattern, closing_tag_pattern, img_pattern]:
                if pattern.search(line):
                    line = pattern.sub('', line)
                    fix_count += 1

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fix_count


def fix_link_spacing(content: str) -> tuple[str, int]:
    """
    Fix missing spaces around links (T033).
    - Add space before [link] if preceded by non-space
    - Add space after (url) if followed by non-space/non-punctuation

    Returns:
        Tuple of (fixed_content, number_of_fixes)
    """
    lines = content.split('\n')
    fixed_lines = []
    fix_count = 0

    in_code_block = False
    # Match link preceded by non-space (capture the char before)
    before_pattern = re.compile(r'(\S)(\[[^\]]+\]\([^)]+\))')
    # Match link followed by non-space/non-punctuation
    after_pattern = re.compile(r'(\[[^\]]+\]\([^)]+\))([^\s\.\,\!\?\;\:\)\]\}])')

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block

        if not in_code_block:
            # Fix missing space before link
            if before_pattern.search(line):
                line = before_pattern.sub(r'\1 \2', line)
                fix_count += 1

            # Fix missing space after link
            if after_pattern.search(line):
                line = after_pattern.sub(r'\1 \2', line)
                fix_count += 1

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fix_count


def fix_broken_link(content: str) -> tuple[str, int]:
    """
    Fix broken links with line breaks inside (T017 fix).
    Removes line breaks from within link text.

    Returns:
        Tuple of (fixed_content, number_of_fixes)
    """
    fix_count = 0
    broken_link_pattern = re.compile(r'\[([^\]]*)\n([^\]]*)\]\(([^)]*)\)', re.MULTILINE)

    while broken_link_pattern.search(content):
        content = broken_link_pattern.sub(r'[\1 \2](\3)', content)
        fix_count += 1

    return content, fix_count


def apply_regex_fixes(content: str, skip_ai: bool = False) -> tuple[str, list[tuple[str, int]]]:
    """
    Apply all regex-based auto-fixes to content.

    Args:
        content: The markdown content to fix
        skip_ai: If True, only apply regex fixes (for [no-ai-fix] flag)

    Returns:
        Tuple of (fixed_content, list of (rule_id, fix_count) tuples)
    """
    fixes_applied = []

    # Apply regex fixes in order
    content, count = fix_trailing_whitespace(content)
    if count > 0:
        fixes_applied.append(("TRAILING_WHITESPACE", count))

    content, count = fix_double_space(content)
    if count > 0:
        fixes_applied.append(("DOUBLE_SPACE", count))

    content, count = fix_html_tags(content)
    if count > 0:
        fixes_applied.append(("HTML_TAG", count))

    content, count = fix_link_spacing(content)
    if count > 0:
        fixes_applied.append(("LINK_SPACING", count))

    content, count = fix_broken_link(content)
    if count > 0:
        fixes_applied.append(("LINK_BROKEN", count))

    return content, fixes_applied


# =============================================================================
# AI-Powered Fixes (T035-T041)
# =============================================================================

import base64
import time
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# AI configuration
AI_CLIENT_ID = os.environ.get("CLIENT_ID")
AI_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
AI_APP_KEY = os.environ.get("APP_KEY")
AI_OAUTH_URL = "https://id.cisco.com/oauth2/default/v1/token"
AI_LLM_URL = "https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini/chat/completions"


def get_ai_access_token() -> Optional[str]:
    """
    Get OAuth2 access token for AI API.

    Returns:
        Access token string, or None if authentication fails
    """
    if not HAS_REQUESTS:
        return None

    if not AI_CLIENT_ID or not AI_CLIENT_SECRET:
        return None

    try:
        payload = "grant_type=client_credentials"
        credentials = base64.b64encode(
            f'{AI_CLIENT_ID}:{AI_CLIENT_SECRET}'.encode('utf-8')
        ).decode('utf-8')

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}"
        }

        response = requests.post(AI_OAUTH_URL, headers=headers, data=payload, timeout=30)
        response.raise_for_status()

        token_data = response.json()
        return token_data.get('access_token')

    except Exception:
        return None


def ai_reformat_markdown(
    content: str,
    issue_type: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    verbose: bool = False
) -> Optional[str]:
    """
    Use AI to reformat markdown content (T035-T036).

    Args:
        content: The problematic markdown section
        issue_type: Type of issue (LIST_INDENT_INCONSISTENT, CODE_BLOCK_IN_LIST)
        max_retries: Maximum number of retry attempts
        base_delay: Base delay for exponential backoff
        verbose: Whether to print debug info

    Returns:
        Reformatted content, or None if AI fails
    """
    if verbose:
        print(f"  🤖 Attempting AI fix for {issue_type}...")

    if not HAS_REQUESTS:
        if verbose:
            print("  ⚠️ AI fix skipped: requests library not available")
        return None

    token = get_ai_access_token()
    if not token:
        if verbose:
            print("  ⚠️ AI fix skipped: Could not get access token (check CLIENT_ID/CLIENT_SECRET)")
        return None

    if verbose:
        print(f"  ✓ Got AI access token, sending request...")

    # Build prompt based on issue type
    if issue_type == "LIST_INDENT_INCONSISTENT":
        prompt = f"""Fix the indentation of this nested markdown list to use consistent 2-space indentation.
Only fix the indentation - do not change the content, links, or formatting otherwise.
Return ONLY the fixed markdown, no explanation.

{content}"""
    elif issue_type == "CODE_BLOCK_IN_LIST":
        prompt = f"""Fix this markdown so the code block is properly indented within the list.
The code block should be indented to align with the list item content (2 spaces).
Return ONLY the fixed markdown, no explanation.

{content}"""
    else:
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": token
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a markdown formatting assistant. Fix formatting issues and return only the corrected markdown."},
            {"role": "user", "content": prompt}
        ],
        "user": json.dumps({"appkey": AI_APP_KEY}) if AI_APP_KEY else "{}",
        "stop": ["<|im_end|>"]
    }

    # Retry with exponential backoff (T036)
    for attempt in range(max_retries):
        try:
            response = requests.post(
                AI_LLM_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 401 and attempt < max_retries - 1:
                # Token expired, get new token and retry
                token = get_ai_access_token()
                if token:
                    headers['api-key'] = token
                    continue

            response.raise_for_status()

            data = response.json()
            reformatted = data['choices'][0]['message']['content']

            # Validate AI response (T037)
            if validate_ai_response(content, reformatted):
                if verbose:
                    print(f"  ✅ AI fix successful!")
                return reformatted
            else:
                if verbose:
                    print(f"  ⚠️ AI response failed validation")
                return None  # T039: Reject invalid response

        except Exception as e:
            if verbose:
                print(f"  ⚠️ AI request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                # Exponential backoff
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                if verbose:
                    print(f"  ❌ AI fix failed after {max_retries} attempts")
                return None  # T038: All retries exhausted

    return None


def validate_ai_response(original: str, reformatted: str) -> bool:
    """
    Validate AI response for correctness (T037).

    Checks:
    - URLs are preserved
    - Content length is within ±20%
    - Code blocks are unchanged

    Returns:
        True if response is valid, False otherwise
    """
    if not reformatted:
        return False

    # Check content length (±20%)
    original_len = len(original)
    reformatted_len = len(reformatted)
    if original_len > 0:
        ratio = reformatted_len / original_len
        if ratio < 0.8 or ratio > 1.2:
            return False

    # Check URLs are preserved
    url_pattern = re.compile(r'https?://[^\s\)]+')
    original_urls = set(url_pattern.findall(original))
    reformatted_urls = set(url_pattern.findall(reformatted))
    if original_urls != reformatted_urls:
        return False

    # Check code blocks are preserved
    code_block_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
    original_blocks = code_block_pattern.findall(original)
    reformatted_blocks = code_block_pattern.findall(reformatted)

    # Code block content should match (ignoring leading whitespace)
    def normalize_block(block):
        lines = block.split('\n')
        return '\n'.join(line.strip() for line in lines)

    original_normalized = [normalize_block(b) for b in original_blocks]
    reformatted_normalized = [normalize_block(b) for b in reformatted_blocks]

    if original_normalized != reformatted_normalized:
        return False

    return True


# =============================================================================
# Commit Message Flag Detection (T042-T043)
# =============================================================================

def parse_commit_flags(commit_message: str) -> dict:
    """
    Parse commit message for auto-fix control flags.

    Flags:
    - [no-autofix]: Skip all auto-fixes
    - [no-ai-fix]: Skip AI fixes, allow regex fixes

    Returns:
        Dict with 'skip_all_fixes' and 'skip_ai_fixes' booleans
    """
    flags = {
        'skip_all_fixes': False,
        'skip_ai_fixes': False
    }

    if not commit_message:
        return flags

    commit_lower = commit_message.lower()

    if '[no-autofix]' in commit_lower:
        flags['skip_all_fixes'] = True

    if '[no-ai-fix]' in commit_lower:
        flags['skip_ai_fixes'] = True

    return flags


# =============================================================================
# PR Comment Generation (T044-T045)
# =============================================================================

def generate_pr_comment(result: ValidationResult, fixes_applied: list) -> str:
    """
    Generate PR comment body with before/after diffs (T044).

    Args:
        result: ValidationResult with issues found
        fixes_applied: List of (file_path, rule_id, original, fixed) tuples

    Returns:
        Markdown-formatted PR comment
    """
    lines = []

    # Header
    lines.append("## Markdown Validation Report")
    lines.append("")

    # Summary
    if result.has_blocking_issues():
        lines.append("**Status:** :x: Blocking issues found")
    elif result.warning_count > 0:
        lines.append("**Status:** :warning: Warnings found")
    else:
        lines.append("**Status:** :white_check_mark: All checks passed")

    lines.append("")
    lines.append(f"- **Blocking issues:** {result.blocking_count}")
    lines.append(f"- **Warnings:** {result.warning_count}")
    lines.append(f"- **Files scanned:** {len(result.files_scanned)}")
    lines.append(f"- **Files modified:** {len(result.files_modified)}")
    lines.append("")

    # Auto-fix details
    if fixes_applied:
        lines.append("### Auto-Fixes Applied")
        lines.append("")

        for file_path, rule_id, original, fixed in fixes_applied:
            lines.append(f"**{os.path.basename(file_path)}** - {rule_id}")
            lines.append("")
            lines.append("<details>")
            lines.append("<summary>View diff</summary>")
            lines.append("")
            lines.append("```diff")
            for orig_line in original.split('\n')[:5]:  # Limit to 5 lines
                lines.append(f"- {orig_line}")
            for fix_line in fixed.split('\n')[:5]:
                lines.append(f"+ {fix_line}")
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    # Issues that weren't auto-fixed
    unfixed_blocking = [i for i in result.issues if i.severity == Severity.BLOCKING and not i.fixed]
    if unfixed_blocking:
        lines.append("### Remaining Blocking Issues")
        lines.append("")
        for issue in unfixed_blocking[:10]:  # Limit to 10
            lines.append(f"- **{os.path.basename(issue.file_path)}:{issue.line_number}** - {issue.message}")
            if issue.fix_suggestion:
                lines.append(f"  - Fix: {issue.fix_suggestion}")
        lines.append("")

    # Footer with opt-out instructions (T045)
    lines.append("---")
    lines.append("")
    lines.append("**Opt-out Options:**")
    lines.append("- Add `[no-autofix]` to your commit message to disable all auto-fixes")
    lines.append("- Add `[no-ai-fix]` to disable AI-powered fixes (regex fixes still apply)")
    lines.append("")
    lines.append("*This check is powered by the Enhanced Markdown Validation tool.*")

    return '\n'.join(lines)


# =============================================================================
# Main Validation Functions
# =============================================================================

def validate_file(file_path: str, auto_fix: bool = True, skip_ai: bool = False, verbose: bool = False) -> ValidationResult:
    """
    Validate a single markdown file for all rules.

    Args:
        file_path: Path to the markdown file
        auto_fix: Whether to apply auto-fixes (default True)
        skip_ai: Whether to skip AI-powered fixes (default False)
        verbose: Whether to print debug info (default False)

    Returns:
        ValidationResult with all issues found
    """
    result = ValidationResult(auto_fix_enabled=auto_fix)
    result.files_scanned.append(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        result.add_issue(ValidationIssue(
            rule_id="FILE_ERROR",
            file_path=file_path,
            line_number=0,
            message=f"Could not read file: {e}",
            severity=Severity.BLOCKING,
        ))
        return result

    content = original_content
    file_modified = False

    # Apply regex-based auto-fixes first if enabled
    if auto_fix:
        content, fixes_applied = apply_regex_fixes(content, skip_ai=skip_ai)
        if fixes_applied:
            file_modified = True
            # Mark corresponding issues as fixed
            for rule_id, count in fixes_applied:
                result.add_issue(ValidationIssue(
                    rule_id=rule_id,
                    file_path=file_path,
                    line_number=0,
                    message=f"Auto-fixed {count} {rule_id} issue(s)",
                    severity=Severity.WARNING,
                    fixed=True,
                ))

    # Run all detection checks on (potentially fixed) content
    all_issues = []
    all_issues.extend(check_html_tags(content, file_path))
    all_issues.extend(check_link_spacing_before(content, file_path))
    all_issues.extend(check_link_spacing_after(content, file_path))
    all_issues.extend(check_link_broken(content, file_path))
    all_issues.extend(check_list_indent(content, file_path))
    all_issues.extend(check_code_block_in_list(content, file_path))
    all_issues.extend(check_trailing_whitespace(content, file_path))
    all_issues.extend(check_double_space(content, file_path))

    # Apply AI fixes for complex issues if enabled
    if auto_fix and not skip_ai:
        for issue in all_issues:
            if issue.rule_id in ["LIST_INDENT_INCONSISTENT", "CODE_BLOCK_IN_LIST"]:
                if not issue.original_text:
                    if verbose:
                        print(f"  ⚠️ No original_text captured for {issue.rule_id} at line {issue.line_number}")
                    continue
                # Try AI reformatting for this section
                reformatted = ai_reformat_markdown(
                    issue.original_text,
                    issue.rule_id,
                    verbose=verbose
                )
                if reformatted:
                    content = content.replace(issue.original_text, reformatted)
                    issue.fixed = True
                    issue.fixed_text = reformatted
                    file_modified = True

    # Add all remaining issues to result
    for issue in all_issues:
        result.add_issue(issue)

    # Write fixed content back to file if modified
    if file_modified and content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            result.files_modified.append(file_path)
        except Exception as e:
            result.add_issue(ValidationIssue(
                rule_id="WRITE_ERROR",
                file_path=file_path,
                line_number=0,
                message=f"Could not write fixed file: {e}",
                severity=Severity.WARNING,
            ))

    # Generate summary
    result.summary = generate_summary(result)

    return result


def validate_folder(folder_path: str, auto_fix: bool = True, skip_ai: bool = False, verbose: bool = False) -> ValidationResult:
    """
    Validate all markdown files in a folder.

    Args:
        folder_path: Path to the folder containing markdown files
        auto_fix: Whether to apply auto-fixes
        skip_ai: Whether to skip AI-powered fixes
        verbose: Whether to print debug info

    Returns:
        ValidationResult with all issues found
    """
    result = ValidationResult(auto_fix_enabled=auto_fix)

    if not os.path.isdir(folder_path):
        result.add_issue(ValidationIssue(
            rule_id="FOLDER_ERROR",
            file_path=folder_path,
            line_number=0,
            message=f"Folder not found: {folder_path}",
            severity=Severity.BLOCKING,
        ))
        return result

    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            file_result = validate_file(file_path, auto_fix, skip_ai, verbose)

            # Merge results
            result.issues.extend(file_result.issues)
            result.blocking_count += file_result.blocking_count
            result.warning_count += file_result.warning_count
            result.files_scanned.extend(file_result.files_scanned)
            result.files_modified.extend(file_result.files_modified)

    result.summary = generate_summary(result)
    return result


def generate_summary(result: ValidationResult) -> str:
    """Generate a human-readable summary"""
    lines = []

    if not result.issues:
        lines.append("No markdown issues found!")
        return '\n'.join(lines)

    lines.append(f"Found {len(result.issues)} issue(s):")
    lines.append(f"  - BLOCKING: {result.blocking_count}")
    lines.append(f"  - WARNING: {result.warning_count}")

    if result.files_modified:
        lines.append(f"Files modified: {', '.join(result.files_modified)}")

    return '\n'.join(lines)


# =============================================================================
# Output Formatting
# =============================================================================

# ANSI color codes for terminal output (T056)
class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def format_text_output(result: ValidationResult, verbose: bool = False, use_color: bool = True) -> str:
    """Format validation result as human-readable text with color coding (T056)"""
    lines = []

    # Determine if terminal supports color
    import sys
    if not use_color or not sys.stdout.isatty():
        # No color codes
        red = yellow = green = reset = bold = ""
    else:
        red = Colors.RED
        yellow = Colors.YELLOW
        green = Colors.GREEN
        reset = Colors.RESET
        bold = Colors.BOLD

    if not result.issues:
        lines.append(f"{green}No markdown issues found!{reset}")
        return '\n'.join(lines)

    # Group issues by severity
    blocking = [i for i in result.issues if i.severity == Severity.BLOCKING]
    warnings = [i for i in result.issues if i.severity == Severity.WARNING]

    if blocking:
        lines.append(f"\n{bold}{red}BLOCKING:{reset}")
        for issue in blocking:
            fixed_marker = f" {green}[FIXED]{reset}" if issue.fixed else ""
            lines.append(f"  {red}●{reset} {issue.message}{fixed_marker}")
            if verbose and issue.fix_suggestion:
                lines.append(f"    → {issue.fix_suggestion}")

    if warnings:
        lines.append(f"\n{bold}{yellow}WARNING:{reset}")
        for issue in warnings:
            fixed_marker = f" {green}[FIXED]{reset}" if issue.fixed else ""
            lines.append(f"  {yellow}●{reset} {issue.message}{fixed_marker}")
            if verbose and issue.fix_suggestion:
                lines.append(f"    → {issue.fix_suggestion}")

    lines.append("")
    lines.append(result.summary)

    return '\n'.join(lines)


def format_json_output(result: ValidationResult) -> str:
    """Format validation result as JSON"""
    return json.dumps({
        "success": not result.has_blocking_issues(),
        "blocking_count": result.blocking_count,
        "warning_count": result.warning_count,
        "issues": [
            {
                "rule_id": i.rule_id,
                "file": i.file_path,
                "line": i.line_number,
                "severity": i.severity.value,
                "message": i.message,
                "fixed": i.fixed,
                "original": i.original_text,
                "fixed_text": i.fixed_text,
            }
            for i in result.issues
        ],
        "files_scanned": result.files_scanned,
        "files_modified": result.files_modified,
        "auto_fix_enabled": result.auto_fix_enabled,
    }, indent=2)


# =============================================================================
# CLI Interface
# =============================================================================

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Validate markdown files for XML conversion compatibility"
    )
    parser.add_argument(
        "folder_path",
        nargs="?",
        default=os.environ.get("FOLDER_NAME"),
        help="Path to folder containing markdown files"
    )
    parser.add_argument(
        "--no-fix",
        action="store_true",
        help="Disable auto-fix; report issues only"
    )
    parser.add_argument(
        "--no-ai-fix",
        action="store_true",
        help="Disable AI-powered fixes (regex fixes still apply)"
    )
    parser.add_argument(
        "--commit-message",
        type=str,
        default=os.environ.get("COMMIT_MESSAGE", ""),
        help="Commit message to check for [no-autofix] or [no-ai-fix] flags"
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings (not just blockers)"
    )
    parser.add_argument(
        "--pr-comment",
        action="store_true",
        help="Output PR comment format instead of plain text"
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()

    if not args.folder_path:
        print("Error: No folder path provided. Set FOLDER_NAME environment variable or pass as argument.")
        exit(2)

    # Parse commit message for flags (T042-T043)
    commit_flags = parse_commit_flags(args.commit_message)

    # Determine auto-fix behavior
    auto_fix = not args.no_fix and not commit_flags['skip_all_fixes']
    skip_ai = args.no_ai_fix or commit_flags['skip_ai_fixes']

    result = validate_folder(args.folder_path, auto_fix=auto_fix, skip_ai=skip_ai, verbose=args.verbose)

    # Output results
    if args.pr_comment:
        # Generate PR comment format
        fixes_applied = []  # Would need to track these during validation
        print(generate_pr_comment(result, fixes_applied))
    elif args.json_output:
        print(format_json_output(result))
    else:
        print(format_text_output(result, verbose=args.verbose))

    # Determine exit code
    if result.has_blocking_issues():
        exit(1)
    elif args.strict and result.warning_count > 0:
        exit(1)
    else:
        exit(0)


# Legacy function for backwards compatibility
def clean_markdown_file(file_path):
    """
    Legacy function - wraps new validation system.
    Returns (modified, changed_lines) tuple for compatibility.
    """
    result = validate_file(file_path, auto_fix=False)
    changed_lines = [i.line_number for i in result.issues]
    return bool(result.issues), changed_lines


def clean_folder(folder_path, log_path="whitespace_report.txt"):
    """
    Legacy function - wraps new validation system.
    Logs issues to file for compatibility.
    """
    result = validate_folder(folder_path, auto_fix=False)

    if result.issues:
        with open(log_path, 'a') as log:
            log.write("Markdown validation issues found:\n")
            for issue in result.issues:
                log.write(f"[{issue.severity.value}] {issue.file_path}:{issue.line_number} - {issue.message}\n")
        print(f"Issues logged in {log_path}")
    else:
        print("No markdown issues found.")


if __name__ == "__main__":
    main()
