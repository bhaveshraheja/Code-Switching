'''Program that downloads the tweets of a give user'''
import auth_details as auth
from twython import Twython
from twython import TwythonError
from twython import TwythonRateLimitError

class TwitterException(Exception):
    pass

class tweetdownloader():

    _tweets = []
    _twitter = Twython(auth.APP_KEY, auth.APP_SECRET, auth.OAUTH_TOKEN, auth.OAUTH_TOKEN_SECRET)

    def get_user_tweets(self, twitterhandle, count=200):
        count = 0
        attempt = 0
        tweetid = ''
        if count <= 200:
            tweets = self._twitter.get_user_timeline(screen_name=twitterhandle, count=count)
        for tweet in tweets:
            self._tweets.append(tweet['text'].encode('UTF-8'))
            tweetid = tweet['id']
            count = count + 1
        '''while count < 3200 or attempt < 5:
            furthertweets = []
            try:
                furthertweets.append(self.get_user_tweetsfrom(twitterhandle, tweetid))
                count = count+len(furthertweets)
                print "count =",count
            except TwitterException:
                attempt = attempt + 1
                print "attempt =",attempt'''
        return self.get_user_tweetsfrom(twitterhandle, tweetid)


    def get_user_tweetsfrom(self, twitterhandle, sinceid):
        try:
            tweets = self._twitter.get_user_timeline(screen_name=twitterhandle, max_id=sinceid)
        except TwythonRateLimitError,TwythonError:
            raise TwitterException
        for tweet in tweets:
            self._tweets.append(tweet['text'])
            tweetid = tweet['id']
        return self._tweets

