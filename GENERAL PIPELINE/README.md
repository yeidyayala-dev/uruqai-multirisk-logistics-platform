# Wildfire Data Pipeline

End‑to‑end pipeline (raw → staging → curated).

# Wildfires pipeline
Pipeline to process data for Wildfires from CONAFOR (raw → staging → curated).

Run:
1. python scripts/download.py --config Wildfires/config.yaml
2. python scripts/transform.py --config Wildfires/config.yaml
3. python scripts/qa.py --config Wildfires/config.yaml

# PIPELINE STRUCUCTURE

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