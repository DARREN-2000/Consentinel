"""Experiment suggestion agent (AI placeholder)."""


class ExperimentAgent:
    """Suggests experiments to improve journey performance.

    This is a placeholder for real LLM-based experiment design.
    """

    def suggest_experiment(self, journey_performance: dict) -> dict:
        """Return mock experiment suggestions based on journey metrics."""
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
