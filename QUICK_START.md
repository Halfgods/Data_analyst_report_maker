# 🚀 CSV Analysis App - Quick Start Guide

## **One-Line Commands to Run Your App**

### **Option 1: Python Script (Recommended)**
```bash
python start.py
```

### **Option 2: Make Commands**
```bash
make start    # Full startup with dependency checks
make dev      # Quick start (assumes dependencies installed)
```

### **Option 3: Bash Script**
```bash
./start_dev.sh
```

## **What Each Command Does**

### **`python start.py`** ⭐ **BEST OPTION**
- ✅ Automatically activates virtual environment
- ✅ Checks and installs missing dependencies
- ✅ Starts both backend (FastAPI) and frontend (Vite)
- ✅ Handles errors gracefully
- ✅ Cross-platform compatible

### **`make start`**
- ✅ Runs the enhanced startup script
- ✅ Good for dependency management
- ✅ Requires Make to be installed

### **`make dev`**
- ✅ Quick start for development
- ✅ Assumes all dependencies are already installed
- ✅ Good for daily development

## **What Gets Started**

1. **Backend Server**: FastAPI on http://127.0.0.1:8000
   - CSV analysis API
   - AI commentary generation
   - Chart generation
   - PDF report creation

2. **Frontend Server**: React + Vite on http://localhost:5173
   - Modern web interface
   - File upload
   - Data visualization
   - Interactive charts

## **First Time Setup**

If this is your first time running the app:

```bash
# Install all dependencies first
make install

# Then start the app
python start.py
```

## **Troubleshooting**

### **Port Already in Use**
```bash
# Kill processes using ports 8000 and 5173
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5173 | xargs kill -9
```

### **Permission Denied**
```bash
chmod +x start.py start_dev.sh
```

### **Virtual Environment Issues**
```bash
# Remove and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## **Usage**

1. Run one of the startup commands above
2. Open http://localhost:5173 in your browser
3. Upload a CSV file
4. View analysis results and AI insights
5. Generate comprehensive reports

## **Stopping the App**

Press `Ctrl+C` in the terminal where you started the app.

---

**💡 Pro Tip**: Use `python start.py` for the most reliable startup experience!
