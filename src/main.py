#!/usr/bin/env python
import os
from claude_summary import claude_summary
from linear import linear
from openai_summary import openai_summary
from notion import notion

DEFAULT_PROMPT = 'Provide a detailed summary of the following commit messages in markdown format: '

def is_empty(value):
    return value is None or len(value) == 0

def main():
    # Get env variables
    OPENAI_KEY = os.environ.get("OPENAI_KEY")
    OPENAI_ORG = os.environ.get("OPENAI_ORG")
    ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
    NOTION_KEY = os.environ.get("NOTION_KEY")
    NOTION_DB_ID = os.environ.get("NOTION_DB_ID")
    LINEAR_KEY = os.environ.get("LINEAR_KEY") 
    LINEAR_VIEW_ID = os.environ.get("LINEAR_VIEW_ID")
    CHANGELOG = os.environ.get("CHANGELOG")
    VERSION = os.environ.get("VERSION")
    PROMPT = os.environ.get("PROMPT") or DEFAULT_PROMPT
    COMMITS = os.environ.get("COMMITS")
    
    if(not is_empty(LINEAR_KEY)):
        issues = linear(LINEAR_VIEW_ID, 100, LINEAR_KEY)
        
    # fallback to commits
    issues = issues or COMMITS
    print(f"Using issues: {issues}")

    if(not is_empty(issues)):
        release_notes = None
        if(not is_empty(ANTHROPIC_KEY)):
            release_notes = claude_summary(issues, PROMPT, ANTHROPIC_KEY)
        elif(not is_empty(OPENAI_KEY) and not is_empty(OPENAI_ORG)):
            release_notes = openai_summary(issues, PROMPT, OPENAI_KEY, OPENAI_ORG)
        
        if(not is_empty(NOTION_KEY) and not is_empty(release_notes)):
            notion(release_notes, COMMITS, NOTION_KEY, NOTION_DB_ID, VERSION, CHANGELOG)

        # Format the release_notes for multiline output
        if release_notes:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
                fh.write('summary<<EOF\n')
                fh.write(release_notes)
                fh.write('\nEOF\n')
                
        return release_notes
    
    return None

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()