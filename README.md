# Intelligent Data Analysis Dashboard

This project is a web-based application that allows users to upload CSV files, analyze the data, and generate reports. The application is built with a FastAPI backend and a React frontend.

## Features

-   **CSV Upload**: Upload one or more CSV files for analysis.
-   **Data Analysis**: The application performs data analysis, including descriptive statistics, data cleaning, and visualization.
-   **AI-Powered Insights**: The application uses a large language model to generate commentary and answer questions about the data.
-   **PDF Reports**: Generate PDF reports of the analysis.

## Technologies Used

### Backend

-   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
-   **Pandas**: A powerful data manipulation and analysis library for Python.
-   **Google Generative AI**: Used for AI-powered insights.
-   **Matplotlib and Seaborn**: Used for generating charts and visualizations.

### Frontend

-   **React**: A JavaScript library for building user interfaces.
-   **Vite**: A build tool that aims to provide a faster and leaner development experience for modern web projects.
-   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom user interfaces.

## Project Structure

```
.
├── app/                  # Backend FastAPI application
│   ├── ai_commentary.py
│   ├── analyzer.py
│   ├── cleaner.py
│   ├── csv_analyzer.py
│   ├── main.py
│   ├── merger.py
│   ├── pdf_generator.py
│   └── ...
├── UI/                   # Frontend React application
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
├── uploads/              # Directory for uploaded CSVs and session-specific data
├── test_csvs/            # Example CSV files for testing
├── venv/                 # Python virtual environment
├── .gitignore
├── README.md
├── requirements.txt
└── test_large_csv.py
```

## Setup and Installation

### Prerequisites

-   Python 3.9+
-   Node.js and npm
-   Google Gemini API Key

### Backend

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd Project
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the environment variables**:
    Create a `.env` file in the root directory and add your `GEMINI_API_KEY`:
    ```
    GEMINI_API_KEY=your_api_key
    ```

### Frontend

1.  **Navigate to the `UI` directory**:
    ```bash
    cd UI
    ```

2.  **Install the dependencies**:
    ```bash
    npm install
    ```

## Running the Application

### Backend

1.  **Start the FastAPI server**:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  **Start the development server**:
    ```bash
    npm run dev
    ```

The application will be available at `http://localhost:5173`.
