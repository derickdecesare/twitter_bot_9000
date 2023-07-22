import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access Twitter API credentials from environment variables
consumer_key = os.getenv("YOUR_CONSUMER_KEY")
consumer_secret = os.getenv("YOUR_CONSUMER_SECRET")
access_token = os.getenv("YOUR_ACCESS_TOKEN")
access_token_secret = os.getenv("YOUR_ACCESS_TOKEN_SECRET")

# Check if all required Twitter API credentials are successfully loaded
if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
    raise ValueError(
        "Please set all required Twitter API credentials in the .env file.")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create Tweepy API object
api = tweepy.API(auth)

# Function to create a tweet


def create_tweet(tweet_text):
    try:
        api.update_status(tweet_text)
        print("Tweet successfully posted:", tweet_text)

    except tweepy.TweepError as e:
        print("Error posting tweet:", e)


# Example usage:
if __name__ == "__main__":
    tweet_text = "Hello, this is a sample tweet!"
    create_tweet(tweet_text)
