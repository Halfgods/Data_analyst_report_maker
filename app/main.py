
import os
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from fastapi.responses import HTMLResponse
import pandas as pd

from app.ai_commentary import prepare_ai_prompt, get_ai_commentary,get_data_specific_ai_response
from app.analyzer import analyze_dataframe
from app.cleaner import clean_dataframe
from app.csv_analyzer import analyze_csv_files
from app.merger import merge_dataframes
from app.report_generator import generate_full_report

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)



UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-csv/")
async def upload_csv(files: List[UploadFile] = File(...)):
    """
    Accepts multiple CSV files, saves them to a session-specific folder,
    and returns the session ID.
    """
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
    """
    Serves a specific chart image from a session folder.
    """
    chart_path = os.path.join(UPLOAD_DIR, session_id, chart_name)
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart not found.")
    return FileResponse(chart_path)

@app.post("/analyze/{session_id}")
async def analyze_session(session_id: str):
    """
    Triggers analysis for a given session ID and returns the analysis results,
    including paths to generated charts.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    # Assuming for simplicity that we'll analyze the first CSV found
    # In a real application, you might want to merge them or analyze individually
    df = pd.read_csv(csv_files[0])

    analysis_results = analyze_dataframe(df, session_dir)

    # Convert chart paths to URLs for the frontend
    for chart_type, paths in analysis_results.get('chart_paths', {}).items():
        analysis_results['chart_paths'][chart_type] = [
            f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths
        ]

    return JSONResponse(status_code=200, content=analysis_results)

@app.post("/commentary/{session_id}")
async def get_ai_commentary_for_session(session_id: str):
    """
    Generates AI commentary for a given session's analysis results.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    # Assuming analysis results are stored or can be re-generated
    # For simplicity, we'll re-run analysis to get results for commentary
    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    df = pd.read_csv(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    prompt = prepare_ai_prompt(analysis_results)
    commentary = get_ai_commentary(prompt)

    return JSONResponse(status_code=200, content=commentary)

@app.post("/metadata/{session_id}")
async def get_csv_metadata(session_id: str):
    """
    Returns metadata for CSV files in a given session.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    metadata = analyze_csv_files(csv_files)

    return JSONResponse(status_code=200, content=metadata)

@app.post("/generate-report/{session_id}")
async def generate_report_for_session(
    session_id: str,
    doc_title: str = "Data Analysis Report",
    author: str = "",
    date: str = "",
    client: str = "",
):
    """
    Generates a full PDF report for a given session.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    df = pd.read_csv(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    # Prepare data for report generation
    stats = str(analysis_results.get('descriptive_statistics', {}))
    visuals = analysis_results.get('chart_paths', {})
    insights = "No insights generated yet." # Placeholder
    anomalies = "No anomalies detected yet." # Placeholder
    recommendations = "No recommendations yet." # Placeholder

    # Get AI commentary for insights, anomalies, recommendations if available
    prompt = prepare_ai_prompt(analysis_results)
    ai_commentary_response = get_ai_commentary(prompt)
    if "commentary" in ai_commentary_response:
        insights = ai_commentary_response["commentary"]
        # You might want to parse the commentary to extract anomalies and recommendations
        # For now, we'll just use the full commentary as insights

    output_report_path = os.path.join(session_dir, f"report_{session_id}")
    generated_pdf_path = generate_full_report(
        doc_title, author, date, client, stats, visuals, insights, anomalies, recommendations, output_report_path
    )

    return JSONResponse(status_code=200, content={"report_path": generated_pdf_path})

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

    # 1. CSV Analysis
    csv_metadata = analyze_csv_files(csv_file_paths)

    # Read DataFrames for merging and cleaning
    dataframes = []
    for fp in csv_file_paths:
        try:
            dataframes.append(pd.read_csv(fp))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read CSV {os.path.basename(fp)}: {str(e)}")

    # 2. Merge DataFrames
    merged_dfs = merge_dataframes(dataframes, [os.path.basename(f) for f in csv_file_paths])
    
    # Assuming we proceed with the first (or only) merged/cleaned dataframe
    # In a more complex scenario, you might handle multiple dataframes differently
    if not merged_dfs:
        raise HTTPException(status_code=500, detail="No dataframes to process after merging.")
    
    df_to_process = merged_dfs[0] # Take the first dataframe after merging

    # 3. Clean Data
    cleaned_df, cleaning_errors = clean_dataframe(df_to_process)

    # 4. Analyze Data
    analysis_results = analyze_dataframe(cleaned_df, session_dir)

    # Convert chart paths to URLs for the frontend
    chart_urls = {}
    for chart_type, paths in analysis_results.get('chart_paths', {}).items():
        chart_urls[chart_type] = [
            f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths
        ]
    analysis_results['chart_urls'] = chart_urls
    del analysis_results['chart_paths'] # Remove local paths

    # 5. AI Commentary
    prompt = prepare_ai_prompt(analysis_results)
    ai_commentary_response = get_ai_commentary(prompt)
    ai_commentary = ai_commentary_response.get("commentary", "Error generating commentary.")

    # 6. Generate Report
    doc_title = "Comprehensive Data Analysis Report"
    author = "Automated System"
    date = pd.Timestamp.now().strftime("%Y-%m-%d")
    client = "User Data" # This could be dynamic based on user input

    stats = str(analysis_results.get('descriptive_statistics', {}))
    visuals = analysis_results.get('chart_urls', {})
    insights = ai_commentary
    anomalies = "Refer to AI commentary for potential anomalies." # Placeholder, could be parsed from commentary
    recommendations = "Refer to AI commentary for recommendations." # Placeholder, could be parsed from commentary

    output_report_path = os.path.join(session_dir, f"full_report_{session_id}")
    generated_pdf_path = generate_full_report(
        doc_title, author, date, client, stats, visuals, insights, anomalies, recommendations, output_report_path
    )
    report_url = f"/reports/{session_id}/{os.path.basename(generated_pdf_path)}"

    return JSONResponse(
        status_code=200,
        content={
            "session_id": session_id,
            "csv_metadata": csv_metadata,
            "cleaning_errors": cleaning_errors,
            "analysis_results": analysis_results,
            "chart_urls": chart_urls
        }
    )

@app.post("/generate-ai-report/{session_id}")
async def generate_ai_report(session_id: str):
    """
    Generates AI commentary and a full PDF report for a given session.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    # Re-run analysis to get the analysis_results for AI and report generation
    df = pd.read_csv(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    # AI Commentary
    prompt = prepare_ai_prompt(analysis_results)
    ai_commentary_response = get_ai_commentary(prompt)
    ai_commentary = ai_commentary_response.get("commentary", "Error generating commentary.")

    # Generate Report
    doc_title = "Comprehensive Data Analysis Report"
    author = "Automated System"
    date = pd.Timestamp.now().strftime("%Y-%m-%d")
    client = "User Data" # This could be dynamic based on user input

    stats = str(analysis_results.get('descriptive_statistics', {}))
    visuals = analysis_results.get('chart_urls', {}) # Use chart_urls from analysis_results
    insights = ai_commentary
    anomalies = "Refer to AI commentary for potential anomalies." # Placeholder
    recommendations = "Refer to AI commentary for recommendations." # Placeholder

    output_report_path = os.path.join(session_dir, f"full_report_{session_id}")
    generated_pdf_path = generate_full_report(
        doc_title, author, date, client, stats, visuals, insights, anomalies, recommendations, output_report_path
    )
    report_url = f"/reports/{session_id}/{os.path.basename(generated_pdf_path)}"

    return JSONResponse(
        status_code=200,
        content={
            "ai_commentary": ai_commentary,
            "report_url": report_url
        }
    )

@app.get("/reports/{session_id}/{report_name}")
async def get_report(session_id: str, report_name: str):
    """
    Serves a generated PDF report from a session folder.
    """
    report_path = os.path.join(UPLOAD_DIR, session_id, report_name)
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(report_path, media_type="application/pdf")

@app.post("/query-data/{session_id}")
async def query_data_with_ai(session_id: str, user_question: dict):
    """
    Allows users to ask questions about the data, with AI answers restricted to the data given.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    # Re-run analysis to get the analysis_results for the AI context
    df = pd.read_csv(csv_files[0])
    analysis_results = analyze_dataframe(df, session_dir)

    question_text = user_question.get("question")
    if not question_text:
        raise HTTPException(status_code=400, detail="'question' field is required in the request body.")

    ai_answer = get_data_specific_ai_response(question_text, analysis_results)

    return JSONResponse(status_code=200, content=ai_answer)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)