import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_negotiate_endpoint_exists():
    """Test that the /negotiate endpoint exists and returns 200."""
    response = client.post("/negotiate", json={"issue": "Technology Trade", "rounds": 1})
    assert response.status_code == 200

def test_negotiation_three_rounds():
    """Test that negotiation with rounds:3 returns exactly 3 rounds."""
    response = client.post("/negotiate", json={"issue": "Technology Trade", "rounds": 3})
    assert response.status_code == 200
    data = response.json()
    assert "rounds" in data
    assert "outcome" in data
    assert len(data["rounds"]) == 3

def test_negotiation_single_round():
    """Test that rounds parameter works with rounds:1."""
    response = client.post("/negotiate", json={"issue": "Test", "rounds": 1})
    data = response.json()
    assert len(data["rounds"]) == 1

def test_round_contains_both_agents():
    """Test that each round contains proposals from both USA and China."""
    response = client.post("/negotiate", json={"issue": "Technology Trade", "rounds": 1})
    data = response.json()
    
    round_obj = data["rounds"][0]
    assert "round" in round_obj
    assert "usa_proposal" in round_obj
    assert "china_response" in round_obj
    assert isinstance(round_obj["usa_proposal"], str)
    assert isinstance(round_obj["china_response"], str)
    assert len(round_obj["usa_proposal"]) > 0
    assert len(round_obj["china_response"]) > 0

def test_outcome_structure():
    """Test that outcome object contains required keys with correct types."""
    response = client.post("/negotiate", json={"issue": "Trade", "rounds": 2})
    data = response.json()
    
    outcome = data["outcome"]
    assert "agreement_reached" in outcome
    assert "final_terms" in outcome
    assert "compromise_score" in outcome
    
    assert isinstance(outcome["agreement_reached"], bool)
    assert isinstance(outcome["final_terms"], str)
    assert isinstance(outcome["compromise_score"], (int, float))

def test_compromise_score_range():
    """Test that compromise_score is between 0.0 and 1.0 inclusive."""
    response = client.post("/negotiate", json={"issue": "Trade", "rounds": 3})
    data = response.json()
    
    score = data["outcome"]["compromise_score"]
    assert 0.0 <= score <= 1.0

def test_priorities_referenced():
    """Test that agents' proposals reference their initial priorities."""
    response = client.post("/negotiate", json={"issue": "Trade", "rounds": 1})
    data = response.json()

    usa_text = data["rounds"][0]["usa_proposal"].lower()
    china_text = data["rounds"][0]["china_response"].lower()

    # USA priorities: tariffs, intellectual property
    assert "intellectual" in usa_text or "tariff" in usa_text or "ip" in usa_text
    
    # China priorities: market access, technology transfer
    assert "market" in china_text or "technology" in china_text or "transfer" in china_text

def test_negotiation_logging():
    """Test that negotiations are logged to negotiation_log.json."""
    # Remove the log file if it exists
    log_file = "negotiation_log.json"
    if os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")  # Clear the file
    
    # Make a request
    response = client.post("/negotiate", json={"issue": "Trade Negotiation", "rounds": 2})
    assert response.status_code == 200
    
    # Check that log file exists and contains the negotiation
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        log_content = f.read()
        assert len(log_content) > 0
        # Parse the JSON line
        log_entry = json.loads(log_content.strip().split('\n')[-1])
        assert "rounds" in log_entry
        assert "outcome" in log_entry
        assert len(log_entry["rounds"]) == 2

def test_default_rounds():
    """Test that default rounds is 3 when not specified."""
    response = client.post("/negotiate", json={"issue": "Test"})
    data = response.json()
    assert len(data["rounds"]) == 3
