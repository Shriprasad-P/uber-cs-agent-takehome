"""Main Uber CS Agent orchestrating intent, retrieval, reply, and escalation."""

from pathlib import Path
from typing import Optional

from .escalate import should_escalate
from .intents import IntentClassifier
from .reply import ReplyGenerator
from .retrieve import KnowledgeBase


class UberCSAgent:
    """Uber customer support agent."""

    def __init__(
        self,
        intent_model_path: Optional[Path] = None,
        kb_path: Optional[Path] = None,
        use_llm: bool = False,
    ):
        self.intent_classifier = IntentClassifier(intent_model_path)
        self.knowledge_base = KnowledgeBase(kb_path)
        self.reply_generator = ReplyGenerator(use_llm=use_llm)

    def handle_query(self, query: str, context: Optional[dict] = None) -> dict:
        """
        Handle a customer support query end-to-end.

        Args:
            query: Customer query text
            context: Optional context (user_id, trip_id, etc.)

        Returns:
            dict with intent, confidence, retrieved_docs, response, escalated, escalation_reason
        """
        intent = self.intent_classifier.predict(query)
        intent_probs = self.intent_classifier.predict_proba(query)
        confidence = intent_probs.get(intent, 0.0)

        retrieved_docs = self.knowledge_base.retrieve(query, top_k=3)

        escalated, escalation_reason = should_escalate(
            intent, query, confidence, retrieved_docs
        )

        if escalated:
            response = self._generate_escalation_response(query, escalation_reason)
        else:
            response = self.reply_generator.generate(
                query, intent, retrieved_docs, context
            )

        return {
            "query": query,
            "intent": intent,
            "confidence": confidence,
            "retrieved_docs": retrieved_docs,
            "response": response,
            "escalated": escalated,
            "escalation_reason": escalation_reason,
        }

    def _generate_escalation_response(self, query: str, reason: str) -> str:
        """Generate response for escalated queries."""
        return (
            "Thank you for contacting Uber support. Your issue requires specialized attention, "
            "and I'm connecting you with one of our expert agents who can better assist you. "
            "You'll receive a response shortly."
        )
