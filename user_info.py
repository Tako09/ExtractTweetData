# user id からフォロワー数などを取得するスクリプト 
import requests
import json
from copy import deepcopy
import re

class GetUserInfo():
    '''
    user idからユーザー情報を抜き出す
    '''
    def __init__(self, bearer_token:str()) -> None:
        self.bearer_token = bearer_token # APIキー的な

    def create_url(self, usernames:str(), user_fields:str()) -> str():
        # 取得したい情報を取るためのURLを生成する
        # userから欲しい情報は下記の中から選ぶことができる。
        # APIのレベルによって取得出来ないものもあるので公式HP参照する
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        url = "https://api.twitter.com/2/users/by?{}&{}".format('usernames='+usernames, user_fields)
        return url


    def bearer_oauth(self,r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(self, url:str()) -> dict():
        response = requests.request("GET", url, auth=self.bearer_oauth,)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


    def get(self, usernames:list(), user_columns:dict(), user_fields:str()) -> dict():
        # user情報を取得する関数
        self.raw_lst = [] # ローデータを保管しておく
        self.metrics_table = deepcopy(user_columns) # 後からでもアクセスできるようにする
        public_metrics = ['following_count', 'tweet_count', 'listed_count', 'followers_count'] # public_metricsに含まれる値
        
        for i, v in enumerate(usernames):
            url = self.create_url(v, user_fields)
            json_response = self.connect_to_endpoint(url)
            raw = json_response['data'][0]
            self.raw_lst.append(raw)
            
            for k in user_columns.keys():
                if k in public_metrics:
                    self.metrics_table[k].append(raw['public_metrics'][k])
                else:
                    self.metrics_table[k].append(raw[k])
        
        return self.metrics_table
