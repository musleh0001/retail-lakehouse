import logging

from pyspark.sql import SparkSession

from retail_lakehouse.config.settings import settings

logger = logging.getLogger(__name__)


def create_spark_session() -> SparkSession:
    """
    Create or retrieve the application SparkSession.
    """

    logger.info("Initializing Spark session")

    spark = (
        SparkSession.builder.appName(settings.spark_app_name)
        .master(settings.spark_master)
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    logger.info(
        "Spark session initialized: %s",
        spark.version,
    )

    return spark
