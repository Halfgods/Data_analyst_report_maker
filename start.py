#!/usr/bin/env python3
"""
Simple startup script for CSV Analysis App
Run with: python start.py
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def activate_venv():
    """Activate virtual environment if it exists"""
    venv_path = Path("venv")
    if venv_path.exists():
        if sys.platform == "win32":
            activate_script = venv_path / "Scripts" / "activate.bat"
            if activate_script.exists():
                os.environ["VIRTUAL_ENV"] = str(venv_path.absolute())
                os.environ["PATH"] = f"{venv_path / 'Scripts'}{os.pathsep}{os.environ['PATH']}"
        else:
            activate_script = venv_path / "bin" / "activate"
            if activate_script.exists():
                # Source the activation script
                activate_cmd = f"source {activate_script}"
                if os.system(f"bash -c '{activate_cmd} && exec \"$@\"' bash") == 0:
                    return True
        print(" Virtual environment activated")
        return True
    else:
        print("⚠️  Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print(" Virtual environment created")
        return activate_venv()

def start_backend():
    """Start the FastAPI backend server"""
    print("🔧 Starting Backend Server (FastAPI)...")
    os.chdir("app")
    try:
        # Use uvicorn to start the server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "127.0.0.1", "--port", "8000", "--reload"
        ])
        print(" Backend server starting on http://127.0.0.1:8000")
        return process
    except Exception as e:
        print(f" Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Vite frontend server"""
    print("🎨 Starting Frontend Server (Vite)...")
    os.chdir("dataui-main")
    try:
        # Use npm to start the dev server
        process = subprocess.Popen(["npm", "run", "dev"])
        print(" Frontend server starting on http://localhost:5173")
        return process
    except Exception as e:
        print(f" Failed to start frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🚀 Starting CSV Analysis App Development Environment")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app").exists() or not Path("dataui-main").exists():
        print(" Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Activate virtual environment
        if not activate_venv():
            print(" Failed to activate virtual environment")
            sys.exit(1)
        
        # Check dependencies
        print("📦 Checking dependencies...")
        try:
            import fastapi, pandas, numpy
            print(" Python dependencies OK")
        except ImportError:
            print("⚠️  Installing Python dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Check if node_modules exists
        if not Path("dataui-main/node_modules").exists():
            print("⚠️  Installing Node.js dependencies...")
            os.chdir("dataui-main")
            subprocess.run(["npm", "install"], check=True)
            os.chdir(original_dir)
        
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            sys.exit(1)
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend
        os.chdir(original_dir)
        frontend_process = start_frontend()
        if not frontend_process:
            backend_process.terminate()
            sys.exit(1)
        
        # Wait a bit for frontend to start
        time.sleep(3)
        
        print("\n🌐 Your application is now running!")
        print("=" * 60)
        print("📊 Backend API:  http://127.0.0.1:8000")
        print("🎨 Frontend UI:  http://localhost:5173")
        print("📖 API Docs:     http://127.0.0.1:8000/docs")
        print("=" * 60)
        print("\n💡 Usage:")
        print("1. Open http://localhost:5173 in your browser")
        print("2. Upload a CSV file for analysis")
        print("3. Use the 'Comprehensive Report' button for detailed analysis")
        print("\n Press Ctrl+C to stop both servers")
        
        # Wait for processes to complete
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n Shutting down servers...")
            backend_process.terminate()
            frontend_process.terminate()
            print(" Servers stopped")
    
    except Exception as e:
        print(f" Error: {e}")
        sys.exit(1)
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
