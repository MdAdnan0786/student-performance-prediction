from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
from typing import Optional
from sklearn.impute import SimpleImputer

# env and optional AI recommendations
from dotenv import load_dotenv

app = FastAPI(title="Student Performance Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Versioning ---
API_VERSION = "1.1.0"

class StudentInput(BaseModel):
    age: int
    gender: str
    study_time_hours: float
    absences: int
    parental_education: str
    previous_grade: float
    extracurricular: str
    sleep_hours: float

class PredictionResponse(BaseModel):
    predicted_grade: float
    performance_level: str
    confidence_score: float
    model_used: str
    recommendations: list[str]

# Global model artifacts
pipeline = None
preprocessor = None
model_metrics = {}
train_target_stats = {"min": 0.0, "max": 100.0}

# Load environment for recommendations API
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
RECS_API_KEY = os.getenv('GEMNIE_API_KEY')


# --- Helper mappers to ensure consistency across training and batch prediction ---
def _map_df1(df1: pd.DataFrame) -> pd.DataFrame:
    if df1.empty:
        return pd.DataFrame(columns=['age','gender','study_time_hours','absences','parental_education','previous_grade','extracurricular','sleep_hours','final_grade'])
    out = pd.DataFrame()
    out['age'] = 17
    out['gender'] = 'other'
    out['study_time_hours'] = pd.to_numeric(df1.get('Study_Hours_Per_Day'), errors='coerce').fillna(2.0).clip(0, 12)
    out['absences'] = 5
    out['parental_education'] = 'medium'
    out['previous_grade'] = (pd.to_numeric(df1.get('GPA'), errors='coerce').fillna(2.5).clip(0, 4) / 4.0) * 100.0
    out['extracurricular'] = (pd.to_numeric(df1.get('Extracurricular_Hours_Per_Day'), errors='coerce').fillna(0) > 0.5).map({True: 'yes', False: 'no'})
    out['sleep_hours'] = pd.to_numeric(df1.get('Sleep_Hours_Per_Day'), errors='coerce').fillna(7.0).clip(4, 12)
    out['final_grade'] = np.nan
    return out

def _map_df2(df2: pd.DataFrame) -> pd.DataFrame:
    edu_map = {0: 'none', 1: 'high_school', 2: 'college', 3: 'bachelor', 4: 'graduate'}
    out = pd.DataFrame()
    out['age'] = pd.to_numeric(df2.get('Age'), errors='coerce').fillna(17).clip(12, 25)
    out['gender'] = df2.get('Gender').map({1: 'male', 0: 'female'}).fillna('other').astype(str)
    out['study_time_hours'] = pd.to_numeric(df2.get('StudyTimeWeekly'), errors='coerce').fillna(10.0).clip(0, 70) / 7.0
    out['absences'] = pd.to_numeric(df2.get('Absences'), errors='coerce').fillna(5).clip(0, 30)
    out['parental_education'] = df2.get('ParentalEducation').map(edu_map).fillna('medium').astype(str)
    out['previous_grade'] = (pd.to_numeric(df2.get('GPA'), errors='coerce').fillna(2.5).clip(0, 4) / 4.0) * 100.0
    out['extracurricular'] = df2.get('Extracurricular').map({1: 'yes', 0: 'no'}).fillna('no').astype(str)
    out['sleep_hours'] = 7.0
    grade_class = pd.to_numeric(df2.get('GradeClass'), errors='coerce')
    out['final_grade'] = grade_class.map({1.0: 95.0, 2.0: 85.0, 3.0: 75.0, 4.0: 65.0})
    return out

def _map_df3(df3: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame()
    out['age'] = 18
    out['gender'] = df3.get('Gender').fillna('other').astype(str)
    attendance = pd.to_numeric(df3.get('AttendanceRate'), errors='coerce')
    attendance_alt = pd.to_numeric(df3.get('Attendance (%)'), errors='coerce')
    attendance = attendance.fillna(attendance_alt).fillna(85.0).clip(0, 100)
    weekly_hours = pd.to_numeric(df3.get('StudyHoursPerWeek'), errors='coerce')
    daily_fallback = pd.to_numeric(df3.get('Study Hours'), errors='coerce')
    weekly_hours = weekly_hours.fillna(daily_fallback * 7.0)
    weekly_hours = weekly_hours.fillna(15.0).clip(0, 70)
    out['study_time_hours'] = (weekly_hours / 7.0).clip(0, 12)
    out['absences'] = ((100.0 - attendance) / 100.0 * 30.0).round().clip(0, 30).astype(int)
    support = df3.get('ParentalSupport').fillna('medium').astype(str)
    out['parental_education'] = support
    out['previous_grade'] = pd.to_numeric(df3.get('PreviousGrade'), errors='coerce').fillna(75.0).clip(0, 100)
    extra = pd.to_numeric(df3.get('ExtracurricularActivities'), errors='coerce').fillna(0)
    out['extracurricular'] = (extra > 0).map({True: 'yes', False: 'no'}).astype(str)
    out['sleep_hours'] = 7.0
    final = pd.to_numeric(df3.get('FinalGrade'), errors='coerce')
    out['final_grade'] = final.clip(0, 100)
    return out


def load_and_preprocess_data():
    global pipeline, preprocessor, model_metrics, train_target_stats

    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data')

        # Robustly handle optional lifestyle dataset
        path1 = os.path.join(data_path, 'student_lifestyle_dataset.csv')
        if os.path.exists(path1):
            df1 = pd.read_csv(path1)
        else:
            df1 = pd.DataFrame()

        df2 = pd.read_csv(os.path.join(data_path, 'Student_performance_data.csv'))
        df3 = pd.read_csv(os.path.join(data_path, 'student_performance_updated_1000.csv'))

        # Normalize datasets into common schema (robust column-aware mapping)
        df1_processed = _map_df1(df1)
        df2_processed = _map_df2(df2)
        df3_processed = _map_df3(df3)

        df = pd.concat([df1_processed, df2_processed, df3_processed], ignore_index=True)
        # Basic cleanup
        for col in ['gender', 'parental_education', 'extracurricular']:
            df[col] = df[col].astype(str).str.lower().str.strip()
        # Keep only rows with labeled target
        df = df[df['final_grade'].notna()]
        df['final_grade'] = df['final_grade'].clip(0, 100)
        train_target_stats = {"min": float(df['final_grade'].min()), "max": float(df['final_grade'].max())}

        # Feature columns (include previous_grade; not identical to target)
        categorical_cols = ['gender', 'parental_education', 'extracurricular']
        numeric_cols = ['age', 'study_time_hours', 'absences', 'sleep_hours', 'previous_grade']

        X = df[categorical_cols + numeric_cols]
        y = df['final_grade']

        # Preprocessor: OneHot for categoricals, Standardize numerics
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    'cat',
                    Pipeline(steps=[
                        ('impute', SimpleImputer(strategy='most_frequent')),
                        ('onehot', OneHotEncoder(handle_unknown='ignore'))
                    ]),
                    categorical_cols
                ),
                (
                    'num',
                    Pipeline(steps=[
                        ('impute', SimpleImputer(strategy='median')),
                        ('scale', StandardScaler())
                    ]),
                    numeric_cols
                ),
            ]
        )

        # Models
        rf = RandomForestRegressor(random_state=42, n_jobs=-1)
        gb = GradientBoostingRegressor(random_state=42)

        rf_pipe = Pipeline(steps=[('prep', preprocessor), ('regressor', rf)])
        gb_pipe = Pipeline(steps=[('prep', preprocessor), ('regressor', gb)])

        # Parameter search spaces
        rf_params = {
            'regressor__n_estimators': [200, 300, 400],
            'regressor__max_depth': [10, 15, 20, None],
            'regressor__min_samples_split': [2, 5, 10],
            'regressor__min_samples_leaf': [1, 2, 4]
        }
        gb_params = {
            'regressor__n_estimators': [200, 300],
            'regressor__learning_rate': [0.05, 0.1, 0.2],
            'regressor__max_depth': [3, 4, 5]
        }

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf_search = RandomizedSearchCV(rf_pipe, rf_params, n_iter=10, cv=3, scoring='r2', random_state=42, n_jobs=-1)
        gb_search = RandomizedSearchCV(gb_pipe, gb_params, n_iter=6, cv=3, scoring='r2', random_state=42, n_jobs=-1)

        rf_search.fit(X_train, y_train)
        gb_search.fit(X_train, y_train)

        # Evaluate on test set
        rf_pred = rf_search.best_estimator_.predict(X_test)
        gb_pred = gb_search.best_estimator_.predict(X_test)

        rf_score = r2_score(y_test, rf_pred)
        gb_score = r2_score(y_test, gb_pred)

        if rf_score >= gb_score:
            pipeline = rf_search.best_estimator_
            model_name = "Random Forest"
            predictions = rf_pred
        else:
            pipeline = gb_search.best_estimator_
            model_name = "Gradient Boosting"
            predictions = gb_pred

        model_metrics = {
            'model_name': model_name,
            'r2_score': float(max(rf_score, gb_score)),
            'rmse': float(np.sqrt(mean_squared_error(y_test, predictions))),
            'mae': float(mean_absolute_error(y_test, predictions)),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }

        print(f"Model trained successfully: {model_name}")
        print(f"R² Score: {model_metrics['r2_score']:.4f}")
        print(f"RMSE: {model_metrics['rmse']:.4f}")
        print(f"MAE: {model_metrics['mae']:.4f}")

        return True

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

