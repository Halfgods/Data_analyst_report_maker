# 🚀 Intelligent Data Analysis Dashboard

Welcome to the **Intelligent Data Analysis Dashboard**! This powerful application empowers you to effortlessly transform raw CSV data into actionable insights, leveraging advanced data processing, cleaning, visualization, and cutting-edge AI capabilities. Say goodbye to manual data wrangling and hello to automated intelligence! 📈

## ✨ Key Features & Benefits

*   **Effortless CSV Upload**: 📤 Simply drag-and-drop or select one or more CSV files to begin your analysis journey.
*   **Smart Data Ingestion**:
    *   **Automatic Metadata Discovery**: 🔍 Understand your data at a glance with automated detection of column names and intelligent inference of data types (numeric, categorical, datetime, text).
    *   **Intelligent Merging**: 🤝 Upload multiple CSVs? Our system intelligently checks for schema compatibility. If they align, they're seamlessly merged into a single, unified dataset. Otherwise, they're processed individually, each clearly tagged with its original source.
*   **Robust Data Preprocessing**:
    *   **Automated Cleaning**: 🧹 Say goodbye to messy data! The dashboard automatically handles missing values (filling numeric with mean/median, categorical with mode) and efficiently removes duplicate rows.
    *   **Outlier Detection**: 🚨 Get alerted to unusual data points. Our system flags potential outliers using the Interquartile Range (IQR) method, helping you identify anomalies that might skew your analysis.
*   **Comprehensive Data Analysis**:
    *   **Statistical Summaries**: 📊 Gain immediate insights with automatically generated descriptive statistics, revealing the core characteristics of your dataset.
    *   **Group-by Aggregations**: Grouping data by categorical variables provides powerful insights into relationships and trends.
    *   **Correlation Matrices**: Discover hidden relationships between your numerical variables with automatically computed correlation matrices.
*   **Dynamic Visualizations**: 🎨 Explore your data visually with a suite of automatically generated charts:
    *   **Histograms**: Understand the distribution of your numerical data.
    *   **Bar Charts**: Visualize the frequency and distribution of your categorical data.
    *   **Scatter Plots**: Uncover relationships and patterns between pairs of numerical variables.
*   **AI-Powered Insights (Gemini Integration)**: 🧠
    *   **Automated Commentary**: Receive concise, factual AI-generated commentary on your data's quality, emerging trends, and identified anomalies. It's like having a data analyst by your side!
    *   **Contextual Q&A**: Have specific questions about your data? Ask away! Our AI provides answers *strictly* based on the analysis results, ensuring highly relevant and hallucination-free responses.

## ⚙️ How It Works: The Intelligent Workflow

This application is powered by a robust **FastAPI** backend and an intuitive **HTML/JavaScript** frontend. Here's a step-by-step breakdown of the magic that happens behind the scenes:

1.  **User Interaction (Frontend - `index.html`)**:
    *   You initiate the process by selecting and uploading your CSV file(s) through the user-friendly web interface.
    *   The frontend sends these files to the backend and triggers the data processing pipeline.

