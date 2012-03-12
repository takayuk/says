# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import json
import re
import glob
import time
import argparse
import math
from datetime import datetime, timedelta
from pit import Pit

import site; site.addsitedir('lib')
from Corpus import Corpus
import extractd
import utils


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


def feature(t_begin, t_end, screen_names, type='tfidf'):

    ngram = {}
    table = {}

    for j, u in enumerate(screen_names):
        query = { 'created_at': { '$gt': t_begin, '$lt': t_end }, 'screen_name': u }
        for item in db.find(query):
            text = item['text']
            
            feat = extractd.getngram(text)
            for w in set(feat):
                if not w in ngram: ngram[w] = {}
                
                utils.count(ngram[w], u)
                try:
                    table[w].append(text)
                except KeyError:
                    table[w] = [ text ]

        print('%d/%d' % (j, len(screen_names)))
    return ngram, table


def parse_args():

    usage = "[--tbegin] [t_begin] [--tend] [t_end]"
   
    parser = argparse.ArgumentParser(description="says")
    #parser.add_argument("--tbegin", required=True)
    #parser.add_argument("--tend", required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    #args = parse_args()
    
    dbinfo = Pit.get("says")
    db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    wtables = []

    day_ago, day_span = 3, 1
    
    names = [ line.strip().split() for line in open('temp/graph_000.clstrn').readlines() ]
    cid = int(sys.argv[1])
    
    t_current = datetime.today()
    
    t_begin, t_end = t_current - timedelta(2), t_current - timedelta(1)
    t_begin_u, t_end_u = time.mktime( t_begin.timetuple() ), time.mktime( t_end.timetuple() )
    w_y, table_y = feature(t_begin_u, t_end_u, names[cid])
    
    t_begin, t_end = t_current - timedelta(1), t_current
    t_begin_u, t_end_u = time.mktime( t_begin.timetuple() ), time.mktime( t_end.timetuple() )
    w_t, table_t = feature(t_begin_u, t_end_u, names[cid])

    hot = {}
    for w in w_y:
        if not w in w_t:
            continue

        f_w_y = len(w_y[w])+1
        f_w_t = len(w_t[w])+1

        hot[w] = math.log( float(f_w_t) / f_w_y )

    with file('Y_%03d' % cid, 'w') as opened:
        for w in sorted(hot.items(), key=lambda x:x[1], reverse=True):
            opened.write('%s\t%d\t%d\t%f\n' % (w[0], len(w_y[w[0]]), len(w_t[w[0]]), w[1]))
            opened.write('\n'.join(table_y[w[0]]))
            opened.write('\n#############\n')
            opened.write('\n'.join(table_t[w[0]]))
            opened.write('\n---\n')

