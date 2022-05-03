APP_NAME := puc-airflow
TAG := lastet

build:
	@docker build -t $(APP_NAME):$(TAG) .

run:
	@docker run -d \
	-v /home/marcelo/code-workspace/puc/airflow-v1/pipeline:/airflow/dags \
	-p 8080:8080 -p 5003:5003 puc-airflow:lastet