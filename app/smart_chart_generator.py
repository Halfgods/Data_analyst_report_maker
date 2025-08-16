import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from scipy.stats import pearsonr
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')

def validate_column_for_histogram(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Validates if a numeric column is suitable for histogram visualization.
    """
    series = df[column].dropna()
    
    if len(series) == 0:
        return {"valid": False, "reason": "No data after removing nulls"}
    
    if len(series) < 10:
        return {"valid": False, "reason": "Insufficient data points (< 10)"}
    
    # Check if all values are the same (no variation)
    if series.nunique() <= 1:
        return {"valid": False, "reason": "No variation in data (all values identical)"}
    
    # Check for reasonable distribution
    if series.nunique() < 5 and len(series) > 50:
        return {"valid": False, "reason": "Too few unique values for meaningful histogram"}
    
    # Check for extreme outliers that would make histogram unreadable
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    if IQR > 0:
        outlier_threshold = 3 * IQR
        outliers = series[(series < Q1 - outlier_threshold) | (series > Q3 + outlier_threshold)]
        if len(outliers) > len(series) * 0.5:
            return {"valid": False, "reason": "Too many extreme outliers (> 50%)"}
    
    return {
        "valid": True,
        "sample_size": len(series),
        "unique_values": series.nunique(),
        "data_range": f"{series.min():.2f} to {series.max():.2f}"
    }

def validate_column_for_barchart(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Validates if a categorical column is suitable for bar chart visualization.
    """
    series = df[column].dropna()
    
    if len(series) == 0:
        return {"valid": False, "reason": "No data after removing nulls"}
    
    if len(series) < 5:
        return {"valid": False, "reason": "Insufficient data points (< 5)"}
    
    unique_count = series.nunique()
    
    # Too few categories
    if unique_count < 2:
        return {"valid": False, "reason": "Only one category (no comparison possible)"}
    
    # Too many categories (chart becomes unreadable)
    if unique_count > 20:
        return {"valid": False, "reason": "Too many categories (> 20) - chart would be unreadable"}
    
    # Check if categories have meaningful distribution
    value_counts = series.value_counts()
    max_count = value_counts.max()
    min_count = value_counts.min()
    
    # If one category dominates > 95%, chart is not meaningful
    if max_count / len(series) > 0.95:
        return {"valid": False, "reason": "One category dominates > 95% of data"}
    
    # Check for categories with very low counts that add noise
    low_count_categories = value_counts[value_counts < max(3, len(series) * 0.01)].count()
    if low_count_categories > unique_count * 0.5:
        return {"valid": False, "reason": "Too many low-frequency categories"}
    
    return {
        "valid": True,
        "categories": unique_count,
        "sample_size": len(series),
        "top_category": f"{value_counts.index[0]} ({value_counts.iloc[0]} occurrences)"
    }

def validate_columns_for_scatter(df: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
    """
    Validates if two numeric columns are suitable for scatter plot visualization.
    """
    series1 = df[col1].dropna()
    series2 = df[col2].dropna()
    
    # Get common non-null indices
    common_data = df[[col1, col2]].dropna()
    if len(common_data) < 10:
        return {"valid": False, "reason": "Insufficient paired data points (< 10)"}
    
    x, y = common_data[col1], common_data[col2]
    
    # Check for variation in both dimensions
    if x.nunique() <= 1 or y.nunique() <= 1:
        return {"valid": False, "reason": "No variation in one or both dimensions"}
    
    # Check for correlation significance
    try:
        corr_coef, p_value = pearsonr(x, y)
        
        # Skip if correlation is too weak to be meaningful
        if abs(corr_coef) < 0.1:
            return {"valid": False, "reason": f"Correlation too weak (r={corr_coef:.3f})"}
        
        # Skip if correlation is not statistically significant
        if p_value > 0.05:
            return {"valid": False, "reason": f"Correlation not significant (p={p_value:.3f})"}
            
    except Exception as e:
        return {"valid": False, "reason": f"Could not calculate correlation: {str(e)}"}
    
    return {
        "valid": True,
        "correlation": corr_coef,
        "p_value": p_value,
        "sample_size": len(common_data),
        "interpretation": "Strong" if abs(corr_coef) > 0.7 else "Moderate" if abs(corr_coef) > 0.4 else "Weak"
    }

def create_clean_histogram(df: pd.DataFrame, column: str, session_folder: str) -> Optional[str]:
    """
    Creates a clean, publication-ready histogram.
    """
    series = df[column].dropna()
    # Check for skewness
    skewness = series.skew()
    if abs(skewness) > 2:
        print(f"Skipping mean/median for {column}: highly skewed (skew={skewness:.2f})")
        show_stats = False
    else:
        show_stats = True

    plt.figure(figsize=(10, 6))
    plt.style.use('default')
    bins = min(30, max(10, int(np.sqrt(len(series)))))
    plt.hist(series, bins=bins, alpha=0.7, color='#1f77b4', edgecolor='white', linewidth=0.5)

    if show_stats:
        mean_val = series.mean()
        median_val = series.median()
        plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, alpha=0.8, label=f'Mean: {mean_val:.2f}')
        plt.axvline(median_val, color='green', linestyle='--', linewidth=2, alpha=0.8, label=f'Median: {median_val:.2f}')
        plt.legend(fontsize=10)

    plt.title(f'Distribution of {column.title()}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(column.title(), fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_filename = f'{safe_column_name}_histogram.png'
    chart_path = os.path.join(session_folder, chart_filename)
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    return chart_path

def create_interactive_histogram(df: pd.DataFrame, column: str, session_folder: str) -> Optional[str]:
    """
    Creates an interactive histogram using Plotly.
    """
    series = df[column].dropna()
    fig = px.histogram(
        series,
        nbins=min(30, max(10, int(np.sqrt(len(series))))),
        title=f"Distribution of {column.title()}",
        labels={column: column.title(), "count": "Frequency"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig.update_layout(template="plotly_white")
    
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_path = os.path.join(session_folder, f"{safe_column_name}_histogram.html")
    fig.write_html(chart_path, include_plotlyjs="cdn")
    return chart_path

def create_clean_barchart(df: pd.DataFrame, column: str, session_folder: str) -> Optional[str]:
    """
    Creates a clean, publication-ready bar chart.
    """
    series = df[column].dropna()
    value_counts = series.value_counts()
    
    # Limit to top categories if too many
    if len(value_counts) > 15:
        value_counts = value_counts.head(15)
        title_suffix = f" (Top 15 of {series.nunique()})"
    else:
        title_suffix = ""
    
    plt.figure(figsize=(12, max(6, len(value_counts) * 0.4)))
    plt.style.use('default')
    
    # Create horizontal bar chart for better readability
    bars = plt.barh(range(len(value_counts)), value_counts.values, color='#1f77b4', alpha=0.7)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + width * 0.01, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.yticks(range(len(value_counts)), value_counts.index)
    plt.title(f'Distribution of {column.title()}{title_suffix}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Count', fontsize=12)
    plt.ylabel(column.title(), fontsize=12)
    plt.grid(True, alpha=0.3, axis='x')
    
    # Invert y-axis to show highest values at top
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_filename = f'{safe_column_name}_barchart.png'
    chart_path = os.path.join(session_folder, chart_filename)
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return chart_path

def create_interactive_barchart(df: pd.DataFrame, column: str, session_folder: str) -> Optional[str]:
    """
    Creates an interactive bar chart using Plotly.
    """
    series = df[column].dropna()
    value_counts = series.value_counts()

    if len(value_counts) > 15:
        value_counts = value_counts.head(15)

    fig = px.bar(
        x=value_counts.index,
        y=value_counts.values,
        title=f"Distribution of {column.title()}",
        labels={"x": column.title(), "y": "Count"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig.update_traces(text=value_counts.values, textposition="outside")
    fig.update_layout(template="plotly_white", xaxis_tickangle=-45)
    
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_path = os.path.join(session_folder, f"{safe_column_name}_barchart.html")
    fig.write_html(chart_path, include_plotlyjs="cdn")
    return chart_path

def create_clean_scatterplot(df: pd.DataFrame, col1: str, col2: str, session_folder: str) -> Optional[str]:
    """
    Creates a clean, publication-ready scatter plot with correlation info.
    """
    common_data = df[[col1, col2]].dropna()
    x, y = common_data[col1], common_data[col2]
    
    plt.figure(figsize=(10, 8))
    plt.style.use('default')
    
    # Create scatter plot
    plt.scatter(x, y, alpha=0.6, s=50, color='#1f77b4', edgecolors='white', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", alpha=0.8, linewidth=2, label=f'Trend Line')
    
    # Calculate and display correlation
    corr_coef, p_value = pearsonr(x, y)
    
    plt.title(f'{col1.title()} vs {col2.title()}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(col1.title(), fontsize=12)
    plt.ylabel(col2.title(), fontsize=12)
    
    # Add correlation info to plot
    textstr = f'r = {corr_coef:.3f}\np = {p_value:.3f}\nn = {len(common_data)}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    # Clean column names for filename (remove special characters)
    safe_col1 = "".join(c for c in col1 if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    safe_col2 = "".join(c for c in col2 if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    
    chart_filename = f'{safe_col1}_vs_{safe_col2}_scatterplot.png'
    chart_path = os.path.join(session_folder, chart_filename)
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return chart_path

def create_interactive_scatterplot(df: pd.DataFrame, col1: str, col2: str, session_folder: str) -> Optional[str]:
    """
    Creates an interactive scatter plot using Plotly.
    """
    common_data = df[[col1, col2]].dropna()
    fig = px.scatter(
        common_data,
        x=col1,
        y=col2,
        title=f"{col1.title()} vs {col2.title()}",
        labels={col1: col1.title(), col2: col2.title()}
    )
    
    # Add correlation info to the chart title
    try:
        corr_coef, p_value = pearsonr(common_data[col1], common_data[col2])
        fig.update_layout(
            title=f"{col1.title()} vs {col2.title()}<br><sub>Correlation: r = {corr_coef:.3f}, p = {p_value:.3f}</sub>",
            template="plotly_white"
        )
    except:
        fig.update_layout(template="plotly_white")
    
    # Clean column names for filename (remove special characters)
    safe_col1 = "".join(c for c in col1 if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    safe_col2 = "".join(c for c in col2 if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    
    chart_path = os.path.join(session_folder, f"{safe_col1}_vs_{safe_col2}_scatterplot.html")
    fig.write_html(chart_path, include_plotlyjs="cdn")
    return chart_path

def create_interactive_piechart(df, column, session_folder) -> Optional[str]:
    series = df[column].dropna()
    value_counts = series.value_counts()
    fig = px.pie(names=value_counts.index, values=value_counts.values, title=f"Pie Chart of {column.title()}")
    
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_path = os.path.join(session_folder, f"{safe_column_name}_piechart.html")
    fig.write_html(chart_path, include_plotlyjs="cdn")
    return chart_path

def create_interactive_boxplot(df, column, session_folder) -> Optional[str]:
    series = df[column].dropna()
    fig = px.box(series, title=f"Boxplot of {column.title()}", labels={column: column.title()}, color_discrete_sequence=["#1f77b4"])
    
    # Clean column name for filename (remove special characters)
    safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_column_name = safe_column_name.replace(' ', '_')
    
    chart_path = os.path.join(session_folder, f"{safe_column_name}_boxplot.html")
    fig.write_html(chart_path, include_plotlyjs="cdn")
    return chart_path

def generate_smart_charts(df: pd.DataFrame, session_folder: str) -> Dict[str, Any]:
    """
    Generates only meaningful, interactive charts based on data validation.
    """
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    
    chart_paths = {}
    validation_log = {}
    
    # Get column types
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    # 1. Validate and create interactive histograms for numeric columns
    valid_histograms = []
    for col in numeric_cols:
        validation = validate_column_for_histogram(df, col)
        validation_log[f"{col}_histogram"] = validation
        if validation["valid"]:
            chart_path_html = create_interactive_histogram(df, col, session_folder)
            chart_path_png = create_clean_histogram(df, col, session_folder) # Generate PNG for PDF
            if chart_path_html:
                valid_histograms.append(chart_path_html)
    if valid_histograms:
        chart_paths['histograms'] = valid_histograms

    # 2. Validate and create interactive bar charts for categorical columns
    valid_barcharts = []
    for col in categorical_cols:
        validation = validate_column_for_barchart(df, col)
        validation_log[f"{col}_barchart"] = validation
        if validation["valid"]:
            chart_path_html = create_interactive_barchart(df, col, session_folder)
            chart_path_png = create_clean_barchart(df, col, session_folder) # Generate PNG for PDF
            if chart_path_html:
                valid_barcharts.append(chart_path_html)
    if valid_barcharts:
        chart_paths['barcharts'] = valid_barcharts

    # 3. Validate and create interactive scatter plots for numeric column pairs
    valid_scatterplots = []
    scatter_candidates = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            validation = validate_columns_for_scatter(df, col1, col2)
            validation_log[f"{col1}_vs_{col2}_scatter"] = validation
            if validation["valid"]:
                scatter_candidates.append((col1, col2, abs(validation["correlation"]), validation))

    scatter_candidates.sort(key=lambda x: x[2], reverse=True)
    for col1, col2, _, _ in scatter_candidates[:6]:
        chart_path_html = create_interactive_scatterplot(df, col1, col2, session_folder)
        chart_path_png = create_clean_scatterplot(df, col1, col2, session_folder) # Generate PNG for PDF
        if chart_path_html:
            valid_scatterplots.append(chart_path_html)
    if valid_scatterplots:
        chart_paths['scatterplots'] = valid_scatterplots

    return {
        "chart_paths": chart_paths,
        "validation_log": validation_log,
        "summary": {
            "total_charts_created": len(valid_histograms) + len(valid_barcharts) + len(valid_scatterplots)
        }
    }
