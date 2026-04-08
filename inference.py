import os
from openai import OpenAI
import requests

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


def log_start():
    print("[START]")


def log_step(step, reward):
    print(f"[STEP] step={step} reward={reward:.2f}")


def log_end(success, steps, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")


def get_action(state):
    prompt = f"""
You are a financial decision agent.

State:
{state}

Choose ONE action from:
- invest
- save
- spend

Respond with ONLY the action.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    action = response.choices[0].message.content.strip().lower()

    if action not in ["invest", "save", "spend"]:
        action = "save"

    return action


def main():
    try:
        log_start()

        rewards = []
        step_count = 0
        success = False

        # RESET
        res = requests.post(f"{API_BASE_URL}/reset")
        state = res.json()

        done = False

        while not done and step_count < 10:

            action = get_action(state)

            res = requests.post(
                f"{API_BASE_URL}/step",
                params={"action": action}
            )

            result = res.json()

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