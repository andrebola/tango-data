import json
import requests
from collections import Counter

class LyricCleaner():
    def __init__(self, works):
        self.works = works

    def get_stats(self):
        no_lyrics = 0
        single_verse = 0
        for w in self.works:
            total_lines =0
            for i in w['lyric']:
                for j in i:
                    if j == '\r\n':
                        line_breaks += 1
                    total_lines += 1
            if not total_lines:
                no_lyrics +=1
            if len(w['lyric']) == 1:
                single_verse +=1
        print "Total Works: %d" % len(self.works)
        print "Works with no lyrics: %d" % no_lyrics
        print "Works with lyrics: %d" % (len(self.works) - no_lyrics)
        print "Works with lyrics with only one verse: %d" % single_verse

    def get_lyric_form(self, lyric_array):
        lyric = ''
        for i in lyric_array:
            if len(i)>1:
                ignore =False
                if i[0][0] == '(' and i[0][-1] == ')' or i[0] in (u'Bandone\xf3n,', 'Canto:', 'I', 'II', 'Recitado:'):
                    ignore =True
                for j in range(len(i)):
                    if i[j] == ' ':
                        lyric += '\r\n'
                    elif not ignore or j>0 :
                        lyric += i[j] + '\r\n'
                lyric += '\r\n'
        payload = {'format': 'json', 'radio_method': 'song.segment','lyrics_body': lyric}
        r = requests.get("http://www.lim.di.unimi.it/segmenter/song.segment.php", params=payload)
        return json.loads(r.text)

    def clean_lyrics(self):
        lyrics_form = {}
        for w in self.works:
            while w['id'] not in lyrics_form:
                try:
                    lyrics_form[w['id']] = self.get_lyric_form(w['lyric'])
                except Exception:
                    print "Error retrying %s" % w['id']
                    pass
        self.lyrics_form = lyrics_form
        return lyrics_form

    def get_top_forms(self, top_n):
        return Counter(map(lambda x: ''.join(str(i['section']['section.label']) for i in x), self.lyrics_form.values())).most_common(top_n)
