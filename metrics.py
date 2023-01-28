import requests
import json
from copy import deepcopy
import re

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
with open('key.json', 'r') as f:
    open_json = json.load(f)
bearer_token = open_json['bearer_token']

class GetTweetMetrics():
    '''
    Tweet idから特定のtweetのmetrics
    (tweetの指標(例：インプレッション数など))を取得するクラス
    '''
    def __init__(self, bearer_token) -> None:
        self.bearer_token = bearer_token # APIキー的な
        
    def create_url(self, ids, tweet_fields):
        # 取得したい情報を取るためのURLを生成する
        # Tweetから欲しい情報は下記の中から選ぶことができる。
        # APIのレベルによって取得出来ないものもあるので公式HP参照する
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        ids = "ids=" + ids
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        return url


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r


    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=self.bearer_oauth)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


    def get(self, ids:list(), columns:dict(), tweet_fields:str()):
        # metricsを取得する関数
        self.raw_lst = [] # ローデータを保管しておく
        self.metrics_table = deepcopy(columns) # 後からでもアクセスできるようにする
        public_metrics = ['retweet_count', 'reply_count', 'like_count', 'quote_count', 'impression_count'] # public_metricsに含まれる値
        entities = 'hashtag'
        repeater = re.compile(entities)
        
        for i, v in enumerate(ids):
            # IDからそれぞれのmetricsを取得する
            url = self.create_url(v, tweet_fields)
            json_response = self.connect_to_endpoint(url)
            raw = json_response['data'][0]
            self.raw_lst.append(raw)
            
            hashN = 0
            for k in columns.keys():
            # 欲しいカラムを取得してcolumnsに新し値として入れる
                if k in public_metrics:
                    self.metrics_table[k].append(raw['public_metrics'][k])
                elif repeater.match(k):
                    try:
                        self.metrics_table[k].append(raw['entities']['hashtags'][hashN]['tag'])
                        hashN += 1
                    except IndexError as e:
                        print('もーないよ')
                        self.metrics_table[k].append(None)
                        continue
                elif k == 'url':
                    try:
                        self.metrics_table[k].append(raw['entities']['urls'][0]['url'])
                    except IndexError as e:
                        print('ないよ')
                        self.metrics_table[k].append(None)
                        continue
                else:
                    self.metrics_table[k].append(raw[k])
                
        return self.metrics_table
        
        # print(raw_data)

    