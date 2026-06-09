"""
Script Purpose: Decision Tree Simulation
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 5 of 30

This script simulates a decision tree using nested conditional
statements. It demonstrates how decision trees make decisions
through branching logic with root, internal, and leaf nodes.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55
APP_NAME  = "Decision Tree Simulator"


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 5 — Machine Learning Concepts")
    print(SEPARATOR)


def loan_approval_tree(age, income, credit_score, employment):
    """
    Simulate a loan approval decision tree.

    Parameters:
        age          (int): Age of applicant
        income       (float): Annual income
        credit_score (int): Credit score 300-850
        employment   (str): Employment status

    Returns:
        str: Loan decision with reason
    """
    # ─── ROOT NODE ─────────────────────────────────
    # First question: Is applicant old enough?
    if age < 18:
        return "Rejected — Applicant must be 18 or older"

    # ─── INTERNAL NODE 1 ───────────────────────────
    # Second question: Is credit score acceptable?
    elif credit_score < 300 or credit_score > 850:
        return "Rejected — Invalid credit score"

    elif credit_score < 500:
        return "Rejected — Credit score too low (minimum 500)"

    # ─── INTERNAL NODE 2 ───────────────────────────
    # Third question: Is applicant employed?
    elif employment.lower() not in ("employed", "self-employed"):
        return "Rejected — Must be employed or self-employed"

    # ─── INTERNAL NODE 3 ───────────────────────────
    # Fourth question: Is income sufficient?
    elif income < 25000:
        return "Rejected — Minimum income requirement not met"

    elif income < 50000:
        # ─── LEAF NODE ─────────────────────────────
        # Low income but meets minimum requirements
        if credit_score >= 700:
            return "Approved — Small loan up to 10,000"
        else:
            return "Rejected — Credit score too low for income level"

    elif income < 100000:
        # ─── LEAF NODE ─────────────────────────────
        # Medium income applicant
        if credit_score >= 650:
            return "Approved — Medium loan up to 50,000"
        else:
            return "Approved — Small loan up to 10,000"

    else:
        # ─── LEAF NODE ─────────────────────────────
        # High income applicant
        if credit_score >= 750:
            return "Approved — Premium loan up to 200,000"
        elif credit_score >= 650:
            return "Approved — Large loan up to 100,000"
        else:
            return "Approved — Medium loan up to 50,000"


def medical_diagnosis_tree(age, fever, cough, fatigue, oxygen):
    """
    Simulate a simple medical diagnosis decision tree.

    Parameters:
        age     (int): Patient age
        fever   (float): Body temperature in celsius
        cough   (bool): Has cough or not
        fatigue (bool): Has fatigue or not
        oxygen  (int): Oxygen saturation percentage

    Returns:
        str: Diagnosis result
    """
    # ─── ROOT NODE ─────────────────────────────────
    # Check oxygen level first — critical condition
    if oxygen < 90:
        return "Critical — Immediate medical attention required"

    # ─── INTERNAL NODE 1 ───────────────────────────
    # Check for high fever
    elif fever >= 39.5:
        if cough and fatigue:
            return "High Risk — Possible severe infection, see doctor"
        elif cough or fatigue:
            return "Moderate Risk — Monitor closely, rest recommended"
        else:
            return "Moderate Risk — High fever, consult doctor"

    # ─── INTERNAL NODE 2 ───────────────────────────
    # Check for moderate fever
    elif fever >= 37.5:
        if cough and fatigue:
            return "Moderate Risk — Possible flu, rest and hydrate"
        elif age > 60 or age < 5:
            return "Moderate Risk — Vulnerable age group, monitor closely"
        else:
            return "Low Risk — Mild fever, rest and fluids recommended"

    # ─── LEAF NODE ─────────────────────────────────
    # No significant fever
    else:
        if cough and fatigue:
            return "Low Risk — Possible common cold, rest recommended"
        else:
            return "Healthy — No significant symptoms detected"


def display_tree_structure():
    """
    Display visual representation of a decision tree structure.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   DECISION TREE STRUCTURE — LOAN APPROVAL")
    print(THIN_LINE)
    print("""
   [ROOT] Is age >= 18?
   ├── No  → REJECT
   └── Yes → [NODE] Credit score >= 500?
             ├── No  → REJECT
             └── Yes → [NODE] Is employed?
                       ├── No  → REJECT
                       └── Yes → [NODE] Income >= 25000?
                                 ├── No  → REJECT
                                 └── Yes → [LEAF] Approve loan
    """)
    print(THIN_LINE)


def run_decision_tree():
    """
    Main function to run the decision tree simulator.

    Parameters: None
    Returns: None
    """
    display_header()
    display_tree_structure()

    while True:
        print(f"\n{THIN_LINE}")
        print("   SELECT DEMO")
        print(THIN_LINE)
        print("   1. Loan Approval Decision Tree")
        print("   2. Medical Diagnosis Decision Tree")
        print("   3. Exit")
        print(THIN_LINE)

        choice = input("   Enter choice (1-3): ").strip()

        if choice == "1":
            try:
                print(f"\n{THIN_LINE}")
                print("   LOAN APPROVAL SYSTEM")
                print(THIN_LINE)

                # ─── GET APPLICANT DETAILS ─────────
                age          = int(input("   Age             : "))
                income       = float(input("   Annual Income   : "))
                credit_score = int(input("   Credit Score    : "))
                employment   = input("   Employment      : ")

                # ─── RUN DECISION TREE ─────────────
                result = loan_approval_tree(
                    age, income, credit_score, employment
                )

                print(f"\n   Decision: {result}")

            except ValueError:
                print("\n   Invalid input. Please enter correct values.")

        elif choice == "2":
            try:
                print(f"\n{THIN_LINE}")
                print("   MEDICAL DIAGNOSIS SYSTEM")
                print(THIN_LINE)

                # ─── GET PATIENT DETAILS ───────────
                age     = int(input("   Age                    : "))
                fever   = float(input("   Temperature (celsius)  : "))
                cough   = input("   Has cough? (yes/no)    : ").lower() == "yes"
                fatigue = input("   Has fatigue? (yes/no)  : ").lower() == "yes"
                oxygen  = int(input("   Oxygen level (%)       : "))

                # ─── RUN DECISION TREE ─────────────
                result = medical_diagnosis_tree(
                    age, fever, cough, fatigue, oxygen
                )

                print(f"\n   Diagnosis: {result}")

            except ValueError:
                print("\n   Invalid input. Please enter correct values.")

        elif choice == "3":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using Decision Tree Simulator.")
            print(SEPARATOR)
            break

        else:
            print("\n   Invalid choice. Please enter 1, 2, or 3.")


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_decision_tree()