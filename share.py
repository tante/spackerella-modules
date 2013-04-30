"""
share.py - Willie Twitter Module
Copyright 2013, tante, tante@tante.cc
Licensed under the Eiffel Forum License 2.

(based on the twitter module from the willie distribution)
"""

import tweepy
import urllib

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

def f_update(willie, trigger):
    """Share with Willie's Twitter/identi.ca/ADN account. Admin-only."""
    if trigger.admin:
        # twitter API
        auth = tweepy.OAuthHandler(willie.config.twitter.consumer_key, willie.config.twitter.consumer_secret)
        auth.set_access_token(willie.config.twitter.access_token, willie.config.twitter.access_token_secret)
        api = tweepy.API(auth)
        # identi.ca needs no api
        passwd_manager = urllib.request.HTTPPasswordMgr()
        passwd_manager.add_password("Identi.ca API", "http://identi.ca/api/statuses", willie.config.share.identica_user, willie.config.share.identica_pass)
        auth_handler = urllib.request.HTTPBasicAuthHandler(passwd_manager)
        page_opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(page_opener)
        # ADN
        app = adn.ADN(access_token=willie.config.share.adn_access_token)
        update = str(trigger.group(2))

        if len(update) <= 140:
            #twitter
            api.update_status(update)
            #ADN (which throws an exception just for fun)
            try:
                app.createPost(text=update)
            except:
                pass
            #identi.ca
            parms = urllib.parse.urlencode({'status': update})
            parms = parms.encode("utf8")
            resp = urllib.request.urlopen("http://identi.ca/api/statuses/update.xml", parms)
            resp.read().decode("utf8")
            
            willie.reply("Successfully posted to my Social Media  accounts.")
        else:
            toofar = len(update) - 140
            willie.reply("Please shorten the length of your message by: " + str(toofar) + " characters. To post to Twitter and Identi.ca")

f_update.commands = ['post']
f_update.priority = 'medium'
f_update.example = '.post Hello World!'

if __name__ == '__main__':
    print __doc__.strip()
