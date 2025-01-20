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

### BigQuery

* Serverless data warehouse

There are no servers to manage or database software to install

* Software as well as infrastructure including
  
scalability and high-availability

* Built-in features like 

machine learning

geospatial analysis

business intelligence

* BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage
