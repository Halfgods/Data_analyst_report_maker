import polars as pl
import pandas as pd
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

def analyze_csv_metadata(file_paths: List[str]) -> Dict[str, Any]:
    """
    Fast metadata analysis using Polars for improved performance.
    Reads only the first 1000 rows for type inference and file analysis.
    """
    metadata = {"files": []}
    for file_path in file_paths:
        try:
            # Use Polars for fast metadata extraction
            df_sample = pl.read_csv(file_path, n_rows=1000)
            
            # Get file size for performance estimation
            file_size = os.path.getsize(file_path)
            
            # Estimate total rows based on sample
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                row_count = sum(1 for _ in f) - 1  # Subtract header

            columns = df_sample.columns
            
            # Enhanced type inference with Polars
            inferred_types = {}
            missing_values = {}
            sample_data = {}
            
            for col in columns:
                col_data = df_sample[col]
                null_count = col_data.null_count()
                missing_values[col] = null_count
                
                # Store sample data for preview (first 5 non-null values)
                sample_values = col_data.drop_nulls().head(5).to_list()
                sample_data[col] = sample_values
                
                # Improved type detection
                dtype = col_data.dtype
                if dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64]:
                    inferred_types[col] = "integer"
                elif dtype in [pl.Float32, pl.Float64]:
                    inferred_types[col] = "float"
                elif dtype in [pl.Date, pl.Datetime, pl.Time]:
                    inferred_types[col] = "datetime"
                elif dtype == pl.Boolean:
                    inferred_types[col] = "boolean"
                elif dtype == pl.Utf8:
                    # Check if it's categorical (low cardinality)
                    unique_count = col_data.n_unique()
                    if unique_count / len(col_data) < 0.1 and unique_count < 50:
                        inferred_types[col] = "categorical"
                    else:
                        inferred_types[col] = "text"
                else:
                    inferred_types[col] = "text"
            
            file_metadata = {
                "filename": os.path.basename(file_path),
                "full_path": file_path,
                "rows": row_count,
                "columns": columns,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "inferred_types": inferred_types,
                "missing_values": missing_values,
                "sample_data": sample_data
            }
            metadata["files"].append(file_metadata)
            
        except Exception as e:
            metadata["files"].append({
                "filename": os.path.basename(file_path), 
                "full_path": file_path,
                "error": str(e)
            })
            
    return metadata

def load_csv_with_polars(file_path: str, max_rows: Optional[int] = None) -> pl.DataFrame:
    """
    Load CSV using Polars for optimal performance.
    Handles large files efficiently with lazy loading when needed.
    """
    try:
        if max_rows:
            return pl.read_csv(file_path, n_rows=max_rows)
        else:
            # For large files, use lazy loading
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:  # 50MB threshold
                return pl.scan_csv(file_path).collect()
            else:
                return pl.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Failed to load CSV with Polars: {str(e)}")

def load_csv_fully(file_path: str, chunksize: int = 50000) -> pd.DataFrame:
    """
    Legacy pandas loader for backward compatibility.
    Consider using load_csv_with_polars for better performance.
    """
    try:
        # Try Polars first, fallback to pandas if needed
        try:
            pl_df = load_csv_with_polars(file_path)
            return pl_df.to_pandas()
        except:
            # Fallback to pandas chunking
            chunks = []
            with pd.read_csv(file_path, chunksize=chunksize, low_memory=False) as reader:
                for chunk in reader:
                    chunks.append(chunk)
            
            if not chunks:
                return pd.DataFrame()

            return pd.concat(chunks, ignore_index=True)
    except Exception as e:
        raise e
