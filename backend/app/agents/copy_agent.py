"""Copy / message generation agent."""
import os
import json
from openai import OpenAI

class CopyAgent:
    """Generates message copy variants for campaigns."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_copy(
        self,
        context: dict,
        tone: str = "professional",
        objective: str = "educate",
    ) -> dict:
        """Return generated message variants for the given context."""
        if self.client:
            prompt = (
                f"Context: {json.dumps(context)}\n"
                f"Tone: {tone}\n"
                f"Objective: {objective}\n\n"
                "Generate 2 copy variants. Output as JSON with keys 'channel', 'tone', 'objective', 'variants'. "
                "'variants' should be a list of objects with 'variant_id' (A, B), 'subject', 'body', 'cta'."
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
        channel = context.get("channel", "email")
        product = context.get("product", "our platform")
        user_name = context.get("user_name", "there")

        tone_modifiers = {
            "professional": {"greeting": f"Hi {user_name},", "cta": "Learn more"},
            "friendly": {"greeting": f"Hey {user_name}! 👋", "cta": "Check it out"},
            "urgent": {"greeting": f"{user_name},", "cta": "Act now"},
        }
        mod = tone_modifiers.get(tone, tone_modifiers["professional"])

        variants = [
            {
                "variant_id": "A",
                "subject": f"Discover how {product} can help you",
                "body": (
                    f"{mod['greeting']}\n\n"
                    f"We wanted to share how {product} can help you achieve your goals. "
                    f"Our users typically see results within the first week.\n\n"
                    f"{mod['cta']} →"
                ),
                "cta": mod["cta"],
            },
            {
                "variant_id": "B",
                "subject": f"You're missing out on {product}",
                "body": (
                    f"{mod['greeting']}\n\n"
                    f"Did you know that {product} offers features specifically "
                    f"designed for your use case? Let us show you how.\n\n"
                    f"{mod['cta']} →"
                ),
                "cta": mod["cta"],
            },
        ]

        return {
            "channel": channel,
            "tone": tone,
            "objective": objective,
            "variants": variants,
        }
