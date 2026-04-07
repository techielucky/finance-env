import requests

BASE_URL = "https://lucky02006-finance-env.hf.space"

print("[START] task=finance env=finance_env model=baseline")

state = requests.post(f"{BASE_URL}/reset", params={"task": "medium"}).json()

total_reward = 0

for step in range(10):
    action = "save"

    res = requests.post(f"{BASE_URL}/step", params={"action": action}).json()

    reward = res["reward"]
    done = res["done"]
    event = res.get("event", "none")

    total_reward += reward

    print(f"[STEP] step={step} action={action} reward={reward} event={event} done={done}")

    if done:
        score = res.get("score", 0.0)
        print(f"[END] success=True steps={step+1} rewards={total_reward:.2f} score={score:.2f}")
        break