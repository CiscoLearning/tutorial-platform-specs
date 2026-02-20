#!/usr/bin/env python3
"""
Interactive tutorial creation wizard.

Run this script to create a new tutorial with all required files.
It prompts for all necessary information and generates the folder structure.

Usage:
    python tools/tutorial_wizard.py

The wizard will:
1. Prompt for tutorial details (title, author, duration, etc.)
2. Create the tc-* folder with proper structure
3. Generate sidecar.json with valid GUIDs
4. Create step markdown files with templates
5. Optionally create a git branch and initial commit
"""

import json
import os
import re
import subprocess
import sys
import uuid
from datetime import date
from pathlib import Path


# Valid options from schema
SKILL_LEVELS = ["Beginner", "Intermediate", "Advanced", "Expert"]

TECHNOLOGIES = [
    "Application Performance",
    "Cloud and Computing",
    "Collaboration",
    "Data Center",
    "Mobility and Wireless",
    "Networking",
    "Other",
    "Security",
    "Software"
]

CERTIFICATIONS = [
    "CCNA",
    "CCNP Enterprise",
    "CCNP Security",
    "CCNP Data Center",
    "CCNP Collaboration",
    "CCNP Service Provider",
    "CCIE Enterprise Infrastructure",
    "CCIE Security",
    "CCIE Data Center",
    "CCIE Collaboration",
    "CCIE Service Provider",
    "Cisco Certified DevNet Associate",
    "Cisco Certified DevNet Professional",
    "Cisco Certified DevNet Expert",
    "Cisco Certified Cybersecurity Associate",
    "Cisco Certified Cybersecurity Professional",
    "Cisco Certified Design Expert"
]

DURATION_OPTIONS = [
    ("15 minutes", "15m00s", 15),
    ("20 minutes", "20m00s", 20),
    ("25 minutes", "25m00s", 25),
    ("30 minutes", "30m00s", 30),
    ("35 minutes", "35m00s", 35),
    ("40 minutes", "40m00s", 40),
    ("45 minutes", "45m00s", 45),
    ("50 minutes", "50m00s", 50),
    ("55 minutes", "55m00s", 55),
    ("60 minutes", "1h00m00s", 60),
]


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a styled header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_success(msg: str):
    """Print a success message."""
    print(f"✅ {msg}")


def print_error(msg: str):
    """Print an error message."""
    print(f"❌ {msg}")


def prompt(question: str, default: str = "") -> str:
    """Prompt user for input with optional default."""
    if default:
        result = input(f"{question} [{default}]: ").strip()
        return result if result else default
    else:
        while True:
            result = input(f"{question}: ").strip()
            if result:
                return result
            print("  This field is required.")


def prompt_choice(question: str, options: list, allow_multiple: bool = False) -> list:
    """Prompt user to select from options."""
    print(f"\n{question}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    if allow_multiple:
        print("\n  Enter numbers separated by commas (e.g., 1,3,5)")
        print("  Press Enter for none")

        while True:
            result = input("Your choice: ").strip()
            if not result:
                return []
            try:
                indices = [int(x.strip()) for x in result.split(',')]
                selected = [options[i-1] for i in indices if 1 <= i <= len(options)]
                if selected:
                    return selected
                print("  Invalid selection. Try again.")
            except (ValueError, IndexError):
                print("  Invalid input. Enter numbers separated by commas.")
    else:
        while True:
            result = input("Your choice (number): ").strip()
            try:
                index = int(result)
                if 1 <= index <= len(options):
                    return [options[index-1]]
                print(f"  Enter a number between 1 and {len(options)}")
            except ValueError:
                print("  Enter a valid number.")


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


def generate_guid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4()).lower()


