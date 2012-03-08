# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import json
import re
import glob
import time
import argparse
from subprocess import check_call

from datetime import datetime
from pit import Pit
import networkx

import site; site.addsitedir('lib')
from Corpus import Corpus
import extractd
import utils


def logging(message):
    """ Given log-message, logging to specified output stream.
    """
    sys.stdout.write(message + " %s\n" % datetime.now())


def makegraph(items):
    
    
    graph = networkx.Graph()
    weights = {}
    n2i = {}

    for item in items:
        for link in extractd.getmessages(item):
            u, v = link[0], link[1]
            if u == v:
                continue

            uid = utils.getid(n2i, u)
            vid = utils.getid(n2i, v)

            graph.add_edge(uid, vid)
            
            utils.count(weights, (uid, vid))
            utils.count(weights, (vid, uid))
   
    weighted_edges = {}
    for e in graph.edges():
        w = weights[(e[0], e[1])] if weights[(e[0], e[1])] <= weights[(e[1], e[0])] else weights[(e[1], e[0])]
        weighted_edges[ (e[0], e[1]) ] = w

    edges = utils.filter_gt(weighted_edges, 2)

    bigraph = networkx.Graph()
    for e in edges:
        bigraph.add_edge(e[0], e[1], weight = edges[e])
    
    return bigraph, n2i


def getedges_from(graph):

    edges = []
    for u in graph:
        for v in graph[u]:
            edges.append((u, v, graph[u][v]))

    return edges


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

    t_end = time.mktime( datetime.today().timetuple() )
    t_begin = t_end - (24 * 60 * 60 * 10)
 
    items = [ item for item in db.find({'created_at': { '$gt': t_begin, '$lt': t_end }}) ]
    graph, n2i = makegraph(items)

    with file('%s/n2i' % sys.argv[1], 'w') as opened:
        for u, uid in n2i.items():
            opened.write('%s\t%d\n' % (u, uid))

    ccomps = extractd.ccd(graph)
    for i, ccomp in enumerate(ccomps):
        
        if ccomp.number_of_nodes() < 20:
            continue

        if ccomp.number_of_edges() < 100:
            continue

        with file('%s/graph_%03d' % (sys.argv[1], i), 'w') as opened:
            for u, v, d in ccomp.edges(data=True):
                opened.write('%d\t%d\t%d\n' % (u, v, d['weight']))

    i2n = dict( (v, k) for k, v in n2i.iteritems() )

    binpath = "%s/clstr" % os.path.abspath(sys.argv[2])
    for path in glob.glob('%s/graph_*' % sys.argv[1]):
        basepath = os.path.abspath(path)
        destpath = os.path.abspath(path) + '.clstr'

        check_call([ binpath, basepath, destpath ])

        namebuffer = []
        with file(destpath) as opened:
            for line in opened:
                namebuffer.append(' '.join([ i2n[int(uid)] for uid in line.strip().split() ]))

        with file(destpath + 'n', 'w') as opened:
            opened.write('\n'.join(namebuffer))

