import argparse
import logging

from retail_lakehouse.config.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="retail-lakehouse",
        description="Retail Lakehouse CLI",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "generate-data", help="Generate synthetic retail source datasets"
    )
    subparsers.add_parser(
        "show-config", help="Display current application configuration"
    )
    subparsers.add_parser(
        "build-model",
        help="Build the initial retail dimensional model",
    )

    args = parser.parse_args()

    configure_logging()

    if args.command == "generate-data":
        from retail_lakehouse.ingestion.generate_data import generate_dataset

        generate_dataset()
    elif args.command == "show-config":
        from retail_lakehouse.config.check_config import check_config

        check_config()
    elif args.command == "build-model":
        from retail_lakehouse.modeling.pipeline import run_pipeline

        run_pipeline()
