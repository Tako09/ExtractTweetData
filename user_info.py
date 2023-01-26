import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
with open('key.json', 'r') as f:
    open_json = json.load(f)
bearer_token = open_json['bearer_token']

def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=CographData"
    user_fields = "user.fields=description,created_at,pinned_tweet_id,public_metrics"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()