import random
from grader import grade

class FinanceEnv:
    def __init__(self, task="easy"):
        self.reset(task)

    def reset(self, task="easy"):
        self.task = task

        if task == "easy":
            self.balance = 1200
        elif task == "medium":
            self.balance = 800
        else:
            self.balance = 400

        self.savings = 0
        self.expense = 0
        self.step_count = 0

        # 🔥 GOAL SYSTEM
        self.goal = 1000

        return self.state()

def step(self, action):
    reward = 0

    # ===== ACTION EFFECT =====
    if action == "invest":
        if self.balance >= 100:
            self.balance -= 100
            self.savings += 150
            reward += 1.5
        else:
            reward -= 2.0

    elif action == "save":
        if self.balance >= 50:
            self.balance -= 50
            self.savings += 50
            reward += 1.0
        else:
            reward -= 1.5

    elif action == "spend":
        self.balance -= 100
        self.expense += 100
        reward -= 1.5

    else:
        reward -= 3.0

    # ===== STATE IMPROVEMENT =====
    net_worth = self.balance + self.savings - self.expense

    if net_worth > 500:
        reward += 1.0
    elif net_worth < 0:
        reward -= 2.0

    # ===== GOAL PROGRESS =====
    progress = self.savings / self.goal
    reward += progress * 2.0

    # ===== BAD BEHAVIOR =====
    if self.expense > self.savings:
        reward -= 1.0

    # ===== RANDOM EVENTS =====
    event = random.choice(["none", "bonus", "emergency"])

    if event == "bonus":
        self.balance += 200
        reward += 0.5

    elif event == "emergency":
        self.balance -= 150
        reward -= 0.7

    self.step_count += 1

    done = self.step_count >= 10 or self.balance <= 0

    # ===== FINAL REWARD NORMALIZATION =====
    reward = max(-5.0, min(5.0, reward))

    # ===== FINAL SCORE =====
    final_score = grade(self.state()) if done else 0.0

    return {
        "state": self.state(),
        "reward": reward,
        "done": done,
        "score": final_score,
        "event": event,
        "info": {}
    }

    def state(self):
        return {
            "balance": self.balance,
            "savings": self.savings,
            "expense": self.expense,
            "goal": self.goal
        }