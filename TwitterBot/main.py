import tweepy
import time

config = {'CONSUMER_KEY': '', 'CONSUMER_SECRET': '', 'ACCESS_KEY': '', 'ACCESS_SECRET': ''}
api = ""
ids = []
account = "_teknokta"

def setAuthConfig():
	f = open("authConfig_seferogullari", "r")
	lines = []
	for line in f:
		lines.append(line.strip())
	config['CONSUMER_KEY'] = lines[0]
	config['CONSUMER_SECRET'] = lines[1]
	config['ACCESS_KEY'] = lines[2]
	config['ACCESS_SECRET'] = lines[3]
	#print(config)

def getAuth():
	global api
	#print(config)
	auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
	auth.secure = True
	auth.set_access_token(config['ACCESS_KEY'], config['ACCESS_SECRET'])
	api = tweepy.API(auth)

def autoFollow():
	global api

	for user in tweepy.Cursor(api.followers, screen_name=account).items():
		api.create_friendship(user.id)
		print(user.screen_name)
		time.sleep(6)

def deleteAllTweet():
	global api

	for item in tweepy.Cursor(api.user_timeline).items(34):
		api.destroy_status(item.id)
		print item.text
		#time.sleep(6)

def unfAll():
	global api

	#time.sleep(15*60)

	for id in tweepy.Cursor(api.friends_ids).items(80):
		api.destroy_friendship(id)
		print(api.get_user(id).screen_name)


if __name__ == '__main__':
	setAuthConfig()
	getAuth()
	#autoFollow()
	unfAll()
	#deleteAllTweet()
