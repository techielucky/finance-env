from fastapi import FastAPI
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


# ✅ REQUIRED: callable main()
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ REQUIRED: script entrypoint
if __name__ == "__main__":
    main()