2.  **Backend Orchestration (`main.py`)**:
    *   Upon receiving your files, `main.py` acts as the central coordinator. It creates a unique session ID and a dedicated directory (`uploads/{session_id}`) to store your data and all generated artifacts (charts, analysis results).
    *   It then orchestrates the following sequence of operations:

    *   **CSV Metadata Analysis (`csv_analyzer.py`)**:
        *   Your raw CSVs are read into Pandas DataFrames.
        *   This module meticulously inspects each column, inferring its data type (e.g., `numeric`, `categorical`, `datetime`, `text`) and collecting essential metadata like row counts and column names.

    *   **Intelligent Data Merging (`merger.py`)**:
        *   If you've uploaded multiple CSVs, `merger.py` intelligently assesses their schemas.
        *   If all schemas are identical, the DataFrames are efficiently concatenated into a single, comprehensive DataFrame.
        *   If schemas differ, the DataFrames are kept separate, and a `source_filename` column is added to each, preserving data integrity and traceability.

    *   **Automated Data Cleaning (`cleaner.py`)**:
        *   The DataFrame(s) are passed to `cleaner.py` for preprocessing.
        *   Missing values are systematically handled: numerical columns are imputed with their mean or median, while categorical columns are filled with their mode.
        *   Duplicate rows are identified and removed to ensure data uniqueness.
        *   Outliers are detected using the IQR method, and a new boolean column (`{column_name}_is_outlier`) is added to flag these unusual data points.

    *   **Comprehensive Data Analysis (`analyzer.py`)**:
        *   The cleaned DataFrame(s) are now ready for in-depth analysis.
        *   `analyzer.py` computes crucial statistical measures: descriptive statistics (mean, median, std dev, etc.), group-by aggregations (e.g., average sales by region), and correlation matrices (showing relationships between numerical variables).
        *   It also generates a variety of insightful charts (histograms, bar charts, scatter plots) using `matplotlib` and `seaborn`, saving them as PNG images within your session directory.

    *   **AI-Powered Commentary (`ai_commentary.py`)**:
        *   The rich analysis summary (descriptive stats, aggregations, correlations) is then sent to the Gemini API via `ai_commentary.py`.
        *   The AI processes this summary and generates a concise, factual commentary, highlighting key trends, data quality issues, and potential anomalies.

3.  **Results Delivery & Display**:
    *   All generated analysis results, including URLs to the charts and the AI commentary, are sent back to the frontend.
    *   `index.html` then beautifully renders these results, allowing you to interact with the charts and read the AI's insights directly in your browser.

4.  **Interactive AI Querying**:
    *   Want to dig deeper? You can type specific questions into the AI query box.
    *   Your question, along with the comprehensive analysis summary, is sent back to `ai_commentary.py`.
    *   The AI, constrained to *only* use the provided data, generates a precise answer, ensuring relevance and preventing external knowledge interference.

## 📂 Project Structure

```
.
├── app/
│   ├── ai_commentary.py      # AI interaction (Gemini API) for commentary and Q&A
│   ├── analyzer.py           # Core data analysis and chart generation
│   ├── cleaner.py            # Data cleaning operations (missing values, duplicates, outliers)
│   ├── csv_analyzer.py       # CSV reading and metadata extraction
│   ├── index.html            # Frontend user interface
│   ├── main.py               # FastAPI application entry point, orchestrator
│   └── merger.py             # Logic for merging multiple DataFrames
├── uploads/                  # Directory for uploaded CSVs and session-specific data
├── charts/                   # (Potentially for static charts, though currently session-based)
├── test_csvs/                # Example CSV files for testing
├── venv/                     # Python virtual environment
└── README.md                 # This file!
```

## 🛠️ Setup and Local Development

Follow these steps to get the Data Analysis Dashboard up and running on your local machine.

### Prerequisites

*   **Python 3.9+**: Ensure you have a compatible Python version installed.
*   **pip**: Python's package installer (usually comes with Python).
*   **Google Gemini API Key**: You'll need an API key from Google AI Studio. You can get one [here](https://aistudio.google.com/app/apikey).

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url> # Replace <repository_url> with your actual repo URL
    cd Project # Or whatever your project directory is named
    ```

2.  **Create a Virtual Environment (Recommended)**:
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    *   **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```
    *   **Windows (Command Prompt)**:
        ```bash
        venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell)**:
        ```bash
        venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Set Your Gemini API Key**:
    The application looks for your Gemini API key in two places:
    *   **Environment Variable (Recommended)**:
        ```bash
        export GEMINI_API_KEY='YOUR_API_KEY_HERE' # Linux/macOS
        # For Windows, use: set GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
    *   **`api.json` file**: Create a file named `api.json` in your project's root directory with the following content:
        ```json
        {
          "GEMINI_API_KEY": "YOUR_API_KEY_HERE"
        }
        ```
        **Note**: For production environments, using environment variables is highly recommended for security.

### Running the Application

1.  **Start the FastAPI Server**:
    Make sure your virtual environment is activated.
    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Access the Dashboard**:
    Open your web browser and navigate to:
    ```
    http://127.0.0.1:8000/
    ```
    You should now see the Data Analysis Dashboard interface!
