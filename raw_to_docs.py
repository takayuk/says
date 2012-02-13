# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys
import re
import site; site.addsitedir("python")
import json

import patterns

from Corpus import Corpus

delim_pat = re.compile(u"[、。！？・「」『』【】（）｛｝\(\)\[\]\<\>\!\?\{\}\,]")
word_pat = re.compile(u"[\u30A0-\u30FF]+|[\u3041-\u309F]+|[\u4E00-\u9FFF]+|[a-zA-Z0-9\-\+\.]+")


def countup(t, k):
    try:
        t[k] += 1
    except KeyError:
        t[k] = 1


def extract_words(text, N=3):

    for tag in patterns.hashtag_pat.findall(text):
        text = unicode( re.sub(tag, "", text) )
    
    for url in patterns.url_short_pat.findall(text):
        text = unicode( re.sub(url, "", text) )
    
    for name in patterns.name_pat.findall(text):
        text = unicode( re.sub(name, "", text) )

    words = []
    for sent in delim_pat.split(text):
        tok = word_pat.findall(unicode(sent))

        for n in range(1, N+1):
            for i in range(len(tok)+1-n):
                ngram = tok[i:(i+n)]
                ngram_str = "".join(ngram)
                words.append(ngram_str)

    return words


if __name__ == "__main__":

    corpus = {}
    
    db = Corpus(database="sanal", collection=sys.argv[1])
    query = {}
    for i, item in enumerate(db.find(query)):

        text = item["text"]
        words = extract_words(unicode(text))

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

