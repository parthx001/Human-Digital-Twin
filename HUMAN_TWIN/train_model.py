import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load datasets
student_info = pd.read_csv(r"D:\hackathon\HUMAN_TWIN\data\studentInfo.csv")
student_vle = pd.read_csv(r"D:\hackathon\HUMAN_TWIN\data\studentVle.csv")
student_assessment = pd.read_csv(r"D:\hackathon\HUMAN_TWIN\data\studentAssessment.csv")

# -----------------------------
# Feature Engineering
# -----------------------------

# Aggregate VLE clicks (engagement proxy)
vle_agg = student_vle.groupby("id_student")["sum_click"].sum().reset_index()
vle_agg.rename(columns={"sum_click": "total_clicks"}, inplace=True)

# Aggregate assessment scores
assess_agg = student_assessment.groupby("id_student")["score"].mean().reset_index()
assess_agg.rename(columns={"score": "avg_score"}, inplace=True)

# Merge all
df = student_info.merge(vle_agg, on="id_student", how="left")
df = df.merge(assess_agg, on="id_student", how="left")

df.fillna(0, inplace=True)

# -----------------------------
# Target Variable
# -----------------------------
# Withdrawn = Dropout

df["dropout"] = df["final_result"].apply(lambda x: 1 if x == "Withdrawn" else 0)

# -----------------------------
# Select Features
# -----------------------------

features = [
    "studied_credits",
    "total_clicks",
    "avg_score"
]

X = df[features]
y = df["dropout"]

# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Scaling
# -----------------------------

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Logistic Regression Model
# -----------------------------

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

print(classification_report(y_test, model.predict(X_test_scaled)))

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model trained and saved!")