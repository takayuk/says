#!/usr/bin/env python

# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import site; site.addsitedir('lib')

from Corpus import Corpus
import feature
import subgraph


from pit import Pit
from datetime import datetime
import time

import memcache


if __name__ == '__main__':

    mc = memcache.Client('localhost:11211')
    mc.flush_all()

    dbinfo = Pit.get("says")
    db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    t_end = time.mktime( datetime.today().timetuple() )
    t_begin = t_end - 24 * 60 * 60
    
    items = [ item for item in db.find({'created_at': { '$gt': t_begin, '$lt': t_end }}) ]
    itemsd = {}
    for i in items:
        try:
            itemsd[i["screen_name"]].append(i)
        except KeyError:
            itemsd[i["screen_name"]] = [ i ]


    global_df = feature.getdf_from(items)

    graph, n2i = subgraph.getgraph(items)
    i2n = dict( (v, k) for k, v in n2i.iteritems() )
    #edges = subgraph.getedges_from(graph)
    
    cc = subgraph.ccd(graph)
    for cid, comp in enumerate(cc):
        if len(comp) < 10: continue

        localitems = []
        for u in comp:
            try:
                name = unicode( i2n[u] )
                localitems += itemsd[name]
            except KeyError:
                continue

        local_df = feature.getdf_from(localitems)

        words = [ (w, float(len(local_df[w])) / len(global_df[w])) for w in local_df if len(local_df[w]) > 1 ]

        hotwords = [ hw[0] for hw in sorted(words, key=lambda x:x[1], reverse=True)[:20] ]

        mc.set(str(cid), hotwords)

