#!/usr/bin/env python3
"""
Create a tutorial folder from a GitHub issue form submission.

This script is called by the create-tutorial.yml workflow when a new
issue is created with the 'new-tutorial' label.

It parses the issue body, generates the tutorial files, and outputs
the folder name for the workflow to use.
"""

import json
import os
import re
import uuid
from datetime import date
from pathlib import Path


def parse_issue_body(body: str) -> dict:
    """Parse GitHub issue form body into a dictionary."""
    data = {}
    current_field = None
    current_value = []

    lines = body.split('\n')
    for line in lines:
        # Check for field header (### Field Name)
        if line.startswith('### '):
            # Save previous field
            if current_field:
                data[current_field] = '\n'.join(current_value).strip()

            current_field = line[4:].strip().lower().replace(' ', '_')
            current_value = []
        elif current_field:
            # Skip "_No response_" placeholder
            if line.strip() == '_No response_':
                continue
            current_value.append(line)

    # Save last field
    if current_field:
        data[current_field] = '\n'.join(current_value).strip()

    return data


def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from a title."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


def parse_duration(duration_str: str) -> tuple:
    """Parse duration string and return (total_minutes, duration_str_for_sidecar).

    Returns duration in format for sidecar.json.
    """
    duration_map = {
        "15 minutes": (15, "15m00s"),
        "20 minutes": (20, "20m00s"),
        "25 minutes": (25, "25m00s"),
        "30 minutes": (30, "30m00s"),
        "35 minutes": (35, "35m00s"),
        "40 minutes": (40, "40m00s"),
        "45 minutes": (45, "45m00s"),
        "50 minutes": (50, "50m00s"),
        "55 minutes": (55, "55m00s"),
        "60 minutes": (60, "1h00m00s"),
    }
    return duration_map.get(duration_str.strip(), (30, "30m00s"))


def parse_checkboxes(text: str) -> list:
    """Parse checkbox format and return list of checked items."""
    items = []
    for line in text.split('\n'):
        # Match checked boxes: - [X] Item or - [x] Item
        match = re.match(r'^-\s*\[([xX])\]\s*(.+)$', line.strip())
        if match:
            items.append(match.group(2).strip())
    return items


def parse_num_steps(num_steps_str: str) -> int:
    """Parse number of steps from dropdown selection."""
    # Format: "2 (Overview + 2 steps + Congratulations = 4 total)"
    match = re.match(r'^(\d+)', num_steps_str.strip())
    if match:
        return int(match.group(1))
    return 1


def generate_guid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4()).lower()


def create_sidecar(data: dict, folder_name: str, num_content_steps: int) -> dict:
    """Create sidecar.json content from parsed data."""
    # Parse duration
    total_minutes, duration_str = parse_duration(data.get('estimated_duration', '30 minutes'))

    # Calculate per-step duration (total steps = num_content_steps + 2 for Overview and Congratulations)
    total_steps = num_content_steps + 2
    per_step_minutes = total_minutes // total_steps
    remainder = total_minutes % total_steps

    # Parse technologies
    technologies = parse_checkboxes(data.get('technologies', ''))
    if not technologies:
        technologies = ['Other']

    # Parse certifications
    certifications = parse_checkboxes(data.get('related_certifications_(optional)', ''))

    # Parse tags
    tags_str = data.get('tags', 'tutorial')
    tags = [t.strip() for t in tags_str.split(',') if t.strip()]

    # Parse step titles
    step_titles_str = data.get('step_titles_(optional)', '')
    step_titles = [t.strip() for t in step_titles_str.split('\n') if t.strip()]

    # Build files array
    files = []

    # Overview step
    overview_duration = per_step_minutes + (1 if remainder > 0 else 0)
    files.append({
        "label": "Overview",
        "duration": f"{overview_duration}:00",
        "xy-guid": generate_guid(),
        "file": "step-1.md"
    })

    # Content steps
    for i in range(num_content_steps):
        step_num = i + 2
        step_duration = per_step_minutes + (1 if i + 1 < remainder else 0)

        # Use custom title if provided, otherwise generic
        if i < len(step_titles):
            label = step_titles[i]
        else:
            label = f"Step {i + 1}"

        files.append({
            "label": label,
            "duration": f"{step_duration}:00",
            "xy-guid": generate_guid(),
            "file": f"step-{step_num}.md"
        })

    # Congratulations step
    congrats_step_num = num_content_steps + 2
    files.append({
        "label": "Congratulations",
        "duration": f"{per_step_minutes}:00",
        "xy-guid": generate_guid(),
        "file": f"step-{congrats_step_num}.md"
    })

    sidecar = {
        "id": folder_name,
        "title": data.get('tutorial_title', 'New Tutorial'),
        "description": data.get('description', 'Tutorial description'),
        "date": date.today().strftime('%Y-%m-%d'),
        "duration": duration_str,
        "ia-guid": generate_guid(),
        "lesson-guid": generate_guid(),
        "certifications": [{"cert": c} for c in certifications] if certifications else None,
        "skill-levels": data.get('skill_level', 'Beginner'),
        "tags": [{"tag": t} for t in tags],
        "technologies": [{"tech": t} for t in technologies],
        "files": files,
        "authors": [{
            "name": data.get('author_name', 'Author Name'),
            "email": data.get('author_email', 'author@cisco.com')
        }],
        "active": True
    }

    return sidecar


