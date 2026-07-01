# 🏎️ Granite TORCS Coach

## The Problem
Tuning an autonomous racing AI agent is trial and error — small parameter changes have huge effects and there's no intelligent feedback on what to adjust next.

## AI/Technical Approach
- TORCS simulator used to run an autonomous driving agent
- Lap telemetry (speed, damage, parameters) captured after each run
- IBM Granite (granite-7b-instruct) via Hugging Face analyzes the telemetry
- Granite acts as an AI racing coach, giving structured parameter recommendations
- Output saved to `results/coaching_output.txt` for the next tuning iteration

## Why This Matters for Racing
Real racing teams rely on engineers to analyze telemetry and suggest setup changes between sessions. This project brings that same feedback loop to autonomous AI drivers — closing the gap between simulation and intelligent self-improvement.

## IBM Technology Used
- IBM Granite (`ibm-granite/granite-7b-instruct`) via Hugging Face Inference API

## How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/Hitakshi02/granite-torcs-coach
   cd granite-torcs-coach
   ```

2. Set up your environment file:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Hugging Face token:
   ```
   HF_TOKEN=your_hf_token_here
   ```
   You can generate a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the coach:
   ```bash
   python coach.py
   ```

The coaching output is printed to the console and saved to `results/coaching_output.txt`.

## Sample Output

```
Current Performance Summary:
The driver has demonstrated strong performance on the Forza track, completing it with 0 damage. However, they experienced crashes when pushing speed on tight corners.

Top 3 Parameter Recommendations:
1. Steer_gain: Try decreasing steer_gain by 5% to improve handling in corners.
2. Brake_threshold: Adjust brake_threshold to 0.35 to better approach corners.
3. Centering_gain: Experiment with increasing centering_gain by 5% to maintain stability during high-speed sections.

One Advanced Suggestion: Implement dynamic speed control that automatically slows the car before corners to prevent crashes. This can be achieved by analyzing the car's speed and steering angle and adjusting the target speed accordingly.
```

## Results from TORCS Lab
- Best configuration: `TARGET_SPEED=160`, `STEER_GAIN=45`, `CENTERING_GAIN=0.60`, `BRAKE_THRESHOLD=0.4`
- Track: Forza — completed with 0 damage, top speed 167 km/h
- Key learning: small parameter changes have outsized effects on agent behavior
