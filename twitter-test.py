from requests_oauthlib import OAuth1Session
import os
import json
from dotenv import load_dotenv
import tweepy
from research_agent import research_agent
from idea_agent import generate_idea
from thread_agent import generate_thread
load_dotenv()

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
access_token = os.environ["DERICK_ACCESS_TOKEN"]
access_token_secret = os.environ["DERICK_ACCESS_TOKEN_SECRET"]
twitter_bearer_token = os.environ["TWITTER_BEARER_TOKEN"]

print(consumer_key)
print(consumer_secret)
print(access_token)
print(access_token_secret)
print(twitter_bearer_token)

#########
# Step 1. Have gpt generate a new idea for the research agent to research -- and store then in airtable so we can reference them later (idea_agent.py) ✅
##########

subject = "AI startups"

idea = generate_idea(subject)

print("idea from generate_idea========>", idea["idea"])
print("airtable_id from generate_idea========>", idea["airtable_id"])


#########
# Step 2. Get response from research agent ✅
##########


research_response = research_agent(idea["idea"], idea["airtable_id"])

print("response from research_agent========>", research_response)


#########
# Step 3. Based on response from research agent use GPT to write a thread with emojis 
##########

formatted_research = f"""{research_response}"""

tweets = generate_thread(formatted_research, subject, idea["airtable_id"])


print("tweets from generate_thread========>", tweets)


# print("tweet 1", tweets[0])
# print("tweet 2", tweets[1])
# print("tweet 3", tweets[2])


#########
# Step 4. Use tweepy to post the thread to twitter ✅ 
##########



def post_to_twitter(tweets):
    client = tweepy.Client(bearer_token=twitter_bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True)

    ## character limit is 280 so we'll need to split it up into multiple tweets
    # The text of your tweets.
    # tweets = ["Another super unique Test thread 1.", "Another super unique Test thread 2.", " Another super unique Test thread 3."]

    # Get authenticated user's info
    # user = client.get_me()

    # Post the first tweet.
    tweet = client.create_tweet(text=tweets[0])

    print("TWEET RESPONSE========>", tweet)

    # Post the other tweets, each in reply to the previous one.
    for i in range(1, len(tweets)):
        reply_text = f"{tweets[i]}"
        print("REPLY TEXT========>", reply_text)
        tweet = client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet.data['id'])
        print("TWEET RESPONSE========>", tweet)

post_to_twitter(tweets)

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
# payload = {"text": "Test from twitter API"}


# #I have the access tokens already, so I don't need to do this part...
# # Get request token
# request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
# oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# try:
#     fetch_response = oauth.fetch_request_token(request_token_url)
# except ValueError:
#     print(
#         "There may have been an issue with the consumer_key or consumer_secret you entered."
#     )

# resource_owner_key = fetch_response.get("oauth_token")
# resource_owner_secret = fetch_response.get("oauth_token_secret")
# print("Got OAuth token: %s" % resource_owner_key)



# # Get authorization
# base_authorization_url = "https://api.twitter.com/oauth/authorize"
# authorization_url = oauth.authorization_url(base_authorization_url)
# print("Please go here and authorize: %s" % authorization_url)
# verifier = input("Paste the PIN here: ")



# # Get the access token
# access_token_url = "https://api.twitter.com/oauth/access_token"
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=resource_owner_key,
#     resource_owner_secret=resource_owner_secret,
#     verifier=verifier,
# )
# oauth_tokens = oauth.fetch_access_token(access_token_url)

# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# # we need to save the access token and access token secret somewhere (e.g. a database) for later use

# print("Access token: %s" % access_token)
# print("Access token secret: %s" % access_token_secret)

# # Make the request
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=access_token,
#     resource_owner_secret=access_token_secret,
# )

# # Making the request
# response = oauth.post(
#     "https://api.twitter.com/2/tweets",
#     json=payload,
# )

# if response.status_code != 201:
#     raise Exception(
#         "Request returned an error: {} {}".format(response.status_code, response.text)
#     )

# print("Response code: {}".format(response.status_code))

# # Saving the response as JSON
# json_response = response.json()
# print(json.dumps(json_response, indent=4, sort_keys=True))