@app.on_event("startup")
async def startup_event():
    success = load_and_preprocess_data()
    if not success:
        print("Warning: Model training failed. Some endpoints may not work.")

@app.get("/")
def read_root():
    return {
        "message": "Student Performance Prediction API",
        "status": "active",
        "version": API_VERSION,
        "model_loaded": pipeline is not None
    }

@app.get("/model-info")
def get_model_info():
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "metrics": model_metrics,
        "features": [
            "age", "gender", "study_time_hours", "absences",
            "parental_education", "extracurricular", "sleep_hours", "previous_grade"
        ]
    }


def _compute_confidence(predicted_grade: float, student: StudentInput) -> float:
    # Base confidence derived from model RMSE
    rmse = model_metrics.get('rmse', 15.0)
    base = max(0.5, 1.0 - rmse / 40.0)

    # Adjustments from study/sleep/absences
    if student.study_time_hours >= 3:
        base += 0.05
    if student.sleep_hours >= 7:
        base += 0.03
    if student.absences > 10:
        base -= 0.08

    # Clamp
    return float(max(0.5, min(0.95, base)))


def _generate_rule_based_recommendations(student: StudentInput, predicted_grade: float):
    recs = []
    if student.study_time_hours < 2:
        recs.append("Increase daily study time to at least 2–3 hours.")
    if student.absences > 10:
        recs.append("Reduce class absences to improve concept retention.")
    if student.sleep_hours < 7:
        recs.append("Aim for 7–9 hours of sleep for better cognitive performance.")
    if str(student.extracurricular).lower().strip() == "no":
        recs.append("Consider joining extracurriculars to build motivation and soft skills.")
    if student.previous_grade < 70:
        recs.append("Seek tutoring to strengthen foundational topics from previous courses.")
    if predicted_grade < 70:
        recs.append("Meet advisors to craft a personalized improvement plan.")
    if not recs:
        recs.append("Keep up the great work—maintain your current study habits.")
        recs.append("Challenge yourself with advanced coursework or projects.")
    return recs


