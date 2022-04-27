from airflow import DAG
from datetime import datetime
from plugins.twitter.operator.twitter_to_storage_by_hashtag import TwitterToStorageByHashtagOperator

dag = DAG(dag_id="agora_vai",
          start_date=datetime(2021, 1, 1),
          schedule_interval="@hourly",
          catchup=False)

extract_and_write = TwitterToStorageByHashtagOperator(dag=dag,
                                                      task_id="extract_and_write",
                                                      path="file:///bronze/twitter/hashtag/covid19/",
                                                      hashtag="covid19",
                                                      since="2022-01-01",
                                                      language="en",
                                                      count=100,
                                                      tweet_mode="extended",
                                                      format="parquet",
                                                      mode="append",
                                                      conn_id="twitter_default")

