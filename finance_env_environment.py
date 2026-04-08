import random
from grader import grade

class FinanceEnv:
    def __init__(self, task="easy"):
        self.reset(task)

    def reset(self, task="easy"):
        self.task = task
        # Different starting conditions based on task
        if task == "easy":
            self.balance = 1200
        elif task == "medium":
            self.balance = 800
        else: # hard
            self.balance = 400

        self.savings = 0
        self.expense = 0
        self.step_count = 0
        self.goal = 1000

        return self.state()

    def step(self, action):
        reward = 0.0

        # ===== ACTION LOGIC =====
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

        # ===== STOCHASTIC EVENTS =====
        event = random.choice(["none", "none", "bonus", "emergency"])
        if event == "bonus":
            self.balance += 200
        elif event == "emergency":
            self.balance -= 150

        self.step_count += 1
        
        # Done if max steps reached or bankrupt
        done = self.step_count >= 10 or self.balance <= 0

        # ===== GRADING =====
        # We pass self.task so the grader can validate multiple tasks
        final_score = grade(self.state(), self.task) if done else 0.0

        return {
            "state": self.state(),
            "reward": max(-5.0, min(5.0, reward)),
            "done": done,
            "score": final_score,
            "event": event,
            "info": {"task": self.task}
        }

    def state(self):
        return {
            "balance": self.balance,
            "savings": self.savings,
            "expense": self.expense,
            "goal": self.goal
        }