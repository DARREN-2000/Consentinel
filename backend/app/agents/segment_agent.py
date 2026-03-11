"""Segment / audience generation agent (AI placeholder)."""


class SegmentAgent:
    """Generates audience definitions from natural-language goals.

    This is a placeholder for real LLM-based audience generation.
    """

    def generate_audience(
        self, goal: str, event_schema: dict | None = None
    ) -> dict:
        """Return a mock audience definition with inclusion/exclusion rules."""
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
