"""
Simple launcher for Student Performance Prediction API
Uses subprocess to start uvicorn (which we know works)
"""
import subprocess
import sys
import os

print("=" * 60)
print("Student Performance Prediction API")
print("=" * 60)
print("Starting backend server...")
print()
print("Server will be available at:")
print("  - Local:   http://localhost:8000")
print("  - Network: http://0.0.0.0:8000")
print("  - API Docs: http://localhost:8000/docs")
print("=" * 60)
print("Press CTRL+C to stop the server")
print("=" * 60)
print()

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Start uvicorn using subprocess (this works!)
try:
    subprocess.run([
        sys.executable,  # Use the same Python interpreter
        "-m", "uvicorn",
        "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ], check=True)
except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("Server stopped by user")
    print("=" * 60)
except subprocess.CalledProcessError as e:
    print(f"\n❌ ERROR: Server failed with code {e.returncode}")
    sys.exit(1)
