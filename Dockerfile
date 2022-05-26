FROM python:3.8-slim

ARG USER_NAME=airflow
ARG FIRST_NAME=airflow
ARG LAST_NAME=airflow
ARG PASSWORD=airflow
ARG ROLE=Admin
ARG EMAIL=airflow@airflow.com

ENV AIRFLOW_HOME=/airflow

RUN apt-get update \
    && apt-get install -y --no-install-recommends \ 
        sqlite3 \
        libssl-dev \
        libkrb5-dev

RUN mkdir -p /airflow/dags &&\
    mkdir -p /airflow/plugins &&\
    mkdir -p /airflow/logs

RUN pip install --upgrade pip &&\
    pip install apache-airflow mlflow scikit-learn pandas typing_extensions

RUN airflow db init && airflow users create \
    --username ${USER_NAME} \
    --firstname ${FIRST_NAME} \
    --lastname ${LAST_NAME} \
    --role ${ROLE} \
    --email ${EMAIL} \
    --password ${PASSWORD}

COPY scripts/process.sh /app/

WORKDIR /airflow/dags
EXPOSE 8080 5003
RUN chmod +x ../../app/process.sh 

CMD ["../../app/process.sh"]