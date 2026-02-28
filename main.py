from fastapi import FastAPI, HTTPException
import json
import os
from agents.negotiator import Negotiator
from scoring import calculate_compromise

app = FastAPI()

# Load positions
with open("./data/trade_positions.json") as f:
    positions = json.load(f)

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

usa_agent = Negotiator("USA", positions["usa"], OLLAMA_URL)
china_agent = Negotiator("China", positions["china"], OLLAMA_URL)

@app.post("/negotiate")
async def negotiate(request: dict):
    issue = request.get("issue")
    rounds = request.get("rounds", 3)

    if not isinstance(issue, str) or not issue.strip():
        raise HTTPException(status_code=400, detail="'issue' is required and must be a non-empty string")
    if not isinstance(rounds, int) or rounds < 1:
        raise HTTPException(status_code=400, detail="'rounds' must be an integer >= 1")

    history = []

    for i in range(rounds):
        usa_proposal = await usa_agent.make_proposal(issue, history)
        china_response = await china_agent.make_proposal(issue, history)

        history.append({
            "round": i + 1,
            "usa_proposal": usa_proposal,
            "china_response": china_response
        })

    compromise_score = calculate_compromise(history, positions)

    # Create final terms summary
    if history:
        last_round = history[-1]
        final_terms = f"Round {last_round['round']}: USA: {last_round['usa_proposal'][:100]}... China: {last_round['china_response'][:100]}..."
    else:
        final_terms = "No rounds completed"

    outcome = {
        "agreement_reached": compromise_score > 0.6,
        "final_terms": final_terms,
        "compromise_score": compromise_score
    }

    result = {
        "rounds": history,
        "outcome": outcome
    }

    # Log negotiation
    with open("negotiation_log.json", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(result) + "\n")

    return result