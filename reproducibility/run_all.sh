#!/usr/bin/env bash
set -euo pipefail

echo "====================================================================="
echo " AgentCacheBench: M24 Clean End-to-End Reproduction Pipeline"
echo "====================================================================="

# 1. Clean previous results
echo "[Stage 1/6] Cleaning raw results and output caches..."
rm -rf results/raw/*.json
rm -f results/m23_verified_metrics.json
rm -f results/final_verified_metrics.json
rm -f results/m23_claim_evidence_matrix.csv

# 2. Run Unit Tests
echo "[Stage 2/6] Executing unit test suite..."
PYTHONPATH=. python3 -m pytest tests/

# 3. Execute M2 Pilot
echo "[Stage 3/6] Running M2 Minimal Falsification Pilot..."
PYTHONPATH=. python3 scripts/run_m2_pilot.py

# 4. Execute Main Experiments (M6/M7)
echo "[Stage 4/6] Running Main Experimental Matrix (M6/M7)..."
PYTHONPATH=. python3 scripts/run_experiments.py

# 5. Execute M23 Audit
echo "[Stage 5/6] Running M23 Independent Statistical Audit..."
PYTHONPATH=. python3 scripts/m23_independent_audit.py

# 6. Generate Figures, Tables, and IEEE Paper Artifacts
echo "[Stage 6/6] Generating Figures, LaTeX Tables, and Compiling IEEE Paper..."
PYTHONPATH=. python3 scripts/generate_figures_and_tables.py

if [ -f "paper/main.tex" ]; then
    cd paper
    pdflatex -interaction=nonstopmode main.tex || true
    bibtex main || true
    pdflatex -interaction=nonstopmode main.tex || true
    pdflatex -interaction=nonstopmode main.tex || true
    cd ..
fi

echo "====================================================================="
echo " Reproduction Complete! All outputs generated from raw observation pipeline."
echo " Verified metrics: results/final_verified_metrics.json"
echo " IEEE Paper PDF: paper/main.pdf"
echo "====================================================================="
