# HalltapeSparkCluster


- [HalltapeSparkCluster](#halltapesparkcluster)
  - [Spark Local](#spark-local)
  - [Spark Cluster](#spark-cluster)

***
## Spark Local
Spark is running in local mode on your machine.

1. Git clone this repo
```bash
git clone git@github.com:halltape/HalltapeSparkCluster.git
```
2. Unzip dataset
```bash
cd HalltapeSparkCluster/build/workspace/data/ && unzip output.csv.zip output.csv
```

3. Install pyspark and Jupyter Lab
```bash
pip install pyspark jupyterlab
```

4. Start Jupyter Lab
```bash
jupyterlab
```

5. Open build/workspace/spark.ipynb in Jupyter Lab
- [Spark Notebook](build/workspace/spark.ipynb)


***
## Spark Cluster
**Spark Cluster with 4 executors**

Run docker-compose
```Dockerfile
docker-compose up -d
```

Run your spark cluster here

- [Spark Notebook](build/workspace/spark.ipynb)

Review the out-of-memory and spill cases in Spark
- [Spark Notebook 2](build/workspace/spark_oof_spill.ipynb)