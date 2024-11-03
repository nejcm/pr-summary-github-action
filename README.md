# pr-summary-github-action

This GitHub Action summarizes commit messages from a pull request (PR) and posts the summary to Notion. It can be configured to integrate with other services such as OpenAI, Anthropic, and Linear for enhanced processing and output management.

## Inputs

- **`ghToken`** (required): GitHub token for authentication.
- **`openAiKey`** (optional): OpenAI API key. Ignored if empty.
- **`openAiOrg`** (optional): OpenAI organization ID.
- **`anthropicKey`** (optional): Anthropic API key. Ignored if empty.
- **`linearKey`** (optional): Linear API key. Ignored if empty.
- **`linearViewId`** (optional): Linear view ID.
- **`notionKey`** (optional): Notion API key.
- **`notionDbId`** (optional): Notion database ID.
- **`prompt`** (optional): Prompt to use for summarizing commits. Default: "Provide a detailed summary of the following commit messages in markdown format."
- **`changelog`** (optional): Link to the changelog.
- **`version`** (optional): Release version.

## Outputs

- **`summary`**: The resulting release summary.

> **! IMPORTANT**  
> When checking out the code, make sure to use the `fetch-depth: 0` option. [Read more](https://github.com/actions/checkout?tab=readme-ov-file#fetch-all-history-for-all-tags-and-branches)

> To post to notion database please allow you API integration access to the database.
> [Read more](https://developers.notion.com/docs/create-a-notion-integration)

## Example usage

Here's an example of how to use this action within a GitHub workflow:

```yaml
name: ci

on:
  pull_request:
    branches:
      - develop
  workflow_dispatch:

jobs:
  build:
    name: Running ci
    if: "github.event.pull_request.draft != true"
    runs-on: ubuntu-latest
    env:
      CI: true

    steps:
      - name: 🛒 Checkout code
        uses: actions/checkout@v4

      - name: 📄 PR summary
        id: summary
        uses: nejcm/pr-summary-github-action@v1.0.0
        with:
          anthropicKey: ${{ secrets.ANTHROPIC_KEY }}
          notionKey: ${{ secrets.NOTION_KEY }}
          notionDbId: ${{ secrets.NOTION_DB_ID }}
          linearKey: ${{ secrets.LINEAR_KEY }}
          linearViewId: ${{ secrets.LINEAR_VIEW_ID }}
          prompt: "Provide a set of Release Notes in Markdown format based on the following list of tasks that have been exported from Linear. These notes are for customers, so exclude anything technical or reference to internal or backend fixes / features. Make reference to high level features rather than specifics. Keep your notes fairly high level."

      - name: 💬 Post summary comment
        if: steps.summary.outcome == 'success' && steps.summary.outputs.summary != ''
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}
          number: ${{ github.event.pull_request.number }}
          header: "Release Summary"
          message: |
            ${{ steps.summary.outputs.summary }}
```
