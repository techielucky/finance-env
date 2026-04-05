from pydantic import BaseModel

class Observation(BaseModel):
    balance: int
    savings: int
    expense: int

class Action(BaseModel):
    action: str