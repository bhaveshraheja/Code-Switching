'''Program that downloads the tweets of a give user'''
import auth_details
from twython import Twython

class tweetdownloader():

    _tweetid = None
    _twitter = None
    _tweets = []
    def init(self):
       self._twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def get_user_tweets(self, tweetid, count=200):
        if count <= 200:
            tweets = self._twitter.get_user_timeline(screen_name=tweetid, count=count)
        for tweet in tweets:
            self._tweets.append(tweet['text'])
        return self._tweets
