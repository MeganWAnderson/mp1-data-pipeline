"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --config config.yaml --output clean.csv
    python pipeline.py --input data.csv --config config.yaml --output clean.csv --verbose
"""

import argparse
import logging
import sys

# Import Functions from Other Scripts 
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--config", "-c", required=True, help="Configuration file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, config={args.config}, verbose={args.verbose}"
    )

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as e:
        logger.error(f"Failed to load input or configuration: {e}")
        sys.exit(1)

    validation = config.get("validation", {})
    required_columns = validation.get("required_columns", [])
    numeric_columns = validation.get("numeric_columns", [])

    rows_before_validation = len(data)
    try:
        df_valid = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)
    logger.info(f"Validation complete: {rows_before_validation} --> {len(df_valid)} rows")

    try:
        df_after = process_data(df_valid, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    report = create_cleaning_report(df_valid, df_after)
    logger.info(f"Processing complete: {len(df_valid)} --> {len(df_after)} rows")

    output_path = save_data(df_after, args.output)
    logger.info(f"Saved cleaned data to {output_path}")
    print(f"Cleaning report: {report}")


if __name__ == "__main__":
    main()