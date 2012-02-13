# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import site; site.addsitedir("python")
import patterns

import sys
import glob
import re
import networkx
import copy


def regid(table, key):
    
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


def mcc(graph):

    mcc_graph = copy.deepcopy(graph)
    cc = networkx.connected_components(graph)
    mcomp = sorted([ (i, len(comp)) for i, comp in enumerate(cc) ], key = lambda x:x[1], reverse=True)[0]

    for i, comp in enumerate(cc):
        if i != mcomp[0]:
            for n in comp:
                mcc_graph.remove_node(n)

    return mcc_graph


if __name__ == "__main__":

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
                if len(v) < 2:
                    continue

                u_id = regid(name_to_id, u)
                v_id = regid(name_to_id, v)
                if u_id == v_id:
                    continue

                graph.add_edge(u_id, v_id)
                countup( pairs, tuple(sorted([ u_id, v_id ])) )

                if not u_id in replies:
                    replies[u_id] = {}
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

    exit()


    mcc_comp = mcc(graph)
    V, E = mcc_comp.number_of_nodes(), mcc_comp.number_of_edges()
    print(V, E, float(E) / V)

    with file(output_path, "w") as opened:
        for pair in sorted(mcc_comp.edges(), key = lambda x:x[1], reverse=True):
            opened.write("%s\t%s\t%d\n" % (pair[0], pair[1], pairs[pair]))

    with file(output_path+"_n2i", "w") as opened:
        for k,v in name_to_id.items():
            opened.write("%s\t%d\n" % (k, v))
