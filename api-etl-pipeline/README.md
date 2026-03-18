# API Data Ingestion & ETL Workflow

### 📌 Problem Statement
Modern businesses often rely on disconnected third-party services. Extracting this data manually is error-prone and time-consuming. This project aims to centralize diverse REST API data into a single source of truth for reliable downstream analytics.

### 🏗 Architecture Overview
This project relies on a deeply automated, schedule-driven ETL architecture. It securely authenticates with multiple external APIs, paginates through large datasets, applies complex Python-based transformation logic, and reliably loads the clean data into a central data warehouse.

### 🔄 Data Flow
1. **Extraction:** Python scripts running on a schedule authenticate and pull JSON data from various external REST APIs handling dynamic pagination.
2. **Transformation:** Using `pandas`, the raw JSON is flattened. Null values are handled gracefully, data types are casted, and business logic is applied.
3. **Validation:** Pre-load validation functions check for data anomalies.
4. **Loading:** The pristine data is upserted into a PostgreSQL database.
5. **Orchestration:** Apache Airflow acts as the brain of the operation, scheduling the pipeline to run daily and handling retries.

### 🛠 Technologies Used
* **Python (Pandas, Requests)**, **Apache Airflow**, **PostgreSQL**, **Docker**

### ⚠️ Challenges & Solutions
* **Challenge:** REST API rate limits causing pipeline failures.
  **Solution:** Implemented exponential backoff and localized caching using Python decorators.
* **Challenge:** Evolving JSON structures from third-party APIs.
  **Solution:** Built dynamic flattening algorithms and rigorous data schema validation steps to quarantine bad data into a "dead letter" table.
