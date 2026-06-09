"""
Script Purpose: Simple Decision Tree Simulator — Loan Approval
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 5 of 30

This script simulates a decision tree for loan approval.
It prints the exact decision path taken for each applicant
showing how decision trees work through branching logic.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR   = "=" * 55
THIN_LINE   = "-" * 55
APP_NAME    = "Loan Approval Decision Tree Simulator"

# ─── DECISION RULES ────────────────────────────────
MIN_AGE          = 18
MIN_INCOME       = 30000
MIN_CREDIT_SCORE = 600


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 5 — Decision Tree Simulation")
    print(SEPARATOR)


def display_tree_structure():
    """
    Display visual structure of the decision tree.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   DECISION TREE STRUCTURE")
    print(THIN_LINE)
    print(f"""
   [ROOT NODE] Is age >= {MIN_AGE}?
   │
   ├── No  → REJECTED
   │         Reason: Applicant must be 18 or older
   │
   └── Yes → [NODE 1] Is income >= {MIN_INCOME}?
             │
             ├── No  → REJECTED
             │         Reason: Income below minimum requirement
             │
             └── Yes → [NODE 2] Is credit score >= {MIN_CREDIT_SCORE}?
                       │
                       ├── No  → REJECTED
                       │         Reason: Credit score too low
                       │
                       └── Yes → [LEAF NODE] APPROVED
                                 Reason: All conditions met
    """)
    print(THIN_LINE)


def evaluate_loan(age, income, credit_score):
    """
    Evaluate loan application through decision tree.
    Prints each decision node visited along the path.

    Parameters:
        age          (int): Applicant age
        income       (float): Annual income
        credit_score (int): Credit score

    Returns:
        str: Final decision — Approved or Rejected
    """
    print(f"\n{THIN_LINE}")
    print("   DECISION PATH")
    print(THIN_LINE)

    # ─── ROOT NODE — AGE CHECK ─────────────────────
    # First question in the decision tree
    print(f"   [ROOT NODE] Is age ({age}) >= {MIN_AGE}?")

    if age < MIN_AGE:
        # ─── LEAF NODE — REJECT ────────────────────
        print(f"   └── No → REJECTED")
        print(f"\n   Reason: Applicant must be {MIN_AGE} or older")
        return "Rejected"

    print(f"   └── Yes → Moving to next node...\n")

    # ─── NODE 1 — INCOME CHECK ─────────────────────
    # Second question — only reached if age check passed
    print(f"   [NODE 1] Is income ({income:,}) >= {MIN_INCOME:,}?")

    if income < MIN_INCOME:
        # ─── LEAF NODE — REJECT ────────────────────
        print(f"   └── No → REJECTED")
        print(f"\n   Reason: Income below minimum requirement of "
              f"{MIN_INCOME:,}")
        return "Rejected"

    print(f"   └── Yes → Moving to next node...\n")

    # ─── NODE 2 — CREDIT SCORE CHECK ──────────────
    # Third question — only reached if income check passed
    print(f"   [NODE 2] Is credit score ({credit_score}) "
          f">= {MIN_CREDIT_SCORE}?")

    if credit_score < MIN_CREDIT_SCORE:
        # ─── LEAF NODE — REJECT ────────────────────
        print(f"   └── No → REJECTED")
        print(f"\n   Reason: Credit score below minimum of "
              f"{MIN_CREDIT_SCORE}")
        return "Rejected"

    print(f"   └── Yes → Moving to leaf node...\n")

    # ─── LEAF NODE — APPROVE ───────────────────────
    # All conditions passed — loan approved
    print(f"   [LEAF NODE] All conditions met → APPROVED")
    return "Approved"


def display_result(applicant_name, age, income,
                   credit_score, decision):
    """
    Display final result summary for the applicant.

    Parameters:
        applicant_name (str): Name of applicant
        age            (int): Applicant age
        income         (float): Annual income
        credit_score   (int): Credit score
        decision       (str): Final loan decision

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print("   FINAL RESULT")
    print(THIN_LINE)
    print(f"   Applicant    : {applicant_name}")
    print(f"   Age          : {age}")
    print(f"   Income       : {income:,}")
    print(f"   Credit Score : {credit_score}")
    print(f"   Decision     : {decision.upper()}")
    print(THIN_LINE)


def run_simulator():
    """
    Main function to run the loan approval decision tree.

    Parameters: None
    Returns: None
    """
    display_header()
    display_tree_structure()

    while True:
        try:
            print(f"\n{THIN_LINE}")
            print("   ENTER APPLICANT DETAILS")
            print(THIN_LINE)

            # ─── GET APPLICANT DETAILS ─────────────
            applicant_name = input("   Applicant Name : ").strip()
            age            = int(input("   Age            : "))
            income         = float(input("   Annual Income  : "))
            credit_score   = int(input("   Credit Score   : "))

            # ─── RUN THROUGH DECISION TREE ─────────
            decision = evaluate_loan(age, income, credit_score)

            # ─── DISPLAY FINAL RESULT ──────────────
            display_result(
                applicant_name, age,
                income, credit_score, decision
            )

        except ValueError:
            print("\n   Invalid input. Please enter correct values.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Evaluate another applicant? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using the Decision Tree Simulator.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_simulator()