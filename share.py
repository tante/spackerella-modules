"""
share.py - Willie Twitter Module
Copyright 2013, tante, tante@tante.cc
Licensed under the Eiffel Forum License 2.

(based on the twitter module from the willie distribution)
"""

import tweepy
import time
import re

def configure(config):
    """This module takes its Twitter configuration from the twitter module.
    For identi.ca you have to give name and password.
    ADN is used via the access token you can get via http://jonathonduerig.com/dev-lite/
    """
    
    if config.option('Configure Share?', False):
        config.interactive_add('share', 'adn_access_token', 'adn_access_token')
        config.interactive_add('share', 'identica_user', 'identica_user')
        config.interactive_add('share', 'identica_pass', 'identica_pass')
        pass

def format_thousands(integer):
    """Returns string of integer, with thousands separated by ','"""
    return re.sub(r'(\d{3})(?=\d)', r'\1,', str(integer)[::-1])[::-1]

def f_update(willie, trigger):
    """Share with Willie's Twitter/identi.ca/ADN account. Admin-only."""
    if trigger.admin:
        # twitter API
        auth = tweepy.OAuthHandler(willie.config.twitter.consumer_key, willie.config.twitter.consumer_secret)
        auth.set_access_token(willie.config.twitter.access_token, willie.config.twitter.access_token_secret)
        api = tweepy.API(auth)
        # identi.ca needs no api

        update = str(trigger.group(2))

        if len(update) <= 140:
            api.update_status(update)
            willie.reply("Successfully posted to my twitter account.")
        else:
            toofar = len(update) - 140
            willie.reply("Please shorten the length of your message by: " + str(toofar) + " characters. To post to Twitter and Identi.ca")

f_update.commands = ['share']
f_update.priority = 'medium'
f_update.example = '.share Hello World!'

if __name__ == '__main__':
    print __doc__.strip()
