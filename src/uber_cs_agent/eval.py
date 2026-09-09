"""Evaluation metrics for Uber CS Agent."""

import json
from pathlib import Path
from typing import Optional

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


class AgentEvaluator:
    """Evaluate agent performance on golden set."""

    def __init__(self, golden_set_path: Path):
        self.golden_set_path = golden_set_path
        self.golden_data = self._load_golden_set()

    def _load_golden_set(self) -> list[dict]:
        """Load golden evaluation set."""
        with open(self.golden_set_path) as f:
            return json.load(f)

    def evaluate_agent(self, agent, verbose: bool = True) -> dict:
        """
        Evaluate agent on golden set.

        Returns dict with:
            - intent_accuracy
            - escalation_precision
            - escalation_recall
            - response_quality (if ground truth responses available)
        """
        y_true_intent = []
        y_pred_intent = []
        y_true_escalate = []
        y_pred_escalate = []

        for example in self.golden_data:
            query = example["query"]
            true_intent = example["intent"]
            true_escalate = example.get("should_escalate", False)

            result = agent.handle_query(query)

            y_true_intent.append(true_intent)
            y_pred_intent.append(result["intent"])

            y_true_escalate.append(true_escalate)
            y_pred_escalate.append(result["escalated"])

        intent_acc = accuracy_score(y_true_intent, y_pred_intent)

        escalation_metrics = self._compute_escalation_metrics(
            y_true_escalate, y_pred_escalate
        )

        results = {
            "intent_accuracy": intent_acc,
            "escalation_precision": escalation_metrics["precision"],
            "escalation_recall": escalation_metrics["recall"],
            "escalation_f1": escalation_metrics["f1"],
            "num_examples": len(self.golden_data),
        }

        if verbose:
            print("\n=== Intent Classification ===")
            print(f"Accuracy: {intent_acc:.3f}")
            print("\nPer-Intent Performance:")
            print(classification_report(y_true_intent, y_pred_intent, zero_division=0))

            print("\n=== Escalation Metrics ===")
            print(f"Precision: {escalation_metrics['precision']:.3f}")
            print(f"Recall: {escalation_metrics['recall']:.3f}")
            print(f"F1: {escalation_metrics['f1']:.3f}")

        return results

    def evaluate_intent_only(self, classifier, verbose: bool = True) -> dict:
        """Evaluate just the intent classifier."""
        y_true = [ex["intent"] for ex in self.golden_data]
        y_pred = [classifier.predict(ex["query"]) for ex in self.golden_data]

        acc = accuracy_score(y_true, y_pred)

        if verbose:
            print(f"\nIntent Accuracy: {acc:.3f}")
            print("\n" + classification_report(y_true, y_pred, zero_division=0))

        return {"accuracy": acc, "num_examples": len(self.golden_data)}

    @staticmethod
    def _compute_escalation_metrics(y_true: list, y_pred: list) -> dict:
        """Compute precision, recall, F1 for binary escalation."""
        tp = sum(1 for t, p in zip(y_true, y_pred) if t and p)
        fp = sum(1 for t, p in zip(y_true, y_pred) if not t and p)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t and not p)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        return {"precision": precision, "recall": recall, "f1": f1}

    def evaluate_baselines(self) -> dict:
        """Evaluate trivial and simple baselines."""
        y_true = [ex["intent"] for ex in self.golden_data]

        trivial_pred = ["other"] * len(y_true)
        trivial_acc = accuracy_score(y_true, trivial_pred)

        simple_pred = []
        for ex in self.golden_data:
            query_lower = ex["query"].lower()
            if "payment" in query_lower or "charge" in query_lower:
                simple_pred.append("payment")
            elif "cancel" in query_lower:
                simple_pred.append("cancellation")
            elif "refund" in query_lower:
                simple_pred.append("refund")
            elif "safe" in query_lower or "danger" in query_lower:
                simple_pred.append("safety")
            else:
                simple_pred.append("other")

        simple_acc = accuracy_score(y_true, simple_pred)

        return {
            "trivial_baseline": {"accuracy": trivial_acc},
            "simple_baseline": {"accuracy": simple_acc},
        }
