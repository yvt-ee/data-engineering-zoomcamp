# Module 5 Homework

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2024-10 data from the official website: 

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-10.parquet
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
```python
import pyspark

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

--print(spark.version)

3.3.2
```

**Correct Answer: 3.3.2**

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)


## Question 2: Yellow October 2024

Read the October 2024 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB
- 75MB
- 100MB

```python
df = spark.read.parquet('yellow_tripdata_2024-10.parquet')

df.schema

yellow_schema = types.StructType([
    types.StructField("VendorID", types.IntegerType(), True),
    types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
    types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
    types.StructField("passenger_count", types.IntegerType(), True),
    types.StructField("trip_distance", types.DoubleType(), True),
    types.StructField("RatecodeID", types.IntegerType(), True),
    types.StructField("store_and_fwd_flag", types.StringType(), True),
    types.StructField("PULocationID", types.IntegerType(), True),
    types.StructField("DOLocationID", types.IntegerType(), True),
    types.StructField("payment_type", types.IntegerType(), True),
    types.StructField("fare_amount", types.DoubleType(), True),
    types.StructField("extra", types.DoubleType(), True),
    types.StructField("mta_tax", types.DoubleType(), True),
    types.StructField("tip_amount", types.DoubleType(), True),
    types.StructField("tolls_amount", types.DoubleType(), True),
    types.StructField("improvement_surcharge", types.DoubleType(), True),
    types.StructField("total_amount", types.DoubleType(), True),
    types.StructField("congestion_surcharge", types.DoubleType(), True)
])

df = spark.read \
    .option("header", "true") \
    .schema(yellow_schema) \
    .csv('fhvhv_tripdata_2021-01.csv')

df = spark.read.schema(yellow_schema).parquet('yellow_tripdata_2024-10.parquet')
df = df.repartition(4)
df.write.parquet('yellow/2024/10/')
```

```bash
ls -lh yellow/2024/10/
--25MB
```

**Correct Answer: 25MB**


## Question 3: Count records 

How many taxi trips were there on the 15th of October?

Consider only trips that started on the 15th of October.

- 85,567
- 105,567
- 125,567
- 145,567

```python
df_yellow = spark.read.parquet('data/yellow/2024/10/*')

df_yellow.registerTempTable('yellow_data')

spark.sql("""
SELECT
    COUNT(DISTINCT VendorID)
FROM
    yellow_data
WHERE
    CAST(tpep_pickup_datetime AS DATE) = '2024-10-15'
""").show()
```

**Correct Answer: 125,567**

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 122
- 142
- 162
- 182


```python
spark.sql("""
SELECT
    (unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600 AS trip_duration_hours
FROM
    yellow_data
WHERE
    trip_distance = (SELECT MAX(trip_distance) from yellow_data)
""").show()
```

**Correct Answer: 162**

## Question 5: User Interface

Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080

**Correct Answer: 4040**

## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow October 2024 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

```python
df_zone = spark.read.option("header", "true").csv('taxi_zone_lookup.csv')

df_zone.registerTempTable('zone')  

spark.sql("""
SELECT z.Zone, count(1) AS num_trips
FROM yellow_data y
Left JOIN zone z ON z.LocationID = y.PULocationID
GROUP BY z.Zone
ORDER BY num_trips ASC
Limit 1;
""").show()  
```
**Correct Answer: Governor's Island/Ellis Island/Liberty Island**


## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw5
- Deadline: See the website
