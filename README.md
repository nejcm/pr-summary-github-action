# pr-summary-github-action

Github action that summarizes the PR commits and posts it to notion, slack,
github comment, ...

> **! IMPORTANT**  
> When checking out the code, make sure to use the `fetch-depth: 0` option. [Read more](https://github.com/actions/checkout?tab=readme-ov-file#fetch-all-history-for-all-tags-and-branches)

> To post to notion database please allow you API integration access to the database.
> [Read more](https://developers.notion.com/docs/create-a-notion-integration)

## Example usage

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
          comment: "true"
          prompt: "Provide a set of Release Notes in Markdown format based on the following list of tasks that have been exported from Linear. These notes are for customers, so exclude anything technical or reference to internal or backend fixes / features. Make reference to high level features rather than specifics. Keep your notes fairly high level."

      - name: 🖨️ Print summary
        run: echo ${{ steps.summary.outputs.summary }}

      - name: 💬 Post summary comment
        if: steps.summary.outcome == 'success' && steps.summary.outputs.summary != ''
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          number: ${{ github.event.pull_request.number }}
          header: "Release Summary"
          message: |
            ${{ steps.summary.outputs.summary }}
```
