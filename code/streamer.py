import auth_details
from twython import TwythonStreamer

class MyStreamer(TwythonStreamer):
   def on_success(self,data):
	if 'text' in data:
		print data['text'].encode('utf-8')

   def on_error(self,status_code,data):
	print status_code


stream = MyStreamer(auth_details.APP_KEY,auth_details.APP_SECRET,auth_details.OAUTH_TOKEN,auth_details.OAUTH_TOKEN_SECRET)

stream.statuses.filter(locations='72.68,15.47,81.101,22.4211')
