import urllib
import urllib2
import unicodedata
import lxml.html
from Levenshtein.StringMatcher import StringMatcher

class Songlyrics(object):
    def _remove_accents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def _search(self, artist, title):
        artist = self._remove_accents(artist.lower())
        title = self._remove_accents(title.lower())
        search = "%s %s" % (artist, title)
        search = urllib.quote_plus(unicode(search).encode('utf-8'))
        url = u'http://www.songlyrics.com/index.php?section=search&searchW=%s&submit=Search&searchIn1=artist&searchIn3=song' % search
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = lxml.html.parse(urllib2.urlopen(req))
        links = page.getroot().cssselect('.serpresult')
        resp = []
        search_original = u"%s - %s" % (artist.lower(), title.lower())
        if len(links):
            for link in links:
                current_song = link.cssselect('h3>a')
                if len(current_song) and current_song[0].text != None:
                    song_title = current_song[0].text.replace('Lyrics', '')
                    song_artist = link.cssselect('.serpdesc-2>p>a')[0].text

                    search = u"%s - %s" % (song_artist.lower(), song_title.lower())
                    dist_artist = StringMatcher(seq1=artist.lower(), seq2=unicode(song_artist.lower())).distance()
                    dist_title =  StringMatcher(seq1=title.lower(), seq2=unicode(song_title.lower())).distance()
                    if dist_artist > 60 and dist_title > 60:
                        resp.append(current_song[0].get('href'))
        return resp

    def get_data(self, artist, title):
        urls = self._search(artist, title)
        ret = []
        for url in urls:
            lyr = self._get_lyrics_from_url(url)
            if lyr:
                ret.append(lyr)
        return ret

    def _get_lyrics_from_url(self, url):
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        content = urllib2.urlopen(req)
        page = lxml.html.parse(content)
        div = page.getroot().get_element_by_id('songLyricsDiv')
        text = ''.join([text for text in div.itertext()])
        return text
