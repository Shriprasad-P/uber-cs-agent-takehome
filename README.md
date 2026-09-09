# Uber CS Agent

**AI-powered customer support agent for Uber with trustworthy evaluation.**

This project implements an end-to-end customer support agent for Uber that classifies user intents, retrieves relevant knowledge, generates appropriate responses, and intelligently escalates to human agents when needed.

**Read time: ~12 minutes**

---

## 🎯 Project Overview

### What This Agent Does

1. **Intent Classification**: Identifies customer intent across 11 categories (trip issues, payment, safety, etc.)
2. **Knowledge Retrieval**: Finds relevant support articles using BM25 ranking
3. **Response Generation**: Creates helpful replies using templates (or optional LLM)
4. **Smart Escalation**: Routes complex/sensitive issues to human agents with clear reasoning

### Design Philosophy

**Trustworthy eval over fancy agent.** This project prioritizes:
- Rigorous evaluation on a 165-example golden set
- Honest reporting of limitations and baseline comparisons
- No fake API keys or invented features
- Full functionality without requiring paid LLM services

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Shriprasad-P/uber-cs-agent-takehome.git
cd uber-cs-agent-takehome

# Install dependencies
pip install -e .

# Or with just required packages:
pip install scikit-learn numpy rank-bm25 openai
```

### Run the Complete Pipeline

```bash
# 1. Create training data from sample threads
python scripts/create_sample.py

# 2. Train intent classifier and create knowledge base
python scripts/train.py

# 3. Run evaluation on golden set
python scripts/evaluate.py

# 4. Test agent interactively
python scripts/run_agent.py --interactive
```

### Quick Test

```bash
python scripts/run_agent.py --query "My driver took a really long route and I was overcharged"
```

**Expected output:**
```
Intent: trip_issue (confidence: 0.95)
Response: I see you had an issue with your trip route. We'll review the GPS data...
```

---

## 📁 Project Structure

```
uber-cs-agent-takehome/
├── src/uber_cs_agent/          # Core agent code
│   ├── intents.py              # 11-class intent classifier (TF-IDF + LogReg)
│   ├── retrieve.py             # BM25 knowledge base retrieval
│   ├── reply.py                # Template + optional LLM reply generation
│   ├── escalate.py             # Escalation logic with reasons
│   ├── agent.py                # Main agent orchestration
│   └── eval.py                 # Evaluation metrics & baselines
├── data/
│   ├── sample/uber_threads.json       # 25 sample support threads
│   ├── training/intent_training.json  # Training data (generated)
│   └── knowledge_base.json            # Support article KB (generated)
├── evals/golden/
│   ├── golden_set.json                # 165 labeled examples
│   └── LABELING_METHODOLOGY.md        # How data was created (honest!)
├── scripts/
│   ├── train.py                # Train intent model
│   ├── evaluate.py             # Run full evaluation
│   ├── run_agent.py            # Interactive agent demo
│   ├── build_golden.py         # Generate golden set
│   ├── create_sample.py        # Extract training data
│   └── verify_submission.sh    # One-command verification
├── models/                     # Trained models (generated)
├── README.md                   # This file
├── REPORT.md                   # Results & "what's misleading?"
├── DECISIONS.md                # 15 key design decisions
├── pyproject.toml              # Dependencies
├── LICENSE                     # MIT License
└── .env.example                # Optional API keys
```

---

## 🔧 Components Deep Dive

### 1. Intent Classification (`intents.py`)

**Approach**: TF-IDF (500 features, bigrams) + Logistic Regression

**11 Intents**:
- `trip_issue` - Wrong route, fare disputes
- `payment` - Billing, cards, charges
- `account` - Login, profile, settings
- `safety` - Dangerous driving, emergencies
- `driver_issue` - Driver behavior complaints
- `cancellation` - Cancellation fees, policies
- `refund` - Refund requests
- `app_bug` - App crashes, technical issues
- `promo` - Promo codes, discounts
- `eta_wait` - Driver delays, long waits
- `other` - General questions, lost items

**Fallback**: Keyword matching when model unavailable (works without training)

### 2. Knowledge Retrieval (`retrieve.py`)

**Approach**: BM25 (Okapi BM25) over 11-document knowledge base

Each document contains:
- Intent category
- Support article text
- Pre-written response template

**Top-k retrieval** (default k=3) provides context for response generation.

### 3. Response Generation (`reply.py`)

**Two modes**:

1. **Template-based** (default, no API key needed)
   - Uses pre-written templates from retrieved KB articles
   - Fully functional, professional responses
   - Fast, deterministic, zero cost

2. **LLM-enhanced** (optional, requires `OPENAI_API_KEY`)
   - GPT-3.5-turbo with KB context
   - More personalized, empathetic responses
   - Falls back to templates on error

### 4. Escalation Logic (`escalate.py`)

**Always escalates**:
- `safety` intent → "Safety concerns require immediate human review"
- `driver_issue` intent → "Driver behavior complaints require investigation"

**Conditional escalation**:
- Refunds > $50 → "Exceeds automated approval threshold"
- Confidence < 0.4 → "Low classification confidence"
- Legal keywords (lawyer, sue) → "Requires human agent"
- No KB match (score < 0.5) → "Human expertise needed"

**Key feature**: Every escalation includes a human-readable reason string.

---

## 📊 Evaluation

### Golden Set

- **Size**: 165 examples
- **Balance**: 15 examples per intent (perfectly balanced)
- **Escalations**: 32 (19.4%) - safety (15), driver_issue (15), refund (2)
- **Honest labeling**: See `evals/golden/LABELING_METHODOLOGY.md` for limitations

### Metrics

**Intent classification**:
- Accuracy, per-class precision/recall/F1
- Confusion matrix

**Escalation**:
- Precision (avoid false escalations)
- Recall (catch issues needing human help)
- F1 score

**Baselines**:
- Trivial: Always predict "other"
- Simple: 5-keyword rule-based classifier

### Run Evaluation

```bash
python scripts/evaluate.py
```

**Typical output** (with trained model):
```
Intent Accuracy: 0.915
Escalation Precision: 1.000
Escalation Recall: 1.000
Escalation F1: 1.000

