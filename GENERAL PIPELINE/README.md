
# GENERAL PIPELINE
Pipeline to process ETL on databases extracted via URL or LOCAL FILES (raw → staging → curated).

# MAIN FEATURES 
```
✅ SAFE & ROBUST
✅ Well-logged
✅ QA-oriented
✅ Compatible with universal extractor
✅ Fully aligned with professional ETL architecture
```
# OTHER FEATURES
```
✔ Error handling with graceful failure
✔ Summary of extract/transform/load steps
✔ Column + row validation
✔ Metadata enriched with:
                - row count
                - column count
                - dtypes
                - pipeline runtime
                - QA summary
                - file hash
                - stage & curated file paths

✔ Fully compatible with your universal extract, transform, load modules
```
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
## Other running environments 

- Google Colab
- Jupyter Notebooks
- PyCharm
- Anaconda (anaconda3)
- Command Line
- GitHub Codespaces
- Google Cloud Vertex Notebooks
- VS (Visual Studio) -----> Interpreter:  
                                          - Python 3.11.5 anaconda3/python.exe
                                          - Python anaconda3/envs/BigData1/python.exe