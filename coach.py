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
    laps = json.load(f)

telemetry_str = json.dumps(laps, indent=2)

system_prompt = """You are an expert AI racing coach for the TORCS racing simulator.

You will be shown telemetry from multiple laps, side by side. Respond in exactly this structure, and nothing else:

Best Lap Analysis
(identify which lap performed best and why, 2-3 sentences)

Trend Identified
(what changed across the laps and how it affected performance, 2-3 sentences)

Recommended Lap 4 Configuration
target_speed: ...
steer_gain: ...
centering_gain: ...
brake_threshold: ...

Reasoning
(explain the reasoning behind each recommended value above)

When analyzing trends, lower damage values are better. Damage decreased from 847 to 212 to 0 across laps, meaning performance improved. Do not say damage increased when the numbers show it decreased.

Do not add a self-evaluation, confidence score, or any commentary after the Reasoning section."""

prompt = f"""A driver has shared telemetry data from their last {len(laps)} laps, in chronological order. Compare them carefully.

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
    "stop": ["Confidence:", "<|end|>"],
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
