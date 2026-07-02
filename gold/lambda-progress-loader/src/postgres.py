from __future__ import annotations

import os
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine


DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def upload_to_postgres(datasets: Dict[str, pd.DataFrame]) -> None:
    """
    Upload every Gold dataframe into PostgreSQL.
    Table name = dictionary key.
    """

    engine = create_engine(DATABASE_URL)

    for table_name, df in datasets.items():

        if df.empty:
            print(f"Skipping {table_name} (empty)")
            continue

        print(f"Uploading {table_name} ({len(df)} rows)...")

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1000,
        )

    engine.dispose()

    print("Finished uploading all datasets.")