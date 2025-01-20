Data Warehouse

OLAP vs OLTP

What is data warehouse

BigQuery


  
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

There are no servers to manage or database software to install

* Software as well as infrastructure including
  
scalability and high-availability

* Built-in features like 

machine learning

geospatial analysis

business intelligence

* BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage

### BigQuery Cost

* On demand pricing

1 TB of data processed is $5

* Flat rate pricing

Based on number of pre requested slots. 

100 slots → $2,000/month = 400 TB data processed on demand pricing

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

Filtering by Timestamp Without Using DATE() might cause

BigQuery may scan all partitions (even those not containing the relevant date).

Higher costs and slower performance because it evaluates the condition for all rows, not just the required partition.


**Look into the partitons**

```sql
SELECT DISTINCT(VendorID)
FROM `zoompcamp2025.zoomcamp1.yellow_tripdata_non_partitoned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```
