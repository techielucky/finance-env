import os
import json
import urllib.request

# 🚨 UPDATED: Using the logic from the Hackathon Bot
# The bot says HF_TOKEN is used as the api_key
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 🏠 LOCAL: Point this to your FastAPI server running in the container
ENV_API_BASE = "http://localhost:7860"

def llm_call(prompt):
    url = f"{API_BASE_URL.rstrip('/')}/chat/completions"

    data = json.dumps({
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a financial advisor. Reply ONLY with: invest, save, or spend."},
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}", # Use HF_TOKEN here
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    return result["choices"][0]["message"]["content"].strip().lower()

def post_env(endpoint, data=None):
    url = f"{ENV_API_BASE}{endpoint}"
    if data:
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def main():
    print("[START]")
    try:
        state = post_env("/reset")
        rewards = []
        step_count = 0
        done = False

        while not done and step_count < 10:
            prompt = f"State: {state}. Action?"
            action_raw = llm_call(prompt)
            
            # Simple parsing
            action = "save"
            for a in ["invest", "save", "spend"]:
                if a in action_raw:
                    action = a
                    break

            result = post_env("/step", {"action": action})
            reward = float(result.get("reward", 0.0))
            done = result.get("done", False)
            state = result.get("state", {})
            
            rewards.append(reward)
            step_count += 1
            print(f"[STEP] step={step_count} reward={reward:.2f}")

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success=true steps={step_count} rewards={rewards_str}")

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("[END] success=false steps=0 rewards=")

if __name__ == "__main__":
    main()