from fastapi import FastAPI
from pydantic import BaseModel
from ml_service import predict_dropout_risk
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PolicyInput(BaseModel):
    attendance: float
    assignments: float
    examGap: float
    sleep: float
    cgpa: float

class ChatInput(BaseModel):
    message: str
    context: dict = {}


@app.post("/simulate")
def simulate_policy(data: PolicyInput):
    try:
        # Normalize values
        engagement_norm = data.attendance / 100
        grade_norm = data.cgpa / 10

        risk_prob, risk_level = predict_dropout_risk(
            engagement_norm,
            grade_norm
        )

        # Simple stress formula (backend side)
        stress = (
            (1 - engagement_norm) * 0.4 +
            (data.assignments / 10) * 0.3 +
            (1 - data.sleep / 8) * 0.3
        ) * 100

        engagement = 100 - (stress * 0.7)

        return {
            "stress": round(stress, 2),
            "engagement": round(engagement, 2),
            "risk_prob": round(risk_prob * 100, 2),
            "risk_level": risk_level
        }
    except Exception as e:
        return {"error": str(e), "message": "An error occurred during simulation"}

@app.post("/chat")
def chat_handler(data: ChatInput):
    try:
        msg = data.message.lower().strip()
        context = data.context or {}
        
        # Extract context metrics
        stress = context.get('stress', 50) if isinstance(context, dict) else 50
        engagement = context.get('engagement', 50) if isinstance(context, dict) else 50
        
        # Simple rule-based responses
        if any(w in msg for w in ['stress', 'anxious', 'worried', 'pressure', 'overwhelm']):
            if stress > 70:
                return {"response": "Your stress level is high. Try breaking tasks into smaller steps. Schedule 5-10 min breaks every hour, and ensure you're getting 7-8 hours of sleep."}
            else:
                return {"response": "Stress management tip: Practice deep breathing (4-7-8 technique), take walks, or meditate for 10 min daily. You're managing well!"}
        
        elif any(w in msg for w in ['sleep', 'tired', 'fatigue', 'exhausted']):
            return {"response": "Sleep is critical for academic performance. Aim for 7-8 hours nightly. Create a dark, cool sleep environment and avoid screens 30 min before bed."}
        
        elif any(w in msg for w in ['assignment', 'work', 'task', 'deadline']):
            return {"response": "Manage workload by: 1) Prioritize urgent tasks, 2) Break big assignments into parts, 3) Track deadlines in a calendar, 4) Aim for completion 24h early."}
        
        elif any(w in msg for w in ['attendance', 'class', 'attend']):
            return {"response": "Regular attendance improves learning and mental health. Attend classes consistently—missing even a few impacts your overall engagement and stress levels."}
        
        elif any(w in msg for w in ['grade', 'cgpa', 'performance']):
            return {"response": "Boost grades by: consistent studying, seeking help early, reviewing past exams, and focusing on problem areas. Small improvements compound over time!"}
        
        elif any(w in msg for w in ['hello', 'hi', 'hey', 'help']):
            return {"response": "Hi! I'm your Stress Coach. Ask me about managing stress, improving sleep, handling assignments, or boosting academic performance. What's on your mind?"}
        
        elif any(w in msg for w in ['engage', 'motivation', 'focus']):
            return {"response": "Stay engaged by: setting clear goals, working in focused 25-min blocks (Pomodoro), joining study groups, and celebrating small wins. You've got this!"}
        
        else:
            # Default supportive response
            return {"response": "That's a great question! Remember you're not alone—many students face similar challenges. Breaking things into smaller steps and taking care of yourself goes a long way."}
    
    except Exception as e:
        return {"response": "I'm here to help! Feel free to ask about stress, sleep, assignments, or grades."}

@app.get("/")
def read_root():
    return {"message": "Simpolicy AI Backend API is running", "status": "ok"}