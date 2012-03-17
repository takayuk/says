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
import patterns
import bagofwords as bow


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


def feature(t_begin, t_end, screen_names):

    ngram = {}
    table = {}

    for j, u in enumerate(screen_names):
        query = { 'created_at': { '$gt': t_begin, '$lt': t_end }, 'screen_name': u }
        for item in db.find(query):
            text = item['text']
            id = item['id']

            try:
                replied_id = item['in_reply_to_status_id']
                if replied_id:
                    for ii in db.find({ 'id': replied_id }):
                        text += u'。%s' % ii['text']
                
            except KeyError:
                pass

            """
            feats = bow.bagofwords(text)
            for f in feats:
                print(' '.join(f))
            continue
            """
            feat = extractd.getngram(text)
            for w in set(feat):
                if len(unicode(w)) < 2:
                    continue
                if len(patterns.hiragana.findall(unicode(w))[0]) == len(unicode(w)):
                    continue
                if w in patterns.english_words:
                    continue

                if not w in ngram: ngram[w] = {}
                
                utils.count(ngram[w], u)
                try:
                    #table[w].append(text)
                    table[w].add(id)
                except KeyError:
                    #table[w] = [ text ]
                    table[w] = set([ id ])

            tags = extractd.gethashtags(item)
            for t in set(tags):
                if not t in ngram: ngram[t] = {}
                
                utils.count(ngram[t], u)
                try:
                    #table[t].append(text)
                    table[t].add(id)
                except KeyError:
                    #table[t] = [ text ]
                    table[t] = set([ id ])

            urls = extractd.geturls(item)
            for l in set(urls):
                if not l in ngram: ngram[l] = {}

                utils.count(ngram[l], u)
                try:
                    #table[l].append(text)
                    table[l].add(id)
                except KeyError:
                    #table[l] = [ text ]
                    table[l] = set([ id ])

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

    names = [ line.strip().split() for line in open('temp/graph_000.clstrn').readlines() ]
    cid = int(sys.argv[1])
    
    t_current = datetime.today()
    
    t_begin, t_end = t_current - timedelta(3), t_current - timedelta(2)
    t_begin_u, t_end_u = time.mktime( t_begin.timetuple() ), time.mktime( t_end.timetuple() )
    w_y, table_y = feature(t_begin_u, t_end_u, names[cid])
    
    t_begin, t_end = t_current - timedelta(2), t_current - timedelta(1)
    t_begin_u, t_end_u = time.mktime( t_begin.timetuple() ), time.mktime( t_end.timetuple() )
    w_t, table_t = feature(t_begin_u, t_end_u, names[cid])

    hot = {}
    for w in w_t:

        f_w_y = len(w_y.get(w, []))+1
        f_w_t = len(w_t[w])+1
        if f_w_t < 3 or f_w_t <= f_w_y:
            continue

        hot[w] = math.log( float(f_w_t) / f_w_y )

    with file('temp/Y_%03d' % cid, 'w') as opened:
        for w in sorted(hot.items(), key=lambda x:x[1], reverse=True):

            if w[1] < 1.7: break

            opened.write('!!! %s\t%d\t%d\t%f\n' % (w[0], len(w_y.get(w[0], [])), len(w_t[w[0]]), w[1]))
            opened.write('\n'.join([ str(id) for id in w[0] ]))
            """
            opened.write('\n'.join(table_y.get(w[0], [''])))
            opened.write('\n#############\n')
            opened.write('\n'.join(table_t[w[0]]))
            opened.write('\n---\n')
            """
