# -*- coding: utf-8 -*-
"""
twstreams.py - Willie Twitter Streams Module
Copyright 2013, tante, tante@tante.cc
Licensed under the GPL-3

http://tante.cc
"""

import tweepy
import json

# listener keeps track of the streams listener
# stream keeps the stream alive
listener=None
stream=None


class TwitterListener(tweepy.StreamListener):

    def __init__(self, willie, api=None):
        self.api = api or tweepy.API()
        self.willie = willie

    def on_data(self,data):
        try:
            data=json.loads(data)
            username=data['user']['screen_name']
            text=data['text']
            tweetid=data['id']
            message = username+" tweeted: '"+text+"' - https://twitter.com/"+username+"/statuses/"+str(tweetid)
            self.willie.say(message)
        except:
            pass
        return True

    def on_error(self, status):
        self.willie.say(status)

def configure(config):
    """streams.streams must contain a comma separated list of hashtags or terms you want to follow on Twitter"""
    if config.option('Configure Streams?', False):
        config.interactive_add('streams', 'streams', 'Streams (commaseparated)')


def startlistening(willie, trigger):
    """Sets up the listening process pushing tweets into the channel"""
    global stream
    global listener
    if not listener:
        try:
            streams = [elem.strip() for elem in willie.config.streams.streams.split(",") if elem]
            
            listener=TwitterListener(willie)
            auth = tweepy.OAuthHandler(willie.config.twitter.consumer_key,willie.config.twitter.consumer_secret)
            auth.set_access_token(willie.config.twitter.access_token,willie.config.twitter.access_token_secret)
            
            stream = tweepy.Stream(auth,listener) 
            stream.filter(track=streams)

        except Exception as inst:
            willie.reply(repr(inst))
    else:
        willie.say("Streams already running")

startlistening.commands = ["streams"]
startlistening.priority = "medium"


if __name__ == "__main__":
    print (__doc__.strip())
