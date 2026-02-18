# Project Constitution

This document defines the governing principles and development guidelines for the Cisco U. Tutorial Content ecosystem.

## Project Mission

Enable Cisco technical advocates, instructors, and TMEs to efficiently create high-quality hands-on tutorials for network engineers, with automated validation, editorial assistance, and streamlined publishing to the Cisco U. platform.

## Core Principles

### 1. Tutorial Quality Standards
- Tutorials balance theory and hands-on practice
- Duration: 15 minutes to 1 hour
- Target audience: Network engineers at various skill levels
- Conversational writing style that references both author and learner

### 2. Content Structure
- Step-based progression (step-1.md through step-N.md)
- Step 1: Overview with "What you'll learn" and "What you'll need"
- Final step: Congratulations with call-to-action and resources
- One tutorial per pull request
- One author per tutorial

### 3. Automation Philosophy
- Validate early and provide actionable feedback
- Reduce manual editorial review through AI-powered analysis
- Automate publishing pipeline (markdown → XML → Cisco U. platform)
- Surface errors at PR time, not after merge

### 4. Contribution Workflow
- Branch naming: `tc-{tutorial-name}`
- Folder naming matches branch name
- PR triggers validation pipeline
- Editorial review by part-time editors (currently manual)
- Technical review by Technical Advocates
- Auto-publish to staging on merge

## Technical Constraints

### sidecar.json Requirements
- All GUIDs must be unique (validated against guid_cache.json)
- Duration format: `XXmXXs` or `XhXXmXXs` (top-level)
- Step duration format: `MM:SS`
- Sum of step durations must equal top-level duration
- Valid skill-levels: Beginner, Intermediate, Advanced, Expert
- Valid technologies: Application Performance, Cloud and Computing, Collaboration, Data Center, Mobility and Wireless, Networking, Other, Security, Software

### Markdown to XML Conversion
- Whitespace around links and file references causes XML errors
- Authors must manually fix formatting based on pipeline error messages
- Goal: Reduce manual intervention through better validation

## Stakeholders

- **Technical Advocates**: Primary tutorial authors, PR approvers
- **Learn with Cisco Instructors**: Contributing authors
- **TMEs (Technical Marketing Engineers)**: Contributing authors
- **Part-time Editors**: Editorial review (Jill, Matt Sperling)
- **L&C UAT Team**: Final staging approval before production
- **Publishing Team**: Receives XML via REST API, handles platform publishing

## Success Metrics

- Reduced time from PR to publish
- Fewer manual editorial corrections needed
- Lower XML conversion error rate
- Consistent tutorial quality across authors
