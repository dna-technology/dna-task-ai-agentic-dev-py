import os

import google.generativeai as genai


class GeminiPlanner:
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
    generation_config = genai.types.GenerationConfig(response_mime_type="application/json")

    def __init__(self) -> None:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    async def decide(self, prompt: str) -> str:
        response = self.model.generate_content(prompt, generation_config=self.generation_config)

        return response.text or ""


def create_gemini_planner() -> GeminiPlanner:
    return GeminiPlanner()
