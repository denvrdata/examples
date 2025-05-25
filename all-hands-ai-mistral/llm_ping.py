import requests
import json
import argparse
from huggingface_hub import hf_hub_download

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="AI model interaction script.")
parser.add_argument("ip_address", help="The IP address of the server to connect to.")
args = parser.parse_args()

# Use the IP address from the command line argument
url = f"http://{args.ip_address}:8000/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}

model_id = "mistralai/Devstral-Small-2505"
model = model_id

def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    return system_prompt

SYSTEM_PROMPT = load_system_prompt(model_id, "SYSTEM_PROMPT.txt")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Write a python script that prints 'Hello, World!'",
            },
        ],
    },
]

data = {"model": model, "messages": messages, "temperature": 0.15}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json()["choices"][0]["message"]["content"])
