# MP1 Data Pipeline

This project builds an end-to-end command-line data pipeline that loads, validates, cleans, and saves data. It is able to load CSV files and YAML configuration files. The pipeline validates required columns and numeric values, and removes duplicates, missing values, and outliers according to the configuration file.

The pipeline is organized as follows: 
1. The `pipeline.py` module directs the end-to-end workflow and handles all error exits
2. `src/data_loaders.py` handles loading supported file formats 
3. `src/data_validator.py` checks the data before processing 
4. `src/data_processor.py` performs configured cleaning operations and generates cleaning report
5. `src/data_output.py` saves the cleaned DataFrame as a CSV file
6. `src/utils.py` module provides input-file validation and logging utilities
7. `config/config.yaml` defines the validation and processing settings such as outlier method and threshold
8. The `fixtures/` directory includes all sample datasets for testing 
9. Generated output files are saved to `output/`

Data moves through the pipeline in four stages: it is loaded from the input CSV and the YAML config, validated against the required and numeric columns, cleaned by removing duplicates, missing values, and outliers, and then saved as a CSV in `output/`.

## Run it

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Output
```text
15:38:41 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml, verbose=True
15:38:41 INFO     src.utils — Input file validated: fixtures/sample_data.csv
15:38:41 INFO     src.utils — Input file validated: config/config.yaml
15:38:41 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
15:38:41 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
15:38:41 WARNING  src.data_validator — Removed 2 rows with invalid numeric values from column 'rating'
15:38:41 DEBUG    src.data_validator — Validation: 100 --> 98 rows
15:38:41 INFO     __main__ — Validation complete: 100 --> 98 rows
15:38:41 DEBUG    src.data_processor — Removed 2 duplicate rows.
15:38:41 DEBUG    src.data_processor — Dropped 2 rows with missing values.
15:38:41 DEBUG    src.data_processor — Removed 2 outliers from column 'rating' using IQR method with threshold 1.5.
15:38:41 INFO     __main__ — Processing complete: 98 --> 92 rows
15:38:41 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
15:38:41 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report: {'rows_before': 98, 'rows_after': 92, 'columns_before': 5, 'columns_after': 5, 'rows_removed': 6,'columns_removed': 0}
```