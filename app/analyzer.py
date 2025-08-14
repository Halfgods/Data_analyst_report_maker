
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any
from app.smart_chart_generator import generate_smart_charts

def analyze_dataframe(df: pd.DataFrame, session_folder: str) -> Dict[str, Any]:
    """
    Generates descriptive statistics, group-by aggregations, and correlation matrices.
    Uses smart chart generation that only creates meaningful, clean visualizations.
    """
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)

    analysis_results = {}

    # 1. Descriptive Statistics
    analysis_results['descriptive_statistics'] = df.describe().to_dict()

    # 2. Group-by Aggregations
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        analysis_results['groupby_aggregations'] = {}
        for cat_col in categorical_cols:
            try:
                # Only generate aggregations for meaningful categorical columns
                if df[cat_col].nunique() <= 20 and df[cat_col].nunique() >= 2:
                    analysis_results['groupby_aggregations'][cat_col] = df.groupby(cat_col)[numeric_cols].mean().to_dict()
            except Exception as e:
                print(f"Warning: Could not generate aggregations for {cat_col}: {str(e)}")

    # 3. Correlation Matrix (only for numeric columns with sufficient variation)
    valid_numeric_cols = []
    for col in numeric_cols:
        if df[col].nunique() > 1 and df[col].notna().sum() >= 10:
            valid_numeric_cols.append(col)
    
    if len(valid_numeric_cols) > 1:
        try:
            correlation_df = df[valid_numeric_cols].corr()
            analysis_results['correlation_matrix'] = correlation_df.to_dict()
        except Exception as e:
            print(f"Warning: Could not generate correlation matrix: {str(e)}")
            analysis_results['correlation_matrix'] = {}
    else:
        analysis_results['correlation_matrix'] = {}

    # 4. Generate Smart Charts
    print("\n=== Generating Smart Charts ===\n")
    chart_generation_results = generate_smart_charts(df, session_folder)
    
    # Include chart paths and generation metadata
    analysis_results['chart_paths'] = chart_generation_results.get('chart_paths', {})
    analysis_results['chart_generation_summary'] = chart_generation_results.get('summary', {})
    analysis_results['chart_validation_log'] = chart_generation_results.get('validation_log', {})
    
    return analysis_results
