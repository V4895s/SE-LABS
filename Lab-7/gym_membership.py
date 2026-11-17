import math


def parse_plan(code):
    """Parse a plan code like 'GOLD-12' into ('GOLD', 12).

    Returns None if the input is not a valid plan code.
    """
    if not isinstance(code, str):
        return None
    parts = code.strip().split('-')
    if len(parts) != 2:
        return None
    plan, months = parts[0].strip(), parts[1].strip()
    if not plan or not plan.isalpha():
        return None
    # ASCII digits only, short enough to avoid huge-int issues
    if not (months.isascii() and months.isdigit()) or len(months) > 4:
        return None
    months = int(months)
    if months <= 0:
        return None
    return plan.upper(), months


def calculate_bmi(data):
    """Calculate BMI from 'weight,height' (kg, metres).

    Returns the BMI rounded to 1 decimal, or None if the input is invalid.
    """
    if not isinstance(data, str):
        return None
    parts = data.split(',')
    if len(parts) != 2:
        return None
    try:
        weight = float(parts[0])
        height = float(parts[1])
        if not (math.isfinite(weight) and math.isfinite(height)):
            return None
        if weight <= 0 or height <= 0:
            return None
        bmi = weight / (height ** 2)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(bmi):
        return None
    return round(bmi, 1)


def average_workout(minutes):
    """Average of space-separated workout minutes (integer division).

    Returns None if the input is empty or contains invalid values.
    """
    if not isinstance(minutes, str):
        return None
    tokens = minutes.split()
    if not tokens:
        return None
    values = []
    for token in tokens:
        try:
            value = int(token)
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    return sum(values) // len(values)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter a plan code (e.g. GOLD-12): ")
    result = parse_plan(user_input)
    if result is None:
        print("Invalid plan code. Expected format: NAME-MONTHS (e.g. GOLD-12)")
    else:
        print("Plan and Months:", result)

    print("\n==== Running calculate_bmi ====")
    user_input = input("Enter weight and height (e.g. 70,1.75): ")
    result = calculate_bmi(user_input)
    if result is None:
        print("Invalid input. Expected: weight,height with positive numbers (e.g. 70,1.75)")
    else:
        print("BMI:", result)

    print("\n==== Running average_workout ====")
    user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    result = average_workout(user_input)
    if result is None:
        print("Invalid input. Enter non-negative whole numbers separated by spaces.")
    else:
        print("Average Minutes:", result)


if __name__ == "__main__":
    main()
