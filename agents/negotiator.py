import httpx
import asyncio


class Negotiator:
    def __init__(self, country: str, positions: dict, ollama_url: str):
        self.country = country
        self.positions = positions
        self.ollama_url = ollama_url
        self.model = "llama3"

    async def generate_response(self, prompt: str) -> str:
        max_retries = 3
        backoff_seconds = 1

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.ollama_url}/api/generate",
                        json={
                            "model": self.model,
                            "prompt": prompt,
                            "stream": False,
                            "temperature": 0.3
                        },
                        timeout=20.0
                    )
                    response.raise_for_status()
                    body = response.json()
                    model_response = body.get("response", "").strip()
                    if model_response:
                        return model_response
            except Exception:
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_seconds * (2 ** attempt))

        return self._fallback_response()

    def _fallback_response(self) -> str:
        if self.country.lower() == "usa":
            return "We propose reducing tariffs and strengthening intellectual property protection."
        else:
            return "We propose increasing market access for agricultural products and limiting technology transfer restrictions."

    async def make_proposal(self, issue: str, history: list):
        prompt = f"""
        You are a trade negotiator representing {self.country}.
        Your priorities are:
        {', '.join(self.positions['priorities'])}

        Negotiation topic: {issue}
        Negotiation history: {history}

        Make a concise one-sentence proposal.
        """
        return await self.generate_response(prompt)