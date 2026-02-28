# 🤖 AI Negotiation Agents for Trade Agreements

A multi-agent system where AI agents representing the USA and China negotiate trade agreements over multiple rounds using **Ollama (LLM)** and **FastAPI**, fully containerized with **Docker**.

---

# 📌 Overview

This project demonstrates a simplified **Multi-Agent System (MAS)** where:

- Two autonomous AI agents (USA and China) negotiate
- Each agent follows predefined priorities
- Negotiation occurs over multiple rounds
- A compromise score evaluates the outcome
- All results are logged persistently

The system runs entirely locally using **Ollama** for LLM inference.

---

# 🏗️ Architecture

**Tech Stack:**

- 🧠 Ollama (Llama 3 or other local models)
- 🚀 FastAPI (REST API backend)
- 🐳 Docker & Docker Compose (container orchestration)
- 🧪 Pytest (automated testing)

---

# 📁 Project Structure

```
.
├── agents/
│   └── negotiator.py        # Negotiator agent class
├── data/
│   └── trade_positions.json # Initial country priorities
├── tests/
│   └── test_negotiation.py  # Pytest test suite
├── .dockerignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── main.py                  # FastAPI entry point
├── requirements.txt
├── scoring.py               # Compromise scoring logic
├── negotiation_log.json     # Auto-generated at runtime
└── README.md
```

⚠️ `negotiation_log.json` is created automatically after the first negotiation.

---

# ✅ Prerequisites

- Docker Desktop installed
- Docker Compose enabled
- Minimum 8GB RAM recommended (for Llama 3)

---

# 🚀 Complete Setup Guide (Step-by-Step)

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/srujanaA02/ai-negotiation-agents-ollama.git
cd ai-negotiation-agents-ollama
```

---

## 2️⃣ Start Docker Services

```bash
docker-compose up -d --build
```

This will:

- Pull the `ollama/ollama` image
- Build the API container
- Start both services

Verify services are running:

```bash
docker-compose ps
```

You should see:

```
api      Up   0.0.0.0:8000->8000
ollama   Up   0.0.0.0:11434->11434
```

---

## 3️⃣ Pull the LLM Model (First Time Only)

```bash
docker exec -it ollama ollama pull llama3
```

⚠️ This may take several minutes (4–8 GB download).

---

## 4️⃣ Run Tests

```bash
docker-compose exec api pytest -v
```

Expected result:

```
9 passed
```

---

## 5️⃣ Access the API

Open in browser:

```
http://localhost:8000/docs
```

You will see Swagger UI.

---

## 6️⃣ Run a Negotiation

Example using curl:

```bash
curl -X POST http://localhost:8000/negotiate \
  -H "Content-Type: application/json" \
  -d '{
    "issue": "Technology Tariffs",
    "rounds": 3
  }'
```

Example Response:

```json
{
  "rounds": [
    {
      "round": 1,
      "usa_proposal": "...",
      "china_response": "..."
    }
  ],
  "outcome": {
    "agreement_reached": false,
    "final_terms": "...",
    "compromise_score": 0.2
  }
}
```

---

## 7️⃣ Verify Logging

After running negotiation:

```bash
ls
```

You should see:

```
negotiation_log.json
```

Each negotiation is appended as a JSON entry.

---

# 📡 API Specification

## POST `/negotiate`

### Request Body

```json
{
  "issue": "string (required)",
  "rounds": "integer (optional, default: 3)"
}
```

### Response Format

```json
{
  "rounds": [
    {
      "round": 1,
      "usa_proposal": "string",
      "china_response": "string"
    }
  ],
  "outcome": {
    "agreement_reached": boolean,
    "final_terms": "string",
    "compromise_score": float (0.0 - 1.0)
  }
}
```

---

# 🧠 How It Works

---

## 1️⃣ Agent Initialization

Agents load their priorities from:

```
data/trade_positions.json
```

Each country has:

- Strategic priorities
- Flexibility levels

---

## 2️⃣ Negotiation Loop

For each round:

1. USA generates a proposal
2. China responds
3. Both are appended to history
4. Loop continues for N rounds

---

## 3️⃣ Scoring Mechanism

`calculate_compromise()`:

- Scans proposals for concession keywords
- Computes normalized score
- Returns value between `0.0` and `1.0`

Higher score → more compromise.

---

## 4️⃣ Fallback Safety

If Ollama fails:

- Agents return deterministic fallback responses
- Ensures tests always pass
- Improves system robustness

---

# 🧪 Test Coverage

The test suite validates:

- `/negotiate` returns 200
- Rounds count matches input
- Each round contains both agents
- Outcome contains required keys
- Compromise score ∈ [0,1]
- Agents reference initial priorities
- Logging file is created
- Tests pass inside Docker container

Run tests:

```bash
docker-compose exec api pytest -v
```

---

# ⚙️ Configuration

## Environment Variables

`.env.example`

```
OLLAMA_BASE_URL=http://ollama:11434
```

---

## Modify Country Positions

Edit:

```
data/trade_positions.json
```

You can change priorities and flexibility levels.

---

# 🔧 Customization

## Change Model

In `agents/negotiator.py`:

```python
self.model = "mistral"
```

Then pull model:

```bash
docker exec -it ollama ollama pull mistral
```

---

## Adjust Temperature

Modify `temperature` in:

```python
generate_response()
```

Lower → deterministic  
Higher → creative

---

# 🛠 Troubleshooting

## Ollama Not Responding

```bash
docker-compose logs ollama
```

---

## Model Not Found

```bash
docker exec -it ollama ollama pull llama3
```

---

## Service Not Running

```bash
docker-compose up -d
```

---

# 📈 Performance Notes

- First model download: 5–15 minutes
- Inference time: ~5–10 seconds per proposal
- Recommended RAM: 8GB+

---

# 🔮 Future Enhancements

- Database-backed state persistence
- Multi-country negotiations (3+ agents)
- Semantic similarity scoring
- Moderator AI agent
- Web UI frontend
- WebSocket real-time updates

---

# 🏁 Conclusion

This project demonstrates:

- Multi-agent orchestration
- Prompt engineering
- LLM integration
- Docker containerization
- API development
- Automated testing
- Persistent logging
- Modular architecture

A practical introduction to autonomous AI systems and real-world backend AI development.
````

---

