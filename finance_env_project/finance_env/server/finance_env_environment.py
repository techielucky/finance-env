from typing import Tuple, Dict, Any

class FinanceEnvironment:

    def __init__(self):
        self.balance = 1000
        self.savings = 0
        self.expense = 0
        self.step_count = 0
        self.done = False

    def reset(self) -> Dict[str, Any]:
        self.balance = 1000
        self.savings = 0
        self.expense = 0
        self.step_count = 0
        self.done = False
        return self.state()

    def state(self) -> Dict[str, Any]:
        return {
            "balance": self.balance,
            "savings": self.savings,
            "expense": self.expense
        }

    def step(self, action: str) -> Tuple[Dict, float, bool, Dict]:
        reward = 0.0

        if action == "spend":
            self.balance -= 100
            self.expense += 100
            reward = -0.5

        elif action == "save":
            self.balance -= 50
            self.savings += 50
            reward = 1.0

        elif action == "invest":
            self.balance -= 100
            self.savings += 150
            reward = 1.5

        self.step_count += 1

        if self.balance <= 0 or self.step_count >= 10:
            self.done = True

        return self.state(), reward, self.done, {}