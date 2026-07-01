import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN environment variable is not set.")

MODEL = "ibm-granite/granite-7b-instruct"
API_URL = f"https://router.huggingface.co/featherless-ai/v1/chat/completions"
OUTPUT_PATH = "results/coaching_output.txt"

with open("telemetry.json", "r") as f:
    telemetry = json.load(f)

telemetry_str = json.dumps(telemetry, indent=2)

system_prompt = """You are an expert AI racing coach for the TORCS racing simulator.

Respond in exactly this structure, and nothing else:

Current Performance Summary
(2-3 sentences)

Top 3 Parameter Recommendations
1. ...
2. ...
3. ...
(each with a specific value to try)

One Advanced Suggestion
(a single concrete next step)

Do not add a self-evaluation, confidence score, or any commentary after the Advanced Suggestion."""

prompt = f"""A driver has shared their latest lap telemetry data with you. Analyze it carefully.

Telemetry data:
{telemetry_str}"""

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 400,
    "temperature": 0.7,
    "stop": ["Confidence:"],
}

print("Sending telemetry to Granite racing coach...")

response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()

result = response.json()
coaching_text = result["choices"][0]["message"]["content"]

print("\n--- Granite Racing Coach ---\n")
print(coaching_text)

os.makedirs("results", exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    f.write(coaching_text)

print(f"\nCoaching output saved to {OUTPUT_PATH}")
