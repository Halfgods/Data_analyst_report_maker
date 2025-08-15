import os
import uuid
import shutil
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import HTMLResponse
import pandas as pd

from ai_commentary import prepare_ai_prompt, get_ai_commentary, get_data_specific_ai_response
from analyzer import analyze_dataframe
from cleaner import clean_dataframe
from csv_analyzer import analyze_csv_metadata, load_csv_fully
from merger import merge_dataframes
from csv_validator import validate_csv_file, validate_dataframe
from pdf_generator import generate_data_analysis_report

# Simple implementations for missing functions
def generate_pdf_report(session_id: str, csv_metadata: dict, analysis_results: dict, 
                       ai_commentary: str, session_dir: str, chart_urls: dict) -> str:
    """Generate a comprehensive HTML report with embedded charts"""
    report_path = os.path.join(session_dir, f"report_{session_id}.html")
    
    # Create HTML content with embedded charts
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report - {session_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
        .chart-container {{ margin: 20px 0; text-align: center; }}
        .chart-container iframe {{ border: 1px solid #ddd; border-radius: 8px; }}
        .stats-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .stats-table th, .stats-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .stats-table th {{ background-color: #f5f5f5; }}
        .insight {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Data Analysis Report</h1>
        <p>Session ID: {session_id}</p>
        <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="section">
        <h2>📋 Dataset Overview</h2>
        <table class="stats-table">
            <tr><th>File Name</th><td>{csv_metadata['files'][0]['filename']}</td></tr>
            <tr><th>Rows</th><td>{csv_metadata['files'][0]['rows']}</td></tr>
            <tr><th>Columns</th><td>{len(csv_metadata['files'][0]['columns'])}</td></tr>
            <tr><th>File Size</th><td>{csv_metadata['files'][0]['file_size_mb']:.2f} MB</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>🤖 AI Insights</h2>
        <div class="insight">
            {ai_commentary.replace(chr(10), '<br>')}
        </div>
    </div>

    <div class="section">
        <h2>📈 Interactive Charts</h2>
    """
    
    # Add embedded charts
    if chart_urls:
        for chart_type, urls in chart_urls.items():
            html_content += f'<h3>{chart_type.title()}</h3>'
            for url in urls:
                chart_name = url.split('/')[-1]
                full_url = f"http://127.0.0.1:8000{url}"
                html_content += f"""
                <div class="chart-container">
                    <h4>{chart_name.replace('_', ' ').title()}</h4>
                    <iframe src="{full_url}" width="100%" height="500px" frameborder="0"></iframe>
                </div>
                """
    
    # Add statistics
    html_content += """
    <div class="section">
        <h2>📊 Descriptive Statistics</h2>
        <table class="stats-table">
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Count</th>
                    <th>Mean</th>
                    <th>Std</th>
                    <th>Min</th>
                    <th>25%</th>
                    <th>50%</th>
                    <th>75%</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Add statistics rows
    for col, stats in analysis_results.get('descriptive_statistics', {}).items():
        html_content += f"""
            <tr>
                <td><strong>{col}</strong></td>
                <td>{stats.get('count', 'N/A'):.0f}</td>
                <td>{stats.get('mean', 'N/A'):.2f}</td>
                <td>{stats.get('std', 'N/A'):.2f}</td>
                <td>{stats.get('min', 'N/A'):.2f}</td>
                <td>{stats.get('25%', 'N/A'):.2f}</td>
                <td>{stats.get('50%', 'N/A'):.2f}</td>
                <td>{stats.get('75%', 'N/A'):.2f}</td>
                <td>{stats.get('max', 'N/A'):.2f}</td>
            </tr>
        """
    
    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
    """
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return report_path

def get_pdf_report_info(pdf_path: str) -> dict:
    """Get information about the generated report"""
    if not os.path.exists(pdf_path):
        return {"error": "Report file not found"}
    
    file_size = os.path.getsize(pdf_path)
    return {
        "filename": os.path.basename(pdf_path),
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "path": pdf_path
    }

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8081"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Cache the analysis results and AI commentary for future use
    try:
        analysis_cache_file = os.path.join(session_dir, "analysis_cache.json")
        ai_commentary_cache_file = os.path.join(session_dir, "ai_commentary_cache.json")
        
        with open(analysis_cache_file, 'w') as f:
            json.dump(analysis_results, f)
        
        with open(ai_commentary_cache_file, 'w') as f:
            json.dump({"commentary": ai_commentary}, f)
    except:
        pass  # Don't fail if caching fails

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

    # Check if analysis results are already cached
    analysis_cache_file = os.path.join(session_dir, "analysis_cache.json")
    
    if os.path.exists(analysis_cache_file):
        # Load cached analysis results
        try:
            with open(analysis_cache_file, 'r') as f:
                analysis_results = json.load(f)
        except:
            analysis_results = None
    else:
        analysis_results = None

    # Only re-analyze if cache doesn't exist
    if analysis_results is None:
        csv_files = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
        if not csv_files:
            raise HTTPException(status_code=404, detail="No CSV files found in session.")

        df = load_csv_fully(csv_files[0])
        analysis_results = analyze_dataframe(df, session_dir)
        
        # Cache the analysis results
        try:
            with open(analysis_cache_file, 'w') as f:
                json.dump(analysis_results, f)
        except:
            pass  # Don't fail if caching fails

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

    try:
        # Check if analysis results are already cached
        analysis_cache_file = os.path.join(session_dir, "analysis_cache.json")
        ai_commentary_cache_file = os.path.join(session_dir, "ai_commentary_cache.json")
        
        # Load cached analysis results if available
        if os.path.exists(analysis_cache_file):
            try:
                with open(analysis_cache_file, 'r') as f:
                    analysis_results = json.load(f)
            except:
                analysis_results = None
        else:
            analysis_results = None

        # Load cached AI commentary if available
        if os.path.exists(ai_commentary_cache_file):
            try:
                with open(ai_commentary_cache_file, 'r') as f:
                    ai_commentary = json.load(f).get("commentary", "Error generating commentary.")
            except:
                ai_commentary = None
        else:
            ai_commentary = None

        # Only re-process if cache doesn't exist
        if analysis_results is None:
            csv_file_paths = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
            if not csv_file_paths:
                raise HTTPException(status_code=404, detail="No CSV files found in session.")

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
            
            # Cache the analysis results
            try:
                with open(analysis_cache_file, 'w') as f:
                    json.dump(analysis_results, f)
            except:
                pass

            # 5. Generate AI commentary if not cached
            if ai_commentary is None:
                prompt = prepare_ai_prompt(analysis_results)
                ai_commentary_response = get_ai_commentary(prompt)
                ai_commentary = ai_commentary_response.get("commentary", "Error generating commentary.")
                
                # Cache the AI commentary
                try:
                    with open(ai_commentary_cache_file, 'w') as f:
                        json.dump({"commentary": ai_commentary}, f)
                except:
                    pass

        # Convert chart paths to URLs for PDF embedding
        chart_urls = {}
        if 'chart_paths' in analysis_results:
            for chart_type, paths in analysis_results['chart_paths'].items():
                chart_urls[chart_type] = [f"/sessions/{session_id}/charts/{os.path.basename(p)}" for p in paths]

        # 6. Generate PDF report
        pdf_path = generate_pdf_report(
            session_id=session_id,
            csv_metadata=csv_metadata if 'csv_metadata' in locals() else None,
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



@app.post("/generate-comprehensive-report/{session_id}")
async def generate_comprehensive_report_endpoint(session_id: str):
    """
    Generate a comprehensive data analysis report in Markdown format.
    Returns the report content and file information.
    """
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found.")

    csv_file_paths = [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith(".csv")]
    if not csv_file_paths:
        raise HTTPException(status_code=404, detail="No CSV files found in session.")

    try:
        # Use the first CSV file for the comprehensive report
        csv_file_path = csv_file_paths[0]
        
        # Generate the comprehensive report
        report_path = generate_data_analysis_report(csv_file_path)
        
        # Read the generated report content
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Get file info
        file_size = os.path.getsize(report_path)
        file_size_mb = file_size / (1024 * 1024)
        
        return JSONResponse(status_code=200, content={
            "session_id": session_id,
            "report_generated": True,
            "report_path": report_path,
            "report_filename": os.path.basename(report_path),
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size_mb, 2),
            "report_content": report_content,
            "download_url": f"/sessions/{session_id}/reports/{os.path.basename(report_path)}",
            "message": "Comprehensive data analysis report generated successfully"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate comprehensive report: {str(e)}")

@app.get("/sessions/{session_id}/reports/{report_name}")
async def download_comprehensive_report(session_id: str, report_name: str):
    """
    Download generated comprehensive report (Markdown or other formats).
    """
    report_path = os.path.join(UPLOAD_DIR, session_id, report_name)
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    
    # Determine content type based on file extension
    if report_name.endswith('.md'):
        media_type = "text/markdown"
    elif report_name.endswith('.pdf'):
        media_type = "application/pdf"
    else:
        media_type = "text/plain"
    
    return FileResponse(
        report_path,
        media_type=media_type,
        filename=report_name,
        headers={"Content-Disposition": f"attachment; filename={report_name}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
