#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import time

users = []
toSendTweet = ""
config = {'CONSUMER_KEY': '', 'CONSUMER_SECRET': '', 'ACCESS_KEY': '', 'ACCESS_SECRET': ''}
api = ""

def setAuthConfig():
    f = open("authConfig", "r")
    lines = []
    for line in f:
        lines.append(line.strip())
    config['CONSUMER_KEY'] = lines[0]
    config['CONSUMER_SECRET'] = lines[1]
    config['ACCESS_KEY'] = lines[2]
    config['ACCESS_SECRET'] = lines[3]
    #print(config)

def getAuth():
    #print(config)
    auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
    auth.secure = True
    auth.set_access_token(config['ACCESS_KEY'], config['ACCESS_SECRET'])
    global api
    api = tweepy.API(auth)


def getUsers():
    global users
    global api

    f = open("users", "r")
    for user in f:
        users.append(user.strip())
    f.close()

    for user in users:
        last_tweet = api.user_timeline(screen_name = user, count = 1)[0]
        last_id = last_tweet.id
        f = open("last_tweet_id_" + user, "w")
        f.write(str(last_id))
        f.close()

def getMessage():
    global toSendTweet
    f = open("tweetMessage", "r")
    toSendTweet = f.read()
    #toSendTweet = unicode(toSendTweet, errors="replace").encode("utf-8")
    f.close()
    print(toSendTweet)


def bot():
    global api

    for user in users:
        print("Bot start for: " + user)
        last_tweet = api.user_timeline(screen_name = user, count = 1)[0]
        new_id = last_tweet.id
        f = open("last_tweet_id_" + user, "r")
        old_id = f.readline()
        f.close()

        if str(new_id) != str(old_id):
            api.update_status(status = "@" + user + " " + toSendTweet, in_reply_to_status_id = new_id)
            f = open("last_tweet_id_" + user, "w")
            f.write(str(new_id))
            print(str(new_id) + " - " + user)
            f.close()


def loop():
    global api

    while 1:
        try:
            bot()
            time.sleep(6)
        except tweepy.TweepError as e:
            print(str(e))
            data = api.rate_limit_status()
            print(data['resources']['statuses']['/statuses/user_timeline'])
            time.sleep(60*1)
            continue

if __name__ == '__main__':

    setAuthConfig()
    getAuth()
    getUsers()
    getMessage()
    loop()

