import requests

def deepseek_summary(issues, prompt, key, model="deepseek-chat"):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    prompt = f"{prompt} {issues}"
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if not result.choices:
            raise ValueError("No response choices available")
        if not result.choices[0]:
            raise ValueError("First choice is null")
        if not result.choices[0].message:
            raise ValueError("Message is null")

        summary = result.choices[0].message.content
        if not summary:
            raise ValueError("Summary is null or empty.")

        return summary
    else:
        raise ValueError("Request failed with status code: " + str(response.status_code))