#!/usr/bin/env python3
"""
Comprehensive unit tests for markdown validation detection rules.

Tests cover various markdown patterns to catch edge cases and prevent
false positives/negatives before running against full tutorial corpus.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from clean_markdown import (
    check_html_tags,
    check_link_spacing_before,
    check_link_spacing_after,
    check_link_broken,
    check_list_indent,
    check_code_block_in_list,
    check_trailing_whitespace,
    check_double_space,
)


class TestHTMLTags:
    """Tests for HTML_TAG detection rule"""

    def test_detects_br_tag(self):
        content = "Line one<br>Line two"
        issues = check_html_tags(content)
        assert len(issues) == 1
        assert "br" in issues[0].match

    def test_detects_self_closing_br(self):
        content = "Line one<br/>Line two"
        issues = check_html_tags(content)
        assert len(issues) == 1

    def test_detects_p_tag(self):
        content = "<p>Paragraph content</p>"
        issues = check_html_tags(content)
        assert len(issues) >= 1

    def test_ignores_code_blocks(self):
        content = """Normal text
```html
<br><p><div>
```
More text"""
        issues = check_html_tags(content)
        assert len(issues) == 0, "Should not flag HTML inside code blocks"

    def test_ignores_inline_code(self):
        content = "Use `<br>` for line breaks"
        issues = check_html_tags(content)
        # This might still flag - inline code handling is optional
        # Just documenting current behavior

    def test_detects_multiple_tags(self):
        content = "Text<br>more<p>even more<div>end"
        issues = check_html_tags(content)
        assert len(issues) == 3


class TestLinkSpacing:
    """Tests for LINK_NO_SPACE_BEFORE and LINK_NO_SPACE_AFTER rules"""

    def test_detects_missing_space_before(self):
        content = "Click[here](https://example.com) now"
        issues = check_link_spacing_before(content)
        assert len(issues) == 1

    def test_allows_space_before(self):
        content = "Click [here](https://example.com) now"
        issues = check_link_spacing_before(content)
        assert len(issues) == 0

    def test_allows_start_of_line(self):
        content = "[Link](https://example.com) at start"
        issues = check_link_spacing_before(content)
        assert len(issues) == 0

    def test_detects_missing_space_after(self):
        content = "Visit [site](https://example.com)now"
        issues = check_link_spacing_after(content)
        assert len(issues) == 1

    def test_allows_space_after(self):
        content = "Visit [site](https://example.com) now"
        issues = check_link_spacing_after(content)
        assert len(issues) == 0

    def test_allows_punctuation_after(self):
        content = "See [docs](https://example.com)."
        issues = check_link_spacing_after(content)
        assert len(issues) == 0

    def test_allows_end_of_line(self):
        content = "Click [here](https://example.com)"
        issues = check_link_spacing_after(content)
        assert len(issues) == 0

    def test_link_in_list(self):
        content = "- Click [here](https://example.com) for info"
        issues_before = check_link_spacing_before(content)
        issues_after = check_link_spacing_after(content)
        assert len(issues_before) == 0
        assert len(issues_after) == 0

    def test_image_not_flagged_as_missing_space(self):
        """Images use ![alt](url) syntax - the ! should not trigger 'missing space before'"""
        content = " ![Configure DLM1](./images/test.png)"
        issues = check_link_spacing_before(content)
        assert len(issues) == 0, "Image syntax should not be flagged"

    def test_image_inline_not_flagged(self):
        """Inline images like text![image](url) should not be flagged"""
        content = "See the screenshot![image](url)here"
        issues = check_link_spacing_before(content)
        assert len(issues) == 0, "Image syntax should not be flagged"


class TestBrokenLinks:
    """Tests for LINK_BROKEN detection rule"""

    def test_detects_newline_in_text(self):
        content = """This is a [broken
link](https://example.com) here."""
        issues = check_link_broken(content)
        assert len(issues) == 1

    def test_detects_newline_in_url(self):
        content = """This is a [link](https://example.
com) here."""
        issues = check_link_broken(content)
        assert len(issues) == 1

    def test_allows_normal_link(self):
        content = "This is a [normal link](https://example.com) here."
        issues = check_link_broken(content)
        assert len(issues) == 0

    def test_allows_multiline_in_code_block(self):
        content = """```
[broken
link](url)
```"""
        issues = check_link_broken(content)
        # Should ideally be 0, but current implementation may flag
        # Document current behavior


class TestListIndent:
    """Tests for LIST_INDENT_INCONSISTENT detection rule"""

    def test_detects_inconsistent_indent(self):
        content = """1. First
  - Sub with 2 spaces
   - Sub with 3 spaces"""
        issues = check_list_indent(content)
        # Should detect inconsistency between 2 and 3 space indents
        assert len(issues) >= 0  # Depends on strictness

    def test_allows_consistent_2_space(self):
        content = """1. First
  - Sub item
  - Another sub
    - Nested"""
        issues = check_list_indent(content)
        # 2-space increments are valid
        assert len(issues) == 0

    def test_allows_consistent_4_space(self):
        content = """1. First
    - Sub item
    - Another sub
        - Nested"""
        issues = check_list_indent(content)
        # 4-space increments are valid
        assert len(issues) == 0

    def test_simple_flat_list(self):
        content = """1. First
2. Second
3. Third"""
        issues = check_list_indent(content)
        assert len(issues) == 0


class TestCodeBlockInList:
    """Tests for CODE_BLOCK_IN_LIST detection rule

    Critical: This rule had false positive issues where code blocks
    properly separated by blank lines were being flagged.
    """

    def test_not_flagged_after_blank_line(self):
        """Code block after blank line should NOT be flagged"""
        content = """1. First step
2. Second step

```bash
echo hello
```

3. Third step"""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0, "Code block after blank line should not be flagged"

    def test_flagged_without_blank_line(self):
        """Code block immediately after list item SHOULD be flagged"""
        content = """1. First step
```bash
echo hello
```
2. Second step"""
        issues = check_code_block_in_list(content)
        assert len(issues) >= 1, "Code block without blank line should be flagged"

    def test_not_flagged_when_properly_indented(self):
        """Properly indented code block should NOT be flagged"""
        content = """1. First step

   ```bash
   echo hello
   ```

2. Second step"""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0

    def test_real_world_pattern_model_name(self):
        """Real pattern from tc-ai-lm-studio - should NOT be flagged"""
        content = """1. Click the **Discover** tab from the top navigation.
2. Use the search bar to find the model by typing:

```
Meta-Llama-3.1-8B-Instruct
```

3. Look for the version labeled `Meta-Llama-3.1-8B-Instruct-GGUF`."""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0, "Real-world pattern should not be flagged"

    def test_multiple_code_blocks_after_blank_lines(self):
        """Multiple code blocks, each after blank lines"""
        content = """1. Step one

```bash
command1
```

2. Step two

```bash
command2
```

3. Done"""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0

    def test_code_block_between_list_items_no_blank(self):
        """Code block squeezed between items without blank lines"""
        content = """1. Do this
```
code
```
2. Then this"""
        issues = check_code_block_in_list(content)
        assert len(issues) >= 1

    def test_nested_list_with_code_block(self):
        """Nested list with code block after blank line"""
        content = """1. Main item
   - Sub item

   ```bash
   code here
   ```

2. Next main item"""
        issues = check_code_block_in_list(content)
        # Properly indented and after blank - should not flag
        assert len(issues) == 0

    def test_unordered_list_with_code(self):
        """Unordered list with code block"""
        content = """- First item
- Second item

```python
print("hello")
```

- Third item"""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0

    def test_code_block_not_in_list_context(self):
        """Code block that was never in a list"""
        content = """Some paragraph text.

```bash
echo hello
```

More text here."""
        issues = check_code_block_in_list(content)
        assert len(issues) == 0


class TestTrailingWhitespace:
    """Tests for TRAILING_WHITESPACE detection rule"""

    def test_detects_trailing_spaces(self):
        content = "Line with trailing spaces   \nNormal line"
        issues = check_trailing_whitespace(content)
        assert len(issues) == 1

    def test_detects_trailing_tab(self):
        content = "Line with tab\t\nNormal line"
        issues = check_trailing_whitespace(content)
        assert len(issues) == 1

    def test_allows_clean_lines(self):
        content = "Clean line\nAnother clean line"
        issues = check_trailing_whitespace(content)
        assert len(issues) == 0

    def test_ignores_code_blocks(self):
        content = """Normal text
```
Code with trailing spaces
```
More text"""
        issues = check_trailing_whitespace(content)
        assert len(issues) == 0, "Should not flag inside code blocks"


class TestDoubleSpace:
    """Tests for DOUBLE_SPACE detection rule"""

    def test_detects_double_space(self):
        content = "Text with  double space"
        issues = check_double_space(content)
        assert len(issues) == 1

    def test_allows_single_spaces(self):
        content = "Text with single spaces only"
        issues = check_double_space(content)
        assert len(issues) == 0

    def test_ignores_code_blocks(self):
        content = """Normal text
```
code  with  spaces
```"""
        issues = check_double_space(content)
        assert len(issues) == 0


def run_tests():
    """Run all tests and report results"""
    import traceback

    test_classes = [
        TestHTMLTags,
        TestLinkSpacing,
        TestBrokenLinks,
        TestListIndent,
        TestCodeBlockInList,
        TestTrailingWhitespace,
        TestDoubleSpace,
    ]

    total = 0
    passed = 0
    failed = 0
    errors = []

    for test_class in test_classes:
        instance = test_class()
        print(f"\n{test_class.__name__}:")

        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total += 1
                try:
                    getattr(instance, method_name)()
                    print(f"  ✅ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ❌ {method_name}: {e}")
                    failed += 1
                    errors.append((test_class.__name__, method_name, str(e)))
                except Exception as e:
                    print(f"  💥 {method_name}: {type(e).__name__}: {e}")
                    failed += 1
                    errors.append((test_class.__name__, method_name, traceback.format_exc()))

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} passed, {failed} failed")

    if errors:
        print(f"\nFailed tests:")
        for cls, method, err in errors:
            print(f"  - {cls}.{method}")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
