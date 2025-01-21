
## Table of contents

- [Data Warehouse and BigQuery](#Data-Warehouse)

- [Partitioning vs Clustering](#Partitioning-vs-Clustering)

- [BigQuery-Best Practice](#BigQuery-Best-Practice)

- [Internals of BigQuery](#Internals-of-BigQuery)

# Data Warehouse

**OLAP vs OLTP**

OLAP (Online Analytical Processing) and OLTP (Online Transaction Processing)
  
| | OLTP| OLAP| 
|---|---|---|
| Purpose| Control and run essential business operations in real time| Plan, solve problems, support decisions, discover hidden insights| 
| Data updates| Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs| 
| Database design| Normalized databases for efficiency| Denormalized databases for analysis| 
| Space requirements| Generally small if historical data is archived| Generally large due to aggregating large datasets| 
| Backup and recovery |  Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups| 
| Productivity | Increases productivity of end users | Increases productivity of business managers, data analysts, and executives| 
| Data view | Lists day-to-day business transactions | Multi-dimensional view of enterprise data| 
| User examples | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts, and executives| 

### What is data warehouse

OLAP solution
Used for reporting and data analysis
![image](https://github.com/user-attachments/assets/ee9fc3a7-8e04-419e-b4f2-82c8f71632a0)

## BigQuery

* Serverless data warehouse
  * There are no servers to manage or database software to install
* Software as well as infrastructure including
  * scalability and high-availability
* Built-in features like 
  * machine learning
  * geospatial analysis
  * business intelligence
* BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage

### BigQuery Cost

* On demand pricing
  * 1 TB of data processed is $5
* Flat rate pricing
  * Based on number of pre requested slots. 
  * 100 slots → $2,000/month = 400 TB data processed on demand pricing

### Use BigQuery to load data from buket
```sql
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `zoompcamp2025.zoomcamp1.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://your-name-kestra/yellow_tripdata_2019-*.csv', 
          'gs://your-name-kestra/trip data/yellow_tripdata_2020-*.csv']
);

```

External table's size and role can not be determined in BigQuery cause the data itself is not inside BigQuery

# Partitioning vs Clustering

### Partition in BQ

Partitioning in BigQuery is a technique used to improve query performance and reduce query costs by dividing a table into smaller segments (partitions) based on a column’s values.

![image](https://github.com/user-attachments/assets/7eeae184-7770-48ac-b2f2-f41398c1fc39)

```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE zoompcamp2025.zoomcamp1.yellow_tripdata_non_partitoned AS
SELECT * FROM zoompcamp2025.zoomcamp1.external_yellow_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE `zoompcamp2025.zoomcamp1.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_pickup_datetime)
AS
SELECT * FROM `zoompcamp2025.zoomcamp1.external_yellow_tripdata`;
```

Data would be copy from google cloud storage to bigquery storage.

**Impact of partition**

```sql
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_non_partitoned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

```

Filtering by Timestamp Without Using DATE() might cause

BigQuery may scan all partitions (even those not containing the relevant date).

Higher costs and slower performance because it evaluates the condition for all rows, not just the required partition.
```sql
-- 10.72GB
SELECT * FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_non_partitoned`
WHERE tpep_pickup_datetime BETWEEN '2019-01-01 08:00:00' AND '2019-01-01 10:00:00';

-- 23.26MB
SELECT * FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_partitioned`
WHERE tpep_pickup_datetime BETWEEN '2019-01-01 08:00:00' AND '2019-01-01 10:00:00';

-- 23.26MB
SELECT * FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) = '2019-01-01'
  AND tpep_pickup_datetime BETWEEN '2019-01-01 08:00:00' AND '2019-01-01 10:00:00';
```

**Look into the partitons**

We can acyurlt see how many rows are falling into which partion
```sql
SELECT DISTINCT(VendorID)
FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_non_partitoned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```



### Clustering in BigQuery

Improve cost and query performance

![image](https://github.com/user-attachments/assets/e4a87edc-1740-479f-a080-9d699171277b)
```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE zoompcamp2025.zoomcamp1.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM zoompcamp2025.zoomcamp1.external_yellow_tripdata;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM zoompcamp2025.zoomcamp1.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM zoompcamp2025.zoomcamp1.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```

### Partitioning vs Clustering

**BigQuery partition**

* Time-unit column
* Ingestion time (_PARTITIONTIME)
* Integer range partitioning
* When using Time unit or ingestion time
  * Daily (Default)
  * Hourly
  * Monthly or yearly
* Number of partitions limit is 4000

Resource: https://cloud.google.com/bigquery/docs/partitioned-tables

**BigQuery Clustering**

* Columns you specify are used to colocate related data
* Order of the column is important
* The order of the specified columns determines the sort order of the data. 
* Clustering improves
  * Filter queries
  * Aggregate queries
* Table with data size < 1 GB, don’t show significant improvement with partitioning and clustering
* You can specify up to four clustering columns
* Clustering columns must be top-level, non-repeated columns

| Clustering | Partitoning | 
|---|---|
 | Cost benefit unknown | Cost known upfront | 
 | You need more granularity than partitioning alone allows | You need partition-level management. | 
 | Your queries commonly use filters or aggregation against multiple particular columns | Filter or aggregate on single column | 
 | The cardinality of the number of values in a column or group of columns is large | 


**Clustering over paritioning**

* Partitioning results in a small amount of data per partition (approximately less than 1 GB)
* Partitioning results in a large number of partitions beyond the limits on partitioned tables
* Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (for example, every few minutes)

### Automatic reclustering

As data is added to a clustered table

* the newly inserted data can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks
* These overlapping keys weaken the sort property of the table

To maintain the performance characteristics of a clustered table
* BigQuery performs automatic re-clustering in the background to restore the sort property of the table
* For partitioned tables, clustering is maintained for data within the scope of each partition.


# BigQuery-Best Practice

**Cost reduction**
  
Avoid SELECT *

Price your queries before running them

Use clustered or partitioned tables

Use streaming inserts with caution

Materialize query results in stages

**Query performance**

Filter on partitioned columns

Denormalizing data

Use nested or repeated columns

Use external data sources appropriately

Don't use it, in case u want a high query performance

Reduce data before using a JOIN

Do not treat WITH clauses as prepared statements

Avoid oversharding tables

Avoid JavaScript user-defined functions

Use approximate aggregation functions (HyperLogLog++)

Order Last, for query operations to maximize performance

Optimize your join patterns
  
-- As a best practice, place the table with the largest number of rows first, followed by the table with the fewest rows, and then place the remaining tables by decreasing size.


# Internals of BigQuery

BigQuery decouples compute (query execution) from storage (data persistence). This design ensures scalability, cost efficiency, and high performance.

### Storage Layer (Colossus)
* BigQuery stores data in Colossus, Google’s distributed storage system.
* Columnar storage format: Stores data by columns instead of rows, enabling:
  * Faster aggregation and filtering.
  * Compression optimizations for reducing disk I/O.
* Data is replicated and encrypted for durability and security.

### Compute Layer (Dremel Execution Engine)
* The Dremel engine is responsible for query execution.
* Uses massively parallel processing (MPP) to break queries into smaller tasks.
* Compute resources are allocated dynamically, eliminating the need for provisioning.

### Jupiter Network (High-Speed Interconnect)
* Jupiter is Google’s high-speed data center network, which enables ultra-fast data transfer between Colossus (storage) and Dremel (compute).
* This low-latency, high-bandwidth network is a key reason BigQuery performs well at scale.


![image](https://github.com/user-attachments/assets/377a3a87-a52b-4485-af60-383ec1295eb4)


BigQuery processes queries using a distributed execution tree, which is optimized for parallelism.


![image](https://github.com/user-attachments/assets/758923ea-7808-4c81-bfd1-80f4988b161c)


![image](https://github.com/user-attachments/assets/3db8d4bc-171a-4bd7-a04e-bb5cf24fa29b)


### Why BigQuery is So Fast

Columnar storage: Reads only the necessary columns.

Distributed execution (Dremel): Breaks queries into parallel tasks.

Compute & storage separation: Eliminates resource contention.

Jupiter network: Ultra-fast communication between storage and compute.

Automatic scaling: Dynamically allocates resources.

