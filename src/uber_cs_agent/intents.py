"""Intent classification for Uber customer support queries.

Supports 11 intents using TF-IDF + LogisticRegression with keyword fallback.
"""

import json
import pickle
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


INTENTS = [
    "trip_issue",
    "payment",
    "account",
    "safety",
    "driver_issue",
    "cancellation",
    "refund",
    "app_bug",
    "promo",
    "eta_wait",
    "other",
]


KEYWORD_PATTERNS = {
    "trip_issue": ["wrong route", "driver lost", "long route", "detour", "trip problem"],
    "payment": ["charge", "payment", "card", "refund payment", "billed", "overcharged"],
    "account": ["account", "profile", "password", "login", "sign in", "email change"],
    "safety": ["unsafe", "accident", "emergency", "threatened", "dangerous", "assault"],
    "driver_issue": ["driver rude", "driver behavior", "driver complaint", "unprofessional"],
    "cancellation": ["cancel", "cancelled", "cancellation fee"],
    "refund": ["refund", "money back", "reimburs"],
    "app_bug": ["app crash", "bug", "frozen", "not loading", "glitch"],
    "promo": ["promo", "coupon", "discount", "code not working"],
    "eta_wait": ["eta", "wait", "waiting", "late", "delay", "where is driver"],
    "other": [],
}


class IntentClassifier:
    """TF-IDF + LogisticRegression intent classifier with keyword fallback."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path
        self.pipeline: Optional[Pipeline] = None
        if model_path and model_path.exists():
            self.load(model_path)

    def train(self, texts: list[str], labels: list[str]) -> dict:
        """Train the intent classifier."""
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ])
        self.pipeline.fit(texts, labels)

        train_acc = self.pipeline.score(texts, labels)
        return {"train_accuracy": train_acc}

    def predict(self, text: str) -> str:
        """Predict intent for a single query."""
        if self.pipeline:
            try:
                return self.pipeline.predict([text])[0]
            except Exception:
                pass

        return self._keyword_fallback(text)

    def predict_proba(self, text: str) -> dict[str, float]:
        """Return probability distribution over intents."""
        if self.pipeline:
            try:
                probs = self.pipeline.predict_proba([text])[0]
                classes = self.pipeline.classes_
                return dict(zip(classes, probs))
            except Exception:
                pass

        intent = self._keyword_fallback(text)
        return {intent: 1.0}

    def _keyword_fallback(self, text: str) -> str:
        """Keyword-based fallback when model unavailable."""
        text_lower = text.lower()

        for intent, keywords in KEYWORD_PATTERNS.items():
            if intent == "other":
                continue
            for keyword in keywords:
                if keyword in text_lower:
                    return intent

        return "other"

    def save(self, path: Path):
        """Save trained model to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.pipeline, f)

    def load(self, path: Path):
        """Load trained model from disk."""
        with open(path, "rb") as f:
            self.pipeline = pickle.load(f)
