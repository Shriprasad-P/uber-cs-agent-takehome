"""Create sample training data from threads."""

import json
from pathlib import Path


def create_training_data():
    """Extract training data from sample threads."""
    
    threads_path = Path(__file__).parent.parent / "data" / "sample" / "uber_threads.json"
    
    with open(threads_path) as f:
        threads = json.load(f)
    
    training_data = []
    for thread in threads:
        training_data.append({
            "text": thread["query"],
            "intent": thread["intent"]
        })
    
    output_path = Path(__file__).parent.parent / "data" / "training" / "intent_training.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Created {len(training_data)} training examples")
    print(f"Saved to: {output_path}")
    
    intent_counts = {}
    for ex in training_data:
        intent = ex["intent"]
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
    
    print("\nIntent distribution:")
    for intent, count in sorted(intent_counts.items()):
        print(f"  {intent}: {count}")


if __name__ == "__main__":
    create_training_data()
