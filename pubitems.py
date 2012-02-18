# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import json
import re
import glob
from Corpus import Corpus


def extract(line):
    
    try:
        item = json.loads(line)
    except ValueError:
        return None
    
    rawitem = json.loads(item["raw"])
    if rawitem["user"]["lang"] == u"ja":
        return (rawitem["user"]["screen_name"], rawitem["id"], rawitem["created_at"], re.sub("\n", "。", rawitem["text"]))


def pubitems(db, path):

    publicitems = []

    with file(path) as opened:
        items = [ extract(line) for line in opened ]
        publicitems += [ item for item in items if item ]
   
    return publicitems


if __name__ == "__main__":

    dbname, collname = sys.argv[1], sys.argv[2]
    db = Corpus(database=dbname, collection=collname)
   
    basedir = sys.argv[3]
   
    for path in glob.glob("%s/*" % basedir):
        publicitems = pubitems(db, path)

        for item in publicitems:
            itemd = dict(zip( ["screen_name", "id", "created_at", "text"], item ))
            db.append(itemd)

        print(path)
