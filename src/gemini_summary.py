from google import genai

def gemini_summary(issues, prompt, key, model="gemini-2.0-flash"):
    client = genai.Client(api_key=key)
    
    prompt = f"{prompt} {issues}"
    response = client.models.generate_content(
        model=model, contents=prompt
    )
  
    if not response or not response.text:
        raise ValueError("Summary is null or empty.")

    return response.text
