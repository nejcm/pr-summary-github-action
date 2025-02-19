from openai import OpenAI

def openai_summary(issues, prompt, key, org, model="gpt-4o"):
    if not issues:
        raise ValueError("Commit messages are empty!")
      
    client = OpenAI(
        organization=org,
        api_key=key,
    )

    prompt = f"{prompt} {issues}"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.6
    )
    
    if not response.choices:
        raise ValueError("No response choices available")
    if not response.choices[0]:
        raise ValueError("First choice is null")
    if not response.choices[0].message:
        raise ValueError("Message is null")

    summary = response.choices[0].message.content
    if not summary:
        raise ValueError("Summary is null or empty.")

    return summary