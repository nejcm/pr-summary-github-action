from openai import OpenAI

def openai_summary(issues, prompt, key, org):
    if not issues:
        raise ValueError("Commit messages are empty!")
      
    client = OpenAI(
        organization=org,
        api_key=key,
    )

    prompt = f"{prompt} {issues}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.6
    )
    
    if not response['choices']:
        raise ValueError("No response choices available")
    if not response['choices'][0]:
        raise ValueError("First choice is null")

    summary = response['choices'][0]['message'].get('content', None)
    if not summary:
        raise ValueError("Summary is null or empty.")

    return summary