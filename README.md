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

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- Node.js and npm
- Git (optional)

### Installation

1. **Clone the repository** (or download the project)
```bash
git clone <repository-url>
cd student-performance-predict
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

3. **Install Frontend Dependencies**
```bash
npm install
```

### Running the Application

#### Option 1: Using Startup Scripts (Recommended - Windows)

**For PowerShell:**
```powershell
.\start.ps1
```

**For Command Prompt:**
```cmd
start.bat
```

These scripts will automatically start both servers in separate terminal windows.

#### Option 2: Using Python Launcher (Simple)

**Start Backend:**
```bash
cd backend
python start_server.py
```

**Start Frontend (in a new terminal):**
```bash
npm run dev
```

#### Option 3: Manual Start (Advanced)

**Start Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend (in a new terminal):**
```bash
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

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
│   ├── start_server.py      # Simple Python server launcher
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
├── start.ps1              # PowerShell startup script
├── start.bat              # Batch startup script
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

## 🔧 Troubleshooting

### Backend Won't Start
- Ensure Python is installed: `python --version`
- Check if port 8000 is available
- Verify all backend dependencies are installed: `pip install -r backend/requirements.txt`

### Frontend Won't Start
- Ensure Node.js is installed: `node --version`
- Check if port 5173 is available
- Run `npm install` to install dependencies

### "Backend Offline" Message
- Make sure the backend server is running on port 8000
- Check the backend terminal for any error messages
- Try restarting both servers

### NumPy Warnings
- Warnings about NumPy being experimental on Windows 64-bit are normal and don't affect functionality

## 📚 Additional Documentation

- See [`backend/README.md`](backend/README.md) for backend API details
- See [`backend/CHANGELOG.md`](backend/CHANGELOG.md) for version history

## 📄 License

This project is for educational purposes.
