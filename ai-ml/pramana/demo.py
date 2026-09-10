"""
PRAMANA Full Demonstration Runner.
Reproduces DEMO_OUTPUT.txt:
1. Ablation table (NAIVE vs No Grouping vs PRAMANA)
2. 3 representative Evidence Balance Sheets:
   - Case 1: Planted decoy (refused: k=1 < k_min=2)
   - Case 2: True pair (same operator: log10 LR 3.672 [STRONG])
   - Case 3: Account handover (resold account residual risk)
3. Sensitivity analysis sweep on lambda damping
"""

try:
    from pramana.evaluate import ablation_table, balance_sheet
    from pramana.sensitivity import sweep_lambda
except ModuleNotFoundError:
    from evaluate import ablation_table, balance_sheet
    from sensitivity import sweep_lambda


def run_demo():
    # 1. Headline ablation table
    assessments = ablation_table()

    # 2. Case 1: Planted decoy
    print("\n\n>>> CASE 1  planted decoy: two UNRELATED vendors on a rare shared host")
    if "acc_100__acc_129" in assessments:
        balance_sheet("acc_100__acc_129", assessments)

    # 3. Case 2: True pair
    print("\n\n>>> CASE 2  true pair: same operator, two marketplaces")
    if "acc_024__acc_025" in assessments:
        balance_sheet("acc_024__acc_025", assessments)

    # 4. Case 3: Account handover
    print("\n\n>>> CASE 3  account handover: the system is WRONG, and says why it can't tell")
    if "acc_048__acc_106" in assessments:
        balance_sheet("acc_048__acc_106", assessments)
        print("    ground truth: op_22 vs op_46  -> DIFFERENT operators. This is a false merge we do not claim to fix.\n")

    # 5. Sensitivity sweep
    sweep_lambda()


if __name__ == "__main__":
    run_demo()
