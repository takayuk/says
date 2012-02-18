# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import json
import re
import glob
from pit import Pit

from Corpus import Corpus

import site; site.addsitedir("tweepy")
import tweepy


def logging(message):
    
    sys.stdout.write(message + " %s\n" % datetime.now())


def userfriends_fromname(api, db, coll_name, screen_name):

    friends = set([ g.screen_name for g in tweepy.Cursor(api.friends, id=screen_name).items() ])

    time_now = datetime.now()
    stamp = int( time.mktime( time_now.timetuple() ) )
    item = { "screen_name": screen_name, "friends": list(friends), "updated_at": stamp }
    db.append(item)


def activate_api(clientid=3):

    apikeys = Pit.get("twitter_restapi_%02d" % clientid)
    
    # create OAuth handler
    consumer_key, consumer_sec = apikeys["consumer_key"], apikeys["consumer_secret"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_sec)

    # set access token to OAuth handler
    token, token_sec = apikeys["access_token"], apikeys["access_token_secret"]
    auth.set_access_token(token, token_sec)

    # create API
    proxyinfo = Pit.get("proxy")
    api = tweepy.API(auth_handler=auth, proxy_host=proxyinfo["http"], proxy_port=proxyinfo["port"])
    return api


def parse_args():

    usage = "[-f] [path-to-token] [-c] [collection name] [-l] [path-to-log]"
   
    parser = argparse.ArgumentParser(description="sanal.d")
    
    parser.add_argument("-c", "--collname", required=True)
    parser.add_argument("-u", "--screen_name", required=True)
    parser.add_argument("-l", "--log", required=True)

    args = parser.parse_args()
    return args


def extract(line):
    
    try:
        item = json.loads(line)
    except ValueError:
        return None
    
    rawitem = json.loads(item["raw"])
    if rawitem["user"]["lang"] == u"ja":
        return (rawitem["user"]["screen_name"], rawitem["id"], rawitem["created_at"], re.sub("\n", "。", rawitem["text"]))


def friends_of(user, api):

    return set([ g.screen_name for g
        in tweepy.Cursor(api.friends, id=user).items() ])


def pubitems(db, path):

    publicitems = []

    with file(path) as opened:
        items = [ extract(line) for line in opened ]
        publicitems += [ item for item in items if item ]
   
    return publicitems


def useritems(db, path):

    users = users_db.find({})
    for u in users:
        for v in friends_of(u, api):
            pass
        
        



if __name__ == "__main__":

    dbname, collname = sys.argv[1], sys.argv[2]
    db = Corpus(database=dbname, collection=collname)
   
    #basedir = sys.argv[3]

    api = activate_api()
    exit()
   
    for path in glob.glob("%s/*" % basedir):
        publicitems = pubitems(db, path)

        for item in publicitems:
            itemd = dict(zip( ["screen_name", "id", "created_at", "text"], item ))
            db.append(itemd)

        print(path)
