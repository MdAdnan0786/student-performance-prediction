"""
Launcher script for Student Performance Prediction API
This script properly starts the backend server with main.py
"""
import os
import sys
import warnings

# Suppress warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings('ignore')

print("=" * 60)
print("Student Performance Prediction API Launcher")
print("=" * 60)

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Import the main app
print("Loading application...")
sys.path.insert(0, backend_dir)

try:
    from main import app, load_and_preprocess_data
    print("✓ Application modules imported successfully")
except Exception as e:
    print(f"❌ ERROR importing main: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Training ML models...")
print("(This may take 30-60 seconds)")
print("=" * 60)

# Load models
success = load_and_preprocess_data()
if not success:
    print("\n❌ ERROR: Model training failed!")
    print("Please check the data files in the 'data' directory.")
    sys.exit(1)

print("\n✓ Model loaded successfully!")
print("=" * 60)
print("🚀 Starting web server...")
print("=" * 60)
print("Server will be available at:")
print("  - Local:   http://localhost:8000")
print("  - Network: http://0.0.0.0:8000")
print("  - API Docs: http://localhost:8000/docs")
print("=" * 60)
print("Press CTRL+C to stop the server")
print("=" * 60)

# Start server
import uvicorn
try:
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user")
except OSError as e:
    if "address already in use" in str(e).lower() or "10048" in str(e):
        print(f"\n\n❌ ERROR: Port 8000 is already in use!")
        print("Another instance of the server might be running.")
        print("\nTo fix this:")
        print("1. Close the other server instance, OR")
        print("2. Use a different port")
    else:
        print(f"\n\n❌ FATAL ERROR: {e}")
except Exception as e:
    print(f"\n\n❌ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
