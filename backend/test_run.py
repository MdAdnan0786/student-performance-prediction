import sys
print("Python is working!")
print(f"Python version: {sys.version}")
print(f"__name__ = {__name__}")

if __name__ == "__main__":
    print("This is running as main script")
    
    # Try importing the modules
    try:
        print("Importing FastAPI...")
        from fastapi import FastAPI
        print("✓ FastAPI imported")
        
        print("Importing uvicorn...")
        import uvicorn
        print("✓ uvicorn imported")
        
        print("Importing pandas...")
        import pandas as pd
        print("✓ pandas imported")
        
        print("Importing numpy...")
        import numpy as np
        print("✓ numpy imported")
        
        print("\nAll imports successful!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
