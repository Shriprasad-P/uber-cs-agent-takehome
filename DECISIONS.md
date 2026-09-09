# Design Decisions - Uber CS Agent

This document explains 15 key design decisions made during the development of the Uber CS Agent, with rationale, alternatives considered, and tradeoffs.

---

## 1. TF-IDF + Logistic Regression for Intent Classification

**Decision**: Use TF-IDF vectorization (500 features, bigrams) + Logistic Regression instead of transformer models (BERT, GPT).

**Rationale**:
- Small training set (25 examples) - transformers would overfit badly
- Fast inference (<10ms) - no GPU required
- Interpretable - can inspect feature weights
- Easy to debug and iterate

**Alternatives considered**:
- BERT fine-tuning: Requires 100s-1000s of examples, GPU, slower inference
- Few-shot GPT: High latency, cost per query, less consistent
- Rule-based: Too brittle, hard to maintain

**Tradeoffs**:
- ✅ Fast, cheap, works well on clean queries
- ❌ Struggles with typos, rare phrasings, semantic understanding

---

## 2. 11 Intent Categories (Not More, Not Less)

**Decision**: Exactly 11 intents covering core Uber support scenarios.

**Rationale**:
- Covers ~90% of typical rideshare support queries
- Granular enough for appropriate response/escalation
- Small enough to label and evaluate comprehensively

**Alternatives considered**:
- Fewer (5-7): Would force "payment" and "refund" together → different handling
- More (15-20): Would split "trip_issue" into route/fare/timing → over-engineered for MVP
- Hierarchical: e.g., "payment" → ["charge_error", "card_declined", "receipt"]

**Tradeoffs**:
- ✅ Good balance of coverage and simplicity
- ❌ Some ambiguous queries (trip issue leading to refund)

---

## 3. BM25 for Knowledge Base Retrieval (Not Embeddings)

**Decision**: Use BM25 (term-based ranking) instead of semantic embeddings.

**Rationale**:
- No model training/fine-tuning required
- Works well for keyword-heavy support queries ("refund", "cancel")
- Fast, deterministic, no GPU
- Easy to debug (see exact token matches)

**Alternatives considered**:
- Sentence embeddings (Sentence-BERT, OpenAI): Better semantic matching but overkill for 11-document KB
- DPR (Dense Passage Retrieval): Requires training on domain-specific data
- Hybrid (BM25 + embeddings): Added complexity without clear benefit for small KB

**Tradeoffs**:
- ✅ Simple, fast, no dependencies on external models
- ❌ Misses semantic similarity ("refund" vs. "get my money back")

---

## 4. Template-Based Replies as Default (LLM Optional)

**Decision**: Use pre-written response templates by default; LLM enhancement is optional.

**Rationale**:
- Zero cost, zero latency for LLM calls
- Consistent, professional responses
- No risk of hallucination or inappropriate content
- Full pipeline works without API keys (requirement)

**Alternatives considered**:
- LLM-only: High cost, latency, variability
- Hybrid (template + LLM expansion): Adds complexity without clear benefit
- Retrieval-augmented generation: Overkill for fixed KB

**Tradeoffs**:
- ✅ Fast, cheap, reliable
- ❌ Less personalized, can feel robotic

---

## 5. Always Escalate Safety and Driver Issues

**Decision**: Deterministic escalation for `safety` and `driver_issue` intents (100% of cases).

**Rationale**:
- Safety concerns require specialized training and immediate action
- Driver investigations need access to trip logs, driver history
- Legal/regulatory implications (liability, discrimination, assault)
- Better safe than sorry

**Alternatives considered**:
- Severity-based: Only escalate "serious" safety issues → risk missing critical cases
- ML-based: Predict escalation need → requires more training data and complex labeling

**Tradeoffs**:
- ✅ Zero false negatives on critical issues
- ❌ Some minor driver complaints might not need escalation (e.g., "driver didn't talk much")

---

## 6. Escalate Refunds Over $50

