# -*- coding: utf-8 -*-
"""pipeline.ipynb"""

import os
import time
from pathlib import Path
import json
import pandas as pd

from etl.utils import load_config, ensure_dir, log
from etl.extract import extract_dataset
from etl.transform import transform_dataset
from etl.load import load_to_staging, load_to_curated
from etl.qa import qa_checks


def run_pipeline():

    start_time = time.time()

    log("==============================================")
    log("        UNIVERSAL ETL PIPELINE STARTED        ")
    log("==============================================")

    # ========================================================
    # 1. Load Config
    # ========================================================
    config = load_config()
    log("Config loaded successfully.")

    # Ensure directories exist
    ensure_dir(config["paths"]["staging"])
    ensure_dir(config["paths"]["curated"])
    ensure_dir(Path(config["paths"]["metadata"]).parent)

    # ========================================================
    # 2. EXTRACT
    # ========================================================
    log("STEP 1: Extracting dataset...")
    df, metadata = extract_dataset()
    log(f"Extraction complete. Rows: {len(df)}, Columns: {len(df.columns)}")

    # Basic DF type validation
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Extraction did not return a pandas DataFrame.")

    # ========================================================
    # 3. QA ON RAW DATA
    # ========================================================
    log("STEP 2: Running QA checks on raw data...")
    qa_raw = qa_checks(df)
    log("QA (raw) completed.")

    # ========================================================
    # 4. TRANSFORM
    # ========================================================
    log("STEP 3: Applying transformations...")
    df_t = transform_dataset(df)
    log(f"Transform complete. Rows: {len(df_t)}, Columns: {len(df_t.columns)}")

    # ========================================================
    # 5. QA ON TRANSFORMED DATA
    # ========================================================
    log("STEP 4: Running QA checks on transformed data...")
    qa_transformed = qa_checks(df_t)
    log("QA (transformed) completed.")

    # ========================================================
    # 6. LOAD TO STAGING
    # ========================================================
    log("STEP 5: Loading to STAGING...")
    staging_path = load_to_staging(df_t, config)

    # ========================================================
    # 7. LOAD TO CURATED
    # ========================================================
    log("STEP 6: Loading to CURATED...")
    curated_path = load_to_curated(df_t, config)

    # ========================================================
    # 8. METADATA ENRICHMENT
    # ========================================================
    log("STEP 7: Saving metadata...")

    metadata.update({
        "rows_raw": len(df),
        "columns_raw": len(df.columns),
        "rows_transformed": len(df_t),
        "columns_transformed": len(df_t.columns),
        "dtypes": df_t.dtypes.astype(str).to_dict(),
        "qa_raw": qa_raw,
        "qa_transformed": qa_transformed,
        "staging_output": staging_path,
        "curated_output": curated_path,
        "pipeline_runtime_seconds": round(time.time() - start_time, 2)
    })

    # Write metadata file
    with open(config["paths"]["metadata"], "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    # ========================================================
    # Finished
    # ========================================================
    log("==============================================")
    log("       UNIVERSAL ETL PIPELINE COMPLETED       ")
    log("==============================================")

    return df_t, metadata


if __name__ == "__main__":
    run_pipeline()
