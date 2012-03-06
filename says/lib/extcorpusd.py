# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import urllib2
import extractd


def getitem_fromurl(item):

    for shorturl in extractd.geturls(item):
        try:
            extitem = urllib2.urlopen(shorturl)
        except urllib2.HTTPError:
            extitem = None

    return extitem


