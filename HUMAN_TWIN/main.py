from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import SimulationInput, SimulationOutput
from model import simulate_model, recommend_sleep_adjustment

# ---------------------------------------------------
# Create FastAPI app
# ---------------------------------------------------

app = FastAPI(
    title="Simpolicy AI Backend",
    description="Academic Policy Simulation & Dropout Risk Prediction Engine",
    version="1.0.0"
)

# ---------------------------------------------------
# Enable CORS (IMPORTANT for frontend connection)
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Health Check Route
# ---------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Simpolicy AI Backend is running successfully 🚀"
    }

# ---------------------------------------------------
# Main Simulation Endpoint
# ---------------------------------------------------

@app.post("/simulate", response_model=SimulationOutput)
def simulate(data: SimulationInput):
    """
    Receives student parameters from frontend,
    returns:
    - stress
    - engagement
    - dropout risk probability
    - risk level
    - recommended sleep adjustment
    """

    # Core ML prediction
    prediction = simulate_model(data)

    # Counterfactual sleep recommendation
    recommendation = recommend_sleep_adjustment(data)

    # Merge results
    return {
        **prediction,
        **recommendation
    }