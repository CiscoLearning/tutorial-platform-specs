# Network Configuration

This step covers the basics of network configuration.

## Prerequisites

Before you begin, make sure you have:

- Access to a Cisco router or switch
- Basic understanding of CLI commands
- A terminal emulator installed

## Common Issues That Break XML Conversion

The following sections contain intentional issues that our validation tool should catch.

### Issue 1: HTML Tags

Sometimes authors copy content from web pages and accidentally include HTML tags.<br>This line has a break tag that will cause problems.

Here's another example with a<p>paragraph tag</p>embedded in text.

### Issue 2: Missing Link Spacing

Click[here](https://developer.cisco.com)to learn more about Cisco APIs.

The documentation is available[on this page](https://cisco.com/docs)for reference.

### Issue 3: Nested Lists with Inconsistent Indentation

Here's a properly formatted nested list for comparison:

- First item
  - Subitem A
  - Subitem B
    - Deep item 1
    - Deep item 2

Now here's a problematic nested list:

- Item one
  - Subitem with 2 spaces
   - Subitem with 3 spaces (inconsistent!)
    - Subitem with 4 spaces
      - Deep item with 6 spaces

### Issue 4: Code Blocks in Lists

When adding code to list items, proper indentation is critical:

- Here's a list item with code that's NOT properly indented:
```python
# This code block will break XML conversion
def configure_router():
    print("Hello, Network!")
```

- Here's another item with properly indented code:
  ```python
  # This is correct
  def configure_switch():
      print("Hello, Switch!")
  ```

### Issue 5: Broken Link Syntax

Sometimes links get broken across lines when editing:

For more information, see the [official Cisco
documentation](https://cisco.com/docs) for details.

You can also check the [DevNet learning
labs](https://developer.cisco.com/learning) for hands-on practice.

### Issue 6: Multiple Spaces

This line has  double spaces that should be fixed.

Multiple  spaces  scattered  throughout  the  text.

### Issue 7: Complex Nested Structure

Here's a complex example combining multiple issues:

1. First numbered item
   - Nested bullet with code:
```bash
# Not indented properly
show ip route
```
   - Another bullet[with link](https://example.com)missing spaces
2. Second numbered item<br>with HTML break
  1. Sub-numbered with inconsistent indent
   2. Another sub-numbered (wrong indent)

## Valid Content Section

This section contains properly formatted content that should NOT trigger any issues.

Here is a [valid link](https://cisco.com) with proper spacing.

- Properly formatted list
  - With consistent indentation
  - And another item
    - Deeply nested correctly

```python
# Code block outside of list - perfectly fine
def main():
    print("This is valid!")
```

> A blockquote with proper formatting.
> Multiple lines in the quote.
