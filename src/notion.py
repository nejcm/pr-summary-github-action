import requests
import json
from notion_parse import markdown_to_notion_blocks, split_lines, EMPTY_BLOCK
from helpers import is_empty

def calloutBlock(icon, title, text, link):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {
                "type": "emoji",
                "emoji": icon
            },
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                    }
                },
                {
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": {"url": link}
                    }
                }
            ]
        }
    }


def notion(summary, commit_messages, key, db_id, version, changelog, prLink):
    # Transform markdown summary to Notion blocks
    summary_blocks = markdown_to_notion_blocks(summary)
    
    # Split commit messages into chunks
    commit_message_lines = split_lines(commit_messages or '')

    # Create children blocks for commit messages as list items
    commit_blocks = [
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": line
                        }
                    }
                ]
            }
        }
        for line in commit_message_lines if line.strip()  # Ignore empty lines
    ]
    
    # Construct data payload
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Title": {
                "type": "title",
                "title": [{
                    "type": "text",
                    "text": {"content": version or 'Release summary'}
                }]
            }
        },
        "children": summary_blocks + [EMPTY_BLOCK]
    }
    
    # Add changelog paragraph if changelog exists
    if not is_empty(changelog):
        payload["children"].append(calloutBlock("🔗", "CHANGELOG: ", changelog, changelog))
        
    if not is_empty(prLink):
        payload["children"].append(calloutBlock("📄", "Pull request: ", prLink, prLink))
        
    # Add the "Commits" heading and commit blocks
    payload["children"].extend([
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Commits"},
                        "annotations": {
                            "bold": True,
                            "underline": True
                        }
                    }
                ],
                "children": commit_blocks
            }
        },
    ])

    # Set headers for the HTTP request
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Send HTTP request to Notion API
    response = requests.post(
        'https://api.notion.com/v1/pages',
        headers=headers,
        data=json.dumps(payload)
    )

    # Check response
    if response.status_code == 200:
        print(f"Notion page created successfully")
    else:
        print(f"Failed to create Notion page: {response.status_code} - {response.text}")
        
    return response
