# Student Performance Prediction System

A full-stack ML application that predicts student academic performance using machine learning models trained on multiple datasets.

## Features

- **ML-Powered Predictions**: Uses Random Forest and Gradient Boosting models
- **Comprehensive Input**: 8 key features including demographics, study habits, and lifestyle
- **Real-time Analysis**: Instant predictions with confidence scores
- **Personalized Recommendations**: Actionable advice based on student data
- **Model Transparency**: View detailed model metrics and performance

## Tech Stack

### Backend
- Python 3.x
- FastAPI (REST API)
- scikit-learn (Machine Learning)
- pandas (Data Processing)
- NumPy (Numerical Computing)

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Lucide React (Icons)

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
python main.py
```

The backend will start at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Install Node dependencies (from project root)
npm install

# Run the development server
npm run dev
```

The frontend will start at `http://localhost:5173`

## Data Sources

The model is trained on three combined datasets:

1. **Student Lifestyle Dataset** - Demographics and daily habits
2. **Student Performance Data** - Academic records and family background
3. **Student Performance Predictions** - Behavioral patterns and grades

## Input Features

The model requires 8 input features:

- **Age**: Student's age (15-25)
- **Gender**: Male/Female
- **Study Time**: Hours per day
- **Absences**: Number per semester
- **Parental Education**: Education level of parents
- **Previous Grade**: Last academic grade (0-100)
- **Extracurricular Activities**: Participation (Yes/No)
- **Sleep Hours**: Hours per night

## API Endpoints

- `GET /` - Health check
- `GET /model-info` - Get model metrics and information
- `POST /predict` - Make a prediction (requires student data)

## Model Performance

The system automatically selects the best performing model between:
- Random Forest Regressor
- Gradient Boosting Regressor

Typical metrics:
- R² Score: ~85-95%
- RMSE: 5-8 points
- MAE: 3-6 points

## Usage

1. Start the Python backend server
2. Start the React frontend
3. Fill in the student information form
4. Click "Predict Performance"
5. View predicted grade, performance level, and recommendations

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Backend documentation
├── data/                    # Training datasets
├── src/
│   ├── components/         # React components
│   │   ├── PredictionForm.tsx
│   │   ├── ResultsDisplay.tsx
│   │   └── ModelInfo.tsx
│   ├── App.tsx            # Main application
│   └── main.tsx           # React entry point
└── README.md              # This file
```

## Development

```bash
# Build frontend for production
npm run build

# Run type checking
npm run typecheck

# Lint code
npm run lint
```
