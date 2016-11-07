import urllib
import urllib2
import lxml.html
import json

class Musixmatch(object):

    def _search(self, artist, title):
        search = "%s %s" % (artist, title)
        search = urllib.quote_plus(unicode(search).encode('utf-8'))
        url = 'https://www.musixmatch.com/search/%s/tracks' % search
        page = lxml.html.parse(urllib2.urlopen(url))
        links = page.getroot().cssselect('.showArtist')
        ret = []
        for i in links:
            inner_content = i.cssselect('.has-secondary-actions')
            if not len(inner_content):
                links = i.cssselect('.title')
                ret.append(links[0].get('href'))
        return ret

    def get_data(self, artist, title):
        urls = self._search(artist, title)
        ret = []
        for url in urls:
            ret.append(self._get_lyrics_from_url(url))
        return ret

    def _get_lyrics_from_url(self, url):
        page = lxml.html.parse(urllib2.urlopen('https://www.musixmatch.com'+url))
        for s in page.getroot().cssselect('script'):
            c = s.text_content()
            if '__mxmState' in c:
                content = c.split('var __mxmState = ')
                return json.loads(content[1][:-1])
        return {}
