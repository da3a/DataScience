import tweepy
from textblob import TextBlob

consumer_key = 'E8TotsMM7sLwpbCQaLkjwEpHX'
consumer_secret = ''

access_token = '556042914-VTkAF9VSold4I2JHOJQOP2WxvgNJe45RmDleGxei'
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('Macron')

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.Text)
    print(analysis.sentiment)

