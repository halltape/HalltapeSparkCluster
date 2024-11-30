# HalltapeSparkCluster

I took the code from the [Apache Spark Standalone Cluster on Docker](https://github.com/cluster-apps-on-docker/spark-standalone-cluster-on-docker) project and adapted it to suit my needs.

<p align="center">
    <img src="png/spark.png" width="800"/>
</p>


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
2. Download datasets
```bash
cd HalltapeSparkCluster/build/workspace && \
mkdir -p data && \
curl -L -o data/customs_data.csv "https://huggingface.co/datasets/halltape/customs_data/resolve/main/customs_data.csv?download=true" && \
curl -L -o data/output_data.csv "https://huggingface.co/datasets/halltape/output/resolve/main/output_data.csv?download=true" && \
cd ..
```

3. Install pyspark and Jupyter Lab
```bash
pip install pyspark jupyterlab
```

4. Start Jupyter Lab
```bash
jupyter lab
```

5. Open **spark.ipynb** in Jupyter Lab

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