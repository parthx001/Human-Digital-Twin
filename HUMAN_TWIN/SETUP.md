# Human Digital Twin - Complete Setup Guide

## Prerequisites

Make sure you have the required Python packages installed:

```powershell
pip install fastapi uvicorn pandas scikit-learn joblib streamlit matplotlib pydantic python-multipart
```

## Running the Application

The application has multiple components that need to be running simultaneously:

### Option 1: Frontend Web Dashboard (Recommended)

**Terminal 1 - Start the Backend API:**
```powershell
cd d:\hackathon\HUMAN_TWIN
uvicorn backend_api:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Start the Frontend Server:**
```powershell
cd d:\hackathon\HUMAN_TWIN
python serve_frontend.py
```

Then open your browser and go to:
```
http://localhost:3000
```

### Option 2: Streamlit Dashboard

```powershell
cd d:\hackathon\HUMAN_TWIN
streamlit run app.py
```

This opens a Streamlit interface where you can:
- Adjust policy pressure and simulation duration with sliders
- Click "Run AI Simulation" to run the simulation
- View results with stress, learning, and dropout risk metrics
- See visualization graphs

## Troubleshooting

### "ERROR: Could not run simulation" in web dashboard

1. Check that backend API is running (Terminal 1)
   - You should see: `Uvicorn running on http://127.0.0.1:8000`

2. Check browser console for errors (F12 → Console tab)

3. Try accessing the API directly:
   ```powershell
   curl -X GET http://127.0.0.1:8000/
   ```
   Should return: `{"message":"Human Digital Twin Backend API is running","status":"ok"}`

### Model file not found

If you get "Model file not found", regenerate the model:
```powershell
cd d:\hackathon\HUMAN_TWIN
python ml_model.py
```

### Data encoding errors

The CSV files use UTF-8 encoding. The code now handles this automatically with encoding detection.

## File Structure

```
HUMAN_TWIN/
├── app.py                 # Streamlit web interface
├── backend_api.py         # FastAPI backend (used by web dashboard)
├── serve_frontend.py      # Simple HTTP server for frontend
├── ml_model.py           # Model training script
├── ml_service.py         # ML prediction service
├── preprocessing.py      # Data preprocessing
├── simulation.py         # Simulation engine
├── models.py            # Student model definition
├── dropout_model.pkl    # Trained ML model (generated)
├── frontend/
│   ├── index.html       # Web dashboard HTML/CSS/JS
│   └── script.js        # Optional JS module
├── data/
│   ├── studentInfo.csv
│   ├── studentAssessment.csv
│   ├── studentVle.csv
│   └── stress_dataset.csv
└── __pycache__/         # Python cache (ignore)
```

## How It Works

1. **Data Loading**: CSV files are loaded from `data/` directory with UTF-8 encoding
2. **Preprocessing**: Student data is normalized and engagement/grade metrics are calculated
3. **Simulation**: A population of Students is created based on real data
4. **ML Prediction**: Random Forest model predicts dropout risk based on engagement and grades
5. **Visualization**: Results are displayed with stress bars, engagement gauges, and trend graphs

## Key Features

- ✅ Multi-user authentication (web dashboard only)
- ✅ Adjustable simulation parameters
- ✅ Real-time stress/engagement calculations  
- ✅ AI dropout risk prediction
- ✅ Simulation history tracking
- ✅ PDF report export
- ✅ Error handling with user feedback

## API Endpoints

### Backend API (http://127.0.0.1:8000)

#### GET / 
Returns API status
```json
{"message":"Human Digital Twin Backend API is running","status":"ok"}
```

#### POST /simulate
Accepts JSON payload:
```json
{
  "attendance": 85,
  "assignments": 4,
  "examGap": 10,
  "sleep": 7,
  "cgpa": 7.5
}
```

Returns:
```json
{
  "stress": 15.5,
  "engagement": 89.2,
  "risk_prob": 12.5,
  "risk_level": "Low"
}
```

## Support

If you encounter any issues:
1. Check the Python console output for error messages
2. Verify all files in the `data/` folder are present
3. Ensure Python packages are installed: `pip install -r requirements.txt`
4. Regenerate the ML model: `python ml_model.py`
