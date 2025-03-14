#!/usr/bin/env python
import os
from claude_summary import claude_summary
from linear import linear
from openai_summary import openai_summary
from deepseek_summary import deepseek_summary
from gemini_summary import gemini_summary
from notion import notion
from helpers import is_empty

DEFAULT_PROMPT = 'Provide a detailed summary of the following commit messages in markdown format: '

def main():
    # Get env variables
    OPENAI_KEY = os.environ.get("OPENAI_KEY")
    OPENAI_ORG = os.environ.get("OPENAI_ORG")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
    ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
    ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL")
    DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")
    DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL")
    GEMINI_KEY = os.environ.get("GEMINI_KEY")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL")
    NOTION_KEY = os.environ.get("NOTION_KEY")
    NOTION_DB_ID = os.environ.get("NOTION_DB_ID")
    LINEAR_KEY = os.environ.get("LINEAR_KEY") 
    LINEAR_VIEW_ID = os.environ.get("LINEAR_VIEW_ID")
    CHANGELOG = os.environ.get("CHANGELOG")
    PR_LINK = os.environ.get("PR_LINK")
    VERSION = os.environ.get("VERSION")
    PROMPT = os.environ.get("PROMPT") or DEFAULT_PROMPT
    COMMITS = os.environ.get("COMMITS")
    DATA = os.environ.get("DATA")
    issues = None
    
    if(not is_empty(LINEAR_KEY)):
        issues = linear(LINEAR_VIEW_ID, 100, LINEAR_KEY)
        
    # fallback to commits
    issues = issues or DATA or COMMITS
    print(f"Using issues: {issues}")

    if(not is_empty(issues)):
        release_notes = None
        if(not is_empty(ANTHROPIC_KEY)):
            release_notes = claude_summary(issues, PROMPT, ANTHROPIC_KEY, ANTHROPIC_MODEL)
        elif(not is_empty(OPENAI_KEY) and not is_empty(OPENAI_ORG)):
            release_notes = openai_summary(issues, PROMPT, OPENAI_KEY, OPENAI_ORG, OPENAI_MODEL)
        elif(not is_empty(DEEPSEEK_KEY)):
            release_notes = deepseek_summary(issues, PROMPT, DEEPSEEK_KEY, DEEPSEEK_MODEL)
        elif(not is_empty(GEMINI_KEY)):
            release_notes = gemini_summary(issues, PROMPT, GEMINI_KEY, GEMINI_MODEL)
        
        if(not is_empty(NOTION_KEY) and not is_empty(release_notes)):
            notion(release_notes, COMMITS, NOTION_KEY, NOTION_DB_ID, VERSION, CHANGELOG, PR_LINK)

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