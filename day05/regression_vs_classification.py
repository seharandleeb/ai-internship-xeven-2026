"""
Script Purpose: Regression vs Classification Demonstration
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 5 of 30

This script demonstrates the difference between regression
and classification problems using real-world examples.
Regression predicts continuous values, classification
predicts discrete categories.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55
APP_NAME  = "Regression vs Classification Demo"


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


def predict_house_price(size, bedrooms, location_score, age):
    """
    Simulate regression — predict house price as continuous value.
    Uses a simple formula to estimate price based on features.

    Parameters:
        size           (float): Size in square feet
        bedrooms       (int): Number of bedrooms
        location_score (int): Location quality score 1-10
        age            (int): Age of house in years

    Returns:
        float: Estimated house price
    """
    # ─── SIMPLE PRICE FORMULA ──────────────────────
    # Each feature contributes to the final price
    # This simulates how regression models work

    base_price     = 50000                    # base price
    size_value     = size * 100               # 100 per sq ft
    bedroom_value  = bedrooms * 15000         # 15k per bedroom
    location_value = location_score * 10000  # 10k per score
    age_deduction  = age * 500               # depreciation

    # ─── CALCULATE FINAL PRICE ─────────────────────
    estimated_price = (base_price + size_value +
                      bedroom_value + location_value -
                      age_deduction)

    # ─── ENSURE PRICE IS NOT NEGATIVE ──────────────
    if estimated_price < 0:
        estimated_price = base_price

    return round(estimated_price, 2)


def predict_temperature(month, humidity, cloud_cover):
    """
    Simulate regression — predict temperature as continuous value.

    Parameters:
        month       (int): Month number 1-12
        humidity    (int): Humidity percentage 0-100
        cloud_cover (int): Cloud cover percentage 0-100

    Returns:
        float: Predicted temperature in celsius
    """
    # ─── SEASONAL BASE TEMPERATURES ────────────────
    # Temperature varies by month in Pakistan
    seasonal_temps = {
        1: 12, 2: 15, 3: 22, 4: 30,
        5: 36, 6: 40, 7: 38, 8: 37,
        9: 33, 10: 27, 11: 20, 12: 14
    }

    base_temp = seasonal_temps.get(month, 25)

    # ─── ADJUST FOR CONDITIONS ─────────────────────
    humidity_effect    = humidity * 0.05     # humidity adds heat
    cloud_effect       = cloud_cover * 0.1  # clouds reduce heat

    predicted_temp = base_temp + humidity_effect - cloud_effect

    return round(predicted_temp, 1)


def classify_email(has_spam_words, unknown_sender,
                   has_links, all_caps):
    """
    Simulate classification — classify email as spam or not spam.

    Parameters:
        has_spam_words  (bool): Contains spam keywords
        unknown_sender  (bool): Sender is unknown
        has_links       (bool): Contains suspicious links
        all_caps        (bool): Written in all capitals

    Returns:
        str: Classification result with confidence
    """
    # ─── COUNT SPAM INDICATORS ─────────────────────
    # Each indicator adds to spam score
    spam_score = 0

    if has_spam_words:
        spam_score += 40    # strongest indicator
    if unknown_sender:
        spam_score += 25    # moderate indicator
    if has_links:
        spam_score += 20    # moderate indicator
    if all_caps:
        spam_score += 15    # weak indicator

    # ─── CLASSIFY BASED ON SCORE ───────────────────
    if spam_score >= 70:
        return f"SPAM — High confidence ({spam_score}% spam score)"
    elif spam_score >= 40:
        return f"SPAM — Medium confidence ({spam_score}% spam score)"
    elif spam_score >= 20:
        return f"NOT SPAM — Low spam score ({spam_score}%)"
    else:
        return f"NOT SPAM — Very low spam score ({spam_score}%)"


def classify_disease(age, bmi, blood_pressure,
                     blood_sugar, smoker):
    """
    Simulate classification — classify diabetes risk level.

    Parameters:
        age            (int): Patient age
        bmi            (float): Body mass index
        blood_pressure (int): Blood pressure systolic
        blood_sugar    (int): Fasting blood sugar mg/dL
        smoker         (bool): Is patient a smoker

    Returns:
        str: Risk classification
    """
    # ─── CALCULATE RISK SCORE ──────────────────────
    risk_score = 0

    # Age risk factor
    if age > 60:
        risk_score += 30
    elif age > 45:
        risk_score += 20
    elif age > 35:
        risk_score += 10

    # BMI risk factor
    if bmi > 35:
        risk_score += 30
    elif bmi > 30:
        risk_score += 20
    elif bmi > 25:
        risk_score += 10

    # Blood pressure risk factor
    if blood_pressure > 140:
        risk_score += 20
    elif blood_pressure > 120:
        risk_score += 10

    # Blood sugar risk factor
    if blood_sugar > 126:
        risk_score += 25
    elif blood_sugar > 100:
        risk_score += 15

    # Smoking risk factor
    if smoker:
        risk_score += 15

    # ─── CLASSIFY RISK LEVEL ───────────────────────
    if risk_score >= 70:
        return f"HIGH RISK — Immediate medical consultation needed"
    elif risk_score >= 40:
        return f"MODERATE RISK — Regular monitoring recommended"
    else:
        return f"LOW RISK — Maintain healthy lifestyle"


def run_demo():
    """
    Main function to run regression vs classification demo.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        print(f"\n{THIN_LINE}")
        print("   SELECT DEMO")
        print(THIN_LINE)
        print("   1. Regression — House Price Prediction")
        print("   2. Regression — Temperature Prediction")
        print("   3. Classification — Email Spam Detection")
        print("   4. Classification — Disease Risk Detection")
        print("   5. Exit")
        print(THIN_LINE)

        choice = input("   Enter choice (1-5): ").strip()

        if choice == "1":
            try:
                print(f"\n{THIN_LINE}")
                print("   HOUSE PRICE PREDICTION — REGRESSION")
                print(THIN_LINE)

                size           = float(input("   Size (sq ft)      : "))
                bedrooms       = int(input("   Bedrooms          : "))
                location_score = int(input("   Location (1-10)   : "))
                age            = int(input("   House age (years) : "))

                price = predict_house_price(
                    size, bedrooms, location_score, age
                )

                print(f"\n   Estimated Price : ${price:,.2f}")
                print(f"   Output Type     : Continuous value (Regression)")

            except ValueError:
                print("\n   Invalid input. Please enter correct values.")

        elif choice == "2":
            try:
                print(f"\n{THIN_LINE}")
                print("   TEMPERATURE PREDICTION — REGRESSION")
                print(THIN_LINE)

                month       = int(input("   Month (1-12)   : "))
                humidity    = int(input("   Humidity (%)   : "))
                cloud_cover = int(input("   Cloud cover (%) : "))

                temp = predict_temperature(month, humidity, cloud_cover)

                print(f"\n   Predicted Temperature : {temp}°C")
                print(f"   Output Type           : Continuous value (Regression)")

            except ValueError:
                print("\n   Invalid input. Please enter correct values.")

        elif choice == "3":
            print(f"\n{THIN_LINE}")
            print("   EMAIL SPAM DETECTION — CLASSIFICATION")
            print(THIN_LINE)

            has_spam_words = input("   Has spam words? (yes/no) : ").lower() == "yes"
            unknown_sender = input("   Unknown sender? (yes/no) : ").lower() == "yes"
            has_links      = input("   Has links? (yes/no)      : ").lower() == "yes"
            all_caps       = input("   All caps? (yes/no)       : ").lower() == "yes"

            result = classify_email(
                has_spam_words, unknown_sender,
                has_links, all_caps
            )

            print(f"\n   Result      : {result}")
            print(f"   Output Type : Discrete category (Classification)")

        elif choice == "4":
            try:
                print(f"\n{THIN_LINE}")
                print("   DISEASE RISK DETECTION — CLASSIFICATION")
                print(THIN_LINE)

                age            = int(input("   Age                : "))
                bmi            = float(input("   BMI                : "))
                blood_pressure = int(input("   Blood pressure     : "))
                blood_sugar    = int(input("   Blood sugar (mg/dL): "))
                smoker         = input("   Smoker? (yes/no)   : ").lower() == "yes"

                result = classify_disease(
                    age, bmi, blood_pressure,
                    blood_sugar, smoker
                )

                print(f"\n   Result      : {result}")
                print(f"   Output Type : Discrete category (Classification)")

            except ValueError:
                print("\n   Invalid input. Please enter correct values.")

        elif choice == "5":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using Regression vs Classification Demo.")
            print(SEPARATOR)
            break

        else:
            print("\n   Invalid choice. Please enter 1 to 5.")


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_demo()