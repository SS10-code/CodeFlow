import requests

def query_deepseek(prompt, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    get_header = {"Authorization": f"Bearer {api_key}","Content-Type": "application/json"}

    #context for the ai
    request_payloads =  {"model":"deepseek/deepseek-r1-0528:free",  "messages":[{"role": "system","content":"You are an expert Python software developer. When asked to, write clean Python code based on a flowchart description." },  {"role": "user", "content": prompt } ]}

    response = requests.post(url, headers = get_header, json = request_payloads)#reply

    result =  response.json()
    
    return result["choices"][0]["message"]["content"]



