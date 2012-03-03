#!/usr/bin/env python

# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys
import re
import site; site.addsitedir("python")
import json
import argparse

import extractd

from Corpus import Corpus


def parse_args():

    usage = "[--interval] [interval] [-l] [path-to-log]"
   
    parser = argparse.ArgumentParser(description="says")

    parser.add_argument("-d", "--database", default="says")
    
    parser.add_argument("-i", "--items", default="items")
    parser.add_argument("-s", "--itemstats", default="itemstats")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()

    db = Corpus(database=args.database, collection=args.items)
    db_stats = Corpus(database=args.database, collection=args.itemstats)
    
    try:
        latstats = db_stats.findsorted({}, key="id")[0]["id"]
    except IndexError:
        latstats = 0L

    for i, item in enumerate(db.find({ "id": { "$gt": latstats }})):

        words = extractd.getwords(item)
        messages = extractd.getmessages(item)
        tags = extractd.gethashtags(item)
        urls = extractd.geturls(item)
        
        db_stats.append({
            "screen_name": item["screen_name"]
            , "words": words
            , "messages": messages
            , "hashtags": tags
            , "urls": urls
            , "created_at": item["created_at"]
            , "id": item["id"] })
       
        print(i, item["id"])

