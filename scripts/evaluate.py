"""Evaluate the Uber CS Agent."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from uber_cs_agent.agent import UberCSAgent
from uber_cs_agent.eval import AgentEvaluator


def main():
    """Run evaluation on golden set."""
    
    print("=== Evaluating Uber CS Agent ===\n")
    
    model_path = Path("models/intent_classifier.pkl")
    kb_path = Path("data/knowledge_base.json")
    golden_path = Path("evals/golden/golden_set.json")
    
    if not golden_path.exists():
        print("Error: Golden set not found. Run build_golden.py first.")
        return
    
    has_model = model_path.exists()
    has_kb = kb_path.exists()
    
    if not has_model:
        print("⚠️  No trained model found - using keyword fallback")
    if not has_kb:
        print("⚠️  No knowledge base found - retrieval will be empty")
    
    print()
    
    agent = UberCSAgent(
        intent_model_path=model_path if has_model else None,
        kb_path=kb_path if has_kb else None,
        use_llm=False
    )
    
    evaluator = AgentEvaluator(golden_path)
    
    print("Running evaluation on golden set...")
    print("=" * 60)
    
    results = evaluator.evaluate_agent(agent, verbose=True)
    
    print("\n" + "=" * 60)
    print("\n=== Baseline Comparison ===")
    baselines = evaluator.evaluate_baselines()
    
    print(f"\nTrivial baseline (always predict 'other'): {baselines['trivial_baseline']['accuracy']:.3f}")
    print(f"Simple keyword baseline: {baselines['simple_baseline']['accuracy']:.3f}")
    print(f"Our agent: {results['intent_accuracy']:.3f}")
    
    print("\n" + "=" * 60)
    print("\n=== Summary ===")
    print(f"Examples evaluated: {results['num_examples']}")
    print(f"Intent accuracy: {results['intent_accuracy']:.3f}")
    print(f"Escalation precision: {results['escalation_precision']:.3f}")
    print(f"Escalation recall: {results['escalation_recall']:.3f}")
    print(f"Escalation F1: {results['escalation_f1']:.3f}")
    
    print("\n✓ Evaluation complete!")


if __name__ == "__main__":
    main()
