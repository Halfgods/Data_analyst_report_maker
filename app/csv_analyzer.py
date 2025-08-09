import pandas as pd
from typing import List, Dict, Any

def analyze_csv_files(file_paths: List[str]) -> Dict[str, Any]:
    """
    Reads each CSV into a Pandas DataFrame, detects column names and infers 
    data types (numeric, categorical, datetime, text). 
    
    Returns a metadata dict with filename, rows count, columns, and types.
    """
    metadata = {"files": []}
    for file_path in file_paths:
        try:
            # Use low_memory=False to help with mixed types
            df = pd.read_csv(file_path, low_memory=False)
            
            row_count = len(df)
            columns = list(df.columns)
            
            inferred_types = {}
            for col in columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    inferred_types[col] = "numeric"
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    inferred_types[col] = "datetime"
                elif pd.api.types.is_categorical_dtype(df[col]) or (df[col].nunique() / row_count) < 0.5:
                    inferred_types[col] = "categorical"
                else:
                    inferred_types[col] = "text"
            
            file_metadata = {
                "filename": file_path,
                "rows": row_count,
                "columns": columns,
                "inferred_types": inferred_types
            }
            metadata["files"].append(file_metadata)
            
        except MemoryError:
            metadata["files"].append({"filename": file_path, "error": "MemoryError: File is too large to process"})
        except Exception as e:
            metadata["files"].append({"filename": file_path, "error": str(e)})
            
    return metadata