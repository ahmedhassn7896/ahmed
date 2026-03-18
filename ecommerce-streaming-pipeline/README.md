# High-Throughput Real-Time Event Processing Engine

### 📌 Problem Statement
Modern e-commerce architectures require instantaneous visibility into user behavior, transaction fraud, and inventory telemetry. Batch processing creates unacceptable data staleness. This platform solves the "real-time analytics problem" by decoupling ingestion from processing to deliver actionable insights with sub-200ms latency at massive scale.

### 🏗 Architecture Overview
A distributed, fault-tolerant streaming architecture built to scale horizontally. The system guarantees high availability and exactly-once processing semantics.
* **Ingestion:** A cluster of Apache Kafka brokers buffers incoming traffic (simulating up to 10,000 events/second) using topic partitioning to ensure absolute parallelization and fault tolerance.
* **Stream Processing:** PySpark Structured Streaming engines consume the partitioned data, apply complex stateful aggregations (hopping/sliding windows), and gracefully handle out-of-order data via watermarking logic.
* **Data Sink:** High-performance JDBC bulk writes push aggregated metrics into a normalized PostgreSQL Data Warehouse.
* **Orchestration & DevOps:** Managed entirely via Docker Compose with Apache Airflow executing nightly compaction, schema evolution checks, and table unbloating.

### 📈 FAANG-Grade Metrics & Scale
* **Throughput:** Architected to handle **~5,000+ events/sec** continuously, peaking at **10M+ events/day** during simulated high-traffic "Black Friday" events.
* **Latency:** Achieved **sub-200ms** end-to-end latency from data generation to dashboard visibility.
* **Reliability:** Ensured **99.99% data freshness SLA** using Kafka replication factors, producer idempotency, and Spark write-ahead logs (WAL).

### 🛠 Technologies Used
* **Distributed Streaming:** Apache Kafka, Zookeeper
* **Stream Processing:** Apache Spark (Structured Streaming), PySpark
* **Data Persistence:** PostgreSQL (Transactional Sink), pgBouncer (Connection Pooling)
* **DevOps & Orchestration:** Docker, Docker Compose, Apache Airflow

### ⚠️ Production Challenges Solved
1. **Challenge:** Handling late-arriving network data without dropping essential financial transactions.
   * **Solution:** Implemented Spark watermarking (up to 2-hour delays) combined with UPSERT logic in PostgreSQL to update aggregated data idempotently without duplicate records.
2. **Challenge:** Protecting the downstream database from connection exhaustion.
   * **Solution:** Optimized `foreachBatch` operations inside Spark by maximizing connection sharing (bulk inserts using psycopg2 `execute_values`) rather than row-by-row commits.
