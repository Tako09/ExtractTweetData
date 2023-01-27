# tweet idからインプレッション数などを取得するスクリプト
import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
with open('key.json', 'r') as f:
    open_json = json.load(f)
bearer_token = open_json['bearer_token']

def create_url(ids):
    tweet_fields = "tweet.fields=created_at,public_metrics,non_public_metrics,entities"
    # Tweet fields are adjustable.
    # Options include:
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


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    ids = ['1617423718644580352']
    metrics_by_tweet = []
    wanted_column_lst = ['id', 'text']
    for i, v in enumerate(ids):
        url = create_url(v)
        json_response = connect_to_endpoint(url)
        metrics_by_tweet.append(json_response)
    #print(json_response)
    print(metrics_by_tweet)


if __name__ == "__main__":
    main()
    
