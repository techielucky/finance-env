from pydantic import BaseModel
from typing import Dict, Any, Optional

class Observation(BaseModel):
    balance: float
    savings: float
    expense: float
    goal: float

class Action(BaseModel):
    action: str  # invest, save, spend

class StepResult(BaseModel):
    state: Observation
    reward: float
    done: bool
    score: float