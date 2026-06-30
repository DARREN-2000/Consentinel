"""Governance / compliance review agent."""
import os
import json
from openai import OpenAI

class GovernanceAgent:
    """Reviews campaigns for compliance with consent and fatigue rules."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("OPENAI_BASE_URL")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def review_campaign(
        self,
        campaign: dict,
        consent_state: dict,
        fatigue_score: float,
    ) -> dict:
        """Return an approve / suppress / reject decision with reasons."""
        if self.client:
            prompt = (
                f"Campaign: {json.dumps(campaign)}\n"
                f"Consent State: {json.dumps(consent_state)}\n"
                f"Fatigue Score: {fatigue_score}\n\n"
                "Review this campaign against compliance and brand safety rules. "
                "Output JSON with keys 'status' (approved, suppressed, or rejected), "
                "'issues' (list of strings), and 'warnings' (list of strings)."
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
        issues: list[str] = []
        warnings: list[str] = []

        channel = campaign.get("channel", "unknown")
        audience_size = campaign.get("audience_size", 0)

        # Check consent coverage
        channel_consent = consent_state.get(channel, {})
        if channel_consent.get("status") != "granted":
            issues.append(
                f"No active consent for channel '{channel}'. "
                "Campaign must not proceed without explicit consent."
            )

        # Check fatigue
        if fatigue_score > 0.80:
            issues.append(
                f"Fatigue score ({fatigue_score:.2f}) exceeds threshold (0.80). "
                "Suppress to prevent user disengagement."
            )
        elif fatigue_score > 0.60:
            warnings.append(
                f"Fatigue score ({fatigue_score:.2f}) is elevated. "
                "Consider reducing frequency."
            )

        # Check audience size (large blasts need approval)
        if audience_size > 10_000:
            warnings.append(
                f"Large audience ({audience_size:,} users). "
                "Recommend staged rollout and approval from marketing lead."
            )

        # Check required fields
        if not campaign.get("subject"):
            issues.append("Campaign is missing a subject line.")
        if not campaign.get("body"):
            warnings.append("Campaign body is empty — may be a template issue.")

        # Decision
        if issues:
            decision = "reject" if any("consent" in i.lower() for i in issues) else "suppress"
        else:
            decision = "approve"

        return {
            "decision": decision,
            "issues": issues,
            "warnings": warnings,
            "recommendation": (
                "Campaign is compliant and ready to send."
                if decision == "approve"
                else "Resolve the listed issues before sending."
            ),
            "requires_human_approval": audience_size > 10_000,
        }