**Decision**: Automatic escalation for refund requests >$50.

**Rationale**:
- Balances automation with fraud prevention
- Agent can handle small refunds ($5-$20 cancellation fees)
- Large refunds need review (fraud risk, repeated claims, high-value customers)

**Alternatives considered**:
- No threshold: Escalate all refunds → low automation rate
- Higher threshold ($100): Risk of fraud or customer dissatisfaction
- ML-based: Predict refund legitimacy → requires fraud labels, more complex

**Tradeoffs**:
- ✅ Clear policy, easy to explain
- ❌ Somewhat arbitrary threshold (why $50 not $60?)

---

## 7. Escalate on Low Confidence (<0.4)

**Decision**: If intent classifier confidence <0.4, escalate to human.

**Rationale**:
- Wrong intent → wrong response → customer frustration
- Better to admit uncertainty than give wrong answer
- Human can use context/intuition to resolve ambiguity

**Alternatives considered**:
- No confidence threshold: Risk of bad responses on uncertain queries
- Higher threshold (0.6): Too many escalations, defeats automation purpose
- Fallback response: "Can you provide more details?" → feels unhelpful

**Tradeoffs**:
- ✅ Prevents confidently wrong responses
- ❌ Some legitimate queries are escalated unnecessarily

---

## 8. Synthetic Golden Set (165 Examples)

**Decision**: Create synthetic evaluation data instead of collecting real queries.

**Rationale**:
- No access to real Uber customer support data
- Controlled evaluation: balanced, labeled, covers all intents
- Faster iteration than IRB/data partnerships

**Alternatives considered**:
- Scrape Twitter/Reddit: Messy, hard to label, ethical concerns
- Pay for labeling service: Requires upfront cost, still synthetic-ish
- Smaller real dataset (50 examples): Too small for reliable eval

**Tradeoffs**:
- ✅ Full control, balanced, reproducible
- ❌ Doesn't reflect real distribution, messiness, edge cases (documented in REPORT.md)

---

## 9. Balanced Golden Set (15 per Intent)

**Decision**: Exactly 15 examples per intent (perfectly balanced).

**Rationale**:
- Simplifies evaluation (no class weighting needed)
- Ensures every intent is adequately tested
- Easier to spot per-intent weaknesses

**Alternatives considered**:
- Real distribution (30% payment, 5% safety): More realistic but masks minority class failures
- Imbalanced + weighted metrics: Adds complexity to eval interpretation

**Tradeoffs**:
- ✅ Clear per-intent performance, no class dominates results
- ❌ Doesn't reflect real-world query distribution

---

## 10. Keyword Fallback When Model Unavailable

**Decision**: If trained model doesn't exist, use keyword matching for intent classification.

**Rationale**:
- Agent works out-of-the-box without training
- Useful for quick demos, testing, debugging
- Graceful degradation

**Alternatives considered**:
- Fail hard: Require trained model → worse user experience
- Always predict "other": Gives wrong responses
- Random prediction: Unprofessional

**Tradeoffs**:
- ✅ Robustness, works without training data
- ❌ Lower accuracy (keyword matching ~50-60% vs. model 90%)

---

## 11. Single-Intent Classification (Not Multi-Label)

**Decision**: Each query gets exactly one intent label.

**Rationale**:
- Simplifies training, evaluation, response generation
- Most queries have one primary intent
- Multi-label adds complexity without clear benefit for MVP

**Alternatives considered**:
- Multi-label: Allows "trip_issue + refund" → requires different training, more complex eval
- Hierarchical: Primary intent + sub-intents → over-engineered

**Tradeoffs**:
- ✅ Simpler pipeline, clearer responses
- ❌ Forced to pick one intent when query has multiple ("driver was rude and took long route")

---

## 12. No Multi-Turn Conversation Handling

**Decision**: Agent processes each query independently (stateless).

**Rationale**:
- Simpler implementation (no session management, context tracking)
- Most support queries are self-contained
- Multi-turn adds complexity without demo value

