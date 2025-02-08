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

• Reading CSV files

• Partitions

• Saving data to Parquet for local experiments

• Spark master UI


Spark DataFrames

• Actions vs transformations

• Partitions

• Functions and UDFs

Spark SQL

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

Spark Internals

• driver, master and executors

• partitioning + coalesce

• shuffling

• group by or not group by?

• broadcasting

Spark and Docker

• TBD

Running Spark in the Cloud (GCP)

• https://cloud.google.com/solutions/spark

Connecting Spark to a DWH

* spark with BigQuery (Athena/presto/hive/etc - similar)
* 
* reading from GCP and saving to BG



1











 

