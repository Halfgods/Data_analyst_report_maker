
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any

def analyze_dataframe(df: pd.DataFrame, session_folder: str) -> Dict[str, Any]:
    """
    Generates descriptive statistics, group-by aggregations, and correlation matrices.
    Generates charts and saves them as PNG files in the session folder.
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
            analysis_results['groupby_aggregations'][cat_col] = df.groupby(cat_col)[numeric_cols].mean().to_dict()

    # 3. Correlation Matrix
    analysis_results['correlation_matrix'] = df[numeric_cols].corr().to_dict()

    # 4. Generate Charts
    # Histograms
    chart_paths = {}
    for num_col in numeric_cols:
        plt.figure()
        sns.histplot(df[num_col], kde=True)
        plt.title(f'Histogram of {num_col}')
        chart_filename = f'{num_col}_histogram.png'
        chart_path = os.path.join(session_folder, chart_filename)
        plt.savefig(chart_path)
        plt.close()
        if 'histograms' not in chart_paths:
            chart_paths['histograms'] = []
        chart_paths['histograms'].append(chart_path)

    # Bar charts
    for cat_col in categorical_cols:
        plt.figure()
        sns.countplot(y=cat_col, data=df)
        plt.title(f'Bar Chart of {cat_col}')
        chart_filename = f'{cat_col}_barchart.png'
        chart_path = os.path.join(session_folder, chart_filename)
        plt.savefig(chart_path)
        plt.close()
        if 'barcharts' not in chart_paths:
            chart_paths['barcharts'] = []
        chart_paths['barcharts'].append(chart_path)

    # Scatter plots
    if len(numeric_cols) > 1:
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                plt.figure()
                sns.scatterplot(x=numeric_cols[i], y=numeric_cols[j], data=df)
                plt.title(f'Scatter Plot of {numeric_cols[i]} vs {numeric_cols[j]}')
                chart_filename = f'{numeric_cols[i]}_vs_{numeric_cols[j]}_scatterplot.png'
                chart_path = os.path.join(session_folder, chart_filename)
                plt.savefig(chart_path)
                plt.close()
                if 'scatterplots' not in chart_paths:
                    chart_paths['scatterplots'] = []
                chart_paths['scatterplots'].append(chart_path)
    
    analysis_results['chart_paths'] = chart_paths
    return analysis_results