def create_step_file(step_num: int, label: str, is_overview: bool = False,
                     is_congrats: bool = False, title: str = '') -> str:
    """Create content for a step markdown file."""
    if is_overview:
        return f"""## Overview

Welcome to this tutorial on **{title}**!

### What You'll Learn

In this tutorial, you will:

- [ ] First learning objective
- [ ] Second learning objective
- [ ] Third learning objective

### Prerequisites

Before starting, you should have:

- Basic understanding of [topic]
- Access to [required resources]

### Time to Complete

This tutorial takes approximately [X] minutes to complete.

---

Let's get started!
"""
    elif is_congrats:
        return f"""## Congratulations!

You have successfully completed **{title}**!

### What You Learned

In this tutorial, you:

- ✅ First accomplishment
- ✅ Second accomplishment
- ✅ Third accomplishment

### Next Steps

To continue learning:

- Explore [related topic]
- Try [advanced tutorial]
- Check out [additional resources]

### Feedback

We'd love to hear your feedback on this tutorial. Please share your thoughts!
"""
    else:
        return f"""## {label}

[Add your content here]

### Section Heading

Explain the concept or task.

### Example

```python
# Add code examples as needed
print("Hello, World!")
```

### Try It Yourself

1. First step
2. Second step
3. Third step

---

[Continue to next step]
"""


def main():
    """Main entry point."""
    # Get issue body from environment
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', '0')

    if not issue_body:
        print("Error: ISSUE_BODY environment variable not set")
        exit(1)

    # Parse the issue body
    data = parse_issue_body(issue_body)

    # Get or generate slug
    title = data.get('tutorial_title', '').strip()
    if not title:
        # Try to extract from issue title
        issue_title = os.environ.get('ISSUE_TITLE', '')
        # Remove "[New Tutorial] " prefix
        title = re.sub(r'^\[New Tutorial\]\s*', '', issue_title).strip()
        data['tutorial_title'] = title

    slug = data.get('tutorial_slug_(optional)', '').strip()
    if not slug:
        slug = generate_slug(title)

    # Ensure folder name starts with tc-
    folder_name = f"tc-{slug}" if not slug.startswith('tc-') else slug

    # Parse number of content steps
    num_content_steps = parse_num_steps(data.get('number_of_steps', '1'))

    # Create the folder structure
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    (folder_path / 'images').mkdir(exist_ok=True)

    # Create sidecar.json
    sidecar = create_sidecar(data, folder_name, num_content_steps)
    with open(folder_path / 'sidecar.json', 'w') as f:
        json.dump(sidecar, f, indent=2)
        f.write('\n')

    # Create step files
    total_steps = num_content_steps + 2  # +2 for Overview and Congratulations

    for i, file_info in enumerate(sidecar['files']):
        step_num = i + 1
        label = file_info['label']
        is_overview = (step_num == 1)
        is_congrats = (step_num == total_steps)

        content = create_step_file(
            step_num=step_num,
            label=label,
            is_overview=is_overview,
            is_congrats=is_congrats,
            title=sidecar['title']
        )

        with open(folder_path / file_info['file'], 'w') as f:
            f.write(content)

    # Add .gitkeep to images folder
    (folder_path / 'images' / '.gitkeep').touch()

    # Output for GitHub Actions
    github_output = os.environ.get('GITHUB_OUTPUT', '')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"folder_name={folder_name}\n")
            f.write(f"tutorial_title={sidecar['title']}\n")

    print(f"Created tutorial: {folder_name}")
    print(f"  - sidecar.json")
    print(f"  - {total_steps} step files")
    print(f"  - images/ folder")


if __name__ == '__main__':
    main()
