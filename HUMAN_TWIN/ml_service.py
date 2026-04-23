import joblib
import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / "dropout_model.pkl"

# Load model with error handling
try:
    model = joblib.load(str(MODEL_PATH))
except FileNotFoundError:
    print(f"ERROR: Model file not found at {MODEL_PATH}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script directory: {SCRIPT_DIR}")
    raise
except Exception as e:
    print(f"ERROR loading model: {e}")
    raise

def predict_dropout_risk(engagement_norm, grade_norm):

    features = [[engagement_norm, grade_norm]]
    probability = model.predict_proba(features)[0][1]

    if probability < 0.3:
        risk = "Low"
    elif probability < 0.6:
        risk = "Medium"
    else:
        risk = "High"

    return probability, risk