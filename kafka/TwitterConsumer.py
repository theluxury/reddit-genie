import tweepy 
import yaml

config = yaml.safe_load(open("tweepy.yaml"))
auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
auth.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_SECRET'])

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
