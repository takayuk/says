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

import site; site.addsitedir('lib')
from Corpus import Corpus
import extractd


def logging(message):
    """ Given log-message, logging to specified output stream.
    """
    sys.stdout.write(message + " %s\n" % datetime.now())


def getdf_from(items):
    
    df = {}
    for item in items:
        feat = extractd.getngram(item['text']) 

        for w in feat:
            try:
                df[w].add(item["id"])
            except KeyError:
                df[w] = set([ item['id'] ])

    #return [ (w, len(f)) for w, f in df.items() ]
    return df


"""
def feature(t_begin, t_end, type='tfidf'):

    df = {}
    for item in db.find({'created_at': { '$gt': t_begin, '$lt': t_end }}):
        feat = extractd.getngram(item['text']) 

        for w in feat:
            extractd.countup(tf, w)

            try:
                df[w].add(item["id"])
            except KeyError:
                df[w] = set([ item['id'] ])

    for x in sorted(df.items(), key=lambda x:len(x[1]), reverse=True):
        print('%s\t%d' % (x[0], len(x[1])))
"""


def parse_args():

    usage = "[--tbegin] [t_begin] [--tend] [t_end]"
   
    parser = argparse.ArgumentParser(description="says")
    parser.add_argument("--tbegin", required=True)
    parser.add_argument("--tend", required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()

    dbinfo = Pit.get("says")

    db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    t_begin_u = time.mktime( datetime.strptime(args.tbegin, '%Y%m%d').timetuple() )
    t_end_u = time.mktime( datetime.strptime(args.tend, '%Y%m%d').timetuple() )
    feature(t_begin_u, t_end_u)

