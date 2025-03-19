
## Course Project

### Problem statement

The **Seattle Pet Licenses dataset** contains records of pet licenses issued in the city, including details about pet types, breeds, and locations. However, raw data alone is not enough for meaningful insights. Manually processing this dataset can be time-consuming, and without proper data management, tracking trends in pet ownership, license renewals, and compliance becomes difficult.

This project aims to automate the end-to-end data pipeline to process the dataset efficiently. Using **Kestra** as a workflow orchestrator, we will **extract, load, and transform data** into **BigQuery**, where it can be analyzed effectively. The data pipeline is designed as a **scheduled batch process** that runs every month. **dbt** is used for transformation to ensure clean and structured data, making it easier to generate meaningful insights. The final processed data is visualized using **Looker**, providing interactive dashboards to support decision-making related to pet licensing policies, trends, and compliance enforcement in Seattle.

Dataset: [Seattle Pet Licenses data](https://data.seattle.gov/City-Administration/Seattle-Pet-Licenses/jguv-t9rb/about_data)

### Datapipeline design:


![image](https://github.com/user-attachments/assets/4112d870-2f02-4b3d-9925-0861cff232aa)



Before Start: 
use terraform to configure GCP: [terraform](https://github.com/yvt-ee/data-engineering-zoomcamp/tree/main/Project/terraform)

use docker to compose kestra: [docker-compose.yml](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/DataIngestion-kestra/docker-compose.yml)

**Extract & Load**

Using Kestra to extract data from the source.

Using Kestra to put the data to datalake-GCP cloud storage, creat external table in bigquery. Set is as a schedualed job, run every month. [gcp_pet_scheduled.yaml](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/DataIngestion-kestra/gcp_pet_scheduled.yaml)

Tables are partitioned by License Issue Date:

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

**Tranform**

We use dbt to clean and normalize pet licensing data, ensuring consistency in license number. Additionally, dbt helps create aggregated tables for faster query performance in Looker. [dbt](https://github.com/yvt-ee/data-engineering-zoomcamp/tree/main/Project/dbt)

**Visulization**

Use looker to read from bigquery database, build a datadashboard to tablk about: 

- How are pet licenses distributed across different species? 

- What is the trend in pet license registrations over year?

- What is the monthly growth trend in pet licenses?

- What is the most popular pet's name?

- Under which location(zipcode) has the most licensed pet?

[Seattle_Pet_Licenses.pdf](https://github.com/yvt-ee/data-engineering-zoomcamp/blob/main/Project/Seattle_Pet_Licenses.pdf)

### How to Run the Project

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

