import os
import json

from dotenv import load_dotenv
from google import genai

from app.schemas.authorization import AuthorizationRequest


load_dotenv()


class ExtractionAgent:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        self.client = genai.Client(api_key=api_key)

    def extract(self, text: str) -> AuthorizationRequest:

        prompt = f"""
You are a healthcare prior authorization data extraction agent.

Extract the following information from the document text:

- Patient name
- Patient date of birth
- Provider name
- Procedure description
- Diagnosis description
- Payer name
-Clinical notes

Return ONLY valid JSON matching this exact structure:

{{
    "patient": {{
        "name": "...",
        "date_of_birth": "..."
    }},
    "provider": {{
        "name": "..."
    }},
    "procedure": {{
        "description": "..."
    }},
    "diagnosis": {{
        "description": "..."
    }},
    "payer": {{
        "name": "..."
    }},
    "clinical_notes": "..."
}}

Do not add markdown.
Do not add explanations.

Document text:
{text}
"""

        interaction = self.client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )

        response_text = interaction.output_text.strip()

        data = json.loads(response_text)

        return AuthorizationRequest.model_validate(data)