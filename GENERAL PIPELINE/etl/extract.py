# -*- coding: utf-8 -*-
"""extract.ipynb"""

import os
import json
import hashlib
import requests
import csv
import pandas as pd
from datetime import datetime
from .utils import ensure_dir, load_config

# OPTIONAL IMPORTS (SAFE FALLBACKS)
try:
    import sqlite3
except:
    sqlite3 = None

try:
    import sqlalchemy
    from sqlalchemy import create_engine
except:
    sqlalchemy = None
    create_engine = None

try:
    from pymongo import MongoClient
except:
    MongoClient = None

try:
    import pyarrow.parquet as pq
except:
    pq = None

try:
    import xml.etree.ElementTree as ET
except:
    ET = None


# ====================================================
# CONFIG
# ====================================================
LOCAL_FILE = None
METADATA_FILE = "/GENERAL PIPELINE/metadata/metadata.json"
RESOURCE_URL = None


# ====================================================
# LOGGING
# ====================================================
def log(msg):
    print(f"[LOG {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


# ====================================================
# HASHING
# ====================================================
def file_hash(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()


# ====================================================
# INPUT DECISION
# ====================================================
def choose_input(source=None):
    global RESOURCE_URL, LOCAL_FILE

    if source is not None:
        if source.startswith("http"):
            RESOURCE_URL = source
        else:
            LOCAL_FILE = source
        return

    print("\nChoose dataset input option:")
    print("1) Use an existing LOCAL FILE")
    print("2) DOWNLOAD dataset using a URL")

    choice = input("Select 1 or 2: ")

    if choice == "1":
        LOCAL_FILE = input("Enter local file path: ").strip().strip('"').strip("'")
        log(f"Using local file: {LOCAL_FILE}")

    elif choice == "2":
        RESOURCE_URL = input("Enter dataset URL: ").strip()
        log(f"Using URL: {RESOURCE_URL}")

    else:
        log("Invalid choice → defaulting to config")


# ====================================================
# DOWNLOAD DATASET
# ====================================================
def download_dataset(url=None, output=None, save_metadata=True):
    global LOCAL_FILE

    config = load_config()
    default_raw = config["paths"]["raw"]

    if url is None:
        url = RESOURCE_URL
    if output is None:
        output = LOCAL_FILE or default_raw

    LOCAL_FILE = output

    log(f"Downloading dataset from: {url}")

    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        raise Exception(f"ERROR downloading file: HTTP {r.status_code}")

    ensure_dir(os.path.dirname(output))
    with open(output, "wb") as f:
        f.write(r.content)

    log(f"File saved → {output}")

    if save_metadata:
        md = {
            "source": url,
            "file": output,
            "download_date": datetime.now().isoformat(),
            "encoding": "latin-1",
            "size_bytes": os.path.getsize(output),
            "sha256": file_hash(output)
        }
        ensure_dir(os.path.dirname(METADATA_FILE))
        with open(METADATA_FILE, "w") as f:
            json.dump(md, f, indent=4)

    return output


# ====================================================
# LOAD DATASET (Local or URL)
# ====================================================
def load_dataset():
    if LOCAL_FILE and os.path.exists(LOCAL_FILE):
        log(f"Local file found: {LOCAL_FILE}")
        return LOCAL_FILE

    if RESOURCE_URL:
        log("Downloading from URL…")
        return download_dataset()

    raise FileNotFoundError("No local file and no URL provided.")


# ====================================================
# ====================================================
# UNIVERSAL DATA LOADER (FINAL VERSION)
# ====================================================
def load_any_format(file_path):
    """
    Universal, auto-detecting loader that converts any supported file 
    into a pandas DataFrame without requiring code changes.

    Supported:
    - CSV / TXT (auto delimiter & header detection)
    - Excel (xls / xlsx)
    - JSON
    - XML (attributes + child tags)
    - Parquet
    - SQLite / .db
    - SQL URLs
    - MongoDB URLs
    """

    ext = file_path.lower().split(".")[-1].strip()

    # -----------------------------------------------------
    # 1. XML
    # -----------------------------------------------------
    if ext == "xml":
        if ET is None:
            raise ImportError("XML support unavailable: xml.etree.ElementTree missing")

        tree = ET.parse(file_path)
        root = tree.getroot()

        rows = []

        for item in root:
            row = {}

            # extract XML attributes
            row.update(item.attrib)

            # extract <child> values
            for sub in item:
                row[sub.tag] = sub.text

            rows.append(row)

        log("[XML] Parsed successfully.")
        return pd.DataFrame(rows)

    # -----------------------------------------------------
    # 2. CSV / TXT (smart delimiter + smart header)
    # -----------------------------------------------------
    if ext in ["csv", "txt"]:

        # Read sample lines safely
        sample = []
        with open(file_path, "r", encoding="latin-1", errors="replace") as f:
            for _ in range(50):
                try:
                    sample.append(next(f).rstrip("\n"))
                except StopIteration:
                    break

        if not sample:
            raise ValueError("CSV/TXT file is empty or unreadable.")

        delimiters = [",", ";", "|", "\t"]
        delim_scores = {}

        # detect best delimiter
        for d in delimiters:
            counts = [line.count(d) for line in sample]
            delim_scores[d] = sum(counts) / len(sample)

        best_delim = max(delim_scores, key=delim_scores.get)

        # detect header line
        header_line = 0
        for i, line in enumerate(sample):
            parts = [p.strip() for p in line.split(best_delim)]

            if len(parts) < 2:
                continue

            # ignore very long values = likely data
            if any(len(p) > 60 for p in parts):
                continue

            # require alphabetic content
            if not any(any(c.isalpha() for c in p) for p in parts):
                continue

            numeric_like = sum(p.replace(".", "", 1).isdigit() for p in parts)
            if numeric_like > len(parts) * 0.5:
                continue

            header_line = i
            break

        log(f"[CSV] delimiter='{best_delim}' header_line={header_line}")

        return pd.read_csv(
            file_path,
            delimiter=best_delim,
            header=header_line,
            engine="python",
            encoding="latin-1",
            on_bad_lines="skip"
        )

    # -----------------------------------------------------
    # 3. Excel
    # -----------------------------------------------------
    if ext in ["xlsx", "xls"]:
        log("[Excel] Loaded successfully.")
        return pd.read_excel(file_path)

    # -----------------------------------------------------
    # 4. JSON
    # -----------------------------------------------------
    if ext == "json":
        log("[JSON] Loaded successfully.")
        data = json.load(open(file_path, "r", encoding="utf-8"))

        if isinstance(data, list):
            return pd.json_normalize(data)
        else:
            return pd.json_normalize([data])

    # -----------------------------------------------------
    # 5. Parquet
    # -----------------------------------------------------
    if ext == "parquet":
        if pq is None:
            raise ImportError("Parquet support unavailable: pyarrow missing")

        log("[Parquet] Loaded successfully.")
        table = pq.read_table(file_path)
        return table.to_pandas()

    # -----------------------------------------------------
    # 6. SQLite (.db)
    # -----------------------------------------------------
    if ext in ["sqlite", "db"]:
        if sqlite3 is None:
            raise ImportError("SQLite support unavailable.")

        log("[SQLite] Connecting to database...")
        conn = sqlite3.connect(file_path)
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        table_name = tables["name"][0]
        return pd.read_sql(f"SELECT * FROM {table_name}", conn)

    # -----------------------------------------------------
    # 7. SQL URLs
    # -----------------------------------------------------
    if file_path.startswith(("postgresql://", "mysql://", "mssql://", "sqlite://")):
        if sqlalchemy is None:
            raise ImportError("SQLAlchemy required to load database URLs.")

        log("[SQL] Connecting via SQLAlchemy...")
        engine = create_engine(file_path)
        tables = engine.table_names()
        return pd.read_sql(f"SELECT * FROM {tables[0]}", engine)

    # -----------------------------------------------------
    # 8. MongoDB
    # -----------------------------------------------------
    if file_path.startswith("mongodb://"):
        if MongoClient is None:
            raise ImportError("pymongo required for MongoDB support.")

        log("[MongoDB] Connecting...")
        client = MongoClient(file_path)
        db = client.get_default_database()
        coll = db.list_collection_names()[0]
        docs = list(db[coll].find({}, {"_id": 0}))
        return pd.json_normalize(docs)

    # -----------------------------------------------------
    # UNSUPPORTED FORMAT
    # -----------------------------------------------------
    raise ValueError(f"Unsupported or unknown file type for: {file_path}")


# ====================================================
# MAIN EXTRACT FUNCTION
# ====================================================
def extract_dataset(source=None):

    choose_input(source)
    file_path = load_dataset()

    log("Loading dataset using universal loader…")

    df = load_any_format(file_path)

    log("Dataset loaded successfully.")

    metadata = {
        "source": RESOURCE_URL if RESOURCE_URL else "Local File",
        "file": file_path,
        "sha256": file_hash(file_path),
        "load_date": datetime.now().isoformat()
    }

    return df, metadata

