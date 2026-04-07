from fastapi import FastAPI
import uvicorn

from server.finance_env_environment import FinanceEnv

app = FastAPI()
env = FinanceEnv()


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: str):
    return env.step(action)


@app.get("/state")
def state():
    return env.state()


# ✅ REQUIRED ENTRYPOINT
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ MUST BE PRESENT
if __name__ == "__main__":
    main()