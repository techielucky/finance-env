import os
import json
import urllib.request

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")


def llm_call(prompt):
    url = API_BASE_URL

    data = json.dumps({
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
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
    url = f"{API_BASE_URL}{endpoint}"

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

        state = post_env("/reset")

        done = False

        while not done and step_count < 10:

            prompt = f"State: {state}. Choose one action: invest, save, spend."

            action = llm_call(prompt)

            if action not in ["invest", "save", "spend"]:
                action = "save"

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