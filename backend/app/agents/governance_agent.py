"""Governance / compliance review agent (AI placeholder)."""


class GovernanceAgent:
    """Reviews campaigns for compliance with consent and fatigue rules.

    This is a placeholder for real LLM-based governance review.
    """

    def review_campaign(
        self,
        campaign: dict,
        consent_state: dict,
        fatigue_score: float,
    ) -> dict:
        """Return an approve / suppress / reject decision with reasons."""
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
