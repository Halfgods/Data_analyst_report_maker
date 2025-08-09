
import pandas as pd
from typing import List, Tuple, Dict, Any

def clean_dataframe(df: pd.DataFrame, fill_numeric_with: str = 'mean') -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """
    Performs cleaning steps on a DataFrame:
    - Fills missing values (numeric with mean/median, categorical with mode).
    - Removes duplicate rows.
    - Detects and flags outliers using the IQR method.
    
    Returns the cleaned DataFrame and a list of flagged errors.
    """
    if fill_numeric_with not in ['mean', 'median']:
        raise ValueError("fill_numeric_with must be either 'mean' or 'median'")

    cleaned_df = df.copy()
    errors = []

    # 1. Fill missing values
    for col in cleaned_df.columns:
        if pd.api.types.is_numeric_dtype(cleaned_df[col]):
            if cleaned_df[col].isnull().any():
                if fill_numeric_with == 'mean':
                    fill_value = cleaned_df[col].mean()
                else:
                    fill_value = cleaned_df[col].median()
                cleaned_df[col] = cleaned_df[col].fillna(fill_value)
        else:
            if cleaned_df[col].isnull().any():
                fill_value = cleaned_df[col].mode()[0]
                cleaned_df[col] = cleaned_df[col].fillna(fill_value)

    # 2. Remove duplicate rows
    cleaned_df.drop_duplicates(inplace=True)

    # 3. Detect and flag outliers
    for col in cleaned_df.select_dtypes(include=['number']).columns:
        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = cleaned_df[(cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound)]
        if not outliers.empty:
            cleaned_df[f'{col}_is_outlier'] = False
            cleaned_df.loc[(cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound), f'{col}_is_outlier'] = True
            errors.append({
                "type": "outlier_detection",
                "column": col,
                "num_outliers": len(outliers),
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            })

    return cleaned_df, errors
