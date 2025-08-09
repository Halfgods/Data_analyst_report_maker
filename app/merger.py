
import pandas as pd
from typing import List

def merge_dataframes(dataframes: List[pd.DataFrame], filenames: List[str]) -> List[pd.DataFrame]:
    """
    Takes a list of DataFrames and checks if all have identical schemas 
    (same columns with same types). If yes, merge into a single DataFrame; 
    if no, keep separate and add a source filename column to each.
    """
    if not dataframes:
        return []

    first_df = dataframes[0]
    first_schema = first_df.dtypes.to_dict()

    schemas_are_identical = True
    for df in dataframes[1:]:
        if df.dtypes.to_dict() != first_schema:
            schemas_are_identical = False
            break

    if schemas_are_identical:
        merged_df = pd.concat(dataframes, ignore_index=True)
        return [merged_df]
    else:
        for i, df in enumerate(dataframes):
            df["source_filename"] = filenames[i]
        return dataframes
