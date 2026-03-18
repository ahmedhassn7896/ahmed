# Real-Time E-Commerce Data Pipeline

### 📌 Problem Statement
E-commerce platforms generate massive volumes of transaction data every second. Traditional batch processing introduces high latency, preventing business teams from reacting to sudden spikes in sales, inventory shortages, or fraudulent transactions in real-time. 

### 🏗 Architecture Overview
This project simulates a high-throughput e-commerce environment by generating transaction data and streaming it through a distributed, fault-tolerant pipeline. The architecture guarantees low-latency ingestion, scalable processing, and reliable storage for downstream analytical querying.

### 🔄 Data Flow
1. **Event Generation:** A Python-based mock producer continually generates JSON transaction payloads (simulating user purchases, clicks, and cart updates).
2. **Ingestion (Apache Kafka):** Events are ingested into designated Kafka topics, acting as a highly available message broker.
3. **Stream Processing (Apache Spark):** Spark Structured Streaming consumes the Kafka topics in real-time, applying transformations, standardizing timestamps, and filtering invalid records.
4. **Data Sink (PostgreSQL):** Processed and validated data is written to a relational PostgreSQL database.
5. **Orchestration (Apache Airflow):** Airflow orchestrates auxiliary batch jobs such as nightly data deduplication, historical data archiving, and data quality checks.

### 🛠 Technologies Used
* **Apache Kafka**, **Apache Spark**, **PostgreSQL**, **Apache Airflow**, **Docker & Docker Compose**

### ⚠️ Challenges & Solutions
* **Challenge:** Handling late-arriving data and duplicate streaming transactions.
  **Solution:** Implemented Spark watermarking to gracefully handle late data and introduced a deduplication layer in the Airflow nightly batch job using a unique transaction ID constraint.
* **Challenge:** Managing the complexity of setting up a distributed cluster locally.
  **Solution:** Architected a modular `docker-compose.yml` network.
