from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Win Predictor API is live"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

class MatchInput(BaseModel):
    current_score: int
    wickets: int
    overs_completed: float
    target: int

class MatchOutput(BaseModel):
    runs_needed: int
    balls_remaining: int
    required_run_rate: float
    prediction: str

@app.post("/predict/win", response_model=MatchOutput)
def predict(match: MatchInput):
    runs_needed = match.target - match.current_score
    
    balls_done = (int(match.overs_completed) * 6) + (round(match.overs_completed * 10) % 10)
    balls_remaining = 120 - balls_done
    
    if balls_remaining > 0:
        rrr = (runs_needed / balls_remaining) * 6
    else:
        rrr = 0.0

    if match.wickets >= 9 or rrr > 15:
        prob_label = "Low Chance"
    elif rrr > 10:
        prob_label = "Medium Chance"
    else:
        prob_label = "High Chance"

    return {
        "runs_needed": runs_needed,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(rrr, 2),
        "prediction": prob_label
    }