# Optional: integrate Gemini recommendations if API key is present
def _generate_ai_recommendations(student: StudentInput, predicted_grade: float, performance_level: str):
    try:
        if not RECS_API_KEY:
            return None
        # Lazy import to avoid hard dependency when key missing
        import google.generativeai as genai
        genai.configure(api_key=RECS_API_KEY)
        prompt = (
            "You are an academic advisor. Given the student's profile and predicted grade, "
            "provide 4–6 specific, actionable, and personalized recommendations to improve or sustain performance. "
            "Return only bullet points without numbering.\n\n"
            f"Profile: age={student.age}, gender='{student.gender}', study_time_hours={student.study_time_hours}, "
            f"absences={student.absences}, parental_education='{student.parental_education}', previous_grade={student.previous_grade}, "
            f"extracurricular='{student.extracurricular}', sleep_hours={student.sleep_hours}.\n"
            f"Predicted grade: {predicted_grade:.1f}/100, Performance level: {performance_level}."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        text = resp.text or ""
        # Split into lines, clean, keep 4–6 non-empty
        lines = [l.strip("-• ").strip() for l in text.splitlines()]
        lines = [l for l in lines if l]
        if not lines:
            return None
        return lines[:6]
    except Exception:
        return None


@app.post("/predict", response_model=PredictionResponse)
def predict_performance(student: StudentInput):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        input_df = pd.DataFrame([{ 
            'age': student.age,
            'gender': str(student.gender).lower().strip(),
            'study_time_hours': student.study_time_hours,
            'absences': student.absences,
            'parental_education': str(student.parental_education).lower().strip(),
            'extracurricular': str(student.extracurricular).lower().strip(),
            'sleep_hours': student.sleep_hours,
            'previous_grade': student.previous_grade
        }])

        predicted_grade = float(pipeline.predict(input_df)[0])
        predicted_grade = max(0.0, min(100.0, predicted_grade))

        # Performance categories
        if predicted_grade >= 90:
            performance_level = "Excellent"
        elif predicted_grade >= 80:
            performance_level = "Very Good"
        elif predicted_grade >= 70:
            performance_level = "Good"
        elif predicted_grade >= 60:
            performance_level = "Satisfactory"
        else:
            performance_level = "At Risk"

        confidence = _compute_confidence(predicted_grade, student)

        # Recommendations: AI first (if available), otherwise rule-based
        ai_recs = _generate_ai_recommendations(student, predicted_grade, performance_level)
        recommendations = ai_recs if ai_recs else _generate_rule_based_recommendations(student, predicted_grade)

        return PredictionResponse(
            predicted_grade=round(predicted_grade, 2),
            performance_level=performance_level,
            confidence_score=confidence,
            model_used=model_metrics.get('model_name', 'Unknown'),
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# --- Batch prediction endpoint to attach predictions to dataset records ---
@app.get("/batch-predict")
def batch_predict(source: str = 'df3', save: bool = True, limit: Optional[int] = 50):
    """
    Run predictions across a dataset and attach a new column 'PredictedGrade'.
    - source: 'df2' | 'df3' | 'all' (default 'df3')
    - save: whether to write a CSV alongside the original dataset
    - limit: number of preview rows to return in JSON response
    Preserves all original fields; adds 'PredictedGrade' (float, 2 decimals).
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')

    try:
        frames = []
        outputs = []

        if source in ('df2', 'all'):
            df2 = pd.read_csv(os.path.join(data_path, 'Student_performance_data.csv'))
            features_df2 = _map_df2(df2)
            # Clean categorical text like training
            for col in ['gender', 'parental_education', 'extracurricular']:
                features_df2[col] = features_df2[col].astype(str).str.lower().str.strip()
            preds2 = pipeline.predict(features_df2.drop(columns=['final_grade']))
            preds2 = np.clip(preds2, 0, 100)
            df2_out = df2.copy()
            df2_out['PredictedGrade'] = np.round(preds2, 2)
            frames.append(df2_out)
            outputs.append(('Student_performance_data_with_predictions.csv', df2_out))

        if source in ('df3', 'all'):
            df3 = pd.read_csv(os.path.join(data_path, 'student_performance_updated_1000.csv'))
            features_df3 = _map_df3(df3)
            for col in ['gender', 'parental_education', 'extracurricular']:
                features_df3[col] = features_df3[col].astype(str).str.lower().str.strip()
            preds3 = pipeline.predict(features_df3.drop(columns=['final_grade']))
            preds3 = np.clip(preds3, 0, 100)
            df3_out = df3.copy()
            df3_out['PredictedGrade'] = np.round(preds3, 2)
            frames.append(df3_out)
            outputs.append(('student_performance_updated_1000_with_predictions.csv', df3_out))

        if not frames:
            raise HTTPException(status_code=400, detail="Invalid source. Use 'df2', 'df3', or 'all'.")

        # Optionally save CSVs
        saved_files = []
        if save:
            for filename, frame in outputs:
                save_path = os.path.join(data_path, filename)
                frame.to_csv(save_path, index=False)
                saved_files.append(save_path)

        # Return preview rows to avoid huge payloads
        preview = pd.concat(frames, ignore_index=True)
        if limit is not None:
            preview = preview.head(limit)

        return {
            "saved_files": saved_files,
            "rows": preview.to_dict(orient='records'),
            "count": int(preview.shape[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


@app.get("/dataset-stats")
def dataset_stats():
    """
    Analyze training datasets for distribution and feature representation.
    Returns summary statistics for key features in df2 and df3.
    """
    try:
        def clean_desc(s):
            if s is None:
                return {}
            d = s.to_dict()
            return {str(k): (None if pd.isna(v) else float(v)) for k, v in d.items()}

        def counts_dict(series):
            if series is None:
                return {}
            vc = series.value_counts(dropna=False)
            out = {}
            for k, v in vc.items():
                key = 'NaN' if (isinstance(k, float) and pd.isna(k)) else str(k)
                out[key] = int(v)
            return out

        data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        df2 = pd.read_csv(os.path.join(data_path, 'Student_performance_data.csv'))
        df3 = pd.read_csv(os.path.join(data_path, 'student_performance_updated_1000.csv'))

        stats = {
            "df2": {
                "shape": [int(df2.shape[0]), int(df2.shape[1])],
                "grade_class_counts": counts_dict(df2['GradeClass'] if 'GradeClass' in df2.columns else None),
                "gender_counts": counts_dict(df2['Gender'] if 'Gender' in df2.columns else None),
                "extracurricular_counts": counts_dict(df2['Extracurricular'] if 'Extracurricular' in df2.columns else None),
                "gpa_describe": clean_desc(df2['GPA'].describe() if 'GPA' in df2.columns else None),
                "study_time_weekly_describe": clean_desc(df2['StudyTimeWeekly'].describe() if 'StudyTimeWeekly' in df2.columns else None),
                "absences_describe": clean_desc(df2['Absences'].describe() if 'Absences' in df2.columns else None),
            },
            "df3": {
                "shape": [int(df3.shape[0]), int(df3.shape[1])],
                "gender_counts": counts_dict(df3['Gender'] if 'Gender' in df3.columns else None),
                "parental_support_counts": counts_dict(df3['ParentalSupport'] if 'ParentalSupport' in df3.columns else None),
                "previous_grade_describe": clean_desc(df3['PreviousGrade'].describe() if 'PreviousGrade' in df3.columns else None),
                "final_grade_describe": clean_desc(df3['FinalGrade'].describe() if 'FinalGrade' in df3.columns else None),
                "study_hours_week_describe": clean_desc(df3['StudyHoursPerWeek'].describe() if 'StudyHoursPerWeek' in df3.columns else None),
                "attendance_rate_describe": clean_desc(df3['AttendanceRate'].describe() if 'AttendanceRate' in df3.columns else None),
            }
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dataset stats error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import sys
    
    try:
        print("=" * 60)
        print("Starting Student Performance Prediction API")
        print("=" * 60)
        print("Loading and training ML models...")
        sys.stdout.flush()
        
        # Load model before starting the server
        success = load_and_preprocess_data()
        if not success:
            print("ERROR: Model training failed!")
            print("Please check the data files in the 'data' directory.")
            sys.exit(1)
        
        print("✓ Model loaded successfully!")
        print("=" * 60)
        print("Server will be available at:")
        print("  - Local:   http://localhost:8000")
        print("  - Network: http://0.0.0.0:8000")
        print("  - API Docs: http://localhost:8000/docs")
        print("=" * 60)
        print("Press CTRL+C to stop the server")
        print("=" * 60)
        sys.stdout.flush()
        
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
