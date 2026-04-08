from fastapi import FastAPI, Query
from finance_env_environment import FinanceEnv

app = FastAPI()
env = FinanceEnv()

@app.post("/reset")
def reset(task: str = Query("easy")):
    return env.reset(task=task)

@app.post("/step")
def step(data: dict):
    action = data.get("action", "save")
    return env.step(action)

@app.get("/state")
def state():
    return env.state()

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()