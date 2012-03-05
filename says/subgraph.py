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


def getgraph(items):

    messages = []
    for item in items:
        messages += extractd.getmessages(item)

    graph, name_to_id = {}, {}
    for message in messages:
        u, v = message[0], message[1]

        u_id = extractd.getid(name_to_id, u)
        v_id = extractd.getid(name_to_id, v)

        if not u_id in graph: graph[u_id] = {}
        extractd.countup(graph[u_id], v_id)

        if not v_id in graph: graph[v_id] = {}
        extractd.countup(graph[v_id], u_id)

    return graph, name_to_id


def ccd(graph):
    return extractd.ccd(graph)


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

    args = parse_args()

    dbinfo = Pit.get("says")

    db = Corpus(database=dbinfo["db"], collection=dbinfo["items"])

    t_begin_u = time.mktime( datetime.strptime(args.tbegin, '%Y%m%d').timetuple() )
    t_end_u = time.mktime( datetime.strptime(args.tend, '%Y%m%d').timetuple() )
    getgraph( db.find({"created_at": {'$gt': t_begin_u, '$lt': t_end_u} }) )

