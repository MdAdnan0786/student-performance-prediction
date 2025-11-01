# Student Performance Prediction Application

A full-stack web application that predicts student performance using machine learning models.

## 🚀 Quick Start

### Option 1: Using the Startup Scripts (Recommended)

#### For PowerShell:
```powershell
.\start.ps1
```

#### For Command Prompt:
```cmd
start.bat
```

These scripts will automatically start both the backend and frontend servers in separate terminal windows.

### Option 2: Python Launcher (Simple)

Start the backend using the included Python launcher (no extra flags needed):
```bash
cd backend
python start_server.py
```

Then, in a new terminal, start the frontend:
```bash
npm run dev
```

### Option 3: Manual Start

#### Start Backend:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend (in a new terminal):
```bash
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Prerequisites

- Python 3.13 (or compatible version)
- Node.js and npm
- All dependencies installed (see Installation section)

## 📦 Installation

### Backend Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Dependencies:
```bash
npm install
```

## 🛠️ Technology Stack

### Frontend:
- React + TypeScript
- Vite
- Tailwind CSS
- Lucide React (icons)

### Backend:
- FastAPI
- Python 3.13
- scikit-learn
- pandas, numpy
- uvicorn

## 📁 Project Structure

```
student-performance-predict/
├── backend/              # FastAPI backend server
│   ├── main.py          # Main API application
│   ├── start_server.py  # Simple Python launcher for the backend
│   ├── api/             # Minimal FastAPI app for cloud deployment (Vercel)
│   └── requirements.txt # Python dependencies
├── src/                 # React frontend source
│   ├── components/      # React components
│   └── App.tsx         # Main application component
├── data/               # Dataset files
├── start.ps1           # PowerShell startup script
├── start.bat           # Batch startup script
└── package.json        # Node.js configuration
```

## 🔧 Troubleshooting

### Backend Won't Start:
- Ensure Python is installed: `python --version`
- Check if port 8000 is available
- Verify all backend dependencies are installed

### Frontend Won't Start:
- Ensure Node.js is installed: `node --version`
- Check if port 5173 is available
- Run `npm install` to install dependencies

### "Backend Offline" Message:
- Make sure the backend server is running on port 8000
- Check the backend terminal for any error messages
- Try restarting both servers

If you use `npm run backend`, note that `package.json` contains a Windows-specific Python path
(`C:\\Python313\\python.exe`). If your Python is elsewhere, either edit that path or prefer
the startup scripts (`start.ps1` / `start.bat`) or `python backend/start_server.py`.

## 📝 Features

- Student performance prediction using ML models
- Real-time predictions based on student data
- Model performance metrics display
- Responsive web interface
- RESTful API backend

## 🤝 Contributing

This project is part of an Engineering Project. Feel free to contribute by submitting issues or pull requests.

## 📄 License

This project is for educational purposes.
