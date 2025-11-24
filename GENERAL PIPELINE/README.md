
# GENERAL PIPELINE
Pipeline to process ETL on databases extracted via URL or LOCAL FILES (raw → staging → curated).

Run:
1. python scripts/download.py 
2. python scripts/transform.py 
3. python scripts/qa.py --config 

# PIPELINE STRUCUCTURE
```
wildfires_pipeline/
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