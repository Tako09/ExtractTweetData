# Twitterからのデータの抽出を行うプログラム

import json
# import polars as pl 将来的にはpolarsを使いたい
import pandas as pd
import datetime
from metrics import GetTweetMetrics
from user_info import GetUserInfo

with open('key.json', 'r') as f:
    # APIキーがjsonにあるのでそれを取ってくる
    open_json = json.load(f)
bearer_token = open_json['bearer_token']

def main():
    # 共通で使う変数の定義
    bearer_token = open_json['bearer_token']
    
    # tweetを調べるのに使う変数の定義
    ids = ['1617423718644580352'] # ここは自動的に更新できるようにしたい
    tweet_fields = "tweet.fields=created_at,public_metrics,entities" # ここを変えることで取得できる情報が変わる
    tweet_columns = {
                'id':[],'created_at':[], 'text':[],
                'hashtag1':[], 'hashtag2':[], 'hashtag3':[], 'hashtag4':[],
                'retweet_count':[], 'reply_count':[], 'like_count':[],
                'quote_count': [], 'impression_count': [], 'url':[]
            } # 欲しいカラムを値は空で辞書型デモっておく
    
    # userを調べるのに使う変数の定義
    usernames = ["CographData"]
    user_fields = "user.fields=public_metrics"
    user_columns = {
                'username':[],'name':[], 'followers_count':[],
                'following_count':[], 'tweet_count':[],
            } # 欲しいカラムを値は空で辞書型デモっておく
    
    # Tweet idからtweetの情報を取得
    tweet = GetTweetMetrics(bearer_token)
    metrics_table = tweet.get(ids, tweet_columns, tweet_fields)
    # テーブルデータに変更
    tweet_df = pd.DataFrame(metrics_table)
    tweet_df['created_at'] = to_japan_time(tweet_df, 'created_at')
    tweet_df.rename({'url':'main_url'}, inplace=True, axis='columns')
    tweet_df['acquisition_date'] = (datetime.datetime
                                    .now(datetime.timezone(datetime.timedelta(hours=9)))
                                    .today()
                                    .strftime('%Y-%m-%d'))
    tweet_df.to_csv('test.csv', index=False)
    
    # user idからuserの情報を取得
    user = GetUserInfo(bearer_token)
    user_table = user.get(usernames, user_columns, user_fields)
    # テーブルデータに変更
    user_df = pd.DataFrame(user_table)
    # 取得備の日付を取得する
    user_df['acquisition_date'] = (datetime.datetime
                                    .now(datetime.timezone(datetime.timedelta(hours=9)))
                                    .today()
                                    .strftime('%Y-%m-%d')) 
    user_df.to_csv('test(user).csv', index=False)
    
    # TODO : Google driveのAPIキーを発行する
    # TODO : Idsはスプシ管理
    # TODO : Excelのテーブルファイルを作ってgoogle driveに置くまでをする。

def to_japan_time(df, col):
    # 日本時間に修正する関数
    japan_time = []
    tmp = pd.DataFrame()
    for i, v in enumerate(df[col].tolist()):
        japan_time.append(v[0:10]+" "+v[11:19])
        japan_time
        tmp['YMDHMS'] = japan_time
        tmp['Add_hour'] = 9
        tmp['YMDHMS'] = pd.to_datetime(
            tmp['YMDHMS'], format='%Y-%m-%d %H:%M:%S') + \
            pd.to_timedelta(tmp['Add_hour'],unit='h'
        )
        return tmp['YMDHMS'].tolist()

if __name__ == "__main__":
    main()