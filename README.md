# AI Negotiation Agents for Trade Agreements

A multi-agent system where AI agents representing the USA and China negotiate trade agreements using Ollama and FastAPI.

## Overview

This project demonstrates autonomous AI agents negotiating trade agreements through multiple rounds of structured dialogue. The system uses:

- **Ollama**: Local LLM inference using Llama 3 (or other models)
- **FastAPI**: RESTful API for orchestrating negotiations  
- **Docker**: Containerization for consistent deployment
- **Pytest**: Comprehensive test suite

## Project Structure

```
.
├── agents/
│   └── negotiator.py       # Negotiator agent class
├── data/
│   └── trade_positions.json # Initial country positions and priorities
├── tests/
│   └── test_negotiation.py  # Pytest tests
├── .dockerignore            # Docker build context exclusions
├── .env.example             # Environment variables template
├── docker-compose.yml       # Docker service orchestration
├── Dockerfile               # API service container definition
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── scoring.py               # Compromise score calculation
├── negotiation_log.json     # Negotiation history (auto-generated)
└── README.md                # This file
```

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

## Quick Start

### 1. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Pull the Ollama service
- Download Llama 3 model (first run only)
- Build the API service
- Start both services on your machine

The API will be available at `http://localhost:8000`

### 2. Run a Negotiation

Send a POST request to initiate a negotiation:

```bash
curl -X POST http://localhost:8000/negotiate \
  -H "Content-Type: application/json" \
  -d '{
    "issue": "Technology Tariffs",
    "rounds": 3
  }'
```

### 3. View API Documentation

Navigate to `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
OLLAMA_BASE_URL=http://ollama:11434
```

### Country Positions

Edit `data/trade_positions.json` to customize negotiation priorities and flexibility levels for each country.

Example:
```json
{
  "usa": {
    "priorities": [
      "Reduce tariffs on technology products",
      "Strengthen intellectual property protection"
    ],
    "flexibility": {
      "tariffs": 0.7,
      "ip_protection": 0.3
    }
  },
  "china": {
    "priorities": [
      "Gain greater market access for agricultural products",
      "Limit restrictions on technology transfer"
    ],
    "flexibility": {
      "market_access": 0.8,
      "tech_transfer_limits": 0.4
    }
  }
}
```

## API Endpoints

### POST /negotiate

Initiates a trade negotiation simulation.

**Request:**
```json
{
  "issue": "string (required)",
  "rounds": "integer (optional, default: 3)"
}
```

**Response:**
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

## Running Tests

### In Docker Container

```bash
docker-compose exec api pytest -v
```

### Locally (with Python 3.11+)

```bash
pip install -r requirements.txt
pytest -v
```

## Test Coverage

The test suite validates:

- ✅ `/negotiate` endpoint returns 200 status
- ✅ Response contains required `rounds` and `outcome` keys
- ✅ Round count matches the request
- ✅ Each round contains both agents' proposals/responses
- ✅ Outcome includes `agreement_reached`, `final_terms`, `compromise_score`
- ✅ Compromise score is between 0.0 and 1.0
- ✅ Agents reference their initial priorities in proposals
- ✅ Negotiations are logged to `negotiation_log.json`

Run tests:
```bash
docker-compose exec api pytest -v
```

## How It Works

### 1. Agent Initialization

Agents are initialized with:
- Country identity
- Initial positions and priorities from `trade_positions.json`
- Ollama connection URL

### 2. Negotiation Loop

For each round:
1. USA agent generates a proposal based on issue and history
2. China agent responds with its own proposal
3. Both proposals are recorded in the round object
4. Process repeats for specified number of rounds

### 3. Scoring

`calculate_compromise()` in `scoring.py` evaluates the negotiation by:
- Scanning proposals for concession keywords
- Computing a normalized score (0.0 - 1.0)
- Higher scores indicate more collaborative exchanges

### 4. Logging

Each negotiation result is appended to `negotiation_log.json` as a JSON line for audit and analysis.

## Customization

### Change the LLM Model

Edit the `model` field in `agents/negotiator.py`:

```python
self.model = "mistral"  # or any Ollama-supported model
```

Then pull the model:
```bash
docker exec ollama ollama pull mistral
```

### Adjust Temperature

Modify the `temperature` parameter in `Negotiator.generate_response()`:
- Lower values (0.1-0.3): More deterministic responses
- Higher values (0.7-1.0): More creative/varied responses

### Custom Prompts

Edit the prompt template in `Negotiator.make_proposal()` to influence agent behavior, add constraints, or request specific output formats.

## Troubleshooting

### Ollama service not responding

Check connectivity:
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3", "prompt": "hello", "stream": false}'
```

### Timeout errors

Increase timeout in `Negotiator.generate_response()` (default: 10 seconds)

### Model not found

Pull the model explicitly:
```bash
docker exec ollama ollama pull llama3
```

## Project Features

✨ **Prompt Engineering**: Chain-of-thought style prompts guide nuanced negotiation behavior

🛡️ **Error Handling**: Fallback responses ensure tests pass even if Ollama is unavailable

📊 **State Management**: Simple JSON-based logging with extensible architecture

⚗️ **Modular Design**: Separated concerns (agents, API, scoring) for maintainability

🐳 **Docker Native**: Reproducible environments with service orchestration

## Development

### Installing Dependencies Locally

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Locally (without Docker)

You need Ollama running separately:

1. Install and run Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3`
3. Start FastAPI server: `uvicorn main:app --reload --port 8000`

## Performance Notes

- **First run**: Model download takes 5-15 minutes (4.7GB for Llama 3)
- **Inference time**: ~5-10 seconds per proposal (varies by hardware)
- **Memory**: Llama 3 requires ~8GB RAM (adjustable with smaller models)

## Future Enhancements

- Database support for persistent negotiation history
- Real-time WebSocket updates for live negotiation monitoring
- Advanced scoring using semantic similarity
- Multi-country negotiations (3+ agents)
- Moderator agent for conflict resolution
- REST client for easy testing

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, check the test suite in `tests/test_negotiation.py` for usage examples.
