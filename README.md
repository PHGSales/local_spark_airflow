## Local Airflow Spark 
  
![ARCHITECTURE](/doc/architecture.png?raw=true "ARCHITECTURE")

This repository intends to make ETL jobs locally with a Spark Standalone Cluster and Airflow. To enjoy the resources, 
follow the guideline above:
  
Requirements:
  
*Python 3.6*  
*Makefile*  
*Docker Engine*
  
Clone the repository:  
`git glone https://github.com/PHGSales/local_spark_airflow.git`  
  
Install the dependencies and set the local env:  
`make dev-setup`  
  
Run the docker containers:  
`make up-resources`  
  
If you want to create DAGs or Plugins, work in `src/resources/airflow/dags` and `src/resources/airflow/plugins`.
All the SparkSubmitOperator tasks will run in the local Spark cluster, with driver on `spark://spark:7077` as default.
Access the [Spark UI](https://localhost:8080) and [Airflow WebServer UI](https://localhost:8081).  
  
#### TwitterToStorageByHashtagOperator  
This operator intends to extract tweets from Twitter filtering by hashtag. The job will make requests on Twitter API, 
extract the data, parse to a Spark dataframe and write in a specific path.   
  
PS: Get the credentials [here](https://developer.twitter.com/en/portal/dashboard).  
  
The operator architecture is:  
  
![twitter_to_storage_by_hashtag_operator_architecture.png](/doc/twitter_to_storage_by_hashtag_operator_architecture.png?raw=true "twitter_to_storage_by_hashtag_operator_architecture.png")
  
##### Airflow connection  
The airflow connection has to be created with a name and the credentials are inputted just in the extra field, with this
way: `{"api_key": "XXX", "api_secret": "XXX", "access_token": "XXX", "access_token_key": "XXX"}`