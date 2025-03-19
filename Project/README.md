
# Course Project

## Problem statement

The **Seattle Pet Licenses dataset** contains records of pet licenses issued in the city, including details about pet types, breeds, and locations. However, raw data alone is not enough for meaningful insights. Manually processing this dataset can be time-consuming, and without proper data management, tracking trends in pet ownership, license renewals, and compliance becomes difficult.

This project aims to automate the end-to-end data pipeline to process the dataset efficiently. Using **Kestra** as a workflow orchestrator, we will **extract, load, and transform data** into **BigQuery**, where it can be analyzed effectively. The data pipeline is designed as a **scheduled batch process** that runs every month. **dbt** is used for transformation to ensure clean and structured data, making it easier to generate meaningful insights. The final processed data is visualized using **Looker**, providing interactive dashboards to support decision-making related to pet licensing policies, trends, and compliance enforcement in Seattle.

Dataset: [Seattle Pet Licenses data](https://data.seattle.gov/City-Administration/Seattle-Pet-Licenses/jguv-t9rb/about_data)

## Datapipeline design:

The data pipeline follows a structured workflow to ensure efficient data ingestion, transformation, and storage.

![image](https://github.com/user-attachments/assets/4112d870-2f02-4b3d-9925-0861cff232aa)

**Before Start**

Terraform is used to configure GCP services including Cloud Storage and BigQuery: [terraform](https://github.com/yvt-ee/data-engineering-zoomcamp/tree/main/Project/terraform)

Docker is used to deploy Kestra for workflow orchestration: [docker-compose.yml](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/DataIngestion-kestra/docker-compose.yml)

### Extract&Load
Usring Kestra workfow to condeuct extract and load: 

[gcp_pet_scheduled.yaml](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/DataIngestion-kestra/gcp_pet_scheduled.yaml)

**Extract**

Using Kestra to extract data from the source.

The pipeline fetches pet license data from the Seattle Open Data API and processes it using Python.

- Pagination Handling – Fetches data in batches of 1,000 rows to avoid API rate limits.
- Parquet Format – Saves data in Parquet, an optimized format for analytics and storage.
- Timestamp Conversion – Converts update_time to Pacific Time (PST) for consistency.
- Date Handling – Extracts year, month, day from license_issue_date for partitioning.
- Column Renaming – Standardizes column names for clarity.

**Load**

Using Kestra to put the data to datalake-GCP cloud storage, creat external table in bigquery. Set is as a schedualed job, run every month. 

1. Links directly to the Parquet file in GCS to allow querying without duplication.
   
Reduces storage costs by leveraging external tables.

2. Loads the dataset from the external table into a structured partitioned table.
   
Table are partitioned by license_issue_date for optimized querying.

```python
  - id: bq_yellow_replace
    type: io.kestra.plugin.gcp.bigquery.Query
    sql: |
          DROP TABLE IF EXISTS `{{kv('GCP_PROJECT_ID')}}.{{kv('GCP_DATASET')}}.pet_licensesdata`;

          CREATE TABLE `{{kv('GCP_PROJECT_ID')}}.{{kv('GCP_DATASET')}}.pet_licensesdata`
          PARTITION BY license_issue_date
          AS
          SELECT
            update_time,
            filename,
            year,
            month,
            day,
            license_number,
            animal_s_name,
            species,
            primary_breed,
            secondary_breed,
            zip_code,
            DATE(PARSE_DATE('%Y-%m-%d', CONCAT(year, '-', month, '-', day))) AS license_issue_date
          FROM `{{kv('GCP_PROJECT_ID')}}.{{render(vars.table)}}`;
```
Automation & Scheduling
```python
triggers:
  - id: pet_licenses_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 2 10 * *"
```

### Tranform

We use dbt to clean and normalize pet licensing data, ensuring consistency in license number. Additionally, dbt helps create aggregated tables for faster query performance in Looker. [dbt](https://github.com/yvt-ee/data-engineering-zoomcamp/tree/main/Project/dbt)

1. Removing Duplicate License Entries
   
The dataset may contain duplicate records for the same license_number on the same license_issue_date.

To handle this, we use row_number() over(partition by license_number, license_issue_date order by update_time desc) to rank records within each partition.

We keep only the latest record (rn = 1), ensuring that only the most recent update is retained.

2. Converting Timestamp to Pacific Time (PST)
   
The update_time field is stored in UTC or an unspecified timezone.

Using DATETIME(TIMESTAMP(update_time), "America/Los_Angeles") AS update_time_pst, we convert it to Pacific Standard Time (PST) for consistency with Seattle's timezone.

3. Ensuring license_issue_date is a Valid Date
   
The dataset might have inconsistencies in date formatting.

To prevent errors, we use SAFE_CAST(license_issue_date AS DATE) to ensure this column is a proper DATE type.

4. Extracting Year, Month, and Day for Easier Querying
   
Instead of repeatedly extracting these values in Looker or SQL queries, we precompute them:

EXTRACT(YEAR FROM SAFE_CAST(license_issue_date AS DATE)) AS year

EXTRACT(MONTH FROM SAFE_CAST(license_issue_date AS DATE)) AS month

EXTRACT(DAY FROM SAFE_CAST(license_issue_date AS DATE)) AS day

5. Standardizing license_number to Uppercase
   
Since license numbers may have inconsistent casing, we convert them to uppercase using:

UPPER(license_number) AS license_number

This ensures that ABC123 and abc123 are treated as the same entry.

6. Keeping Only Relevant Columns
   
The final dataset includes only the necessary fields:

update_time_pst (Converted timestamp)

license_issue_date, year, month, day

license_number (standardized)

animal_s_name, species, primary_breed, secondary_breed, zip_code

This removes redundant or raw data, improving query performance.


### Visulization

Use looker to read from bigquery database, build a datadashboard to tablk about: 

- How are pet licenses distributed across different species? 

- What is the trend in pet license registrations over year?

- What is the monthly growth trend in pet licenses?

- What is the most popular pet's name?

- Under which location(zipcode) has the most licensed pet?

Link: https://lookerstudio.google.com/s/pw3ute7WaO8

[Seattle_Pet_Licenses.pdf](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/Seattle_Pet_Licenses.pdf)

## How to Run the Project

1. Setup GCP Infrastructure
```
cd terraform
terraform init
terraform apply
```

2. Deploy Kestra Locally
```
cd DataIngestion-kestra
docker-compose up -d
```
After that, run the workflow to load the data to GCP.

3. Run dbt
   
Log in https://py308.us1.dbt.com/

Set up connection to github and bigquery, run the ```dbt build``` in cloud IDE.

4. Build dashboard

Open [looker studio](https://lookerstudio.google.com/), add data scource, connect to big query, select the data transformed by dbt.

