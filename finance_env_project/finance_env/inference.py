import os
import json
import urllib.request

# 🚨 CRITICAL: Use the system-injected variables for the LLM proxy
LLM_API_BASE = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

# 🏠 LOCAL: Point this to your FastAPI server running in the same container
ENV_API_BASE = "http://0.0.0.0:7860"

def llm_call(prompt):
    # Standardize the URL for Chat Completions
    url = LLM_API_BASE
    if not url.endswith("/chat/completions"):
        url = f"{url.rstrip('/')}/chat/completions"

    data = json.dumps({
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a financial advisor. Reply ONLY with the action name."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0 # Keep it deterministic for hackathons
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    return result["choices"][0]["message"]["content"].strip().lower()

def post_env(endpoint, data=None):
    # Use the LOCAL environment base URL here
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

def log_start():
    print("[START]")

def log_step(step, reward):
    print(f"[STEP] step={step} reward={reward:.2f}")

def log_end(success, steps, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")

def main():
    try:
        log_start()
        rewards = []
        step_count = 0
        success = False

        # Reset the local environment
        state = post_env("/reset")
        done = False

        while not done and step_count < 10:
            prompt = f"Current State: {state}. Choose one: invest, save, spend."
            
            action = llm_call(prompt)

            # Robustness check for LLM output
            valid_actions = ["invest", "save", "spend"]
            if action not in valid_actions:
                # Basic parsing if LLM adds extra text
                found = False
                for v in valid_actions:
                    if v in action:
                        action = v
                        found = True
                        break
                if not found:
                    action = "save" # Default fallback

            result = post_env("/step", {"action": action})

            reward = float(result.get("reward", 0.0))
            done = result.get("done", False)
            state = result.get("state", {})

            rewards.append(reward)
            step_count += 1
            log_step(step_count, reward)

        if done:
            success = True

        log_end(success, step_count, rewards)

    except Exception as e:
        print("[ERROR]", str(e))
        log_end(False, 0, [])

if __name__ == "__main__":
    main()