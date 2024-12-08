import torch
from transformers import pipeline
import requests
import threading
import time, os
from concurrent.futures import ThreadPoolExecutor, as_completed


llm_host = os.getenv('LLM_HOST', '')  # Replace 'LLM_HOST' with your env variable name
server_url = f"http://{llm_host}/v1/chat/completions"
headers = {"Content-Type": "application/json"}


# Check if GPU is available
if not torch.cuda.is_available():
    print("GPU is not available. Ensure your environment has access to a GPU.")
else:
    print(f"GPU detected: {torch.cuda.get_device_name(0)}")

# Define the model ID
model_id = "meta-llama/Llama-3.2-1B-Instruct"

# Initialize the pipeline with GPU support
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,  # Use bfloat16 for faster inference on supported GPUs
    device=0  # Explicitly use GPU
)

# Generate text with extended response length
output = pipe(
    "Generate a list of creative and challenging writing prompts. Only list the prompts, no explanation or numbering",
    max_length=2000,  # Allow up to 512 tokens in the response
    min_length=100,  # Ensure at least 100 tokens in the response
    temperature=0.7,  # Control randomness
    top_p=0.9  # Enable diverse sampling
)

# Print the output
print(output[0]["generated_text"])

prompts = output[0]["generated_text"].split('\n')

tgi_model = "meta-llama/Llama-3.3-70B-Instruct"

def send_request(prompt):
    data = {
        "model": tgi_model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    response = requests.post(server_url, headers=headers, json=data)
    print(response)
    if response.status_code == 200:
        return prompt, response.json()
    else:
        response.raise_for_status()
    

# Use ThreadPoolExecutor for concurrent requests
results = []
with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust number of workers as needed
    future_to_prompt = {executor.submit(send_request, prompt): prompt for prompt in prompts}
    for future in as_completed(future_to_prompt):
        prompt, response = future.result()
        results.append((prompt, response))
        print(f"\nPrompt:\n{prompt}")
        print(f"Response:\n{response}")

# Display all results
print("\nAll Results:")
for prompt, response in results:
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print("\n---\n")
