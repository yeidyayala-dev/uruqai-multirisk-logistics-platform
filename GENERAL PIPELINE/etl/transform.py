# -*- coding: utf-8 -*-
"""transform.ipynb"""

import pandas as pd
from etl.utils import log


def transform_dataset(df):
    log("Initializing universal transformations...")

    # ============================================================
    # 1. Clean Column Names (snake_case)
    # ============================================================
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("-", "_")
                  .str.replace(".", "_")
    )

    # ============================================================
    # 2. Remove duplicate columns
    # ============================================================
    df = df.loc[:, ~df.columns.duplicated()]

    # ============================================================
    # 3. Identify & Convert Date Columns Automatically
    # ============================================================
    for col in df.columns:
        if any(keyword in col for keyword in ["date", "fecha", "time", "timestamp", "created"]):
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # ============================================================
    # 4. Convert Numeric Columns Where Possible
    # ============================================================
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="ignore")

    # ============================================================
    # 5. Normalize string columns (trim whitespace)
    # ============================================================
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # ============================================================
    # 6. Drop columns where ALL values are null
    # ============================================================
    df = df.dropna(axis=1, how="all")

    # ============================================================
    # 7. Remove fully duplicated rows
    # ============================================================
    df = df.drop_duplicates()

    log("Transformations completed.")
    return df
