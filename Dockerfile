FROM python:3.8-slim

ARG USER_NAME=airflow
ARG FIRST_NAME=airflow
ARG LAST_NAME=airflow
ARG PASSWORD=airflow
ARG ROLE=Admin
ARG EMAIL=airflow@airflow.com

RUN apt-get update \
&& apt-get install gcc g++ git curl -y 

RUN mkdir /airflow && mkdir /airflow/dags
ENV AIRFLOW_HOME=/airflow
RUN pip install --upgrade pip
RUN pip install apache-airflow mlflow pandas scikit-learn matplotlib

RUN airflow db init

RUN airflow db init && airflow users create \
    --username ${USER_NAME} \
    --firstname ${FIRST_NAME} \
    --lastname ${LAST_NAME} \
    --role ${ROLE} \
    --email ${EMAIL} \
    --password ${PASSWORD}

COPY processo/processo.sh /app/

WORKDIR /airflow/dags
EXPOSE 8080 5003
RUN chmod +x ../../app/processo.sh 

CMD ["../../app/processo.sh"]