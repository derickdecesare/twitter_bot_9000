from requests_oauthlib import OAuth1Session
import os
import json
from dotenv import load_dotenv
from research_agent import research_agent


def get_twitter_credentials():
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    return consumer_key, consumer_secret


def post_tweet(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text):
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret,
                          resource_owner_key=access_token, resource_owner_secret=access_token_secret)
    payload = {"text": tweet_text}

    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

    if response.status_code != 201:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}")

    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    load_dotenv()

    # Step 1: Call the API that will determine what our Twitter thread will be on today
    # Assuming the API response is stored in the variable 'research_response'
    # You should implement research_agent function
    research_response = research_agent()

    # Step 2: Use the response to call research agent (Not implemented in the provided code)
    # research_to_api(api_url, research_response)

    # Step 3: Use research to write the thread (Not implemented in the provided code)

    # Step 4: Post the Twitter thread
    consumer_key, consumer_secret = get_twitter_credentials()

    # You need to obtain access_token and access_token_secret using the OAuth process (Not implemented in the provided code)
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    tweet_text = "Hello world!"  # Replace this with the actual tweet content
    post_tweet(consumer_key, consumer_secret, access_token,
               access_token_secret, tweet_text)
