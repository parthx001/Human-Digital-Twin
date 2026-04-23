import joblib
import numpy as np
from schemas import SimulationInput

# ---------------------------------------------------
# Load trained ML model and scaler
# ---------------------------------------------------

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


# ---------------------------------------------------
# Core Prediction Function
# ---------------------------------------------------

def simulate_model(data: SimulationInput):
    """
    Takes frontend input and returns:
    - stress
    - engagement
    - dropout risk probability
    - risk level
    """

    # --------------------------------------------
    # Map frontend inputs → ML model features
    # --------------------------------------------

    # These mappings approximate dataset structure
    studied_credits = data.attendance * 1.2
    total_clicks = data.assignments * 50 + data.attendance * 5
    avg_score = data.cgpa * 10

    features = np.array([[studied_credits, total_clicks, avg_score]])

    # Scale features
    scaled = scaler.transform(features)

    # Predict probability of dropout (class 1)
    prob = model.predict_proba(scaled)[0][1]
    risk_percentage = int(prob * 100)

    # Risk level classification
    if risk_percentage >= 70:
        level = "High"
    elif risk_percentage >= 40:
        level = "Medium"
    else:
        level = "Low"

    # --------------------------------------------
    # Derived Metrics (Heuristic Calculations)
    # --------------------------------------------

    # Stress increases with assignments, decreases with attendance
    stress = int((100 - data.attendance) * 0.4 + data.assignments * 3)
    stress = max(0, min(100, stress))

    # Engagement increases with attendance and sleep
    engagement = int(data.attendance * 0.5 + data.sleep * 5)
    engagement = max(0, min(100, engagement))

    return {
        "stress": stress,
        "engagement": engagement,
        "risk_prob": risk_percentage,
        "risk_level": level
    }


# ---------------------------------------------------
# Counterfactual Simulation:
# If assignments increase → how much sleep needed?
# ---------------------------------------------------

def recommend_sleep_adjustment(data: SimulationInput):
    """
    If assignments increase by 1,
    determine required sleep increase
    to maintain or reduce dropout risk.
    """

    # Get original risk
    original_result = simulate_model(data)
    original_risk = original_result["risk_prob"]

    new_assignments = data.assignments + 1

    # Try increasing sleep up to +5 hours
    for extra_sleep in range(0, 6):

        test_data = SimulationInput(
            attendance=data.attendance,
            assignments=new_assignments,
            examGap=data.examGap,
            sleep=min(12, data.sleep + extra_sleep),
            cgpa=data.cgpa
        )

        result = simulate_model(test_data)

        if result["risk_prob"] <= original_risk:
            return {
                "recommended_sleep": test_data.sleep,
                "sleep_increase": extra_sleep
            }

    # If no improvement found
    return {
        "recommended_sleep": data.sleep,
        "sleep_increase": 0
    }