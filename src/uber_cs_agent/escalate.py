"""Escalation logic for customer support queries."""

from typing import Optional


ALWAYS_ESCALATE_INTENTS = {"safety", "driver_issue"}


def should_escalate(
    intent: str,
    query: str,
    confidence: float,
    retrieved_docs: list[dict],
) -> tuple[bool, Optional[str]]:
    """
    Determine if query should be escalated to human agent.

    Returns:
        (should_escalate: bool, reason: Optional[str])
    """
    if intent in ALWAYS_ESCALATE_INTENTS:
        if intent == "safety":
            return True, "Safety concerns require immediate human review and specialized handling"
        elif intent == "driver_issue":
            return True, "Driver behavior complaints require investigation by driver quality team"

    if confidence < 0.4:
        return True, f"Low intent classification confidence ({confidence:.2f}). Human review needed to ensure accurate response"

    if _contains_escalation_keywords(query):
        return True, "Query contains language indicating need for human agent (legal, speak to manager, lawsuit)"

    if intent == "refund" and _extract_refund_amount(query) > 50:
        return True, f"Refund request exceeds automated approval threshold ($50). Amount: ${_extract_refund_amount(query)}"

    if not retrieved_docs or (retrieved_docs and retrieved_docs[0].get("score", 0) < 0.5):
        return True, "No relevant knowledge base articles found. Human expertise needed"

    return False, None


def _contains_escalation_keywords(query: str) -> bool:
    """Check if query contains keywords that trigger escalation."""
    escalation_keywords = [
        "lawyer", "legal", "sue", "lawsuit",
        "manager", "supervisor", "speak to someone",
        "unacceptable", "furious", "outraged",
    ]

    query_lower = query.lower()
    return any(keyword in query_lower for keyword in escalation_keywords)


def _extract_refund_amount(query: str) -> float:
    """Extract dollar amount from refund request (simple regex)."""
    import re

    pattern = r'\$?\s*(\d+(?:\.\d{2})?)'
    matches = re.findall(pattern, query)

    if matches:
        try:
            return float(matches[0])
        except ValueError:
            pass

    return 0.0
