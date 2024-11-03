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
    else:
        # fallback to commits
        issues = COMMITS

    if(not is_empty(issues)):
        release_notes = None
        if(not is_empty(ANTHROPIC_KEY)):
            release_notes = claude_summary(issues, PROMPT, ANTHROPIC_KEY)
        elif(not is_empty(OPENAI_KEY) and not is_empty(OPENAI_ORG)):
            release_notes = openai_summary(issues, PROMPT, OPENAI_KEY, OPENAI_ORG)
            
        release_notes = """# Release Notes 123
  
  ## New Features
  
  - **Release Summary**: We've introduced a new feature that provides a comprehensive summary of each release, making it easier for you to stay informed about the latest updates and improvements.
  
  - **Release Action**: We've enhanced our release process with a new action feature, streamlining the deployment and management of updates.
  
  - **Python Code Conversion**: We're in the process of converting parts of our system to Python, which will improve performance and maintainability. This is a work in progress and will be rolled out in phases.
  
  ## Improvements
  
  - **Testing Enhancements**: We've added new tests to ensure the reliability and stability of our system, providing you with a more robust experience.
  
  We hope you enjoy the new features and improvements in this release. As always, we welcome your feedback to help us continue to enhance our product."""
        if(not is_empty(NOTION_KEY) and not is_empty(release_notes)):
            notion(release_notes, issues, NOTION_KEY, NOTION_DB_ID, VERSION, CHANGELOG)

        # Format the release_notes for multiline output
        if release_notes:
            print(f'::set-output name=summary::{release_notes}')
            #with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            #    fh.write('summary<<EOF\n')
            #    fh.write(release_notes)
            #    fh.write('\nEOF\n')
                
        return release_notes
    
    return None

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()