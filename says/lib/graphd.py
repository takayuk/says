# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from Corpus import Corpus
import extractd

from pit import Pit
from datetime import datetime
import time
import networkx

import sys


def make_graph(items):

    graph = networkx.Graph()
    weights = {}
    n2i = {}

    for item in items:
        for link in extractd.getmessages(item):
            u, v = link[0], link[1]
            if u == v:
                continue

            uid = extractd.getid(n2i, u)
            vid = extractd.getid(n2i, v)

            graph.add_edge(uid, vid)
            
            extractd.countup(weights, (uid, vid))
            extractd.countup(weights, (vid, uid))

    with file('%s.wpairs' % sys.argv[1], 'w') as opened:

        for e in graph.edges():
            w = weights[(e[0], e[1])] if weights[(e[0], e[1])] <= weights[(e[1], e[0])] else weights[(e[1], e[0])]
            opened.write( '%d\t%d\t%d\n' % (e[0], e[1], w) )

    with file('%s.n2i' % sys.argv[1], 'w') as opened:
        for u in n2i:
            opened.write('%s\t%d\n' % (u, n2i[u]))


if __name__ == '__main__':
    
    dbinfo = Pit.get("says")
    db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    t_end = time.mktime( datetime.today().timetuple() )
    t_begin = t_end - (24 * 60 * 60 * 10)
 
    items = [ item for item in db.find({'created_at': { '$gt': t_begin, '$lt': t_end }}) ]

    make_graph(items)
