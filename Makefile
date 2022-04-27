dev-setup: ## Setup the local development environment with python3 venv and project dependencies.
	sudo apt-get update
	sudo pip3 install virtualenv
	sudo apt-get install python3-dev python3-venv
	python3 -m venv .env
	( \
		. $(PYTHON_BIN)/activate; \
		 pip install --upgrade pip \
		pip install -r requirements.txt; \
	)

up-resources: ## Config and run Airflow and Spark locally
	@docker-compose up --build -d
	@docker exec local_spark_airflow_airflow-webserver_1 pip install -r docker-requirements.txt.txt
	@docker exec local_spark_airflow_airflow-webserver_1 airflow connections add 'local_spark' --conn-type 'spark' --conn-host 'local[*]' --conn-extra '{"queue": "root.default"}'


###############
# Definitions #
###############

PYTHON_BIN ?= .env/bin