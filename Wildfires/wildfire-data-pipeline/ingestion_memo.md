
## 📄INGESTION MEMO – Wildfire Data Pipeline

Project: Wildfire Analytics & Risk Insights
Dataset: Forest Fires 2015–2024 (Mexico)
Version: 1.0


## 🔍 1. Dataset Overview

| Aspect              | Detail                                                  |
| ------------------- | ------------------------------------------------------- |
| Source              | National Forestry Commission (CONAFOR)                  |
| Platform            | Datos Abiertos México                                   |
| Dataset URL         | `https://www.datos.gob.mx/dataset/incendios_forestales` |
| Data Type           | Tabular CSV (event-level)                               |
| Temporal Coverage   | 2015–2024                                               |
| Geographic Coverage | Mexico (state and municipal level)                      |
| Update Frequency    | Not specified – depends on CONAFOR                      |
| Language            | Spanish                                                 |
| License             | Public / Open Government Data                           |

The dataset contains statistics on forest fires, including causes, affected area, location, and vegetation type. It is critical for risk analysis, prevention, ecological impact assessment, and predictive modeling.


## 🏗 2. Ingestion Strategy

The ingestion strategy follows a modular ETL approach:

✔ **Extract**

- Primary: download from official URL
- Fallback: use local file if previously downloaded
- Metadata captured:
      -  SHA-256 hash
      -  Download date
      -  File size
      -  Source & license

**IMPORTANT NOTE**: The URL used in this case, takes the link that directly downloads the file. This means the link attached to the “DOWNLOAD” Button on the page (see image below) It can be changed manually for another database from the same resource as needed. 
https://www.datos.gob.mx/dataset/incendios_forestales/resource/ddf38874-6243-4437-8f76-19f797cafa5c 

<img width="975" height="510" alt="image" src="https://github.com/user-attachments/assets/5513e108-0131-4f16-acec-f3a39265d39d" />

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


## ⚠️ 5. Risks & Mitigation

| Risk                        | Impact           | Mitigation                                   |
| --------------------------- | ---------------- | -------------------------------------------- |
| URL change                  | Pipeline failure | Use local fallback + alert                   |
| Outdated dataset            | Model accuracy   | Quarterly manual monitoring                  |
| Outliers / anomalous values | Bias in models   | Apply statistical/environmental rules        |
| Geographic inconsistencies  | Analysis errors  | Validate against INEGI catalog               |
| Unclear license             | Legal risk       | Maintain source attribution and public usage |


## 🔮 6. Next Dataset Candidates

| Source   | Dataset                  | Use                            |
| -------- | ------------------------ | ------------------------------ |
| CONABIO  | Vegetation types         | Terrain vulnerability analysis |
| SEMARNAT | Emissions from fires     | Environmental impact           |
| SMN      | Meteorological variables | Risk prediction                |
| INEGI    | Municipal boundaries     | Geospatial validation          |


## 🎯 7. Value Proposition

This pipeline enables:

- Historical and regional analysis of forest fires
- Predictive risk modeling
- Assessment of forest damage by vegetation type
- Resource prioritization for emergency response
- Integration with climate and emissions data
