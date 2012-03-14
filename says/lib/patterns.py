# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import re

delim = re.compile(unicode(r"[,、。？！\!\?〜＜＞「」【】（）『』\[\]()\<\>]"))

hiragana = re.compile(u"[\u3041-\u309F]*")
katakana = re.compile(u"[\u30A0-\u30FF]*")
kanji = re.compile(u"[\u4E00-\u9FFF]*")

alphabet = re.compile(u"[a-zA-Z0-9\.:+-_\/@]*")
time_pat = re.compile(u"[0-9]*:[0-9]*[a-z]m")

name_pat = re.compile(unicode(r"@[a-zA-Z0-9_]*"))
#url_pat = re.compile(unicode(r"[a-z]*:\/\/[a-zA-Z0-9\.\-\_]*"))
url_short_pat = re.compile(unicode(r"[a-z]*:\/\/[a-zA-Z0-9]*\.[a-zA-Z0-9]*/[a-zA-Z0-9]*"))
hashtag_pat = re.compile(u"(#[a-zA-Z0-9_\u3041-\u309F\u30A0-\u30FF\u4E00-\u9FFF]{2,})")

english_words = [ "in", "at", "an", "it", "on", "of", "the", "for", "if", "now", "by", "is", "be", "are", "were", "have", "my", "your", "from", "say", "to", "not", "fav", "via", "users" ]
english_words += [ "pull", "and", "or", "but", "with", "you", "one", "out", "new", "as", "can", "has" ]
english_words += [ "no", "do", "me", "etc", "vs" ]
english_words += [ "orz", "news", "browsing", "qt", "pc", "nowplaying", "nowbrowsing", "bot", "ch", "id", "sta" ]
english_words += [ "so", "more", "up", "just", "all", "about", "kg", "km", "wktk", "ggrks" ]
user_names = []

twitter_pat = re.compile(unicode(r"[rt|RT]"))

delim_pat = re.compile(u"[、。！？・「」『』【】（）｛｝\(\)\[\]\<\>\!\?\{\}\,\"\']")
word_pat = re.compile(u"[\u30A0-\u30FF]+|[\u3041-\u309F]+|[\u4E00-\u9FFF]+|[a-zA-Z0-9\-\+\.]+")


