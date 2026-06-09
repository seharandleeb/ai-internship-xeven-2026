"""
Script Purpose: ML Concepts — Supervised, Unsupervised,
                Reinforcement Learning Demonstration
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 5 of 30

This script demonstrates the three main types of machine
learning through simple Python simulations. It shows how
each type learns and makes decisions differently.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55
APP_NAME  = "ML Concepts Explorer"


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 5 — Supervised, Unsupervised, Reinforcement")
    print(SEPARATOR)


def supervised_learning_demo():
    """
    Demonstrate supervised learning concept.
    Uses labeled training data to make predictions.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SUPERVISED LEARNING — EMAIL SPAM CLASSIFIER")
    print(THIN_LINE)
    print("   Concept: Model learns from labeled examples")
    print("   Training data has both INPUT and correct OUTPUT")
    print(THIN_LINE)

    # ─── SIMULATED TRAINING DATA ───────────────────
    # In real ML, model learns these patterns automatically
    # Here we simulate what the model has learned

    training_data = [
        {"subject": "Win a prize now",    "label": "Spam"},
        {"subject": "Meeting at 3pm",     "label": "Not Spam"},
        {"subject": "Free money click",   "label": "Spam"},
        {"subject": "Project deadline",   "label": "Not Spam"},
        {"subject": "Claim your reward",  "label": "Spam"},
    ]

    print("\n   Training Data the Model Learned From:")
    print(f"   {'Subject':<30} {'Label'}")
    print(f"   {'-'*30} {'-'*10}")

    for item in training_data:
        print(f"   {item['subject']:<30} {item['label']}")

    # ─── SPAM KEYWORDS LEARNED FROM TRAINING ───────
    spam_keywords = ["win", "free", "prize", "money",
                     "claim", "reward", "click"]

    print(f"\n   Keywords model learned indicate spam:")
    print(f"   {spam_keywords}")

    # ─── MAKE PREDICTIONS ON NEW DATA ──────────────
    print(f"\n   Making predictions on new emails:")
    print(THIN_LINE)

    test_emails = [
        "Win free prizes today",
        "Team lunch tomorrow",
        "Claim your free reward",
        "Quarterly report attached"
    ]

    for email in test_emails:
        # Check if any spam keyword is in the email
        is_spam = any(
            keyword in email.lower()
            for keyword in spam_keywords
        )
        prediction = "Spam" if is_spam else "Not Spam"
        print(f"   '{email}'")
        print(f"   Prediction: {prediction}\n")


