# HalltapeSparkCluster

I took the code from the [Apache Spark Standalone Cluster on Docker](https://github.com/cluster-apps-on-docker/spark-standalone-cluster-on-docker) project and adapted it to suit my needs.

<p align="center">
    <img src="png/spark.png" width="800"/>
</p>


- [HalltapeSparkCluster](#halltapesparkcluster)
  - [Spark Local](#spark-local)
  - [Spark Cluster](#spark-cluster)
  - [Spark Resource Lab](#spark-resource-lab)

***
## Spark Local
Spark is running in local mode on your machine.

**Prerequisites:**
- Java must be installed (different versions may work, Java **17** is confirmed to work).
- You can download OpenJDK 17 from [Eclipse Adoptium](https://adoptium.net/temurin/releases/?version=17).
- The `JAVA_HOME` environment variable must be set and point to the Java installation directory.

1. Git clone this repo
```bash
git clone git@github.com:halltape/HalltapeSparkCluster.git
```
2. Download datasets

The dataset can be downloaded using `curl`. (**~2 GB**).

**POSIX shells (Linux / macOS / WSL / Git Bash):**

```bash
cd HalltapeSparkCluster/build/workspace && \
mkdir -p data && \
curl -L -o data/customs_data.csv \
  "https://huggingface.co/datasets/halltape/customs_data/resolve/main/customs_data.csv?download=true"
```

**Windows (PowerShell):**

```powershell
cd HalltapeSparkCluster\build\workspace
mkdir data -Force
curl.exe -L "https://huggingface.co/datasets/halltape/customs_data/resolve/main/customs_data.csv?download=true" -o data\customs_data.csv
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
❌ **If you encounter the following error when running PySpark:**
```
RuntimeError: Python in worker has different version 3.12 than that in driver 3.10, PySpark cannot run with different minor versions. Please check environment variables PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON are correctly set.
```
✅ **Solution**

You can do this by adding the following code snippet at the beginning of your PySpark script or notebook:
```python
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
```

***
## Spark Cluster
Standalone Spark cluster with configurable worker count.

Run docker-compose
```bash
docker compose --env-file profiles/spark-medium.env up -d --scale spark-worker=2
```

Run your spark cluster here

- [Spark Notebook](build/workspace/spark.ipynb)

Review resource allocation, partition pruning, broadcast join, skew, and spill-related behavior in Spark UI:

- [Spark Resource Lab](build/workspace/02_resource_allocation_lab.ipynb)

***
## Spark Resource Lab
This repo can be used as a small commercial-like Spark lab: change cluster resources, change SparkSession executor settings, and compare the same workload in Spark UI.

Start one of the cluster profiles:

```bash
docker compose --env-file profiles/spark-small.env up -d --scale spark-worker=1
docker compose --env-file profiles/spark-medium.env up -d --scale spark-worker=2
docker compose --env-file profiles/spark-large.env up -d --scale spark-worker=4
```

Open:

- JupyterLab: http://localhost:8888
- Spark Master UI: http://localhost:8080
- Spark driver UI: http://localhost:4040

Recommended demo order:

1. Generate synthetic data in [01_generate_spark_datasets.ipynb](build/workspace/01_generate_spark_datasets.ipynb).
2. Compare resource profiles in [02_resource_allocation_lab.ipynb](build/workspace/02_resource_allocation_lab.ipynb).
3. In the notebook, change `PROFILE` between `tiny`, `normal`, and `wide`.
4. Restart the Docker cluster with `spark-small`, `spark-medium`, and `spark-large` profiles and compare Spark UI metrics.

The generated datasets cover common Spark cases:

- fact table + small dimension for join and broadcast join;
- partitioned parquet for partition pruning;
- skewed keys for long tasks and uneven shuffle;
- configurable row count through `SCALE`.

Stop the lab:

```bash
docker compose down
```
