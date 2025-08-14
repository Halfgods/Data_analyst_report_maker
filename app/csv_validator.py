import polars as pl
import pandas as pd
from typing import Dict, List, Any, Optional, Union
import re
from datetime import datetime

class PolarsCSVValidator:
    """
    High-performance CSV validation using vectorized Polars operations.
    Avoids Python loops for maximum speed on large datasets.
    """
    
    def __init__(self):
        # Date regex patterns for validation
        self.date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]
    
    def validate_csv_file(self, file_path: str, expected_types: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Validate entire CSV file using vectorized Polars operations.
        """
        try:
            # Read CSV with Polars (much faster than pandas)
            df = pl.read_csv(file_path)
            return self.validate_dataframe(df, expected_types)
            
        except Exception as e:
            return {
                "file_path": file_path,
                "error": f"Failed to read CSV: {str(e)}",
                "invalid_count": 0,
                "invalid_cells": []
            }
    
    def validate_dataframe(self, df: Union[pd.DataFrame, pl.DataFrame], expected_types: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Validate DataFrame using vectorized operations.
        """
        try:
            # Convert to Polars if pandas
            if isinstance(df, pd.DataFrame):
                df = pl.from_pandas(df)
            
            # Infer types if not provided
            if expected_types is None:
                expected_types = self._infer_column_types_vectorized(df)
            
            # Vectorized validation for all columns
            all_invalid_cells = []
            
            for column in df.columns:
                if column not in expected_types:
                    continue
                
                expected_type = expected_types[column]
                invalid_cells = self._validate_column_vectorized(df, column, expected_type)
                all_invalid_cells.extend(invalid_cells)
            
            return {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "invalid_count": len(all_invalid_cells),
                "invalid_cells": all_invalid_cells,
                "validation_summary": self._generate_validation_summary(all_invalid_cells, expected_types)
            }
            
        except Exception as e:
            return {
                "error": f"Validation failed: {str(e)}",
                "invalid_count": 0,
                "invalid_cells": []
            }
    
    def _infer_column_types_vectorized(self, df: pl.DataFrame) -> Dict[str, str]:
        """
        Vectorized type inference using Polars operations.
        """
        column_types = {}
        
        for col in df.columns:
            col_series = df[col]
            dtype = col_series.dtype
            
            # Direct type mapping from Polars types
            if dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64]:
                column_types[col] = "integer"
            elif dtype in [pl.Float32, pl.Float64]:
                column_types[col] = "float"
            elif dtype in [pl.Date, pl.Datetime]:
                column_types[col] = "datetime"
            elif dtype == pl.Boolean:
                column_types[col] = "boolean"
            elif dtype == pl.Utf8:
                # Use vectorized heuristics for string columns
                column_types[col] = self._infer_string_type_vectorized(col_series)
            else:
                column_types[col] = "text"
        
        return column_types
    
    def _infer_string_type_vectorized(self, col_series: pl.Series) -> str:
        """
        Vectorized heuristics to determine if string column is date, numeric, or text.
        """
        # Get non-null sample for analysis
        non_null = col_series.drop_nulls()
        if len(non_null) == 0:
            return "text"
        
        # Take sample for performance (first 1000 values)
        sample = non_null.head(min(1000, len(non_null)))
        
        # Check for date patterns (vectorized regex)
        date_pattern_combined = "|".join(f"({pattern})" for pattern in self.date_patterns)
        date_matches = sample.str.contains(date_pattern_combined).sum()
        if date_matches >= len(sample) * 0.6:  # 60% threshold
            return "date_string"
        
        # Check for numeric patterns (vectorized)
        # Remove common formatting and check if can convert to float
        cleaned = sample.str.replace_all(",", "").str.replace_all(" ", "")
        
        # Use Polars' built-in numeric detection
        try:
            # Try to cast to float - if most succeed, it's numeric
            numeric_test = cleaned.cast(pl.Float64, strict=False)
            non_null_numeric = numeric_test.drop_nulls()
            if len(non_null_numeric) >= len(sample) * 0.8:  # 80% threshold
                return "numeric_string"
        except:
            pass
        
        return "text"
    
    def _validate_column_vectorized(self, df: pl.DataFrame, column: str, expected_type: str) -> List[Dict[str, Any]]:
        """
        Vectorized validation for a single column.
        Returns list of invalid cells with their positions.
        """
        col_series = df[column]
        invalid_cells = []
        
        # Step 1: Find missing values (vectorized)
        missing_mask = col_series.is_null() | (col_series.str.strip() == "")
        if missing_mask.any():
            missing_indices = missing_mask.arg_true()
            for idx in missing_indices:
                invalid_cells.append({
                    "row": int(idx + 2),  # +2 for 1-based indexing and header
                    "column": column,
                    "value": "",
                    "error": "Missing value"
                })
        
        # Step 2: Validate non-missing values based on type
        non_missing_series = col_series.filter(~missing_mask)
        non_missing_indices = missing_mask.arg_false()  # Indices of non-missing values
        
        if len(non_missing_series) > 0:
            type_invalid_cells = self._validate_type_vectorized(
                non_missing_series, 
                non_missing_indices, 
                column, 
                expected_type
            )
            invalid_cells.extend(type_invalid_cells)
        
        return invalid_cells
    
    def _validate_type_vectorized(self, series: pl.Series, indices: pl.Series, column: str, expected_type: str) -> List[Dict[str, Any]]:
        """
        Vectorized type validation for non-missing values.
        """
        invalid_cells = []
        
        try:
            if expected_type == "integer":
                invalid_cells = self._validate_integer_vectorized(series, indices, column)
            
            elif expected_type == "float":
                invalid_cells = self._validate_float_vectorized(series, indices, column)
            
            elif expected_type == "boolean":
                invalid_cells = self._validate_boolean_vectorized(series, indices, column)
            
            elif expected_type == "date_string":
                invalid_cells = self._validate_date_string_vectorized(series, indices, column)
            
            elif expected_type == "numeric_string":
                invalid_cells = self._validate_numeric_string_vectorized(series, indices, column)
            
            elif expected_type == "datetime":
                invalid_cells = self._validate_datetime_vectorized(series, indices, column)
            
            # "text" type is always valid if not missing
            
        except Exception as e:
            # Fallback: mark all as invalid if vectorized validation fails
            for i, idx in enumerate(indices):
                invalid_cells.append({
                    "row": int(idx + 2),
                    "column": column,
                    "value": str(series[i]) if i < len(series) else "",
                    "error": f"Validation error: {str(e)}"
                })
        
        return invalid_cells
    
    def _validate_integer_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized integer validation."""
        invalid_cells = []
        
        try:
            # Clean common formatting
            cleaned = series.str.replace_all(",", "").str.replace_all(" ", "")
            
            # Try to cast to integer
            try:
                int_cast = cleaned.cast(pl.Int64, strict=False)
                invalid_mask = int_cast.is_null()
            except:
                # If casting fails entirely, mark all as invalid
                invalid_mask = pl.Series([True] * len(series))
            
            if invalid_mask.any():
                invalid_indices = invalid_mask.arg_true()
                for i in invalid_indices:
                    if i < len(series) and i < len(indices):
                        invalid_cells.append({
                            "row": int(indices[i] + 2),
                            "column": column,
                            "value": str(series[i]),
                            "error": "Expected integer"
                        })
        
        except Exception:
            # Fallback: mark all as invalid
            for i, idx in enumerate(indices):
                if i < len(series):
                    invalid_cells.append({
                        "row": int(idx + 2),
                        "column": column,
                        "value": str(series[i]),
                        "error": "Expected integer"
                    })
        
        return invalid_cells
    
    def _validate_float_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized float validation."""
        invalid_cells = []
        
        try:
            # Clean common formatting
            cleaned = series.str.replace_all(",", "").str.replace_all(" ", "")
            
            # Try to cast to float
            try:
                float_cast = cleaned.cast(pl.Float64, strict=False)
                invalid_mask = float_cast.is_null()
            except:
                invalid_mask = pl.Series([True] * len(series))
            
            if invalid_mask.any():
                invalid_indices = invalid_mask.arg_true()
                for i in invalid_indices:
                    if i < len(series) and i < len(indices):
                        invalid_cells.append({
                            "row": int(indices[i] + 2),
                            "column": column,
                            "value": str(series[i]),
                            "error": "Expected number"
                        })
        
        except Exception:
            for i, idx in enumerate(indices):
                if i < len(series):
                    invalid_cells.append({
                        "row": int(idx + 2),
                        "column": column,
                        "value": str(series[i]),
                        "error": "Expected number"
                    })
        
        return invalid_cells
    
    def _validate_boolean_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized boolean validation."""
        invalid_cells = []
        
        # Valid boolean values (case insensitive)
        valid_bools = ["true", "false", "1", "0", "yes", "no", "y", "n"]
        
        # Convert to lowercase for comparison
        lower_series = series.str.to_lowercase()
        
        # Check if each value is in valid list
        is_valid = lower_series.is_in(valid_bools)
        invalid_mask = ~is_valid
        
        if invalid_mask.any():
            invalid_indices = invalid_mask.arg_true()
            for i in invalid_indices:
                if i < len(series) and i < len(indices):
                    invalid_cells.append({
                        "row": int(indices[i] + 2),
                        "column": column,
                        "value": str(series[i]),
                        "error": "Expected boolean (true/false, 1/0, yes/no)"
                    })
        
        return invalid_cells
    
    def _validate_date_string_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized date string validation."""
        invalid_cells = []
        
        # Combined regex pattern for all date formats
        date_pattern = "|".join(f"({pattern})" for pattern in self.date_patterns)
        
        # Check format match
        format_match = series.str.contains(date_pattern)
        format_invalid_mask = ~format_match
        
        if format_invalid_mask.any():
            invalid_indices = format_invalid_mask.arg_true()
            for i in invalid_indices:
                if i < len(series) and i < len(indices):
                    invalid_cells.append({
                        "row": int(indices[i] + 2),
                        "column": column,
                        "value": str(series[i]),
                        "error": "Invalid date format (expected YYYY-MM-DD, MM/DD/YYYY, etc.)"
                    })
        
        return invalid_cells
    
    def _validate_numeric_string_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized numeric string validation."""
        # Same logic as float validation since numeric strings should parse as numbers
        return self._validate_float_vectorized(series, indices, column)
    
    def _validate_datetime_vectorized(self, series: pl.Series, indices: pl.Series, column: str) -> List[Dict[str, Any]]:
        """Vectorized datetime validation."""
        invalid_cells = []
        
        # For datetime columns, check if they're actually datetime type
        if series.dtype not in [pl.Date, pl.Datetime]:
            # Try to parse as datetime
            try:
                datetime_cast = series.str.strptime(pl.Datetime, "%Y-%m-%d", strict=False)
                invalid_mask = datetime_cast.is_null()
                
                if invalid_mask.any():
                    invalid_indices = invalid_mask.arg_true()
                    for i in invalid_indices:
                        if i < len(series) and i < len(indices):
                            invalid_cells.append({
                                "row": int(indices[i] + 2),
                                "column": column,
                                "value": str(series[i]),
                                "error": "Expected datetime"
                            })
            except:
                # Mark all as invalid if parsing fails
                for i, idx in enumerate(indices):
                    if i < len(series):
                        invalid_cells.append({
                            "row": int(idx + 2),
                            "column": column,
                            "value": str(series[i]),
                            "error": "Expected datetime"
                        })
        
        return invalid_cells
    
    def _generate_validation_summary(self, invalid_cells: List[Dict[str, Any]], expected_types: Dict[str, str]) -> Dict[str, Any]:
        """Generate summary of validation results."""
        if not invalid_cells:
            return {
                "status": "valid",
                "message": "No validation errors found"
            }
        
        # Group errors by type and column (vectorized using collections)
        from collections import Counter
        
        error_counts = Counter(cell["error"] for cell in invalid_cells)
        column_counts = Counter(cell["column"] for cell in invalid_cells)
        
        return {
            "status": "invalid",
            "total_errors": len(invalid_cells),
            "error_types": dict(error_counts),
            "columns_with_errors": dict(column_counts),
            "most_common_error": error_counts.most_common(1)[0][0] if error_counts else None
        }

# Convenience functions that maintain the same API
def validate_csv_file(file_path: str, expected_types: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Validate a CSV file using high-performance vectorized operations.
    
    Args:
        file_path: Path to CSV file to validate
        expected_types: Optional dict mapping column names to expected types
    
    Returns:
        Validation results in JSON format
    """
    validator = PolarsCSVValidator()
    result = validator.validate_csv_file(file_path, expected_types)
    result["file_path"] = file_path
    return result

def validate_dataframe(df: Union[pd.DataFrame, pl.DataFrame], expected_types: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Validate a DataFrame using high-performance vectorized operations.
    
    Args:
        df: Pandas or Polars DataFrame to validate
        expected_types: Optional dict mapping column names to expected types
    
    Returns:
        Validation results in JSON format
    """
    validator = PolarsCSVValidator()
    return validator.validate_dataframe(df, expected_types)
