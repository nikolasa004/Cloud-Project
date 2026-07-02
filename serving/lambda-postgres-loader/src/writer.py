from __future__ import annotations

import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_tables(engine: Engine) -> None:
    """
    Creates all analytical tables used by the serving layer.
    Safe to execute multiple times.
    """

    statements = [
        """
        CREATE TABLE IF NOT EXISTS daily_activity_metric (
            date DATE NOT NULL,
            platform VARCHAR(50) NOT NULL,
            post_type VARCHAR(50) NOT NULL,
            total_count INTEGER NOT NULL,
            PRIMARY KEY (date, platform, post_type)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS daily_users_metric (
            date DATE NOT NULL,
            platform VARCHAR(50) NOT NULL,
            total_users INTEGER NOT NULL,
            new_users INTEGER NOT NULL,
            PRIMARY KEY (date, platform)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS top_authors_metric (
            date DATE NOT NULL,
            platform VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            rank INTEGER NOT NULL,
            username TEXT,
            score INTEGER NOT NULL,
            PRIMARY KEY (date, platform, category, rank)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS top_posts_metric (
            date DATE NOT NULL,
            platform VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            rank INTEGER NOT NULL,
            post_id TEXT,
            author_username TEXT,
            title TEXT,
            score INTEGER NOT NULL,
            PRIMARY KEY (date, platform, category, rank)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS data_quality_metric (
            date DATE NOT NULL,
            platform VARCHAR(50) NOT NULL,
            dataset VARCHAR(50) NOT NULL,
            quality_score_percent DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (date, platform, dataset)
        );
        """
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    logger.info("Analytical tables verified successfully.")


def _replace_rows(
    engine: Engine,
    table_name: str,
    df: pd.DataFrame,
    key_columns: list[str]
) -> None:
    """
    Replaces existing metric rows for the same logical partition
    (date/platform/category...) and inserts fresh data.
    """

    if df.empty:
        logger.info("Skipping %s because dataframe is empty.", table_name)
        return

    with engine.begin() as connection:

        for row in df[key_columns].drop_duplicates().to_dict("records"):

            where_clause = " AND ".join(
                f"{column} = :{column}"
                for column in key_columns
            )

            connection.execute(
                text(
                    f"""
                    DELETE FROM {table_name}
                    WHERE {where_clause}
                    """
                ),
                row,
            )

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info(
        "Loaded %d rows into %s.",
        len(df),
        table_name,
    )


def write_daily_activity(
    df: pd.DataFrame,
    engine: Engine,
) -> None:

    _replace_rows(
        engine,
        "daily_activity_metric",
        df,
        ["date", "platform"],
    )


def write_daily_users(
    df: pd.DataFrame,
    engine: Engine,
) -> None:

    _replace_rows(
        engine,
        "daily_users_metric",
        df,
        ["date", "platform"],
    )


def write_top_authors(
    df: pd.DataFrame,
    engine: Engine,
) -> None:

    _replace_rows(
        engine,
        "top_authors_metric",
        df,
        ["date", "platform", "category"],
    )


def write_top_posts(
    df: pd.DataFrame,
    engine: Engine,
) -> None:

    _replace_rows(
        engine,
        "top_posts_metric",
        df,
        ["date", "platform", "category"],
    )


def write_data_quality(
    df: pd.DataFrame,
    engine: Engine,
) -> None:

    _replace_rows(
        engine,
        "data_quality_metric",
        df,
        ["date", "platform", "dataset"],
    )