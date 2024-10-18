import os
from openai import OpenAI

def openai(prompt_message, commit_messages):
    if not commit_messages:
        raise ValueError("Commit messages are empty!")
      
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get(OPENAI_KEY),
    )

    prompt = f"{prompt_message} {commit_messages}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5612,
        temperature=0.6
    )

    summary = response['choices'][0]['message']['content'].strip()

    if not summary:
        raise ValueError("Summary is null or empty.")

    return summary