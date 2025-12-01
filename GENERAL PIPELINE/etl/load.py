# -*- coding: utf-8 -*-
"""load.ipynb"""

import os
import pandas as pd
from etl.utils import log, ensure_dir


def load_to_staging(df, config):
    staging_dir = config["paths"]["staging"]
    ensure_dir(staging_dir)

    path = os.path.join(staging_dir, "staging_clean.csv")

    df.to_csv(path, index=False, encoding="utf-8")

    log(f"[STAGING] Saved → {path}")
    log(f"[STAGING] Rows: {len(df)}, Columns: {len(df.columns)}")

    return path


def load_to_curated(df, config):
    curated_dir = config["paths"]["curated"]
    ensure_dir(curated_dir)

    path = os.path.join(curated_dir, "curated_final.csv")

    df.to_csv(path, index=False, encoding="utf-8")

    log(f"[CURATED] Saved → {path}")
    log(f"[CURATED] Rows: {len(df)}, Columns: {len(df.columns)}")

    return path
