import random

from server.finance_env_environment import FinanceEnvironment
from grader import grade_easy, grade_medium, grade_hard


env = FinanceEnvironment()

state = env.reset()
total_reward = 0
steps = 0

print("[START] task=finance env=finance_env model=baseline")

while True:
    action = random.choice(["spend", "save", "invest"])

    state, reward, done, _ = env.step(action)

    print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    total_reward += reward
    steps += 1

    if done:
        break

# grading
easy_score = grade_easy(state)
medium_score = grade_medium(state)
hard_score = grade_hard(state)

final_score = (easy_score + medium_score + hard_score) / 3

print(f"[END] success=true steps={steps} rewards={total_reward:.2f} score={final_score:.2f}")