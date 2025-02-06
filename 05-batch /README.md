# Module 5: Batch Processing

## Table of contents

- [5.1 Introduction](#Introduction-to-analytics-engineering)
  - [What is analytics engineering?](#What-is-analytics-engineering)
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

Types of batch jobs: SQL, Python scripts, Spark, Flink

Advantages: easy to manage, retry, scale; easier to orchestrate

Disadvantages: delay

## 5.1.2 Introduction to Spark

• What is Spark

• Why do we need it

Spark is a "general purpose distributed processing engine". Common use cases: batch-type workloads. Also streaming, but we won't cover it here.

When would you use Spark? For the same things as you'd use SQL - but for executing the queries on the files in your datalake.

If you can write this in SQL and use Hive/Presto/Athena/BQ - do it. But not everything can/should be expressed in SQL.

Common case - ML algorithms. You can't easily use SQL for most of it.

Typical pipeline





