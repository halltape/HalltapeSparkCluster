import os
import time
from contextlib import contextmanager

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


SPARK_MASTER_URL = os.environ.get("SPARK_MASTER_URL", "spark://spark-master:7077")


def make_spark(
    app_name,
    executor_memory="768m",
    executor_cores=1,
    cores_max=2,
    shuffle_partitions=16,
    broadcast_threshold="10m",
):
    return (
        SparkSession.builder
        .appName(app_name)
        .master(SPARK_MASTER_URL)
        .config("spark.executor.memory", executor_memory)
        .config("spark.executor.cores", str(executor_cores))
        .config("spark.cores.max", str(cores_max))
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions))
        .config("spark.sql.autoBroadcastJoinThreshold", broadcast_threshold)
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )


@contextmanager
def timed(label):
    started_at = time.perf_counter()
    yield
    elapsed = time.perf_counter() - started_at
    print(f"{label}: {elapsed:.2f} sec")


def generate_datasets(spark, base_path="data/lab", scale=1):
    os.makedirs(base_path, exist_ok=True)

    rows = 1_000_000 * scale
    users = 100_000 * scale

    fact = (
        spark.range(rows)
        .withColumn("user_id", (F.col("id") % users).cast("long"))
        .withColumn("event_date", F.date_add(F.lit("2026-01-01"), (F.col("id") % 60).cast("int")))
        .withColumn("country", F.element_at(F.array([F.lit("RU"), F.lit("KZ"), F.lit("DE"), F.lit("US")]), (F.col("id") % 4 + 1).cast("int")))
        .withColumn("amount", ((F.col("id") * 17) % 10_000).cast("double") / 100)
        .withColumn("payload", F.sha2(F.col("id").cast("string"), 256))
    )

    dim_users = (
        spark.range(users)
        .withColumnRenamed("id", "user_id")
        .withColumn("segment", F.element_at(F.array([F.lit("new"), F.lit("active"), F.lit("vip")]), (F.col("user_id") % 3 + 1).cast("int")))
    )

    skewed = (
        spark.range(rows)
        .withColumn("key", F.when((F.col("id") % 100) < 85, F.lit(1)).otherwise((F.col("id") % 10_000).cast("long")))
        .withColumn("amount", ((F.col("id") * 31) % 10_000).cast("double") / 100)
    )

    fact.write.mode("overwrite").partitionBy("event_date").parquet(f"{base_path}/events_partitioned")
    fact.repartition(8).write.mode("overwrite").parquet(f"{base_path}/events")
    dim_users.write.mode("overwrite").parquet(f"{base_path}/users")
    skewed.write.mode("overwrite").parquet(f"{base_path}/skewed_events")

    return {
        "events": f"{base_path}/events",
        "events_partitioned": f"{base_path}/events_partitioned",
        "users": f"{base_path}/users",
        "skewed_events": f"{base_path}/skewed_events",
        "rows": rows,
        "users": users,
    }


def benchmark_groupby(spark, path):
    df = spark.read.parquet(path)
    with timed("group by country/date"):
        result = (
            df.groupBy("country", "event_date")
            .agg(F.count("*").alias("rows"), F.sum("amount").alias("amount"))
            .orderBy("country", "event_date")
        )
        print(result.count())


def benchmark_join(spark, events_path, users_path, broadcast=False):
    events = spark.read.parquet(events_path)
    users = spark.read.parquet(users_path)
    if broadcast:
        users = F.broadcast(users)

    with timed(f"join broadcast={broadcast}"):
        result = events.join(users, "user_id").groupBy("segment").agg(F.sum("amount").alias("amount"))
        result.show()


def benchmark_skew(spark, path):
    df = spark.read.parquet(path)
    with timed("skewed group by"):
        df.groupBy("key").agg(F.count("*").alias("rows"), F.sum("amount").alias("amount")).count()
