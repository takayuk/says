# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import urllib2
import extractd

import threading
import time

def splitseq(seq, size=None, count=None):
    
    if count:
        subseq_size = len(seq) / count
        subseq = [ seq[i:i+subseq_size] for i in range(0, len(seq), subseq_size) ]

        if (len(seq) % count) > 0:
            subseq[-2] += subseq[-1]
            del(subseq[-1])
        return subseq

    elif size:
        return [ seq[i:i+size] for i in range(0, len(seq), size) ]
    
    else:
        return None


class ExternURLOpener(threading.Thread):

    def __init__(self, urls, externitems, interval=1.0):
        threading.Thread.__init__(self)

        self.urls = urls
        self.interval = interval
        self.externitems = externitems


    def run(self):

        items = []

        for i, shorturl in enumerate(self.urls):
            try:
                item = urllib2.urlopen(shorturl)
                self.externitems.append({ "shorturl": shorturl, "url": item.url, "item": item.read() })
            except urllib2.HTTPError:
                item = None
            except AttributeError:
                item = None
            except urllib2.URLError:
                item = None
            finally:
                time.sleep(self.interval)


if __name__ == '__main__':
    pass
