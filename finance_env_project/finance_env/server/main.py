from fastapi import FastAPI
from .finance_env_environment import FinanceEnvironment

app = FastAPI()

env = FinanceEnvironment()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: str):
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }