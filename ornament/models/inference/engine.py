import json
import re
from typing import Type, Any, Optional
from pydantic import BaseModel

class InferenceEngine:
    """
    Inference helper for response cleaning, JSON schema extraction, and context window trimming.
    """

    @staticmethod
    def extract_json(text: str) -> dict:
        """
        Extracts JSON from text, accommodating markdown ```json ... ``` enclosures.
        """
        text = text.strip()
        # Look for markdown code fence
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            candidate = match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass

        # Try raw JSON
        # Find first '{' or '[' and matching end
        start_obj = text.find("{")
        end_obj = text.rfind("}")
        if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
            candidate = text[start_obj:end_obj + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

        # Fallback to direct parse
        return json.loads(text)

    @staticmethod
    def parse_to_model(text: str, schema: Type[BaseModel]) -> BaseModel:
        data = InferenceEngine.extract_json(text)
        return schema.model_validate(data)
