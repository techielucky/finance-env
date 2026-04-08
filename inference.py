import requests
import os
import time
from openai import OpenAI

# Environment API URL (Your Docker container)
API_URL = "http://localhost:7860"

def get_client():
    """Initializes the OpenAI client using the validator's LiteLLM proxy."""
    # 🚨 CRITICAL: Use these exact keys provided by the validator
    api_key = os.environ.get("API_KEY") 
    base_url = os.environ.get("API_BASE_URL")
    
    if not api_key or not base_url:
        print("[ERROR] Missing proxy credentials (API_KEY or API_BASE_URL).")
        return None

    # This routes calls through the hackathon proxy instead of direct OpenAI 
    return OpenAI(base_url=base_url, api_key=api_key)

def post_env(endpoint, data=None):
    """Communicates with your local environment server."""
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data if data else {}, timeout=5)
        return resp.json()
    except Exception as e:
        print(f"[ERROR] Environment connection failed: {e}")
        return {}

def run_task(task_type):
    """Runs a single difficulty tier through the proxy."""
    print(f"[START] task={task_type}") 
    client = get_client()
    
    try:
        state = post_env(f"/reset?task={task_type}")
        done = False
        step_count = 0
        rewards = []
        final_score = 0.01

        while not done and step_count < 10:
            # 💡 Tip: Heuristic saves credits if balance is too low [cite: 6, 7, 8]
            if state.get("balance", 0) < 50:
                action = "save"
            elif client is None:
                action = "save"
            else:
                try:
                    # 💡 Tip: Smaller model (8B) and tiny max_tokens for cost [cite: 3, 4, 14, 15]
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.1-8B-Instruct", 
                        messages=[{"role": "user", "content": f"State: {state}. Reply: invest, save, or spend."}],
                        max_tokens=10, 
                        temperature=0
                    )
                    action_raw = response.choices[0].message.content.strip().lower()
                    action = "save"
                    for a in ["invest", "save", "spend"]:
                        if a in action_raw:
                            action = a
                            break
                except Exception:
                    action = "save"

            result = post_env("/step", {"action": action})
            reward = float(result.get("reward", 0.0))
            done = result.get("done", False)
            state = result.get("observation") or result.get("state") or {}
            
            if done:
                info = result.get("info", {})
                final_score = float(info.get("score") or result.get("score") or 0.01)

            rewards.append(reward)
            step_count += 1
            print(f"[STEP] step={step_count} reward={reward:.2f}")

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success=true steps={step_count} rewards={rewards_str} score={final_score:.3f}")
    
    except Exception as e:
        print(f"[END] success=false steps=0 rewards= score=0.01")

def main():
    # Looping through all 3 tasks as required for Phase 2 
    for task_difficulty in ["easy", "medium", "hard"]:
        run_task(task_difficulty)
        time.sleep(1)

if __name__ == "__main__":
    main()