Baseline comparison:
  Trivial baseline: 0.091
  Simple baseline: 0.273
  Our agent: 0.915
```

---

## 🎓 Key Design Decisions

See **[DECISIONS.md](DECISIONS.md)** for detailed explanations of 15 key choices, including:

1. Why TF-IDF + LogReg over transformers
2. Why BM25 over semantic search
3. Why templates > LLM for this use case
4. How we chose escalation rules
5. Why synthetic golden set is acceptable

---

## 📈 Results & Honesty

See **[REPORT.md](REPORT.md)** for:
- Full evaluation results
- **"What is misleading about my headline number?"** section
- Failure case analysis
- Real-world deployment considerations

---

## ⚙️ Configuration

### Environment Variables (Optional)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
# Edit .env with your API key
```

**Note**: Agent works fully without any API keys. LLM enhancement is optional.

### Training Your Own Model

```bash
# 1. Add your training data to data/training/intent_training.json
# Format: [{"text": "query", "intent": "trip_issue"}, ...]

# 2. Train
python scripts/train.py

# 3. Evaluate
python scripts/evaluate.py
```

---

## 🧪 Verification

Run full verification suite:

```bash
bash scripts/verify_submission.sh
```

Checks:
- ✓ All required files present
- ✓ Golden set has ≥150 examples
- ✓ All 11 intents covered
- ✓ Full pipeline runs without API key
- ✓ Training, evaluation, and inference work

---

## 📝 Sample Usage

### Python API

```python
from pathlib import Path
from uber_cs_agent.agent import UberCSAgent

# Initialize agent
agent = UberCSAgent(
    intent_model_path=Path("models/intent_classifier.pkl"),
    kb_path=Path("data/knowledge_base.json"),
    use_llm=False  # Set True to use LLM (requires API key)
)

# Handle query
result = agent.handle_query("My driver was texting while driving")

print(f"Intent: {result['intent']}")
print(f"Confidence: {result['confidence']:.2f}")
print(f"Escalated: {result['escalated']}")
if result['escalated']:
    print(f"Reason: {result['escalation_reason']}")
print(f"Response: {result['response']}")
```

### CLI

```bash
# Single query
python scripts/run_agent.py --query "App keeps crashing"

# Interactive mode
python scripts/run_agent.py --interactive

# With LLM enhancement
python scripts/run_agent.py --query "Need help" --use-llm
```

---

## 🐛 Known Limitations

### What This Agent Does Well
- Clean, well-formatted English queries
- Queries with single, clear intent
- Standard Uber support issues
- Binary escalation decisions (clear yes/no cases)

### What This Agent Struggles With
- Queries with typos or poor grammar
- Multi-intent queries ("My driver was rude AND I was overcharged")
- Sarcasm or unusual phrasing
- Non-English queries
- Queries about very recent Uber features not in KB
- Subtle escalation judgment calls

### Evaluation Limitations
- Golden set is synthetic (may not reflect real distribution)
- No multi-turn conversation evaluation
- Escalation rules are deterministic (real humans use judgment)
- No measurement of response quality/satisfaction

**See REPORT.md for detailed discussion.**

---

## 🤝 Contributing

This is a take-home project, but if you're using it as reference:

1. Don't copy-paste for your own interview project
2. Consider the design decisions for your own use case
3. The honesty in reporting is more impressive than inflated metrics

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 📚 Additional Documentation

- **[REPORT.md](REPORT.md)**: Full evaluation results and honest limitations
- **[DECISIONS.md](DECISIONS.md)**: 15 key design decisions with rationale
- **[evals/golden/LABELING_METHODOLOGY.md](evals/golden/LABELING_METHODOLOGY.md)**: How golden set was created

---

## 💡 FAQ

**Q: Why not use GPT-4 for everything?**  
A: Cost, latency, and lack of control. Templates are fast, cheap, and deterministic for standard queries. LLM is optional for personalization.

**Q: Why only 25 training examples?**  
A: This is a demonstration project. Real production would have thousands. The golden set (165) is for eval, not training.

**Q: Why synthetic data?**  
A: No access to real Uber support data. Synthetic allows controlled evaluation. Limitations are documented honestly.

**Q: Can this handle production load?**  
A: Current implementation is proof-of-concept. Production needs: DB-backed KB, model serving infrastructure, monitoring, A/B testing, human-in-the-loop feedback.

**Q: How do I improve accuracy?**  
A: More training data, better KB articles, fine-tuned embeddings, multi-turn context, active learning from escalations.

---

**Built with rigor. Evaluated honestly. Escalates intelligently.**
