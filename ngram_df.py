# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys
import extractor
from Corpus import Corpus


if __name__ == "__main__":

    dbname, collname = sys.argv[1], sys.argv[2]
    corpus_db = Corpus(database=dbname, collection=collname)

    df_dbname, df_collname = dbname, sys.argv[3]

    df = {}
    for j, item in enumerate(corpus_db.find({})):
        for word in set( extractor.getwords(item["text"]) ):
            extractor.countup(df, word)

    with file(df_collname, "w") as opened:
        for word, freq in sorted(df.items(), key=lambda x:x[1], reverse=True):
            opened.write("%s\t%d\n" % (word, freq))


