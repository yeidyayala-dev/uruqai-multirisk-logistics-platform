
## 📄INGESTION MEMO 

Project: UruQAI 
Process: Data Preprocessing 
Environment: Python Package (Run Python 3.x environment)

## 🏗 1. Ingestion Strategy

The ingestion strategy follows a modular ETL approach:

✔ **Extract**

- Primary: download from official URL
- Fallback: use local file if previously downloaded
- Metadata captured:
      -  SHA-256 hash
      -  Download date
      -  File size
      -  Source & license

**IMPORTANT NOTES**: 

- The URL used in this case, takes the link that directly downloads the file. This means the link attached to the “DOWNLOAD”    Button on the page (see image below) It can be changed manually for another database from the same resource as needed. 

- If there is no URL containing any dataset, a LOCAL FILE may be used



✔ **Transform**

- Column cleaning and normalization
- Typing: dates, numerics, strings
- Validations:
- Numeric ranges (affected area, temperature, etc.)
- Null values
- Geographic consistency (states/municipalities)

✔ **Load**

- Output stored in curated/ zone, optimized for analytics
- Standardized column names
- Recommended final format: Parquet (compressed, columnar)


## 🔒 3. Quality Controls (QA)

| Control             | Purpose                    | Action                                            |
| ------------------- | -------------------------- | ------------------------------------------------- |
| Hash & Metadata     | Verify data integrity      | Store hash in `metadata/`                         |
| Schema Check        | Validate expected columns  | Fail pipeline if critical columns missing         |
| Null Threshold      | Detect data quality issues | Alert if >10% missing in critical fields          |
| Statistical Ranges  | Catch outliers/errors      | Compare against environmental limits              |
| Duplicate Check     | Avoid duplicate events     | Remove duplicates by ID + date + state            |
| Geospatial Validity | Validate location          | Cross-check against INEGI state/municipal catalog |


## 📦 4. File Storage Architecture
```
wildfires_pipeline/
|
├── data/
|   ├── raw/    ← Original downloaded CSV
|   ├── staging/ ← Preliminary transformations
|   └── curated/  ← Cleaned, optimized dataset
|
├── metadata/  ← Source, hash, size, timestamps
├── logs/      ← Execution logs and errors
└── config/    ← YAML configuration
```

## Other running environments 

- Google Colab
- Jupyter Notebooks
- PyCharm
- Anaconda (anaconda3)
- Command Line
- GitHub Codespaces
- Google Cloud Vertex Notebooks
- VS (Visual Studio) -----> Interpreter:  Python 3.11.5 anaconda3/python.exe
                                          Python anaconda3/envs/BigData1/python.exe