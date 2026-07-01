"""Journey design agent."""
import os
import json
from openai import OpenAI

class JourneyAgent:
    """Designs multi-step journeys from audience definitions and goals."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def design_journey(self, audience: dict, goal: str) -> dict:
        """Return a journey with steps tailored to the goal."""
        if self.client:
            prompt = (
                f"Audience: {json.dumps(audience)}\n"
                f"Goal: {goal}\n\n"
                "Design a multi-step journey for this audience and goal. "
                "Output JSON with keys 'name', 'goal', 'audience', 'steps' (list of objects with 'step', 'type', 'action', 'delay_hours', 'subject'), "
                "'entry_conditions', 'exit_conditions', and 'suppression_rules'."
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
        steps_by_goal: dict[str, list[dict]] = {
            "onboarding": [
                {"step": 1, "type": "email", "action": "educate", "delay_hours": 0,
                 "subject": "Welcome! Here's how to get started"},
                {"step": 2, "type": "in_app", "action": "educate", "delay_hours": 24,
                 "subject": "Complete your setup in 3 easy steps"},
                {"step": 3, "type": "email", "action": "remind", "delay_hours": 72,
                 "subject": "You're almost there — finish setup today"},
                {"step": 4, "type": "push", "action": "offer", "delay_hours": 168,
                 "subject": "Unlock premium features — limited-time offer"},
            ],
            "activation": [
                {"step": 1, "type": "in_app", "action": "educate", "delay_hours": 0,
                 "subject": "Discover your first key feature"},
                {"step": 2, "type": "email", "action": "educate", "delay_hours": 48,
                 "subject": "Teams that do X see 3× results"},
                {"step": 3, "type": "email", "action": "offer", "delay_hours": 120,
                 "subject": "Ready to upgrade? Here's 20% off"},
            ],
            "retention": [
                {"step": 1, "type": "email", "action": "remind", "delay_hours": 0,
                 "subject": "We noticed you've been away"},
                {"step": 2, "type": "push", "action": "educate", "delay_hours": 48,
                 "subject": "New features you haven't tried yet"},
                {"step": 3, "type": "email", "action": "offer", "delay_hours": 168,
                 "subject": "Come back — here's a special offer"},
            ],
        }

        matched_goal = "onboarding"
        for g in steps_by_goal:
            if g in goal.lower():
                matched_goal = g
                break

        return {
            "name": f"{matched_goal.title()} Journey",
            "goal": matched_goal,
            "audience": audience.get("name", "Unknown"),
            "steps": steps_by_goal[matched_goal],
            "entry_conditions": {"event": "user_created"},
            "exit_conditions": {"event": "activated", "or": {"days_elapsed": 30}},
            "suppression_rules": {"fatigue_threshold": 0.8, "respect_quiet_hours": True},
        }
