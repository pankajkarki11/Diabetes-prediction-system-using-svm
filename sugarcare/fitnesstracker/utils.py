# utils.py
def calculate_risk(age, bmi, family_history, physical_activity, smoking, alcohol_consumption):
    risk_score = 0

    # Age-based risk
    if age > 45:
        risk_score += 2

    # BMI-based risk
    if bmi > 25:
        risk_score += 3

    # Family history
    if family_history:
        risk_score += 2

    # Physical activity
    if physical_activity == 'low':
        risk_score += 2

    # Smoking and alcohol
    if smoking:
        risk_score += 2
    if alcohol_consumption:
        risk_score += 1

    return risk_score