**Alternatives considered**:
- Track conversation history: Requires session store, context injection
- Stateful model: Would need RNN/Transformer with memory

**Tradeoffs**:
- ✅ Stateless, scalable, easy to test
- ❌ Can't handle follow-ups ("What about my refund?" after discussing trip issue)

---

## 13. Small Training Set (25 Examples)

**Decision**: Use only 25 training examples from sample threads.

**Rationale**:
- Demonstrates that simple models work with small data
- Creating synthetic training data is time-consuming
- Golden set (165) is for evaluation, not training

**Alternatives considered**:
- Use golden set for training: Data leakage, overly optimistic results
- Generate 1000s of examples: Diminishing returns for TF-IDF+LogReg, time-intensive

**Tradeoffs**:
- ✅ Fast to create, sufficient for simple model
- ❌ Would need 100s for transformer, production deployment

---

## 14. Evaluation Without API Key as Requirement

**Decision**: Full pipeline (train, eval, inference) must work without any API keys.

**Rationale**:
- Not everyone has OpenAI credits for take-home projects
- Demonstrates that LLMs aren't required for good results
- Template-based responses are underrated
- Makes project accessible and reproducible

**Alternatives considered**:
- Require LLM: Adds cost barrier, variable results (GPT-4 vs. GPT-3.5)
- Mock LLM responses: Feels like cheating

**Tradeoffs**:
- ✅ Accessible, reproducible, zero-cost evaluation
- ❌ Can't demonstrate LLM enhancement in eval

---

## 15. Escalation Reason Strings (Explainability)

**Decision**: Every escalation includes a human-readable reason string.

**Rationale**:
- Helps human agents understand why query was escalated
- Builds trust with customers ("Your safety issue needs specialized handling")
- Aids debugging and system improvement
- Regulatory/compliance (explainable AI)

**Alternatives considered**:
- No explanation: Faster but opaque
- Reason codes: Less human-friendly ("ESC_SAFETY_01")
- LLM-generated explanation: Adds latency, less consistent

**Tradeoffs**:
- ✅ Clear, actionable, builds trust
- ❌ Requires maintaining reason string templates

---

## Summary Table

| # | Decision | Key Tradeoff |
|---|----------|--------------|
| 1 | TF-IDF + LogReg | Speed & simplicity vs. semantic understanding |
| 2 | 11 intents | Coverage vs. granularity |
| 3 | BM25 retrieval | Simplicity vs. semantic search |
| 4 | Template replies | Consistency vs. personalization |
| 5 | Always escalate safety | Safety vs. automation rate |
| 6 | $50 refund threshold | Automation vs. fraud prevention |
| 7 | <0.4 confidence escalation | Preventing errors vs. automation |
| 8 | Synthetic golden set | Control vs. realism |
| 9 | Balanced evaluation | Fair testing vs. realistic distribution |
| 10 | Keyword fallback | Robustness vs. accuracy |
| 11 | Single-intent | Simplicity vs. nuance |
| 12 | Stateless agent | Scalability vs. context handling |
| 13 | Small training set | Practicality vs. production readiness |
| 14 | No API key required | Accessibility vs. LLM enhancement |
| 15 | Escalation reasons | Explainability vs. speed |

---

## Meta-Decision: Optimize for Evaluation Rigor

**Overarching principle**: Prioritize trustworthy evaluation over impressive-sounding features.

**Manifestations**:
- Honest LABELING_METHODOLOGY.md acknowledging synthetic data limitations
- "What is misleading?" section in REPORT.md
- Baseline comparisons (trivial, simple, ours)
- Documented failure cases and real-world deployment considerations

**Rationale**: For a take-home project, demonstrating **rigorous thinking** is more valuable than claiming 99% accuracy. Shows engineering maturity, research mindset, and production awareness.

---

**Decisions reflect tradeoffs, not perfection. Good engineering is about making informed choices, documenting them, and being honest about limitations.**
