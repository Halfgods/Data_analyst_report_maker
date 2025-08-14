import os
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from fastapi.responses import HTMLResponse
import pandas as pd

from app.ai_commentary import prepare_ai_prompt, get_ai_commentary, get_data_specific_ai_response
from app.analyzer import analyze_dataframe
from app.cleaner import clean_dataframe
from app.csv_analyzer import analyze_csv_metadata, load_csv_fully
from app.merger import merge_dataframes
from app.csv_validator import validate_csv_file, validate_dataframe
from app.pdf_generator import generate_pdf_report, get_pdf_report_info

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Data Analysis API is running"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-csv/")
async def upload_csv(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")

    session_id = str(uuid.uuid4())
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_dir)

    for file in files:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Only CSV files are allowed.")
        
        file_path = os.path.join(session_dir, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {file.filename}. Error: {str(e)}")

    return JSONResponse(status_code=200, content={"session_id": session_id})

@app.get("/sessions/{session_id}/charts/{chart_name}")
async def get_chart(session_id: str, chart_name: str):
    chart_path = os.path.join(UPLOAD_DIR, session_id, chart_name)
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart not found.")
    return FileResponse(chart_path)

@app.post("/analyze/{session_id}")
async def analyze_session(session_id: str):
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    df = load_csv_fully(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    for chart_type, paths in analysis_results.get('chart_paths', {}).items():
        analysis_results['chart_paths'][chart_type] = [
            f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths
        ]

    return JSONResponse(status_code=200, content=analysis_results)

@app.post("/commentary/{session_id}")
async def get_ai_commentary_for_session(session_id: str, model: str = "flash"):
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    df = load_csv_fully(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    # Map model parameter to full model name
    model_version = "gemini-1.5-pro" if model.lower() == "pro" else "gemini-1.5-flash"
    
    prompt = prepare_ai_prompt(analysis_results)
    commentary = get_ai_commentary(prompt, model_version=model_version)

    return JSONResponse(status_code=200, content=commentary)

@app.post("/metadata/{session_id}")
async def get_csv_metadata(session_id: str):
    """
    Returns metadata for CSV files in a given session by reading only the first 100 rows.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    metadata = analyze_csv_metadata(csv_files)

    return JSONResponse(status_code=200, content=metadata)

@app.post("/process-data/{session_id}")
async def process_data(session_id: str):
    """
    Orchestrates the entire data processing and reporting flow for a given session.
    Returns all generated data, links, and reports.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_file_paths = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_file_paths:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    # 1. CSV Analysis (fast metadata)
    csv_metadata = analyze_csv_metadata(csv_file_paths)

    # Read DataFrames for merging and cleaning (using chunking)
    dataframes = []
    for fp in csv_file_paths:
        try:
            df = load_csv_fully(fp)
            dataframes.append(df)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read CSV {os.path.basename(fp)}: {str(e)}")

    # 2. Merge DataFrames
    merged_dfs = merge_dataframes(dataframes, [os.path.basename(f) for f in csv_file_paths])
    
    if not merged_dfs:
        raise HTTPException(status_code=500, detail="No dataframes to process after merging.")
    
    df_to_process = merged_dfs[0]

    # 3. Clean Data
    cleaned_df, cleaning_errors = clean_dataframe(df_to_process)

    # 4. Analyze Data
    analysis_results = analyze_dataframe(cleaned_df, session_dir)

    # Convert chart paths to URLs
    chart_urls = {}
    if 'chart_paths' in analysis_results:
        for chart_type, paths in analysis_results['chart_paths'].items():
            chart_urls[chart_type] = [f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths]
        del analysis_results['chart_paths']
    analysis_results['chart_urls'] = chart_urls

    # 5. AI Commentary
    prompt = prepare_ai_prompt(analysis_results)
    ai_commentary_response = get_ai_commentary(prompt)
    ai_commentary = ai_commentary_response.get("commentary", "Error generating commentary.")

    return JSONResponse(
        status_code=200,
        content={
            "session_id": session_id,
            "csv_metadata": csv_metadata,
            "cleaning_errors": cleaning_errors,
            "analysis_results": analysis_results,
            "ai_commentary": ai_commentary
        }
    )

@app.post("/query-data/{session_id}")
async def query_data_with_ai(session_id: str, user_question: dict, model: str = "flash"):
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    df = load_csv_fully(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    question_text = user_question.get("question")
    if not question_text:
        raise HTTPException(status_code=400, detail="'question' field is required in the request body.")

    # Map model parameter to full model name
    model_version = "gemini-1.5-pro" if model.lower() == "pro" else "gemini-1.5-flash"
    
    ai_answer = get_data_specific_ai_response(question_text, analysis_results, model_version=model_version)

    return JSONResponse(status_code=200, content=ai_answer)

@app.post("/validate/{session_id}")
async def validate_csv_data(session_id: str):
    """
    Strict CSV validation that reports exact locations of missing or incorrect data.
    Uses high-performance vectorized operations for speed.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    # Validate the first CSV file
    csv_file_path = csv_files[0]
    
    try:
        # Run high-performance validation
        validation_results = validate_csv_file(csv_file_path)
        
        return JSONResponse(status_code=200, content={
            "session_id": session_id,
            "file_name": os.path.basename(csv_file_path),
            "validation_results": validation_results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/generate-report/{session_id}")
async def generate_pdf_report_endpoint(session_id: str):
    """
    Generate a comprehensive PDF report from processed data analysis.
    Returns PDF file information and download URL.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_file_paths = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_file_paths:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    try:
        # 1. Get CSV metadata
        csv_metadata = analyze_csv_metadata(csv_file_paths)

        # 2. Load and process data
        dataframes = []
        for fp in csv_file_paths:
            df = load_csv_fully(fp)
            dataframes.append(df)

        # 3. Merge and clean data
        merged_dfs = merge_dataframes(dataframes, [os.path.basename(f) for f in csv_file_paths])
        if not merged_dfs:
            raise HTTPException(status_code=500, detail="No dataframes to process after merging.")
        
        df_to_process = merged_dfs[0]
        cleaned_df, cleaning_errors = clean_dataframe(df_to_process)

        # 4. Analyze data and generate charts
        analysis_results = analyze_dataframe(cleaned_df, session_dir)

        # Convert chart paths to URLs for PDF embedding
        chart_urls = {}
        if 'chart_paths' in analysis_results:
            for chart_type, paths in analysis_results['chart_paths'].items():
                chart_urls[chart_type] = [f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths]

        # 5. Generate AI commentary
        prompt = prepare_ai_prompt(analysis_results)
        ai_commentary_response = get_ai_commentary(prompt)
        ai_commentary = ai_commentary_response.get("commentary", "Error generating commentary.")

        # 6. Generate PDF report
        pdf_path = generate_pdf_report(
            session_id=session_id,
            csv_metadata=csv_metadata,
            analysis_results=analysis_results,
            ai_commentary=ai_commentary,
            session_dir=session_dir,
            chart_urls=chart_urls
        )

        # 7. Get PDF info
        pdf_info = get_pdf_report_info(pdf_path)
        if "error" in pdf_info:
            raise HTTPException(status_code=500, detail=pdf_info["error"])

        # 8. Add download URL
        pdf_info["download_url"] = f"/sessions/{session_id}/reports/{pdf_info['filename']}"

        return JSONResponse(status_code=200, content={
            "session_id": session_id,
            "report_generated": True,
            "pdf_info": pdf_info,
            "message": "PDF report generated successfully"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")

@app.get("/sessions/{session_id}/reports/{report_name}")
async def download_report(session_id: str, report_name: str):
    """
    Download generated PDF report.
    """
    report_path = os.path.join(UPLOAD_DIR, session_id, report_name)
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=report_name,
        headers={"Content-Disposition": f"attachment; filename={report_name}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
