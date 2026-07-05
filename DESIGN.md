# System Design & Philosophy

Consentinel challenges the foundational premise of most marketing platforms: *that every user should always receive a message.*

## 1. "Do Nothing" is a First-Class Action
Suppressing outreach is not an error state; it is an intelligent decision. Consentinel's core Next-Best-Action (NBA) engine actively evaluates whether to contact a user. If a user is over-contacted (fatigued) or hasn't granted explicit consent, the system deliberately outputs `action: none`.

## 2. Fail Closed
In all security and consent checks, the system defaults to "deny". If the Redis cache is down and fatigue cannot be computed, or if the ConsentHub API is unreachable, Consentinel will suppress the message rather than risk an unconsented touchpoint.

## 3. Pluggable Intelligence
The system uses a deterministic core wrapped in non-deterministic AI agents (OpenAI).
* **Deterministic Core**: Consent verification, fatigue thresholds, suppression rules.
* **Non-deterministic Agents**: Copy generation, audience segmentation, journey orchestration.
This ensures we gain the flexibility of LLMs without compromising the strict regulatory compliance required for enterprise environments.

## 4. Local First & Ephemeral Demo Support
While production assumes PostgreSQL and Redis, the system is designed to run entirely in-memory (SQLite) with mock fallbacks for LLMs. This ensures a seamless "clone and run" developer experience.
