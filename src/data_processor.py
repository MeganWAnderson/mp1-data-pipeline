import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_start = len(df)
    clean_df = df.drop_duplicates()
    rows_end = len(clean_df)
    logger.debug(f"Removed {rows_start - rows_end} duplicate rows.")
    return clean_df



def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    rows_start = len(df)
    cols_start = len(df.columns)
    if axis == "rows":
        clean_df = df.dropna(axis=0)
        rows_end = len(clean_df)
        logger.debug(f"Dropped {rows_start - rows_end} rows with missing values.")
    elif axis == "columns":
        clean_df = df.dropna(axis=1)
        cols_end = len(clean_df.columns)
        logger.debug(f"Dropped {cols_start - cols_end} columns with missing values.")
    else:
        logger.error(f"Invalid axis specified: {axis}. Must be 'rows' or 'columns'.")
        raise ValueError("Invalid axis specified. Must be 'rows' or 'columns'.")
    return clean_df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method == "zscore" or method == "iqr":
        clean_df = df.copy()
        for col in columns:
            if col not in df.columns:
                logger.warning(f"Column '{col}' not found in DataFrame. Skipping outlier removal for this column.")
                continue
            if col not in df.select_dtypes(include=['number']).columns:
                logger.warning(f"Column '{col}' is not numeric. Skipping outlier removal for this column.")
                continue
            rows_start = len(clean_df)
            if method == "zscore":
                mean = clean_df[col].mean()
                std = clean_df[col].std()
                z_scores = (clean_df[col] - mean) / std
                clean_df = clean_df[abs(z_scores) <= threshold]
                rows_end = len(clean_df)
                logger.debug(f"Removed {rows_start - rows_end} outliers from column '{col}' using z-score method with threshold {threshold}.")
            elif method == "iqr":
                Q1 = clean_df[col].quantile(0.25)
                Q3 = clean_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                clean_df = clean_df[(clean_df[col] >= lower_bound) & (clean_df[col] <= upper_bound)]
                rows_end = len(clean_df)
                logger.debug(f"Removed {rows_start - rows_end} outliers from column '{col}' using IQR method with threshold {threshold}.")
    else:
        logger.error(f"Invalid method specified: {method}. Must be 'zscore' or 'iqr'.")
        raise ValueError("Invalid method specified. Must be 'zscore' or 'iqr'.")
    return clean_df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config.get("processing", {})
    if processing.get("remove_duplicates", False):
        df = remove_duplicates(df)
    if processing.get("missing", {}).get("enabled", False):
        axis = processing["missing"].get("axis", "rows")
        df = handle_missing(df, axis=axis)
    if processing.get("outliers", {}).get("enabled", False):
        columns = processing["outliers"].get("columns", [])
        method = processing["outliers"].get("method", "zscore")
        threshold = processing["outliers"].get("threshold", 3)
        df = remove_outliers(df, columns, method, threshold)
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    report = {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "rows_removed": len(df_before) - len(df_after),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }
    return report