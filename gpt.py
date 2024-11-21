import requests

def call_chatgpt(prompt,max_tokens, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for the GPT-3.5 model
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "temperature": 0.7,  # Adjust for creativity (0.0 for deterministic, 1.0 for creative)
        "max_tokens": max_tokens  # Adjust for desired response length
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    API_KEY = ""  # Replace with your OpenAI API key
    user_prompt = "can you tell me a what time is it ?"
    try:
        response = call_chatgpt(user_prompt, API_KEY)
        print("ChatGPT Response:")
        print(response)
    except Exception as e:
        print(e)
