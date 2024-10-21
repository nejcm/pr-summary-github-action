#!/usr/bin/env python
import os
from claude import claude_summary
from linear import linear
from openai import openai_summary
from notion import notion

def main():
    # Get env variables
    try:
        OPENAI_KEY = os.environ["OPENAI_KEY"]
        CLAUDE_KEY = os.environ["CLAUDE_KEY"]
        NOTION_KEY = os.environ["NOTION_KEY"]
        LINEAR_KEY = os.environ["LINEAR_KEY"]
        LINEAR_VIEW_ID = os.environ["LINEAR_VIEW_ID"]
        CHANGELOG = os.environ["CHANGELOG"]
        VERSION = os.environ["VERSION"]
        PROMPT = os.environ["PROMPT"]
        COMMITS = os.environ["COMMITS"]
    except KeyError:
        VERSION = "UNKNOWN"
    
    if(len(LINEAR_KEY) > 0):
        issues = linear(LINEAR_VIEW_ID, 100, LINEAR_KEY)
    else:
        # fallback to commits
        issues = COMMITS

    if(len(issues) > 0):
        if(len(CLAUDE_KEY) > 0):
            release_notes = claude_summary(issues, PROMPT, CLAUDE_KEY)
        elif(len(OPENAI_KEY) > 0):
            release_notes = openai_summary(issues, PROMPT, OPENAI_KEY)

    
    if(len(NOTION_KEY) > 0 & len(release_notes) > 0):
        notion(release_notes, COMMITS, NOTION_KEY, VERSION, CHANGELOG)
    
    return release_notes

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()