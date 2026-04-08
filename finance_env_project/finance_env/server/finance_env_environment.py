import random
from grader import grade

class FinanceEnv:
    def __init__(self):
        self.task = "easy"
        self.reset()

    def reset(self, task="easy"):
        self.task = task
        self.step_count = 0
        self.savings = 0
        self.expense = 0
        self.goal = 1000
        
        if task == "easy":
            self.balance = 1200
        elif task == "medium":
            self.balance = 800
        else:
            self.balance = 400
            
        return self.state()

    def step(self, action):
        reward = 0.0
        if action == "invest":
            if self.balance >= 100:
                self.balance -= 100
                self.savings += 150
                reward = 1.0
            else: reward = -1.0
        elif action == "save":
            if self.balance >= 50:
                self.balance -= 50
                self.savings += 50
                reward = 0.5
            else: reward = -0.5
        else: # spend
            self.balance -= 100
            self.expense += 100
            reward = -1.0

        self.step_count += 1
        done = self.step_count >= 10 or self.balance <= 0

        # Score is only returned on the final step
        final_score = 0.0
        if done:
            final_score = float(grade(self.state(), self.task))

        return {
            "state": self.state(),
            "reward": reward,
            "done": done,
            "score": final_score
        }

    def state(self):
        return {
            "balance": self.balance,
            "savings": self.savings,
            "expense": self.expense,
            "goal": self.goal
        }