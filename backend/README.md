# Student Performance Prediction Backend

Python FastAPI backend for ML-based student performance prediction.

## Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the server:

**Option A: Simple Python launcher (Recommended)**
```bash
python start_server.py
```

**Option B: Direct uvicorn command**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Using uvicorn CLI**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000` with API docs at `http://localhost:8000/docs`.

## API Endpoints

- `GET /` - Health check (includes `version` and `model_loaded`)
- `GET /model-info` - Model metrics and feature information
- `POST /predict` - Predict student performance for a single input
- `GET /batch-predict` - Batch predictions for datasets; appends `PredictedGrade` and optionally saves enriched CSVs
- `GET /dataset-stats` - Summary distribution stats for training datasets (df2/df3)

### Batch Predict Usage

Query params:
- `source`: `df2` | `df3` | `all` (default: `df3`)
- `save`: `true` | `false` (default: `true`)
- `limit`: integer preview row count (default: `50`)

Example:
```bash
curl "http://localhost:8000/batch-predict?source=df3&save=true&limit=20"
```
Response includes saved file paths (if `save=true`) and preview rows.

### Dataset Stats Usage

Example:
```bash
curl "http://localhost:8000/dataset-stats"
```
Returns descriptive statistics for key features and category counts to help diagnose data distribution issues.

## Data Sources

The model is trained on three combined datasets:
1. Student Lifestyle Dataset
2. Student Performance Data
3. Student Performance Updated Dataset

Features used for prediction:
- Age
- Gender
- Study time per week (hours)
- Absences
- Parental education level
- Previous grade
- Extracurricular activities
- Sleep hours per night

## Versioning

Backend version is tracked in `CHANGELOG.md` and exposed via `GET /` as `version`.
