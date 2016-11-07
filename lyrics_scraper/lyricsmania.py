import requests
import urllib
import urllib2
import codecs
import unicodedata
import lxml.html
from Levenshtein.StringMatcher import StringMatcher

class Lyricsmania(object):
    def _remove_accents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def _search(self, artist, title):
        search = "%s %s" % (self._remove_accents(artist), self._remove_accents(title))
        #query = urllib.urlencode({'k': search, 'x':'0', 'y': '0'})
        search = urllib.quote_plus(unicode(search).encode('utf-8'))
        url = u'http://www.lyricsmania.com/searchnew.php?k=%s&x=0&y=0' % search
        #req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
        #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, sdch',
        #'Accept-Language': 'en,es;q=0.8,en-US;q=0.6',
        #'Connection': 'keep-alive' ,
        #'Host':'www.lyricsmania.com'})
        r = requests.get(url, timeout=15)
        #o = urllib2.urlopen(url)
        #response_unicode = codecs.decode(o.read(), 'UTF-8', 'ignore').encode('utf-8')
        page = lxml.html.document_fromstring(r.text)
        links = page.cssselect('.list-search>li>a')

        #this sorting hell is just to find the better result: lyricsmania sucks at this
        resp = []
        search  = u"%s - %s" % (artist.lower(), title.lower())
        for link in links:
            dist = StringMatcher(seq1=link.text.lower().encode('utf-8'),
                    seq2=search.lower().encode('utf-8')).distance()
            if dist > 60:
                print dist
                print link.text +"  ----  "+ search
                resp.append('http://www.lyricsmania.com' + link.get('href').encode('utf-8'))
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
        o = urllib2.urlopen(req)
        response_unicode = codecs.decode(o.read(), 'UTF-8', 'ignore').encode('utf-8')
        page = lxml.html.document_fromstring(response_unicode)
        div = page.cssselect('.')
        if div:
            part1 = ''.join([text.text for text in div])
            div = div.cssselect('. p402_premium')
            return part1 + ''.join([text.text for text in div])
        return ''
