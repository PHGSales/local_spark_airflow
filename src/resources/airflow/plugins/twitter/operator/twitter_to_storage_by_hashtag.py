import json
from abc import ABC
from typing import List
from airflow.models import BaseOperator
import tweepy
from plugins.twitter.hook.twitter_hook import TwitterHook
from tweepy.cursor import ItemIterator
import datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


class TwitterToStorageByHashtagOperator(BaseOperator, ABC):
    def __init__(self,
                 task_id: str,
                 conn_id: str,
                 hashtag: str,
                 since: str,
                 language: str,
                 count: int,
                 tweet_mode: str,
                 path: str,
                 format: str,
                 mode: str,
                 **kwargs):
        super().__init__(task_id=task_id,
                         **kwargs)
        self.conn_id = conn_id
        self.hashtag = hashtag
        self.since = since
        self.language = language
        self.count = count
        self.tweet_mode = tweet_mode
        self.path = path
        self.format = format
        self.mode = mode
        self.hook = TwitterHook(conn_id=conn_id)

    def get_tweets(self) -> ItemIterator:
        connection = self.hook.connect()
        return tweepy.Cursor(connection.search_tweets,
                             q=self.hashtag,
                             lang=self.language,
                             since=self.since,
                             tweet_mode=self.tweet_mode).items(self.count)

    def parse_to_dict(self, tweets: ItemIterator) -> List:
        data = []
        for tweet in tweets:
            field = {"tweet_created_at": tweet.created_at,
                     "author_name": tweet.author.screen_name,
                     "full_text": tweet.full_text,
                     "query": self.hashtag,
                     "insert_date": datetime.datetime.now()}
            data.append(field)
        return data

    def parse_list_to_dataframe_and_write(self, data: list) -> None:
        SparkSubmitOperator(conn_id='local_spark',
                            task_id='parse_list_to_dataframe_and_write',
                            application='plugins/twitter/utils/spark_jobs.py',
                            application_args=[json.dumps(data, indent=4, sort_keys=True, default=str),
                                              self.path, self.format, self.mode]).execute(context=None)

    def execute(self, context, **kwargs):
        tweets = self.get_tweets()
        data = self.parse_to_dict(tweets=tweets)
        self.parse_list_to_dataframe_and_write(data=data)
