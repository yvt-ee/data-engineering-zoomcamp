# Module 5: Batch Processing

## Table of contents

- [5.1 Introduction](#51-Introduction)
  - [Introduction to Batch Processing](#511-introduction-to-batch-processing)
  - [ETL vs ELT](#ETL-vs-ELT)
  - [Data Modeling concepts](#Data-Modeling-concepts)
- [What is dbt?](#What-is-dbt)
- [Create a dbt project](#Create-a-dbt-project)
- [Development of dbt models](#Development-of-dbt-models)
- [Testing and Documenting the Project](#Testing-and-Documenting-the-Project)
- [Deployment Using dbt Cloud](#Deployment-Using-dbt-Cloud)
- [Visualising the transformed data](#Visualising-the-transformed-data)

# 5.1 Introduction
## 5.1.1 Introduction to Batch Processing

• Batch vs streaming
 
• Types of batch jobs

• Orchestrating batch jobs

• Advantages and disadvantages of batch jobs

Batch - processing a chunk of data at regular intervals. Stream - processing data on the fly

![image](https://github.com/user-attachments/assets/bfb632f1-c026-4e3d-be54-e2e3f7dbc96b)

![image](https://github.com/user-attachments/assets/20b9a178-51d1-4148-8a85-8357cf7d3e9f)

Types of batch jobs: SQL, Python scripts, Spark, Flink

![image](https://github.com/user-attachments/assets/77637762-b69f-4f00-8bd8-5c838576b36d)

![image](https://github.com/user-attachments/assets/b1d162f5-9066-4da5-84bd-234474f58aff)

Advantages: easy to manage, retry, scale; easier to orchestrate

Disadvantages: delay

![image](https://github.com/user-attachments/assets/e8d8b294-7825-4277-bd1d-32547d2015a0)


## 5.1.2 Introduction to Spark
 
• What is Spark

• Why do we need it

Spark is a "general purpose distributed processing engine". Common use cases: batch-type workloads. Also streaming, but we won't cover it here.

When would you use Spark? For the same things as you'd use SQL - but for executing the queries on the files in your datalake.

If you can write this in SQL and use Hive/Presto/Athena/BQ - do it. But not everything can/should be expressed in SQL.

![image](https://github.com/user-attachments/assets/d029187e-463e-4257-b370-76d15809cb73)

Common case - ML algorithms. You can't easily use SQL for most of it.

![image](https://github.com/user-attachments/assets/e99f6e6b-bfed-44ba-8569-835c57b77f3e)

![image](https://github.com/user-attachments/assets/d4253312-a83c-426c-a9e9-4e9b1cf9c02a)

Typical pipeline

Raw data -> Data lake -> Some transformation in SQL -> Spark -> Batch job in Python for training a model

Raw data -> Data lake -> SQL -> Spark -> Spark for applying the model -> SQL

All orchestrated with Airflow

# 5.2 Installation

Installing Spark (Linux)

• Connecting to an instance on GCP and installing it there


# 5.3 Spark SQL and DataFrames

## 5.3.1 First Look at Spark/PySpark

• Reading CSV/Parquet files

• Partitions

smaller partitions been process by instances in Spark Cluster by order.

![image](https://github.com/user-attachments/assets/cba4b7fa-7220-470e-bcab-75381f79ff1e)

• Saving data to Parquet for local experiments

• Spark master UI



## 5.3.2 - Spark DataFrames

• Actions vs transformations

![image](https://github.com/user-attachments/assets/777e097a-1c80-492e-8968-1e96bb61303d)


![image](https://github.com/user-attachments/assets/4a28e502-13f2-4a3c-8658-3b5401723b46)

• Partitions

• Functions and UDFs

## 5.3.3 - Preparing Yellow and Green Taxi Data

## 5.3.4 - Spark SQL

• Temporary tables

• Some simple queries from week 4

Joins in Spark

• merge sort join
  
• broadcasting

RDDs

• From DF to RDD

• map

• reduce

• mapPartition

• From RDD to DF

# 5.4 Spark Internals

## 5.4.1 - Anatomy of a Spark Cluster

Spark Internals

• driver, master and executors

![image](https://github.com/user-attachments/assets/eb5f63fb-123d-4c97-9a9b-502c8a154bbf)

## 5.4.2 GroupBy in Spark

• How Groupby works internally

• Shuffling

![image](https://github.com/user-attachments/assets/f90b376b-9fb2-4221-a5f8-50ed03123a7e)

![image](https://github.com/user-attachments/assets/5778dd71-cb87-43e5-981a-9f853cd13bb3)



## 5.4.3 - Joins in Spark

• Join two large tables

• external merge sort algo

• Join one large table and a small table

![image](https://github.com/user-attachments/assets/25ef629d-c77c-4fcb-b91b-5be843f60b11)

![image](https://github.com/user-attachments/assets/faa68880-8d85-41a8-b2e0-47d8a5ec9d3e)

# 5.5 (Optional) Resilient Distributed Datasets

## 5.5.1 Operations on Spark RDDs



![image](https://github.com/user-attachments/assets/297ce2fb-0889-4945-9425-6f572ff5b2e1)

![image](https://github.com/user-attachments/assets/41c4a8ca-035d-4585-884c-0cb58e496ac7)


![image](https://github.com/user-attachments/assets/846ed72e-cf66-48cb-8610-cc9b1013703e)



## 5.5.2 - (Optional) Spark RDD mapPartition




# 5.6 Running Spark in the Cloud

## 5.6.1 - Connecting to Google Cloud Storage

• Uploading data to GCS

• Connecting spark jobs to GCS

• https://cloud.google.com/solutions/spark

Connecting Spark to a DWH

* spark with BigQuery (Athena/presto/hive/etc - similar)
* 
* reading from GCP and saving to BG

## 5.6.2 - Creating a Local Spark Cluster

• Creating the cluster cluster
• Turning the notebook into a script.
• Using spark-submit for submitting spark jobs

https://spark.apache.org/docs/latest/spark-standalone.html

jupyter nbconvert --to=script 06_spark_sql.ipynb



python 06_spark_sql.py \
＞
--input_green=data/pq/green/2020/*/ \
>
--input_yellow=data/pq/yellow/2020/*/ \
>
--output=data/report-2020


spark submit


URL="spark: //de-zoomcamp. europe-westl-b.c.de-zoomcamp-nytaxi.internal:7077"
spark-submit \
  --master="${URL}". \
  06_spark_sql.py \
    --input_green=data/pq/green/2021}*/ \
    --input_yellow=data/pq/yellow/2021/*/ \
    --output=data/report-2021

## 5.6.3 Setting up a Dataproc Cluster
• Creating a cluster
• Runing a soark job with Daraproc
• Submitting the job with the cloud SDK


 

