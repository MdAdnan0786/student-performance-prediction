import os
import sys
# Suppress all warnings before importing anything else
os.environ['PYTHONWARNINGS'] = 'ignore::RuntimeWarning'
import warnings
warnings.filterwarnings('ignore')

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Global variables for models
rf_model = None
gb_model = None
preprocessor = None
le_dict = {}
sc_dict = {}
models_loaded = False

app = FastAPI(title="Student Performance Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    hours_studied: float
    previous_scores: float
    extracurricular_activities: int
    sleep_hours: float
    sample_question_papers_practiced: float
    parents_schooling: float

class PredictionResponse(BaseModel):
    predicted_performance_index: float
    model_source: str
    message: str

def load_models():
    """Load pre-trained models if available, otherwise skip."""
    global rf_model, gb_model, preprocessor, models_loaded
    
    # For Vercel deployment, we return demo predictions
    # In production with pre-trained models saved as joblib files:
    # try:
    #     rf_model = joblib.load('path/to/rf_model.pkl')
    #     gb_model = joblib.load('path/to/gb_model.pkl')
    #     models_loaded = True
    # except:
    #     models_loaded = False
    
    models_loaded = False
    print("Models loading skipped for Vercel deployment", flush=True)

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    try:
        load_models()
        print("API initialized successfully", flush=True)
    except Exception as e:
        print(f"Warning during initialization: {e}", flush=True)
        # Continue anyway - API will work in demo mode

@app.get("/")
def root():
    return {
        "message": "Student Performance Prediction API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "models_available": models_loaded
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    """
    Predict student performance index.
    
    - **hours_studied**: Hours spent studying
    - **previous_scores**: Previous exam scores (0-100)
    - **extracurricular_activities**: Whether engaged (0/1)
    - **sleep_hours**: Hours of sleep per night
    - **sample_question_papers_practiced**: Number of practice papers
    - **parents_schooling**: Parents education level (1-2)
    """
    
    # For demo mode on Vercel, return a reasonable prediction
    # based on simple heuristics
    if not models_loaded:
        # Simple heuristic for demo prediction
        base_score = 40
        base_score += input_data.hours_studied * 3
        base_score += input_data.previous_scores * 0.2
        base_score += input_data.sleep_hours * 1.5
        base_score += input_data.sample_question_papers_practiced * 0.5
        base_score += input_data.extracurricular_activities * 5
        
        predicted_score = min(100, max(0, base_score))
        
        return PredictionResponse(
            predicted_performance_index=round(predicted_score, 2),
            model_source="heuristic_demo",
            message="Using demo prediction heuristic. For production, upload pre-trained models."
        )
    
    # If models were loaded, use them for prediction
    try:
        features = [[  
            input_data.hours_studied,
            input_data.previous_scores,
            input_data.extracurricular_activities,
            input_data.sleep_hours,
            input_data.sample_question_papers_practiced,
            input_data.parents_schooling
        ]]
        
        # Average predictions from both models
        rf_pred = rf_model.predict(features)[0]
        gb_pred = gb_model.predict(features)[0]
        prediction = (rf_pred + gb_pred) / 2
        
        return PredictionResponse(
            predicted_performance_index=round(prediction, 2),
            model_source="ensemble",
            message="Prediction from trained ensemble models."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/predict/batch")
def predict_batch():
    return {
        "message": "Batch prediction endpoint",
        "status": "available",
        "note": "Use POST /predict with student data"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
