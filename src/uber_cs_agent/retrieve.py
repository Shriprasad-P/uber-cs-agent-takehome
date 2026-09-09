"""BM25-based retrieval for Uber CS knowledge base."""

import json
from pathlib import Path
from typing import Optional

import numpy as np
from rank_bm25 import BM25Okapi


class KnowledgeBase:
    """BM25 retriever for Uber support knowledge base."""

    def __init__(self, kb_path: Optional[Path] = None):
        self.documents: list[dict] = []
        self.bm25: Optional[BM25Okapi] = None

        if kb_path and kb_path.exists():
            self.load(kb_path)

    def load(self, path: Path):
        """Load knowledge base from JSON."""
        with open(path) as f:
            self.documents = json.load(f)

        corpus = [doc["text"] for doc in self.documents]
        tokenized_corpus = [doc.lower().split() for doc in corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """Retrieve top-k most relevant documents."""
        if not self.bm25:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            doc = self.documents[idx].copy()
            doc["score"] = float(scores[idx])
            results.append(doc)

        return results

    @staticmethod
    def create_default_kb(path: Path):
        """Create a default Uber support knowledge base."""
        kb = [
            {
                "id": "kb_001",
                "intent": "trip_issue",
                "text": "If your trip took an unexpected route or was longer than expected, please report it. We'll review the route and adjust the fare if needed.",
                "template": "I see you had an issue with your trip route. We'll review the GPS data and adjust your fare if the route was inefficient.",
            },
            {
                "id": "kb_002",
                "intent": "payment",
                "text": "Payment issues can occur due to expired cards, insufficient funds, or bank declines. Check your payment method and try updating it.",
                "template": "I notice a payment issue on your account. Please verify your payment method is up to date and has sufficient funds.",
            },
            {
                "id": "kb_003",
                "intent": "account",
                "text": "To update your account information, go to Settings > Account. You can change your name, email, phone number, and password there.",
                "template": "You can update your account details in Settings > Account. Let me know if you need help with specific changes.",
            },
            {
                "id": "kb_004",
                "intent": "safety",
                "text": "Your safety is our top priority. For immediate emergencies, call 911. For safety concerns, contact our safety team immediately through the app.",
                "template": "I'm escalating your safety concern to our specialized safety team immediately. They will contact you within the hour.",
            },
            {
                "id": "kb_005",
                "intent": "driver_issue",
                "text": "Driver behavior complaints are taken seriously. We'll review your report and take appropriate action, which may include warnings or account deactivation.",
                "template": "I'm escalating your driver complaint to our driver quality team. They'll investigate and take appropriate action.",
            },
            {
                "id": "kb_006",
                "intent": "cancellation",
                "text": "Cancellation fees apply if you cancel after the driver has waited 2 minutes. Fees typically range from $5-10 depending on your city.",
                "template": "I see you were charged a cancellation fee. This applies when canceling after the driver has waited 2 minutes. I can review your specific case.",
            },
            {
                "id": "kb_007",
                "intent": "refund",
                "text": "Refunds are processed to your original payment method within 3-5 business days. For immediate issues, we can provide Uber Cash credits.",
                "template": "I can process a refund for you. It will appear on your original payment method in 3-5 business days.",
            },
            {
                "id": "kb_008",
                "intent": "app_bug",
                "text": "If the app is crashing or not loading, try: 1) Close and reopen the app, 2) Update to the latest version, 3) Clear app cache, 4) Reinstall the app.",
                "template": "I see you're experiencing app issues. Please try updating to the latest version and clearing your cache. Let me know if that helps.",
            },
            {
                "id": "kb_009",
                "intent": "promo",
                "text": "Promo codes must be entered before requesting a trip. Each code has specific terms including expiration dates, user eligibility, and minimum trip amounts.",
                "template": "I see your promo code didn't apply. Let me check the code terms and help you apply it to a future trip if it's still valid.",
            },
            {
                "id": "kb_010",
                "intent": "eta_wait",
                "text": "ETAs are estimated based on real-time traffic and driver location. If your driver is delayed, you can cancel without a fee if they're more than 5 minutes late.",
                "template": "I see your driver is taking longer than expected. You can cancel without a fee if they're more than 5 minutes past the ETA.",
            },
            {
                "id": "kb_011",
                "intent": "other",
                "text": "For other questions, please provide more details so I can assist you better. You can also visit help.uber.com for common questions.",
                "template": "I'd be happy to help! Could you provide more details about your issue? You can also check help.uber.com for common questions.",
            },
        ]

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(kb, f, indent=2)

        return kb
