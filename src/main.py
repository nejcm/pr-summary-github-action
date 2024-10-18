import os

def main():
    # Get env variables
    try:
        OPENAI_KEY = os.environ["OPENAI_KEY"]
        CLAUDE_KEY = os.environ["CLAUDE_KEY"]
        NOTION_KEY = os.environ["NOTION_KEY"]
        LINEAR_KEY = os.environ["LINEAR_KEY"]
        PROMPT = os.environ["PROMPT"]
    except KeyError:
        NOTION_KEY = "Token not available!"
    
    custom_view_id = "72c7011b3e8b"  # Using the ID from the original code
    if(LINEAR_KEY):
        issues = linear(custom_view_id)
        
    if(CLAUDE_KEY & issues):
        release_notes = claude(issues)
    elif(OPENAI_KEY & issues):
        release_notes = openai(issues)
    
    if(NOTION_KEY & release_notes):
        notion(release_notes, COMMITS)
    
    return release_notes

main()