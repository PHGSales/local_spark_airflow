import json
from abc import ABC
import tweepy
from airflow.hooks.base import BaseHook
from tweepy import API


class TwitterHook(BaseHook, ABC):
    def __init__(self, conn_id: str):
        super().__init__()
        self.conn_id = conn_id

    def connect(self) -> API:
        conn_extra = json.loads(self.get_connection(conn_id=self.conn_id).extra)
        auth = tweepy.OAuthHandler(conn_extra.get('api_key'), conn_extra.get('api_secret'))
        auth.set_access_token(conn_extra.get('access_token'), conn_extra.get('access_token_key'))
        return tweepy.API(auth)
