# Twitterからのデータの抽出を行うプログラム

import json
# import polars as pl 将来的にはpolarsを使いたい
import pandas as pd
from metrics import GetTweetMetrics

with open('key.json', 'r') as f:
    # APIキーがjsonにあるのでそれを取ってくる
    open_json = json.load(f)
bearer_token = open_json['bearer_token']

def main():
    bearer_token = open_json['bearer_token']
    ids = ['1617423718644580352'] # ここは自動的に更新できるようにしたい
    tweet_fields = "tweet.fields=created_at,public_metrics,entities" # ここを変えることで取得できる情報が変わる
    columns = {
                'id':[],'created_at':[], 'text':[],
                'hashtag1':[], 'hashtag2':[], 'hashtag3':[], 'hashtag4':[],
                'retweet_count':[], 'reply_count':[], 'like_count':[],
                'quote_count': [], 'impression_count': [], 'url':[]
            } # 欲しいカラムを値は空で辞書型デモっておく
    
    get_metrics = GetTweetMetrics(bearer_token)
    metrics_table = get_metrics.get(ids, columns, tweet_fields)
    
    df = pd.DataFrame(metrics_table)
    df['created_at'] = to_japan_time(df, 'created_at')
    df.rename({'url':'main_url'}, inplace=True, axis='columns')
    df.to_csv('test.csv', index=False)
    print(df)
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