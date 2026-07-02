from __future__ import annotations

import logging
import os

from db import get_engine, test_connection
from reader import (
    read_daily_activity,
    read_daily_users,
    read_top_authors,
    read_top_posts,
    read_data_quality,
)
from writer import (
    create_tables,
    write_daily_activity,
    write_daily_users,
    write_top_authors,
    write_top_posts,
    write_data_quality,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Loads Gold-layer analytical datasets from S3 into PostgreSQL.
    """

    bucket_name = os.environ["DATA_LAKE_BUCKET"]

    logger.info("Starting PostgreSQL serving loader.")

    engine = get_engine()

    if not test_connection(engine):
        logger.error("Unable to connect to PostgreSQL.")
        raise RuntimeError("Database connection failed.")

    logger.info("Successfully connected to PostgreSQL.")

    create_tables(engine)

    logger.info("Loading daily_activity_metric...")
    write_daily_activity(
        read_daily_activity(bucket_name),
        engine,
    )

    logger.info("Loading daily_users_metric...")
    write_daily_users(
        read_daily_users(bucket_name),
        engine,
    )

    logger.info("Loading top_authors_metric...")
    write_top_authors(
        read_top_authors(bucket_name),
        engine,
    )

    logger.info("Loading top_posts_metric...")
    write_top_posts(
        read_top_posts(bucket_name),
        engine,
    )

    logger.info("Loading data_quality_metric...")
    write_data_quality(
        read_data_quality(bucket_name),
        engine,
    )

    logger.info("Serving layer successfully synchronized.")

    return {
        "statusCode": 200,
        "body": {
            "message": "Serving layer loaded successfully."
        },
    }