def unsupervised_learning_demo():
    """
    Demonstrate unsupervised learning concept.
    Finds patterns in data without any labels.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   UNSUPERVISED LEARNING — CUSTOMER SEGMENTATION")
    print(THIN_LINE)
    print("   Concept: Model finds patterns without labels")
    print("   No correct answers given — model groups similar data")
    print(THIN_LINE)

    # ─── CUSTOMER DATA WITHOUT LABELS ──────────────
    # No spam/not spam, no categories given
    # Model must find groups on its own

    customers = [
        {"name": "Ali",    "age": 25, "spending": 5000,  "visits": 2},
        {"name": "Sara",   "age": 45, "spending": 25000, "visits": 8},
        {"name": "Ahmed",  "age": 28, "spending": 4500,  "visits": 3},
        {"name": "Fatima", "age": 52, "spending": 30000, "visits": 10},
        {"name": "Usman",  "age": 23, "spending": 3000,  "visits": 1},
        {"name": "Ayesha", "age": 48, "spending": 22000, "visits": 7},
    ]

    print("\n   Customer Data (No Labels Given):")
    print(f"   {'Name':<10} {'Age':<6} {'Spending':<12} {'Visits'}")
    print(f"   {'-'*10} {'-'*6} {'-'*12} {'-'*6}")

    for customer in customers:
        print(f"   {customer['name']:<10} "
              f"{customer['age']:<6} "
              f"{customer['spending']:<12} "
              f"{customer['visits']}")

    # ─── SIMPLE CLUSTERING SIMULATION ──────────────
    # Group customers by spending pattern
    # This simulates what clustering algorithms do

    print("\n   Model discovered these natural groups:")
    print(THIN_LINE)

    high_value   = []
    medium_value = []
    low_value    = []

    for customer in customers:
        if customer["spending"] >= 20000:
            high_value.append(customer["name"])
        elif customer["spending"] >= 10000:
            medium_value.append(customer["name"])
        else:
            low_value.append(customer["name"])

    print(f"   Group 1 — High Value Customers  : {high_value}")
    print(f"   Group 2 — Medium Value Customers: {medium_value}")
    print(f"   Group 3 — Low Value Customers   : {low_value}")
    print(f"\n   Note: No labels were given — model found these")
    print(f"   groups by itself based on spending patterns.")


def reinforcement_learning_demo():
    """
    Demonstrate reinforcement learning concept.
    Agent learns by taking actions and receiving rewards.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   REINFORCEMENT LEARNING — GAME AGENT SIMULATION")
    print(THIN_LINE)
    print("   Concept: Agent learns through trial and error")
    print("   Good actions get rewards, bad actions get penalties")
    print(THIN_LINE)

    # ─── AGENT SIMULATION ──────────────────────────
    # Simulate an agent learning to navigate a simple game
    # Agent starts with no knowledge and learns over time

    agent_score  = 0
    total_moves  = 0
    good_moves   = 0
    bad_moves    = 0

    # ─── SIMULATED LEARNING EPISODES ───────────────
    # Each episode represents the agent trying an action

    episodes = [
        {"action": "Move Right", "result": "Found food",    "reward": 10},
        {"action": "Move Left",  "result": "Hit wall",      "reward": -5},
        {"action": "Move Up",    "result": "Found exit",    "reward": 50},
        {"action": "Move Down",  "result": "Found nothing", "reward": -1},
        {"action": "Move Right", "result": "Found food",    "reward": 10},
        {"action": "Move Right", "result": "Found food",    "reward": 10},
    ]

    print("\n   Agent Learning Episodes:")
    print(f"   {'Episode':<10} {'Action':<15} {'Result':<20} {'Reward'}")
    print(f"   {'-'*10} {'-'*15} {'-'*20} {'-'*6}")

    for index, episode in enumerate(episodes):
        agent_score += episode["reward"]
        total_moves += 1

        if episode["reward"] > 0:
            good_moves += 1
        else:
            bad_moves += 1

        print(f"   {index + 1:<10} "
              f"{episode['action']:<15} "
              f"{episode['result']:<20} "
              f"{episode['reward']:+}")

    # ─── LEARNING SUMMARY ──────────────────────────
    print(f"\n   Learning Summary:")
    print(THIN_LINE)
    print(f"   Total Moves  : {total_moves}")
    print(f"   Good Moves   : {good_moves}")
    print(f"   Bad Moves    : {bad_moves}")
    print(f"   Final Score  : {agent_score}")
    print(f"\n   Agent learned: Move Right gives rewards!")
    print(f"   Next time it will prefer moving right.")


def display_comparison_table():
    """
    Display comparison table of all three ML types.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   ML TYPES COMPARISON TABLE")
    print(THIN_LINE)
    print(f"   {'Aspect':<20} {'Supervised':<18} "
          f"{'Unsupervised':<18} {'Reinforcement'}")
    print(f"   {'-'*20} {'-'*18} {'-'*18} {'-'*15}")
    print(f"   {'Data':<20} {'Labeled':<18} "
          f"{'Unlabeled':<18} {'No data needed'}")
    print(f"   {'Learning':<20} {'From examples':<18} "
          f"{'Find patterns':<18} {'Trial and error'}")
    print(f"   {'Output':<20} {'Prediction':<18} "
          f"{'Groups/clusters':<18} {'Policy/actions'}")
    print(f"   {'Example':<20} {'Spam filter':<18} "
          f"{'Customer groups':<18} {'Game AI'}")
    print(THIN_LINE)


def run_ml_concepts():
    """
    Main function to run the ML concepts explorer.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        print(f"\n{THIN_LINE}")
        print("   SELECT CONCEPT")
        print(THIN_LINE)
        print("   1. Supervised Learning Demo")
        print("   2. Unsupervised Learning Demo")
        print("   3. Reinforcement Learning Demo")
        print("   4. ML Types Comparison Table")
        print("   5. Exit")
        print(THIN_LINE)

        choice = input("   Enter choice (1-5): ").strip()

        if choice == "1":
            supervised_learning_demo()
        elif choice == "2":
            unsupervised_learning_demo()
        elif choice == "3":
            reinforcement_learning_demo()
        elif choice == "4":
            display_comparison_table()
        elif choice == "5":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using ML Concepts Explorer.")
            print(SEPARATOR)
            break
        else:
            print("\n   Invalid choice. Please enter 1 to 5.")


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_ml_concepts()