"""Experiment suggestion agent."""
import os
import json
from openai import OpenAI

class ExperimentAgent:
    """Suggests experiments to improve journey performance."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def suggest_experiment(self, journey_performance: dict) -> dict:
        """Return experiment suggestions based on journey metrics."""
        journey_name = journey_performance.get("journey_name", "Unknown Journey")

        if self.client:
            prompt = (
                f"Journey: {journey_name}\n"
                f"Metrics: {json.dumps(journey_performance)}\n\n"
                "Suggest 1-3 A/B experiments to improve performance. "
                "Output JSON with keys 'journey_name', 'current_metrics', and 'suggestions'. "
                "'suggestions' should be a list of objects with 'experiment_type', 'name', 'description', "
                "'variants' (list of {id, description}), 'traffic_split', 'primary_metric', and 'estimated_duration_days'."
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
        open_rate = journey_performance.get("open_rate", 0.0)
        click_rate = journey_performance.get("click_rate", 0.0)
        conversion_rate = journey_performance.get("conversion_rate", 0.0)
        journey_name = journey_performance.get("journey_name", "Unknown Journey")

        suggestions: list[dict] = []

        if open_rate < 0.25:
            suggestions.append({
                "experiment_type": "ab_test",
                "name": f"Subject line test for {journey_name}",
                "description": "Test alternative subject lines to improve open rates",
                "variants": [
                    {"id": "control", "description": "Current subject line"},
                    {"id": "variant_a", "description": "Question-based subject"},
                    {"id": "variant_b", "description": "Personalized subject with name"},
                ],
                "traffic_split": {"control": 34, "variant_a": 33, "variant_b": 33},
                "primary_metric": "open_rate",
                "estimated_duration_days": 14,
            })

        if click_rate < 0.05:
            suggestions.append({
                "experiment_type": "ab_test",
                "name": f"CTA test for {journey_name}",
                "description": "Test different call-to-action copy and placement",
                "variants": [
                    {"id": "control", "description": "Current CTA"},
                    {"id": "variant_a", "description": "Action-oriented CTA"},
                ],
                "traffic_split": {"control": 50, "variant_a": 50},
                "primary_metric": "click_rate",
                "estimated_duration_days": 7,
            })

        if conversion_rate < 0.02:
            suggestions.append({
                "experiment_type": "channel_test",
                "name": f"Channel optimization for {journey_name}",
                "description": "Test email vs. push vs. in-app for conversion",
                "variants": [
                    {"id": "email", "description": "Email channel"},
                    {"id": "push", "description": "Push notification"},
                    {"id": "in_app", "description": "In-app message"},
                ],
                "traffic_split": {"email": 34, "push": 33, "in_app": 33},
                "primary_metric": "conversion_rate",
                "estimated_duration_days": 21,
            })

        if not suggestions:
            suggestions.append({
                "experiment_type": "send_time",
                "name": f"Send time optimization for {journey_name}",
                "description": "Find the optimal send time for this journey",
                "variants": [
                    {"id": "morning", "description": "9 AM local time"},
                    {"id": "afternoon", "description": "2 PM local time"},
                    {"id": "evening", "description": "7 PM local time"},
                ],
                "traffic_split": {"morning": 34, "afternoon": 33, "evening": 33},
                "primary_metric": "open_rate",
                "estimated_duration_days": 14,
            })

        return {
            "journey_name": journey_name,
            "current_metrics": journey_performance,
            "suggestions": suggestions,
        }
