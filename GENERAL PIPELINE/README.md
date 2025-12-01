
# GENERAL PIPELINE
Pipeline to process ETL on databases extracted via URL or LOCAL FILES (raw → staging → curated).

✅ UNIVERSAL

pipeline can ingest:
 - CSV / Excel / JSON / XML / Parquet
 - SQLite / MySQL / PostgreSQL / SQL Server
 - MongoDB
 - APIs
 - Any messy or complex delimiter
 - Any nested JSON
 - Any dataset shape

✅ PRODUCTION-GRADE
✅ SAFE & ROBUST
✅ Well-logged
✅ QA-oriented
✅ Compatible with your new universal extractor
✅ Fully aligned with professional ETL architecture

Run:
1. python scripts/download.py 
2. python scripts/transform.py 
3. python scripts/qa.py --config 

# PIPELINE STRUCUCTURE
```
General_pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── staging/
│   └── curated/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── qa.py
│   └── utils.py
│
├── metadata/
│   └── metadata.json
│
├── logs/
│   └── pipeline.log
│
└── pipeline.py
```