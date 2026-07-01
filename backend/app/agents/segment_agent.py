"""Segment / audience generation agent."""
import os
import json
from openai import OpenAI

class SegmentAgent:
    """Generates audience definitions from natural-language goals."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_audience(
        self, goal: str, event_schema: dict | None = None
    ) -> dict:
        """Return generated audience definition with inclusion/exclusion rules."""
        if self.client:
            prompt = (
                f"Goal: {goal}\n"
                f"Event Schema: {json.dumps(event_schema) if event_schema else 'None'}\n\n"
                "Generate an audience definition. Output JSON with keys 'name', 'description', 'definition' (which has 'include' and 'exclude' lists), and 'estimated_size'."
            )
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            try:
                return json.loads(response.choices[0].message.content)
            except Exception:
                pass # fallback
        templates: dict[str, dict] = {
            "activation": {
                "name": "Users needing activation",
                "description": f"Auto-generated audience for goal: {goal}",
                "definition": {
                    "include": [
                        {"field": "lifecycle_stage", "operator": "in", "value": ["lead", "trial"]},
                        {"field": "activation_score", "operator": "<", "value": 0.5},
                        {"field": "intent_score", "operator": ">", "value": 0.3},
                    ],
                    "exclude": [
                        {"field": "activated", "operator": "==", "value": True},
                    ],
                },
                "estimated_size": 1250,
            },
            "retention": {
                "name": "At-risk churning users",
                "description": f"Auto-generated audience for goal: {goal}",
                "definition": {
                    "include": [
                        {"field": "churn_risk", "operator": ">", "value": 0.6},
                        {"field": "lifecycle_stage", "operator": "in", "value": ["paying", "activated"]},
                    ],
                    "exclude": [
                        {"field": "lifecycle_stage", "operator": "==", "value": "churned"},
                    ],
                },
                "estimated_size": 430,
            },
        }

        # Pick closest template or return a generic one
        key = "activation"
        for k in templates:
            if k in goal.lower():
                key = k
                break

        result = templates[key]
        if event_schema:
            result["event_schema_used"] = list(event_schema.keys())
        return result
