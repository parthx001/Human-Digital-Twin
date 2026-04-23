import streamlit as st
import matplotlib.pyplot as plt
import copy
import traceback

from preprocessing import build_master_dataset
from simulation import create_population_from_data, simulate
from ml_service import predict_dropout_risk


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Human Digital Twin", layout="wide")


# ===============================
# CUSTOM DARK THEME
# ===============================
def apply_custom_style():
    st.markdown("""
        <style>
        body {
            background-color: #0f1117;
        }

        .stApp {
            background-color: #0f1117;
            color: white;
        }

        .metric-card {
            background-color: #141822;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0,255,136,0.2);
        }

        .risk-low {
            color: #00ff88;
            font-weight: bold;
            font-size: 22px;
        }

        .risk-medium {
            color: orange;
            font-weight: bold;
            font-size: 22px;
        }

        .risk-high {
            color: red;
            font-weight: bold;
            font-size: 22px;
        }

        .stButton>button {
            background-color: #00ff88;
            color: black;
            border-radius: 8px;
            font-weight: bold;
        }

        </style>
    """, unsafe_allow_html=True)


apply_custom_style()


# ===============================
# TITLE
# ===============================
st.title("🏛 Human Digital Twin – Academic Policy Impact Simulator")
st.markdown("AI-powered Digital Twin for Institutional Policy Risk Forecasting")


# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    try:
        print("[DEBUG] Starting to load master dataset...")
        df = build_master_dataset()
        print(f"[DEBUG] Successfully loaded data with {len(df)} rows")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        print(traceback.format_exc())
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()


try:
    df = load_data()
    if df is None or len(df) == 0:
        st.error(f"No data loaded!")
        st.stop()
except Exception as e:
    st.error(f"Fatal error during initialization: {str(e)}")
    st.stop()


# ===============================
# SIDEBAR CONTROLS
# ===============================
st.sidebar.header("Policy Controls")

policy_pressure = st.sidebar.slider(
    "Policy Strictness Level",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

weeks = st.sidebar.slider(
    "Simulation Duration (Weeks)",
    min_value=8,
    max_value=24,
    value=16
)

run_button = st.sidebar.button("Run AI Simulation")


# ===============================
# RUN SIMULATION
# ===============================
if run_button:
    try:
        st.info("Running AI Simulation...")
        
        students = create_population_from_data(df)
        students_copy = copy.deepcopy(students)

        stress, motivation, learning, population = simulate(
            students_copy,
            weeks=weeks,
            policy_pressure=policy_pressure
        )

        avg_stress = stress[-1]
        avg_learning = learning[-1]

        # AI Risk Prediction
        risk_prob, risk_level = predict_dropout_risk(
            1 - avg_stress,
            avg_learning
        )

        # ===============================
        # METRIC CARDS
        # ===============================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Final Stress</h3>
                    <h2>{round(avg_stress*100,2)}%</h2>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Final Learning</h3>
                    <h2>{round(avg_learning*100,2)}%</h2>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>AI Dropout Risk</h3>
                    <h2>{round(risk_prob*100,2)}%</h2>
                </div>
            """, unsafe_allow_html=True)

        # ===============================
        # RISK LEVEL COLOR DISPLAY
        # ===============================
        if risk_level == "Low":
            risk_class = "risk-low"
        elif risk_level == "Medium":
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"

        st.markdown(f"""
            <div class="{risk_class}">
                Risk Level: {risk_level}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ===============================
        # GRAPH SECTION
        # ===============================
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(stress, linewidth=3)
        ax.plot(learning, linewidth=3)

        ax.set_facecolor("#141822")
        fig.patch.set_facecolor("#0f1117")

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        ax.legend(["Stress", "Learning"])
        ax.grid(alpha=0.2)

        st.pyplot(fig)

        st.success("Simulation Completed Successfully")
        
    except Exception as e:
        st.error(f"Simulation failed: {str(e)}")
        print(f"[ERROR] Simulation error: {e}")
        print(traceback.format_exc())