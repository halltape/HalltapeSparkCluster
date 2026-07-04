# HalltapeSparkCluster

Мини-лаборатория Spark Standalone в Docker: JupyterLab + Spark Master + несколько Spark Workers.

Цель: запускать один и тот же Spark workload с разными ресурсами и смотреть разницу в Spark UI.

## Что нужно

- Docker Desktop
- Docker Compose v2

На Mac ARM JupyterLab собирается локально из `build/docker/jupyterlab-local/Dockerfile`, чтобы notebook/kernel работали нативно, без amd64-эмуляции.

## Быстрый старт

Поднять средний кластер с 4 воркерами:

```bash
docker compose --env-file profiles/spark-medium.env up -d --build --scale spark-worker=4
```

Проверить контейнеры:

```bash
docker compose --env-file profiles/spark-medium.env ps
```

Открыть:

- JupyterLab: http://localhost:8888/lab
- Spark Master UI: http://localhost:8080
- Spark Driver UI: http://localhost:4040

Текущая средняя конфигурация:

```text
4 workers x 2 cores x 2g RAM
= 8 cores и 8g RAM суммарно
```

## Как тестировать

1. Открой `01_generate_spark_datasets.ipynb`.
2. Запусти все ячейки сверху вниз.
3. Должны создаться parquet-датасеты в `build/workspace/data/lab`.
4. Открой `02_resource_allocation_lab.ipynb`.
5. Меняй `PROFILE`: `tiny`, `normal`, `wide`.
6. Запускай одинаковые тесты и сравнивай время + Spark UI.

Первый notebook генерирует:

- `events` - факт на 1 млн строк;
- `events_partitioned` - партиционированный факт;
- `users` - справочник пользователей;
- `skewed_events` - данные с перекосом ключей.

Если нужно больше данных, в `01_generate_spark_datasets.ipynb` поменяй:

```python
SCALE = 1
```

на `2`, `3` или больше. На локальной машине лучше начинать с `1`.

## Профили кластера

Маленький:

```bash
docker compose --env-file profiles/spark-small.env up -d --build --scale spark-worker=1
```

Средний:

```bash
docker compose --env-file profiles/spark-medium.env up -d --build --scale spark-worker=4
```

Большой:

```bash
docker compose --env-file profiles/spark-large.env up -d --build --scale spark-worker=4
```

Что меняется:

```text
profiles/spark-small.env   1 core  / 1g на worker
profiles/spark-medium.env  2 cores / 2g на worker
profiles/spark-large.env   2 cores / 3g на worker
```

Количество воркеров задается через `--scale spark-worker=N`.

## Что смотреть в Spark UI

Spark Master UI: http://localhost:8080

- сколько workers подключено;
- сколько всего cores и memory;
- какие applications запущены.

Spark Driver UI: http://localhost:4040

- Jobs;
- Stages;
- Tasks;
- Executors;
- Shuffle read/write;
- долгие tasks при skew.

## Остановить

```bash
docker compose --env-file profiles/spark-medium.env down
```

Если нужно удалить сгенерированные данные:

```bash
rm -rf build/workspace/data/lab
```
