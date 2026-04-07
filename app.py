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


# 🔥 REQUIRED MAIN FUNCTION (STRICT FORMAT)
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# 🔥 REQUIRED CALL
if __name__ == "__main__":
    main()