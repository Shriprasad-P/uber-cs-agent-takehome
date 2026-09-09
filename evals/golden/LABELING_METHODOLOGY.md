# Labeling Methodology for Uber CS Agent Golden Set

## Overview

This document describes how the 165-example golden evaluation set was created and labeled for the Uber CS Agent project.

## Data Source

**All examples are synthetic** and were created by the project author specifically for this evaluation task. No real Uber customer support data was used.

## Creation Process

### 1. Intent Definition
First, we defined 11 intent categories based on common Uber customer support scenarios:
- `trip_issue`: Problems with route, fare, or trip execution
- `payment`: Billing, charges, payment methods
- `account`: Login, profile settings, account management
- `safety`: Dangerous driving, safety concerns, emergencies
- `driver_issue`: Driver behavior, professionalism complaints
- `cancellation`: Cancellation fees and policies
- `refund`: Refund requests and reimbursements
- `app_bug`: Technical issues with the Uber app
- `promo`: Promo codes, discounts, credits
- `eta_wait`: Driver delays, ETA issues, long wait times
- `other`: General questions, lost items, scheduling

### 2. Query Generation
For each intent, we created 15 realistic customer queries by:
- Researching common Uber support topics on forums (Reddit, Twitter)
- Drawing from general rideshare customer service patterns
- Ensuring diversity in:
  - Query length (short: "App keeps crashing" to long: multi-sentence descriptions)
  - Formality (casual to formal)
  - Sentiment (neutral, frustrated, angry)
  - Specificity (vague vs. detailed with dollar amounts, times)

### 3. Escalation Labeling
Each example was labeled with `should_escalate: true/false` based on these rules:

**Always Escalate:**
- `safety` intent: 15/15 escalations (all safety issues require specialized handling)
- `driver_issue` intent: 15/15 escalations (driver behavior requires investigation)

**Conditional Escalation:**
- `refund` intent: 2/15 escalations (large amounts: $80 cleaning fee, $120 surge refund)
- Other intents: 0 escalations (can be handled by automated agent)

**Escalation Criteria Applied:**
1. Safety risk to customer
2. Driver investigation required
3. High-value refund (>$50)
4. Legal/regulatory implications
5. Low confidence scenarios (though not explicitly in synthetic data)

### 4. Quality Control

**Validation steps:**
- Verified each query clearly belongs to its labeled intent
- Ensured no ambiguous queries (e.g., "refund for bad driver" could be refund OR driver_issue)
- Checked for typos and grammatical errors
- Balanced dataset: exactly 15 examples per intent
- Verified escalation rules were consistently applied

**Known Limitations:**
- Synthetic data may not capture all real-world query variations
- No spelling errors or non-English queries (real data has these)
- Sentiment may be less extreme than real frustrated customers
- Technical details (trip IDs, amounts) are fabricated

## Statistics

- **Total examples:** 165
- **Examples per intent:** 15 (perfectly balanced)
- **Total escalations:** 32 (19.4%)
  - safety: 15
  - driver_issue: 15
  - refund: 2
  - All others: 0

## Honest Assessment

**What this golden set is good for:**
- Measuring basic intent classification accuracy
- Testing escalation logic on clear-cut cases
- Evaluating system on clean, well-formatted queries

**What this golden set misses:**
- Real-world noise (typos, unclear language, multiple issues in one query)
- Edge cases and ambiguous queries
- Customer sentiment nuances
- Queries in languages other than English
- Follow-up queries in multi-turn conversations

**Impact on reported metrics:**
- Accuracy numbers will be **higher** than real-world performance
- System may fail on messier real queries not represented here
- Escalation metrics reflect policy, not real gray-area decisions

## Reproducibility

To regenerate the golden set:
```bash
python scripts/build_golden.py
```

The generation script is deterministic (no randomization), so running it will produce identical output.

## Maintenance

When updating the golden set:
1. Maintain balance across intents (15 each)
2. Document any changes to escalation rules
3. Re-run full evaluation after changes
4. Update this document with methodology changes
