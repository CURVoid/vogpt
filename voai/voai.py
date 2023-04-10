import requests

class GPT35Turbo:
    def __init__(self, key: str):
        self.key = key
        self.history = []

    def ask(self, query: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 300:
            raise RuntimeError(f"{response.status_code} {response.json()['error']['message']}")

        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def ask_with_context(self, query: str):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

        self.history += [{
            "role": "user",
            "content": query
        }]
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": message["role"],
                    "content": message["content"]
                } for message in self.history
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 300:
            raise RuntimeError(f"{response.status_code} {response.json()['error']['message']}")

        data = response.json()
        message = data["choices"][0]["message"]["content"]
        
        self.history += [{
            "role": "assistant",
            "content": message
        }]
        return message
    
class Davinci3: # continues text, for example if you ask him "Hello, world" he will return "!" 
    def __init__(self, key: str):
        self.key = key

    def ask(self, query: str, temperature: float = 0.5) -> str:
        url = "https://api.openai.com/v1/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

        payload = {
            "model": "text-davinci-003",
            "prompt": query,
            "temperature": temperature,
            "n": 1,
            "stop": "\n"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 300:
            raise RuntimeError(f"{response.status_code} {response.json()['error']['message']}")

        data = response.json()
        return data["choices"][0]["text"]