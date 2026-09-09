"""Run the Uber CS Agent interactively or on a query."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from uber_cs_agent.agent import UberCSAgent


def main():
    parser = argparse.ArgumentParser(description="Run Uber CS Agent")
    parser.add_argument("--query", type=str, help="Single query to process")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM for reply generation (requires API key)")
    
    args = parser.parse_args()
    
    model_path = Path("models/intent_classifier.pkl")
    kb_path = Path("data/knowledge_base.json")
    
    agent = UberCSAgent(
        intent_model_path=model_path if model_path.exists() else None,
        kb_path=kb_path if kb_path.exists() else None,
        use_llm=args.use_llm
    )
    
    if not model_path.exists():
        print("⚠️  No trained model found - using keyword fallback\n")
    
    if args.query:
        result = agent.handle_query(args.query)
        print_result(result)
    
    elif args.interactive:
        print("=== Uber CS Agent - Interactive Mode ===")
        print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                query = input("Customer query: ").strip()
                if query.lower() in ["quit", "exit", "q"]:
                    break
                
                if not query:
                    continue
                
                result = agent.handle_query(query)
                print_result(result)
                print()
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
    
    else:
        print("Usage: python run_agent.py --query 'your query' or --interactive")


def print_result(result: dict):
    """Pretty-print agent result."""
    print(f"\n{'='*60}")
    print(f"Query: {result['query']}")
    print(f"{'='*60}")
    print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
    
    if result['escalated']:
        print(f"\n🚨 ESCALATED")
        print(f"Reason: {result['escalation_reason']}")
    
    print(f"\nResponse:")
    print(result['response'])
    
    if result['retrieved_docs']:
        print(f"\nRetrieved docs:")
        for i, doc in enumerate(result['retrieved_docs'][:2], 1):
            print(f"  {i}. [{doc.get('id', 'N/A')}] (score: {doc.get('score', 0):.2f})")


if __name__ == "__main__":
    main()
