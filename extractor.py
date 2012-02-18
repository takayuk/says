#!/usr/bin/env python

# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys
import re
import site; site.addsitedir("python")
import json

import patterns

from Corpus import Corpus


def getid(table, key):
    try:
        id = table[key]
    except KeyError:
        table[key] = len(table)+1
        id = table[key]
    return id


def countup(table, key):
    try:
        table[key] += 1
    except KeyError:
        table[key] = 1


def getwords(text, N=3):

    for tag in patterns.hashtag_pat.findall(text):
        text = unicode( re.sub(tag, "", text) )
    
    for url in patterns.url_short_pat.findall(text):
        text = unicode( re.sub(url, "", text) )
    
    for name in patterns.name_pat.findall(text):
        text = unicode( re.sub(name, "", text) )

    words = []
    for sent in patterns.delim_pat.split(text):
        tok = patterns.word_pat.findall(unicode(sent))

        for n in range(1, N+1):
            for i in range(len(tok)+1-n):
                ngram = tok[i:(i+n)]
                ngram_str = "".join(ngram)
                words.append(ngram_str)

    return words


def main2():
    corpus = {}
    
    db = Corpus(database="sanal", collection=sys.argv[1])
    query = {}
    for i, item in enumerate(db.find(query)):

        text = item["text"]
        words = getwords(unicode(text))

        wordsd = {}
        for w in words:
            countup(wordsd, w)

        doc = { "text": wordsd, "id": item["id"] }
        #u = item["user"]["screen_name"]
        u = item["screen_name"]

        try:
            corpus[u].append(doc)
        except KeyError:
            corpus[u] = [ doc ]
    
        print(i)


    with file(sys.argv[2], "w") as opened:
        for k, v in corpus.items():
            opened.write("%s\n" % json.dumps({k: v}))


def getbigraph(pairs_seq):
   
    graph = networkx.DiGraph()
    graph.add_edges_from(pairs_seq)

    bigraph = networkx.Graph()
    for u in graph.nodes():
        for v in graph.neighbors(u):
            if u in graph.neighbors(v):
                bigraph.add_edge(u, v)

    return bigraph


def getmcc(graph):

    mcc_graph = copy.deepcopy(graph)
    cc = networkx.connected_components(graph)
    mcomp = sorted([ (i, len(comp)) for i, comp in enumerate(cc) ], key=lambda x:x[1], reverse=True)[0]

    for i, comp in enumerate(cc):
        if i != mcomp[0]:
            for n in comp:
                mcc_graph.remove_node(n)

    return mcc_graph


if __name__ == "__main__":

    dbname, collname = sys.argv[1], sys.argv[2]
    db = Corpus(database=dbname, collection=collname)
    path, output_path = sys.argv[1], sys.argv[2]

    pairs = {}
    name_to_id = {}

    graph = networkx.Graph()
    replies = {}

    digraph = networkx.DiGraph()

    with file(path) as opened:
        for line in opened:
            try:
                item = json.loads(line)
            except ValueError:
                continue

            text = item["text"]
            
            u = item["user"]["screen_name"]

            for v in patterns.name_pat.findall(text):
                
                v = re.sub("@", "", v)
                if len(v) < 2: continue

                u_id = regid(name_to_id, u)
                v_id = regid(name_to_id, v)
                
                # Exclude self-loop.
                if u_id == v_id: continue

                #graph.add_edge(u_id, v_id)
                countup( pairs, tuple(sorted([ u_id, v_id ])) )

                if not u_id in replies: replies[u_id] = {}
                countup(replies[u_id], v_id)
                digraph.add_edge(u_id, v_id)

    bigraph = networkx.Graph()
    for u in digraph.nodes():
        for v in digraph.neighbors(u):
            if u in digraph.neighbors(v):
                bigraph.add_edge(u, v)

    bimcc = mcc(bigraph)
    V, E = bimcc.number_of_nodes(), bimcc.number_of_edges()
    print(V, E, float(E) / V)
    
    with file(output_path, "w") as opened:
        for pair in sorted(bimcc.edges(), key = lambda x:x[1], reverse=True):
            
            u, v = pair
            weight = replies[u][v] if replies[u][v] <= replies[v][u] else replies[v][u]
            opened.write("%s\t%s\t%d\n" % (u, v, weight))

    with file(output_path+"_n2i", "w") as opened:
        for k,v in name_to_id.items():
            opened.write("%s\t%d\n" % (k, v))   

