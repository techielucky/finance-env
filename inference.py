import os
import json
import urllib.request

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
TASK_TYPE = os.getenv("TASK_TYPE", "easy") 

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is required")

ENV_API_BASE = "http://localhost:7860"

def llm_call(prompt):
    url = f"{API_BASE_URL.rstrip('/')}/chat/completions"
    data = json.dumps({
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Choose one: invest, save, spend."},
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read().decode())
    return result["choices"][0]["message"]["content"].strip().lower()

def post_env(endpoint, data=None):
    url = f"{ENV_API_BASE}{endpoint}"
    if data: data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

def main():
    print(f"[START] Task: {TASK_TYPE}")
    try:
        state = post_env(f"/reset?task={TASK_TYPE}")
        done = False
        step_idx = 0
        rewards = []
        final_score = 0.0

        while not done and step_idx < 10:
            action_raw = llm_call(f"State: {state}")
            action = "save"
            for a in ["invest", "save", "spend"]:
                if a in action_raw:
                    action = a
                    break
            
            result = post_env("/step", {"action": action})
            state = result.get("state")
            done = result.get("done")
            reward = float(result.get("reward", 0.0))
            final_score = result.get("score", 0.0)
            
            rewards.append(reward)
            step_idx += 1
            print(f"[STEP] {step_idx} reward={reward}")

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success=true steps={step_idx} rewards={rewards_str} score={final_score}")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("[END] success=false steps=0 rewards= score=0.0")

if __name__ == "__main__":
    main()