from anthropic import Anthropic

def claude_summary(issues, prompt, key, model="claude-3-5-sonnet-20240620"):
    client = Anthropic(
      api_key=key,
    )
    fullPrompt = f"""
      {prompt}
      {issues}
    """
    message = client.messages.create(
        model=model,
        max_tokens=5612,
        temperature=0.6,
        # system=system,
        messages=[
          {"role": "user", "content": fullPrompt}
        ]
    )

    if isinstance(message.content, list):
        release_notes = "\n".join([item.text for item in message.content if hasattr(item, 'text')])
    elif hasattr(message.content, 'text'):
        release_notes = message.content.text
    else:
        release_notes = "Error: Couldn't extract release notes from the API response."

    return release_notes