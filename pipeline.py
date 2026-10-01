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
from pathlib import Path

# Import Functions from Other Scripts 
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    # use logging.DEBUG when verbose is True 
    # use logging.INFO when verbose is False 
    # include time, log level, and messagge in each log entry
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--config", "-c", required=True, help="Configuration file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    path = Path(filepath)
    if not path.exists():
        logger.error(f"Input file does not exist: {filepath}")
        return False
    if not path.is_file():
        logger.error(f"Input path is not a file: {filepath}")
        return False
    logger.info(f"Input file validated: {filepath}")
    return True 


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

    df_before = data.copy()
    try:
        df_after = process_data(data, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    report = create_cleaning_report(df_before, df_after)
    print(f"Cleaning report: {report}")
    logger.info(f"Processing complete: {len(df_before)} --> {len(df_after)} rows")

    df_after.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")



if __name__ == "__main__":
    main()