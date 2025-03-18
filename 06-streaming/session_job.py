from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_green_trips_source_kafka(t_env):
    table_name = 'green-trips'
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime TIMESTAMP(3),
            lpep_dropoff_datetime TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance FLOAT,
            tip_amount FLOAT,
            event_watermark AS lpep_dropoff_datetime,
            WATERMARK FOR event_watermark AS event_watermark - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name

def create_longest_streak_sink(t_env):
    """Defines the sink table for the longest unbroken taxi trip streaks."""
    table_name = 'longest_trip_streaks'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            duration BIGINT,
            PRIMARY KEY (PULocationID, DOLocationID, session_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name


def process_taxi_data():
    try:
        # Set up the execution environment
        env = StreamExecutionEnvironment.get_execution_environment()
        env.enable_checkpointing(10 * 1000)
        env.set_parallelism(3)

        # Set up the table environment
        settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        t_env = StreamTableEnvironment.create(env, environment_settings=settings)

        # Create source and sink tables
        source_table = create_green_trips_source_kafka(t_env)
        sink_table = create_longest_streak_sink(t_env)

        logger.info("Starting Flink job: Finding longest unbroken taxi trip streaks.")

        # Apply session window aggregation
        t_env.execute_sql(f"""
        INSERT INTO {sink_table}
        SELECT
            PULocationID,
            DOLocationID,
            session_window_start AS session_start,
            session_window_end AS session_end,
            UNIX_TIMESTAMP(session_window_end) - UNIX_TIMESTAMP(session_window_start) AS duration
        FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(event_watermark), INTERVAL '5' MINUTE)
        )
        GROUP BY PULocationID, DOLocationID, session_window_start, session_window_end
        ORDER BY duration DESC
        LIMIT 1;
        """)

        logger.info("Flink job completed successfully.")

    except Exception as e:
        logger.error(f"Writing records from Kafka to PostgreSQL failed: {e}", exc_info=True)

if __name__ == '__main__':
    process_taxi_data()