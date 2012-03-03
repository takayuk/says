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

exclude = []
exclude += [u"今日", u"自分", u"ニュース", u"時間", u"ビジネス", u"経済", u"明日", u"仕事", u"日本", u"問題", u"必要", u"ツイート"]
exclude += [u"意味", u"会社", u"本当", u"出来", u"アプリ", u"一番", u"参加", u"理解", u"女性", u"ツイッタ", u"本日", u"テレビ"]
exclude += [u"簡単", u"動画", u"対応", u"大変", u"一緒", u"友達", u"状態", u"公開", u"リア", u"今年", u"記事", u"女子", u"予定"]
exclude += [u"最初", u"帰宅", u"相手", u"大事", u"画像", u"質問", u"勝手", u"面倒", u"面倒臭", u"話題", u"大人", u"電話", u"学校", u"バイト"]
exclude += [u"発言", u"気分", u"絶対", u"他人", u"状況", u"開始", u"余裕", u"重要", u"結構", u"毎日", u"以外", u"仕方", u"正直"]

# 時間に関する単語
exclude += [u"回目", u"年後", u"今朝", u"今晩", u"最近", u"一瞬", u"過去", u"未来", u"現在", u"午前", u"午後", u"一日"]

# 程度に関する単語
exclude += [u"程度", u"実際", u"最高", u"最低", u"十分", u"普通", u"多分"]

# その他
exclude += [u"気持", u"場合", u"場所", u"結局", u"無理", u"是非", u"間違", u"面白", u"早速"]

# カタカナ語
exclude += [u"オレ", u"アレ", u"コレ", u"マジ", u"クソ", u"カス", u"クズ", u"ヨロシク", u"ニュ", u"スゴ", u"ダサ", u"ダメ"]

# 何
exclude += [u"何日", u"何回", u"何年", u"何度"]

delim_pat = re.compile(u"[、。！？・「」『』【】（）｛｝\(\)\[\]\<\>\!\?\{\}\,\"\']")
word_pat = re.compile(u"[\u30A0-\u30FF]+|[\u3041-\u309F]+|[\u4E00-\u9FFF]+|[a-zA-Z0-9\-\+\.]+")


