"""
run_pipeline.py
Master pipeline runner for the Delivery Performance, Delay Risk, and
Logistics Efficiency Analysis project.

Runs Module 1 -> 2 -> 3 -> 4 -> 5 automatically, IN ORDER.
Each module only starts after the previous one finishes successfully.
If any module fails, the pipeline stops immediately and tells you which
one broke, so you're not left wondering why a later step has bad data.

USAGE:
    python run_pipeline.py

REQUIREMENTS:
    - APL_Logistics.csv must be in the same folder as this script
    - All module1_*.py ... module5_*.py files must be in the same folder
    - pandas, numpy, matplotlib, seaborn, scikit-learn installed
"""

import subprocess
import sys
import time
import os

# ------------------------------------------------------------------
# Pipeline definition - add/remove/reorder modules here if needed
# ------------------------------------------------------------------
PIPELINE = [
    ("Module 1 - Data Cleaning",        "module1_cleaning.py"),
    ("Module 2 - Feature Engineering",  "module2_feature_engineering.py"),
    ("Module 3 - EDA",                  "module3_eda.py"),
    ("Module 4 - KPI Calculation",      "module4_kpi.py"),
    ("Module 5 - Delay Risk Model",     "module5_risk_model.py"),
]

REQUIRED_INPUT = "APL_Logistics.csv"


def check_prerequisites():
    """Make sure the raw file and all module scripts exist before starting."""
    missing = []
    if not os.path.exists(REQUIRED_INPUT):
        missing.append(REQUIRED_INPUT)
    for _, script in PIPELINE:
        if not os.path.exists(script):
            missing.append(script)

    if missing:
        print("ERROR: The following required files are missing from this folder:")
        for m in missing:
            print(f"   - {m}")
        print("\nPlace all module scripts and the raw CSV in the same folder as")
        print("run_pipeline.py, then try again.")
        sys.exit(1)


def run_module(name, script):
    """Run a single module script and stream its output live."""
    print("\n" + "=" * 70)
    print(f"RUNNING: {name}  ({script})")
    print("=" * 70)

    start = time.time()
    result = subprocess.run([sys.executable, script])
    elapsed = time.time() - start

    if result.returncode != 0:
        print("\n" + "!" * 70)
        print(f"PIPELINE STOPPED: {name} failed (exit code {result.returncode})")
        print(f"Fix the error above in '{script}', then re-run the pipeline.")
        print("!" * 70)
        sys.exit(result.returncode)

    print(f"\n{name} completed successfully in {elapsed:.1f}s")


def main():
    print("Delivery Performance & Delay Risk Analysis - Full Pipeline")
    print(f"Modules to run: {len(PIPELINE)}")

    check_prerequisites()

    overall_start = time.time()
    for name, script in PIPELINE:
        run_module(name, script)

    total = time.time() - overall_start
    print("\n" + "=" * 70)
    print(f"ALL MODULES COMPLETE  |  Total time: {total:.1f}s")
    print("=" * 70)
    print("\nOutputs generated:")
    print("  - cleaned_logistics.csv        (Module 1)")
    print("  - featured_logistics.csv       (Module 2)")
    print("  - eda_charts/ + eda_summary.txt (Module 3)")
    print("  - kpi_tables/ + kpi_summary.txt (Module 4)")
    print("  - feature_importance.csv/.png, confusion_matrix.png,")
    print("    roc_curve.png, model_summary.txt (Module 5)")


if __name__ == "__main__":
    main()