def create_step_content(step_num: int, label: str, title: str,
                        is_overview: bool = False, is_congrats: bool = False) -> str:
    """Generate content for a step file."""
    if is_overview:
        return f"""## Overview

Welcome to **{title}**!

### What You'll Learn

In this tutorial, you will:

- [ ] First learning objective
- [ ] Second learning objective
- [ ] Third learning objective

### Prerequisites

Before starting, ensure you have:

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

We'd love to hear your feedback on this tutorial!
"""
    else:
        return f"""## {label}

[Add your content for this step here]

### Concept Explanation

Explain the key concepts for this step.

### Hands-On Exercise

```bash
# Example command or code
echo "Hello, World!"
```

### Verification

How can the learner verify they completed this step correctly?

---

[Continue to next step]
"""


def run_wizard():
    """Run the interactive tutorial wizard."""
    clear_screen()
    print_header("🚀 Cisco U. Tutorial Creation Wizard")

    print("This wizard will help you create a new tutorial with all required files.")
    print("Press Ctrl+C at any time to cancel.\n")

    # Gather information
    title = prompt("Tutorial title (e.g., 'Getting Started with Ansible')")

    slug_default = generate_slug(title)
    slug = prompt(f"Tutorial slug (URL-friendly name)", slug_default)
    folder_name = f"tc-{slug}" if not slug.startswith("tc-") else slug

    # Check if folder already exists
    if Path(folder_name).exists():
        print_error(f"Folder '{folder_name}' already exists!")
        sys.exit(1)

    description = prompt("Brief description (1-2 sentences)")
    author_name = prompt("Your name")
    author_email = prompt("Your email (e.g., jadoe@cisco.com)")

    # Duration
    print("\nSelect tutorial duration:")
    duration_labels = [d[0] for d in DURATION_OPTIONS]
    duration_choice = prompt_choice("How long will this tutorial take?", duration_labels)[0]
    duration_info = next(d for d in DURATION_OPTIONS if d[0] == duration_choice)
    duration_str = duration_info[1]
    total_minutes = duration_info[2]

    # Skill level
    skill_level = prompt_choice("Target skill level?", SKILL_LEVELS)[0]

    # Technologies
    technologies = prompt_choice(
        "Select technologies (can select multiple):",
        TECHNOLOGIES,
        allow_multiple=True
    )
    if not technologies:
        technologies = ["Other"]

    # Certifications
    certifications = prompt_choice(
        "Related certifications (optional, can select multiple):",
        CERTIFICATIONS,
        allow_multiple=True
    )

    # Tags
    tags_input = prompt("Tags (comma-separated, e.g., python, automation, api)")
    tags = [t.strip() for t in tags_input.split(',') if t.strip()]

    # Number of steps
    print("\nHow many content steps? (Overview and Congratulations added automatically)")
    num_steps_options = [
        "3 steps (5 total)",
        "4 steps (6 total)",
        "5 steps (7 total)",
        "6 steps (8 total)",
        "7 steps (9 total)",
        "8 steps (10 total)",
        "9 steps (11 total)",
        "10 steps (12 total)",
    ]
    num_choice = prompt_choice("Select:", num_steps_options)[0]
    num_content_steps = int(num_choice.split()[0])

    # Step titles
    step_titles = []
    print(f"\nEnter titles for your {num_content_steps} content step(s):")
    for i in range(num_content_steps):
        default_title = f"Step {i + 1}"
        step_title = prompt(f"  Step {i + 2} title", default_title)
        step_titles.append(step_title)

    # Confirm
    print_header("📋 Summary")
    print(f"  Folder:        {folder_name}/")
    print(f"  Title:         {title}")
    print(f"  Author:        {author_name} <{author_email}>")
    print(f"  Duration:      {duration_choice}")
    print(f"  Skill Level:   {skill_level}")
    print(f"  Technologies:  {', '.join(technologies)}")
    if certifications:
        print(f"  Certifications: {', '.join(certifications)}")
    print(f"  Tags:          {', '.join(tags)}")
    print(f"  Steps:         {num_content_steps + 2} total")
    print()

    confirm = input("Create this tutorial? [Y/n]: ").strip().lower()
    if confirm and confirm != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Create the tutorial
    print_header("🔨 Creating Tutorial")

    # Create folder structure
    folder_path = Path(folder_name)
    folder_path.mkdir()
    (folder_path / 'images').mkdir()
    (folder_path / 'images' / '.gitkeep').touch()
    print_success(f"Created folder: {folder_name}/")

    # Calculate per-step duration
    total_steps = num_content_steps + 2
    per_step_minutes = total_minutes // total_steps
    remainder = total_minutes % total_steps

    # Build files array for sidecar
    files = []

    # Overview
    overview_duration = per_step_minutes + (1 if remainder > 0 else 0)
    files.append({
        "label": "Overview",
        "duration": f"{overview_duration}:00",
        "xy-guid": generate_guid(),
        "file": "step-1.md"
    })

    # Content steps
    for i in range(num_content_steps):
        step_duration = per_step_minutes + (1 if i + 1 < remainder else 0)
        files.append({
            "label": step_titles[i],
            "duration": f"{step_duration}:00",
            "xy-guid": generate_guid(),
            "file": f"step-{i + 2}.md"
        })

    # Congratulations
    files.append({
        "label": "Congratulations",
        "duration": f"{per_step_minutes}:00",
        "xy-guid": generate_guid(),
        "file": f"step-{total_steps}.md"
    })

    # Create sidecar.json
    sidecar = {
        "id": folder_name,
        "title": title,
        "description": description,
        "date": date.today().strftime('%Y-%m-%d'),
        "duration": duration_str,
        "ia-guid": generate_guid(),
        "lesson-guid": generate_guid(),
        "certifications": [{"cert": c} for c in certifications] if certifications else None,
        "skill-levels": skill_level,
        "tags": [{"tag": t} for t in tags],
        "technologies": [{"tech": t} for t in technologies],
        "files": files,
        "authors": [{"name": author_name, "email": author_email}],
        "active": True
    }

    with open(folder_path / 'sidecar.json', 'w') as f:
        json.dump(sidecar, f, indent=2)
        f.write('\n')
    print_success("Created sidecar.json")

    # Create step files
    for i, file_info in enumerate(files):
        is_overview = (i == 0)
        is_congrats = (i == len(files) - 1)

        content = create_step_content(
            step_num=i + 1,
            label=file_info['label'],
            title=title,
            is_overview=is_overview,
            is_congrats=is_congrats
        )

        with open(folder_path / file_info['file'], 'w') as f:
            f.write(content)
        print_success(f"Created {file_info['file']}")

    # Git operations (optional)
    print()
    use_git = input("Create git branch and initial commit? [Y/n]: ").strip().lower()
    if not use_git or use_git == 'y':
        try:
            # Check if we're in a git repo
            subprocess.run(['git', 'rev-parse', '--git-dir'],
                          capture_output=True, check=True)

            # Create branch
            subprocess.run(['git', 'checkout', '-b', folder_name], check=True)
            print_success(f"Created branch: {folder_name}")

            # Stage files
            subprocess.run(['git', 'add', folder_name], check=True)

            # Commit
            commit_msg = f"Create tutorial: {title}\n\nGenerated by tutorial_wizard.py"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print_success("Created initial commit")

            print(f"\n💡 Next: Push your branch with: git push -u origin {folder_name}")

        except subprocess.CalledProcessError:
            print("⚠️  Git operations skipped (not in a git repository or error occurred)")

    # Final message
    print_header("✅ Tutorial Created Successfully!")
    print(f"Your tutorial is ready at: {folder_name}/")
    print()
    print("Next steps:")
    print(f"  1. Edit the markdown files in {folder_name}/")
    print(f"  2. Add images to {folder_name}/images/")
    print(f"  3. Update step durations in sidecar.json")
    print(f"  4. Validate: python tools/validate_tutorial.py {folder_name}/")
    print(f"  5. Push and create a PR")
    print()


if __name__ == '__main__':
    try:
        run_wizard()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
