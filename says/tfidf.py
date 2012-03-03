# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import sys

path=sys.argv[1]

tfidf_thresh = float(sys.argv[2])

df={}
with file(path) as opened:
    for line in opened:
        item=json.loads(line)

        words = []
        for docs in item.values():
            for item in docs:
                words += item["text"].keys()

        words = list(set(words))
        for w in words:
            try:
                df[w] += 1
            except KeyError:
                df[w] = 1


with file(path) as opened:
    for line in opened:
        item=json.loads(line)

        u = item.keys()[0]

        tf = {}
        for docs in item.values():
            for item in docs:
                words = item["text"].items()
                for w in words:
                    try:
                        tf[w[0]] += w[1]
                    except KeyError:
                        tf[w[0]] = w[1]


        tfidf = {}
        for w in tf:
            if df[w] < 2: continue
            tfidf[w] = float(tf[w]) / df[w]
       
        impwords = [ w for w in sorted(tfidf.items(), key=lambda x:x[1], reverse=True)
                if w[1] > tfidf_thresh ]

        if len(impwords) > 0:
            for w in impwords:
                print("%s\t%f" % (w[0], w[1]))
            
            print("--- %s " % u)
