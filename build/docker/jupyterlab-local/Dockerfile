FROM python:3.12-slim-bookworm

ARG SPARK_VERSION=3.5.7
ARG JUPYTERLAB_VERSION=4.4.10

ENV PYSPARK_PYTHON=python3 \
    PYSPARK_DRIVER_PYTHON=python3 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless bash procps && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    jupyterlab==${JUPYTERLAB_VERSION} \
    pyspark==${SPARK_VERSION} \
    ipykernel==6.29.5

WORKDIR /opt/workspace

EXPOSE 8888 4040

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--ServerApp.token=", "--ServerApp.password="]
