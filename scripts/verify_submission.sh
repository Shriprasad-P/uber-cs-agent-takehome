#!/bin/bash

# Uber CS Agent - Submission Verification Script
# Verifies all required deliverables are present and working

set -e

echo "==================================="
echo "Uber CS Agent - Verifying Submission"
echo "==================================="
echo ""

ERRORS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ MISSING: $1"
        ERRORS=$((ERRORS + 1))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ MISSING: $1/"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "Checking project structure..."
echo "-----------------------------------"

# Core source files
check_file "src/uber_cs_agent/__init__.py"
check_file "src/uber_cs_agent/intents.py"
check_file "src/uber_cs_agent/retrieve.py"
check_file "src/uber_cs_agent/reply.py"
check_file "src/uber_cs_agent/escalate.py"
check_file "src/uber_cs_agent/agent.py"
check_file "src/uber_cs_agent/eval.py"

# Data files
check_file "data/sample/uber_threads.json"
check_file "evals/golden/golden_set.json"
check_file "evals/golden/LABELING_METHODOLOGY.md"

# Scripts
check_file "scripts/train.py"
check_file "scripts/evaluate.py"
check_file "scripts/run_agent.py"
check_file "scripts/build_golden.py"
check_file "scripts/create_sample.py"

# Documentation
check_file "README.md"
check_file "REPORT.md"
check_file "DECISIONS.md"
check_file "LICENSE"
check_file ".env.example"
check_file "pyproject.toml"

echo ""
echo "Checking golden set..."
echo "-----------------------------------"

GOLDEN_COUNT=$(python3 -c "import json; data = json.load(open('evals/golden/golden_set.json')); print(len(data))")
echo "Golden set size: $GOLDEN_COUNT examples"

if [ "$GOLDEN_COUNT" -ge 150 ]; then
    echo "✓ Golden set has ≥150 examples"
else
    echo "✗ Golden set has <150 examples (required: ≥150)"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "Checking intent coverage..."
echo "-----------------------------------"

python3 -c "
import json
data = json.load(open('evals/golden/golden_set.json'))
intents = set(ex['intent'] for ex in data)
required = {'trip_issue', 'payment', 'account', 'safety', 'driver_issue', 
            'cancellation', 'refund', 'app_bug', 'promo', 'eta_wait', 'other'}
missing = required - intents
if missing:
    print(f'✗ Missing intents: {missing}')
    exit(1)
else:
    print('✓ All 11 intents present in golden set')
"

if [ $? -ne 0 ]; then
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "Testing pipeline without API key..."
echo "-----------------------------------"

# Ensure no API key is set
unset OPENAI_API_KEY
unset HIVER_LLM_API_KEY

# Create training data
echo "Creating training data..."
python3 scripts/create_sample.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ create_sample.py runs successfully"
else
    echo "✗ create_sample.py failed"
    ERRORS=$((ERRORS + 1))
fi

# Train model
echo "Training model..."
python3 scripts/train.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ train.py runs successfully"
else
    echo "✗ train.py failed"
    ERRORS=$((ERRORS + 1))
fi

# Run evaluation
echo "Running evaluation..."
python3 scripts/evaluate.py > /tmp/eval_output.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✓ evaluate.py runs successfully"
    
    # Extract key metrics
    INTENT_ACC=$(grep "Intent accuracy:" /tmp/eval_output.txt | tail -1 | awk '{print $3}')
    echo "  Intent accuracy: $INTENT_ACC"
else
    echo "✗ evaluate.py failed"
    cat /tmp/eval_output.txt
    ERRORS=$((ERRORS + 1))
fi

# Test run_agent
echo "Testing run_agent..."
python3 scripts/run_agent.py --query "My driver took a long route" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ run_agent.py runs successfully"
else
    echo "✗ run_agent.py failed"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ ALL CHECKS PASSED"
    echo "==================================="
    exit 0
else
    echo "✗ $ERRORS ERRORS FOUND"
    echo "==================================="
    exit 1
fi
