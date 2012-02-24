# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import networkx
from networkx.utils import powerlaw_sequence

import numpy

z = networkx.utils.create_degree_sequence(100, powerlaw_sequence)
G = networkx.configuration_model(z)

G = networkx.Graph(G)
G.remove_edges_from(G.selfloop_edges())


with file("karate.wpairs", "w") as opened:
    for e in G.edges():
        opened.write("%d\t%d\t%d\n" % (e[0], e[1], numpy.random.poisson(4)+1))

