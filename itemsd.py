# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import json
import re
import glob
import time
import argparse

from datetime import datetime
from pit import Pit

from Corpus import Corpus
import extractd

import site; site.addsitedir("tweepy")
import tweepy


def logging(message):
    """ Given log-message, logging to specified output stream.
    """
    sys.stdout.write(message + " %s\n" % datetime.now())


def activate_api(clientid=3):
    """ Given client-id, activate Twitter REST API corresponds client-id.
    """
    apikeys = Pit.get("twitter_restapi_%02d" % clientid)
    
    # create OAuth handler
    cons_key, cons_sec = apikeys["consumer_key"], apikeys["consumer_secret"]
    auth = tweepy.OAuthHandler(cons_key, cons_sec)

    # set access token to OAuth handler
    token, token_sec = apikeys["access_token"], apikeys["access_token_secret"]
    auth.set_access_token(token, token_sec)

    # create API
    proxy = Pit.get("proxy")
    url, port = proxy["http"], proxy["port"]
    
    api = tweepy.API(auth_handler=auth, proxy_host=url, proxy_port=port)
    return api


def response_to_item(response):

    item = {}
    item["text"] = response.text
    item["id"] = int(response.id_str)

    item["created_at"] = int(time.mktime( response.created_at.timetuple() ))
    
    item["screen_name"] = response.author.screen_name

    return item
        

def friends_of(user, api):

    return set([ g.screen_name for g
        in tweepy.Cursor(api.friends, id=user).items() ])


def useritems(db, screen_name):

    try:
        latestitem = db.findsorted(query={ "screen_name": screen_name }, key="id")[0]
        since_id = latestitem["id"]
        
        return [ response_to_item(res) for res
                in api.user_timeline(id=screen_name, since_id=since_id) ]
    except:
        return [ response_to_item(res) for res
                in api.user_timeline(id=screen_name, count=50) ]


def getmessages(db, items):

    for item in items:
        for reply_item in extractd.getmessages(item):

            v = reply_item[1]
            try:
                v_items = useritems(db, v)
            except tweepy.error.TweepError:
                continue

            for item in v_items: db.append(item)
            logging( "%s updated (%d items added)" % (v, len(v_items)) )


def getitems(users, api, db):
    
    for u in users:
        try:
            gamma_u = friends_of(u, api)
        except tweepy.error.TweepError:
            continue

        for v in gamma_u:
            try:
                items = useritems(items_db, v)
            except tweepy.error.TweepError:
                continue

            for item in items: db.append(item)
            logging( "%s updated (%d items added)" % (v, len(items)) )
            
            getmessages(db, items)

            try:
                req_remain = api.rate_limit_status()["remaining_hits"]
                logging("API request limit: %d" % req_remain)
            except tweepy.error.TweepError:
                continue
      
            time.sleep(args.interval)


def parse_args():

    usage = "[--interval] [interval] [-l] [path-to-log]"
   
    parser = argparse.ArgumentParser(description="says")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("-l", "--log", default=".log/log")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()

    dbinfo = Pit.get("says")

    users_db = Corpus(database=dbinfo["db"], collection=dbinfo["users"])
    #users = users_db.find({})
    users = [ item["screen_name"] for item in users_db.find({}) ]

    api = activate_api()

    items_db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    getitems(users, api, items_db)

