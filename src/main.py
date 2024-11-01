#!/usr/bin/env python
import os
from claude_summary import claude_summary
from linear import linear
from openai_summary import openai_summary
from notion import notion

DEFAULT_PROMPT = 'Provide a detailed summary of the following commit messages in markdown format: '

def main():
    # Get env variables
    OPENAI_KEY = os.environ.get("OPENAI_KEY")
    ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
    NOTION_KEY = os.environ.get("NOTION_KEY")
    LINEAR_KEY = os.environ.get("LINEAR_KEY")
    LINEAR_VIEW_ID = os.environ.get("LINEAR_VIEW_ID")
    CHANGELOG = os.environ.get("CHANGELOG")
    VERSION = os.environ.get("VERSION")
    PROMPT = os.environ.get("PROMPT") or DEFAULT_PROMPT
    COMMITS = os.environ.get("COMMITS")
    
    if(LINEAR_KEY is not None and len(LINEAR_KEY) > 0):
        issues = linear(LINEAR_VIEW_ID, 100, LINEAR_KEY)
    else:
        # fallback to commits
        issues = COMMITS

    if(issues is not None and len(issues) > 0):
        release_notes = None
        if(ANTHROPIC_KEY is not None and len(ANTHROPIC_KEY) > 0):
            release_notes = claude_summary(issues, PROMPT, ANTHROPIC_KEY)
        elif(OPENAI_KEY is not None and len(OPENAI_KEY) > 0):
            release_notes = openai_summary(issues, PROMPT, OPENAI_KEY)

        if(NOTION_KEY is not None and len(NOTION_KEY) > 0 & release_notes is not None and len(release_notes) > 0):
            notion(release_notes, COMMITS, NOTION_KEY, VERSION, CHANGELOG)
            
        return release_notes
    
    return None

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()