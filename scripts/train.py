"""Train the intent classifier."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from uber_cs_agent.intents import IntentClassifier
from uber_cs_agent.retrieve import KnowledgeBase


def train_intent_classifier():
    """Train and save intent classifier."""
    
    training_path = Path("data/training/intent_training.json")
    model_path = Path("models/intent_classifier.pkl")
    
    if not training_path.exists():
        print("Training data not found. Run create_sample.py first.")
        return
    
    with open(training_path) as f:
        training_data = json.load(f)
    
    texts = [ex["text"] for ex in training_data]
    labels = [ex["intent"] for ex in training_data]
    
    print(f"Training on {len(texts)} examples...")
    
    classifier = IntentClassifier()
    metrics = classifier.train(texts, labels)
    
    model_path.parent.mkdir(parents=True, exist_ok=True)
    classifier.save(model_path)
    
    print(f"\nTraining accuracy: {metrics['train_accuracy']:.3f}")
    print(f"Model saved to: {model_path}")


def create_knowledge_base():
    """Create default knowledge base."""
    
    kb_path = Path("data/knowledge_base.json")
    KnowledgeBase.create_default_kb(kb_path)
    
    print(f"\nKnowledge base created at: {kb_path}")


if __name__ == "__main__":
    print("=== Training Uber CS Agent ===\n")
    train_intent_classifier()
    create_knowledge_base()
    print("\n✓ Training complete!")
