import requests
import json

def split_into_chunks(text, limit):
    chunks = []
    while len(text) > limit:
        chunks.append(text[:limit])
        text = text[limit:]
    chunks.append(text)
    return chunks

def notion(summary, commit_messages, key, version, changelog):
    # Split commit messages into chunks
    commit_message_chunks = split_into_chunks(commit_messages, 2000)

    # Create children blocks for commit messages
    commit_blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chunk
                        }
                    }
                ]
            }
        }
        for chunk in commit_message_chunks
    ]
    
    # Construct data payload
    payload = {
        "parent": {"database_id": "cd227b78703e499d81b902b402fcc128"},
        "properties": {
            "Title": {
                "type": "title",
                "title": [{
                    "type": "text",
                    "text": {"content": f"v{version}"}
                }]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Summary"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": summary}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Commits"}
                        }
                    ]
                }
            },
            *commit_blocks
        ]
    }

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
        print(f"Page created successfully")
    else:
        print(f"Failed to create page: {response.status_code} - {response.text}")
        
    return response
