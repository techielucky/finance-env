from fastapi import FastAPI
from server.finance_env_environment import FinanceEnv

app = FastAPI()

env = FinanceEnv()


# 🔁 RESET
@app.post("/reset")
def reset():
    return env.reset()


# ⚡ STEP
@app.post("/step")
def step(action: str):
    return env.step(action)


# 📊 STATE
@app.get("/state")
def state():
    return env.state()


# 🚀 REQUIRED ENTRYPOINT (IMPORTANT FOR VALIDATION)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)