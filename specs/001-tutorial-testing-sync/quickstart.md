# Quickstart: Tutorial-Testing Environment Sync

**Feature**: 001-tutorial-testing-sync
**Date**: 2026-02-18

## Prerequisites

Before setting up the sync, ensure you have:

1. **Admin access** to the `tutorial-testing` repository
2. **Read access** to the production `ciscou-tutorial-content` repository (private, org-owned)
3. **Personal Access Token (PAT)** with `repo` scope from a user who is a member of the organization

## Setup Steps

### Step 1: Create Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Name: `tutorial-testing-sync`
4. Expiration: Set appropriate expiration (recommend 90 days with calendar reminder)
5. Scopes: Select `repo` (full control of private repositories)
6. Click "Generate token" and copy the token value

### Step 2: Configure Repository Secrets

In the `tutorial-testing` repository:

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PROD_REPO_TOKEN`
4. Value: Paste the PAT from Step 1
5. Click "Add secret"

### Step 3: Configure Repository Variables

In the `tutorial-testing` repository:

1. Go to Settings → Secrets and variables → Actions → Variables tab
2. Click "New repository variable"
3. Name: `PROD_REPO`
4. Value: `{org}/ciscou-tutorial-content` (replace `{org}` with actual org name)
5. Click "Add variable"

### Step 4: Archive Test Fixtures (One-Time)

Before enabling sync, archive existing test content:

```bash
cd tutorial-testing

# Create archive folder
mkdir -p _test-fixtures

# Move test tutorials (those not in production)
mv tc-avocado-test tc-jira-demo tc-broken-link _test-fixtures/
mv tc-cache-check tc-cache-check2 tc-cache-check3 _test-fixtures/
mv tc-a2 tc-d2 tc-ex tc-full-demo tc-full-test _test-fixtures/
mv tc-github-action-test tc-image-check tc-jira-new _test-fixtures/
mv tc-jira-test tc-jira-test-2 tc-llm-start tc-new tc-new-tests _test-fixtures/
mv tc-start-to-finish tc-starting-github-actions-copy _test-fixtures/
mv tc-tech-test-1213 tc-template-test tc-whitespace-check _test-fixtures/
mv tc-whole tc-work-check _test-fixtures/

# Move poplartest folders
mv poplartest* _test-fixtures/

# Commit the archive
git add _test-fixtures/
git add -A  # Stage removals from original locations
git commit -m "Archive test fixtures before enabling production sync"
git push
```

### Step 5: Add Sync Workflow

Create `.github/workflows/sync-from-production.yml`:

```yaml
name: Sync from Production

on:
  schedule:
    - cron: '0 4 * * *'  # Daily at 4 AM UTC
  workflow_dispatch:
    inputs:
      force_full_sync:
        description: 'Force full sync even if no changes'
        required: false
        default: 'false'
        type: boolean

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout production repo
        uses: actions/checkout@v4
        with:
          repository: ${{ vars.PROD_REPO }}
          path: production
          token: ${{ secrets.PROD_REPO_TOKEN }}

      - name: Checkout testing repo
        uses: actions/checkout@v4
        with:
          path: testing
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Sync tutorials
        run: |
          # Sync all tc-* folders (delete removed tutorials)
          rsync -av --delete \
            --include='tc-*/' \
            --include='tc-*/**' \
            --exclude='*' \
            production/ testing/

          # Sync guid_cache.json
          cp production/guid_cache.json testing/guid_cache.json

          # Sync workflow files
          cp production/.github/workflows/*.yml testing/.github/workflows/

      - name: Check for changes
        id: changes
        working-directory: testing
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Commit and push
        if: steps.changes.outputs.has_changes == 'true'
        working-directory: testing
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "Sync from production $(date +%Y-%m-%d)"
          git push
```

### Step 6: Test the Workflow

1. Go to Actions tab in `tutorial-testing` repository
2. Select "Sync from Production" workflow
3. Click "Run workflow" → "Run workflow"
4. Monitor the run for any errors

## Verification

After sync completes, verify:

- [ ] Production tutorials appear in testing (check `tc-*` folder count)
- [ ] Test fixtures are preserved in `_test-fixtures/`
- [ ] `tools/` folder is unchanged
- [ ] `template/` folder is unchanged
- [ ] `guid_cache.json` matches production
- [ ] Workflow files match production

## Troubleshooting

### "Resource not accessible by integration"
- Check that `PROD_REPO_TOKEN` has `repo` scope
- Verify the token owner has access to the production repository
- Ensure the token has not expired

### "Repository not found"
- Verify `PROD_REPO` variable is set correctly
- Check org/repo name spelling
- Confirm the repository is accessible with the provided token

### Sync takes too long
- Check repository size (137+ tutorials is expected)
- First sync may take longer than subsequent runs
- Consider using shallow clone if performance is critical

## Maintenance

### Token Rotation
- PATs expire based on configured expiration
- Set calendar reminder to rotate before expiration
- Update `PROD_REPO_TOKEN` secret with new token

### Monitoring
- Check Actions tab periodically for failed runs
- GitHub sends email notifications for workflow failures
- Consider adding Slack/Teams notification for failures
