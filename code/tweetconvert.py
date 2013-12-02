class converter():

    def convert(self, read_file, out_file):
        
        f = open(read_file,'rb')
        f1 = open(out_file,'wb')

        text = f.read()
        
        tweets = text.split('\n')
        tweet_text = []
        
        #tweets[0] is usually Authentication complete
        
        for tweet in tweets:
            try:
                if not tweet == 'Authentication Complete':
                    tweetline = tweet.split(',')[2].split(':')[1]
                    # Remove the ' u' from the beginning of the string and the ' at the end of it
                    tweet_text.append(tweetline[3:len(tweetline)-1])
            except IndexError:
                print 'IndexError'
        f1.write('\n'.join(tweet_text)) 
        return tweet_text
