# src/data_validator.py
import logging
import re
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    # Create static before df for comparison 
    before_rows = len(df)

    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Deal with non-numeric values in numeric columns
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    # TODO: Log a warning and record this row's index.
                    invalid_rows.append(i)
        # TODO: Remove the invalid rows.
        if invalid_rows:
            logger.warning(f"Removed {len(invalid_rows)} rows with invalid numeric values from column '{col}'")
        df = df.drop(index=invalid_rows)

        #convert to a numeric data type
        df[col] = pd.to_numeric(df[col])


    logger.debug(f"Validation: {before_rows} --> {len(df)} rows")
    return df
