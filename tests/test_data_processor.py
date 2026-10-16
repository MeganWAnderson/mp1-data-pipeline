#tests/test_data_processor.py

import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers
from tests.conftest import sample_df
from tests.test_data_validator import test_validate_dataframe_with_missing_column
from tests.test_data_validator import test_validate_dataframe_with_missing_column


def test_remove_duplicates(sample_df):
    # TODO: Call remove_duplicates() on sample_df.
    removed_df = remove_duplicates(sample_df)
    # TODO: Assert that 98 rows remain.
    assert len(removed_df) == 98


def test_handle_missing_rows(sample_df):
    # Arrange: use the existing rating column.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    # note: errors="coerce" converts invalid numeric strings to missing values.

    # TODO: Call handle_missing() with axis="rows".
    handled_df = handle_missing(df, axis="rows")
    # TODO: Assert that 97 rows remain.
    assert len(handled_df) == 97


def test_remove_outliers_iqr(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.
    
    # TODO: Call remove_outliers() for ["rating"], using method="iqr", and threshold=1.5.
    removed_df = remove_outliers(df, ["rating"], method="iqr", threshold=1.5)
    # TODO: Assert that 95 rows remain.
    assert len(removed_df) == 95

# TODO: Use test_remove_outliers_iqr() as a reference to write test_remove_outliers_zscore(). Use the same numeric rating data without missing values, but set method="zscore" and threshold=3. Check the expected result for zscore and update your assertions accordingly.
def test_remove_outliers_zscore(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    # Call remove_outliers() using z-score.
    removed_df = remove_outliers(
        df, ["rating"], method="zscore", threshold=3
    )

    # Assert the expected number of remaining rows.
    assert len(removed_df) == 95

# TODO: Use test_validate_dataframe_with_missing_column() as a reference to write test_remove_outliers_with_unsupported_method(). Use pytest.raises(ValueError) to confirm that remove_outliers() raises an error when called with method="unknown".
def test_remove_outliers_with_unsupported_method(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    # Assert that an unsupported method raises a ValueError.
    with pytest.raises(ValueError):
        remove_outliers(
            df, ["rating"], method="unknown", threshold=3)