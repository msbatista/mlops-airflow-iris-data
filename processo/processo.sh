#!/bin/bash

# Start the first process
airflow webserver --port 8080 &
  
# Start the second process
airflow scheduler &

mlflow ui --port 5003 \
    --backend-store-uri sqlite:///mlruns/mlflow.db \
    --default-artifact-root ./mlruns \
    --host 0.0.0.0 &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?