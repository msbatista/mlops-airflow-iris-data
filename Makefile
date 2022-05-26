APP_NAME := puc-airflow
TAG := lastet

build:
	@docker build -t $(APP_NAME):$(TAG) .

run:
	@docker run -v /home/marcelo/code-workspace/airflow/dags:/airflow/dags -v /home/marcelo/code-workspace/airflow/:/airflow/plugins -v /home/marcelo/code-workspace/airflow/:/airflow/logs -p 8080:8080 -p 5003:5003 puc-airflow:lastet