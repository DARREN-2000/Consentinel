"""Copy / message generation agent (AI placeholder)."""


class CopyAgent:
    """Generates message copy variants for campaigns.

    This is a placeholder for real LLM-based copy generation.
    """

    def generate_copy(
        self,
        context: dict,
        tone: str = "professional",
        objective: str = "educate",
    ) -> dict:
        """Return mock message variants for the given context."""
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
