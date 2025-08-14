import polars as pl
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

def detect_chart_type(column_data: pl.Series, column_name: str, data_type: str) -> Dict[str, Any]:
    """
    Intelligently detect the best chart type for a column based on its characteristics.
    Returns chart configuration for frontend rendering.
    """
    
    unique_count = column_data.n_unique()
    total_count = len(column_data)
    null_count = column_data.null_count()
    
    # Handle different data types
    if data_type in ["integer", "float"]:
        # Numeric data
        if unique_count < 10:
            # Few unique values - bar chart
            return {
                "type": "bar",
                "title": f"Distribution of {column_name}",
                "data": prepare_bar_data(column_data, column_name),
                "config": {
                    "xAxis": {"type": "category", "name": column_name},
                    "yAxis": {"type": "value", "name": "Count"},
                    "showLegend": False
                }
            }
        else:
            # Many unique values - histogram
            return {
                "type": "histogram", 
                "title": f"Distribution of {column_name}",
                "data": prepare_histogram_data(column_data, column_name),
                "config": {
                    "xAxis": {"type": "value", "name": column_name},
                    "yAxis": {"type": "value", "name": "Frequency"},
                    "binCount": min(30, max(10, unique_count // 10))
                }
            }
    
    elif data_type == "categorical":
        if unique_count <= 10:
            # Pie chart for small categories
            return {
                "type": "pie",
                "title": f"Composition of {column_name}",
                "data": prepare_pie_data(column_data, column_name),
                "config": {
                    "showLegend": True,
                    "radius": ["40%", "70%"]
                }
            }
        else:
            # Bar chart for many categories (top 10)
            return {
                "type": "bar",
                "title": f"Top Categories in {column_name}",
                "data": prepare_bar_data(column_data, column_name, limit=10),
                "config": {
                    "xAxis": {"type": "category", "name": column_name},
                    "yAxis": {"type": "value", "name": "Count"},
                    "showLegend": False
                }
            }
    
    elif data_type == "datetime":
        return {
            "type": "line",
            "title": f"Timeline of {column_name}",
            "data": prepare_timeline_data(column_data, column_name),
            "config": {
                "xAxis": {"type": "time", "name": "Date"},
                "yAxis": {"type": "value", "name": "Count"},
                "showLegend": False
            }
        }
    
    else:
        # Default to bar chart for text data
        return {
            "type": "bar",
            "title": f"Distribution of {column_name}",
            "data": prepare_bar_data(column_data, column_name, limit=10),
            "config": {
                "xAxis": {"type": "category", "name": column_name},
                "yAxis": {"type": "value", "name": "Count"},
                "showLegend": False
            }
        }

def prepare_bar_data(column_data: pl.Series, column_name: str, limit: Optional[int] = None) -> List[Dict]:
    """Prepare data for bar charts"""
    value_counts = column_data.value_counts().sort("counts", descending=True)
    
    if limit:
        value_counts = value_counts.head(limit)
    
    return [
        {"name": str(row[column_name]), "value": int(row["counts"])}
        for row in value_counts.iter_rows(named=True)
    ]

def prepare_pie_data(column_data: pl.Series, column_name: str) -> List[Dict]:
    """Prepare data for pie charts"""
    value_counts = column_data.value_counts().sort("counts", descending=True)
    
    return [
        {"name": str(row[column_name]), "value": int(row["counts"])}
        for row in value_counts.iter_rows(named=True)
    ]

def prepare_histogram_data(column_data: pl.Series, column_name: str, bins: int = 20) -> List[Dict]:
    """Prepare data for histograms"""
    # Convert to pandas for histogram calculation
    pd_series = column_data.to_pandas().dropna()
    
    if len(pd_series) == 0:
        return []
    
    hist, bin_edges = np.histogram(pd_series, bins=bins)
    
    return [
        {
            "bin_start": float(bin_edges[i]),
            "bin_end": float(bin_edges[i + 1]),
            "count": int(hist[i]),
            "bin_center": float((bin_edges[i] + bin_edges[i + 1]) / 2)
        }
        for i in range(len(hist))
    ]

def prepare_timeline_data(column_data: pl.Series, column_name: str) -> List[Dict]:
    """Prepare data for timeline charts"""
    try:
        # Convert to datetime if not already
        if column_data.dtype != pl.Datetime:
            date_series = pl.col(column_name).str.strptime(pl.Datetime, "%Y-%m-%d", strict=False)
        else:
            date_series = column_data
        
        # Group by date and count occurrences
        df = pl.DataFrame({column_name: date_series})
        timeline_data = df.groupby(column_name).agg(pl.count().alias("count")).sort(column_name)
        
        return [
            {
                "date": row[column_name].isoformat() if row[column_name] else None,
                "count": int(row["count"])
            }
            for row in timeline_data.iter_rows(named=True)
            if row[column_name] is not None
        ]
    except:
        # Fallback to simple counting if datetime parsing fails
        return prepare_bar_data(column_data, column_name)

def generate_correlation_chart(df: pl.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
    """Generate correlation matrix visualization data"""
    if len(numeric_columns) < 2:
        return None
    
    # Calculate correlation matrix using pandas (Polars correlation is limited)
    pd_df = df.select(numeric_columns).to_pandas()
    corr_matrix = pd_df.corr()
    
    # Prepare data for heatmap
    data = []
    for i, col1 in enumerate(numeric_columns):
        for j, col2 in enumerate(numeric_columns):
            data.append({
                "x": j,
                "y": i,
                "value": float(corr_matrix.loc[col1, col2]),
                "col1": col1,
                "col2": col2
            })
    
    return {
        "type": "heatmap",
        "title": "Correlation Matrix",
        "data": data,
        "config": {
            "xAxis": {"type": "category", "data": numeric_columns},
            "yAxis": {"type": "category", "data": numeric_columns},
            "visualMap": {
                "min": -1,
                "max": 1,
                "color": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", 
                         "#ffffcc", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
            }
        }
    }

def generate_scatter_plots(df: pl.DataFrame, numeric_columns: List[str], max_pairs: int = 6) -> List[Dict[str, Any]]:
    """Generate scatter plot configurations for numeric column pairs"""
    scatter_plots = []
    
    if len(numeric_columns) < 2:
        return scatter_plots
    
    # Generate scatter plots for most correlated pairs
    pd_df = df.select(numeric_columns).to_pandas()
    corr_matrix = pd_df.corr().abs()
    
    # Get top correlated pairs
    pairs = []
    for i in range(len(numeric_columns)):
        for j in range(i + 1, len(numeric_columns)):
            col1, col2 = numeric_columns[i], numeric_columns[j]
            corr_value = corr_matrix.loc[col1, col2]
            pairs.append((col1, col2, corr_value))
    
    # Sort by correlation and take top pairs
    pairs.sort(key=lambda x: x[2], reverse=True)
    top_pairs = pairs[:max_pairs]
    
    for col1, col2, corr in top_pairs:
        # Sample data if too large (for performance)
        sample_df = df.sample(n=min(1000, len(df))) if len(df) > 1000 else df
        
        scatter_data = [
            {"x": float(row[col1]), "y": float(row[col2])}
            for row in sample_df.select([col1, col2]).iter_rows(named=True)
            if row[col1] is not None and row[col2] is not None
        ]
        
        scatter_plots.append({
            "type": "scatter",
            "title": f"{col1} vs {col2} (r={corr:.3f})",
            "data": scatter_data,
            "config": {
                "xAxis": {"type": "value", "name": col1},
                "yAxis": {"type": "value", "name": col2},
                "showLegend": False
            }
        })
    
    return scatter_plots

def generate_all_charts(df: pl.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate all recommended charts for the dataset.
    Returns a complete chart configuration for frontend rendering.
    """
    charts = {
        "individual_columns": [],
        "correlations": None,
        "scatter_plots": [],
        "summary": {
            "total_charts": 0,
            "recommended_charts": []
        }
    }
    
    if len(df) == 0:
        return charts
    
    # Get column types from metadata
    inferred_types = metadata.get("inferred_types", {})
    
    # Generate individual column charts
    for column in df.columns:
        if column not in inferred_types:
            continue
            
        data_type = inferred_types[column]
        column_data = df[column]
        
        # Skip columns with too many nulls (>80%)
        null_percentage = column_data.null_count() / len(column_data)
        if null_percentage > 0.8:
            continue
        
        chart_config = detect_chart_type(column_data, column, data_type)
        if chart_config:
            charts["individual_columns"].append(chart_config)
    
    # Generate correlation matrix for numeric columns
    numeric_columns = [col for col, dtype in inferred_types.items() 
                      if dtype in ["integer", "float"] and col in df.columns]
    
    if len(numeric_columns) >= 2:
        correlation_chart = generate_correlation_chart(df, numeric_columns)
        if correlation_chart:
            charts["correlations"] = correlation_chart
    
    # Generate scatter plots
    scatter_plots = generate_scatter_plots(df, numeric_columns)
    charts["scatter_plots"] = scatter_plots
    
    # Update summary
    total_charts = len(charts["individual_columns"]) + len(charts["scatter_plots"])
    if charts["correlations"]:
        total_charts += 1
    
    charts["summary"]["total_charts"] = total_charts
    charts["summary"]["recommended_charts"] = [
        chart["type"] for chart in charts["individual_columns"]
    ]
    
    return charts
