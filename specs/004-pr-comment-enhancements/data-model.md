# Data Model: PR Comment Enhancements

**Feature**: FR-5 PR Comment Enhancements
**Date**: 2026-02-19

## Overview

This document defines the data structures used for capturing validation errors and generating formatted PR comments.

## Entities

### ValidationError

Represents a single validation error or warning found during CI pipeline execution.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | enum | Yes | Error category (see Error Types below) |
| `source` | enum | Yes | Validation step that produced the error |
| `file` | string | No | Relative path to affected file |
| `line` | integer | No | Line number where error occurs (1-indexed) |
| `value` | string | No | Specific error value (URL, image path, etc.) |
| `message` | string | Yes | Human-readable error description |
| `severity` | enum | Yes | `blocking` or `warning` |
| `fix_suggestion` | string | No | Actionable fix instruction |
| `raw_output` | string | No | Original output for fallback display |

#### Error Types

| Type | Description | Custom Formatter |
|------|-------------|------------------|
| `broken_url` | HTTP request failed (404, timeout, etc.) | Yes |
| `missing_image` | Referenced image file not found | Yes |
| `xml_error` | Solomon XML conversion failed | Yes |
| `duration_mismatch` | Step durations don't sum to total | Yes |
| `guid_uniqueness` | Duplicate GUID detected | Fallback |
| `extra_files` | Unexpected .md files in folder | Fallback |
| `skill_level` | Invalid skill level value | Fallback |
| `technology` | Invalid technology value | Fallback |
| `solomon_lint` | Solomon linting warning | Fallback |
| `folder_structure` | Missing images folder, naming error | Fallback |
| `schema` | sidecar.json schema violation | Existing (no change) |
| `other` | Unrecognized error type | Fallback |

#### Source Steps

| Source | Workflow Step | Output File |
|--------|---------------|-------------|
| `pytest` | Validate sidecar against Pytest checks | `pytest_results.json` |
| `schema` | Validate sidecar against JSON schema | `schema_output.txt` |
| `markdown` | Validate and auto-fix markdown files | `validation_result.json` |
| `solomon_transform` | Convert raw XML into Solomon XML | `transform_stderr.log` |
| `solomon_lint` | Perform Solomon XML linting | `linting_output.log` |
| `folder_check` | Ensure only one folder in PR | (workflow output) |

### ValidationResult

Aggregated result from a single validation step.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `step` | string | Yes | Name of the validation step |
| `status` | enum | Yes | `passed`, `failed`, or `skipped` |
| `errors` | ValidationError[] | Yes | List of errors (empty if passed) |
| `summary` | string | No | Brief description of result |
| `duration_ms` | integer | No | Step execution time |

### PRCommentPayload

Complete payload for generating the PR comment.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pr_number` | integer | Yes | Pull request number |
| `tutorial_folder` | string | Yes | Name of tutorial folder (tc-*) |
| `overall_status` | enum | Yes | `passed`, `failed`, or `warnings` |
| `validation_results` | ValidationResult[] | Yes | Results from all steps |
| `blocking_count` | integer | Yes | Total blocking errors |
| `warning_count` | integer | Yes | Total warnings |
| `generated_at` | datetime | Yes | ISO 8601 timestamp |

## State Transitions

### Validation Pipeline Flow

```
┌─────────────────┐
│   PR Created    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐
│  Folder Check   │───▶│  ValidationError │
└────────┬────────┘    │  (folder_structure)
         │             └──────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐
│ Schema Validate │───▶│  ValidationError │
└────────┬────────┘    │  (schema)        │
         │             └──────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐
│  Pytest Checks  │───▶│  ValidationError │
└────────┬────────┘    │  (broken_url,    │
         │             │   duration, etc.) │
         ▼             └──────────────────┘
┌─────────────────┐    ┌──────────────────┐
│ Markdown Clean  │───▶│  ValidationError │
└────────┬────────┘    │  (markdown)      │
         │             └──────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐
│ Solomon Convert │───▶│  ValidationError │
└────────┬────────┘    │  (xml_error)     │
         │             └──────────────────┘
         ▼
┌─────────────────┐    ┌──────────────────┐
│  Solomon Lint   │───▶│  ValidationError │
└────────┬────────┘    │  (solomon_lint)  │
         │             └──────────────────┘
         ▼
┌─────────────────┐
│ Aggregate into  │
│ PRCommentPayload│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ format_pr_      │
│ comment.py      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  gh pr comment  │
└─────────────────┘
```

## Validation Rules

### ValidationError Constraints

1. `file` MUST be relative path from repository root
2. `line` MUST be 1-indexed (first line = 1)
3. `value` SHOULD be truncated to 500 characters max
4. `raw_output` SHOULD be truncated to 5000 characters max
5. `type` MUST match one of the defined error types

### PRCommentPayload Constraints

1. `blocking_count` MUST equal count of errors with `severity: blocking`
2. `warning_count` MUST equal count of errors with `severity: warning`
3. `overall_status` logic:
   - `passed`: blocking_count == 0 AND warning_count == 0
   - `warnings`: blocking_count == 0 AND warning_count > 0
   - `failed`: blocking_count > 0
