import re
import requests
import json
from  bs4 import BeautifulSoup

class Lyricswikia(object):
    def get_data(self, artist, title):
       url = self._search(artist, title)
       if url:
           lyrics = self._get_lyrics_from_url(url)
           return {'lyrics': lyrics}
       return []

    def _search(self, artist, title):
        url = u'http://lyrics.wikia.com/api.php?action=lyrics&artist={artist}&song={title}&fmt=json&func=getSong'.format(artist=artist,
                                                                                                                        title=title).replace(" ","%20")
        r = requests.get(url, timeout=15)
        # We got some bad formatted JSON data... So we need to fix stuff :/
        returned = r.text
        returned = returned.replace('"', "")
        returned = returned.replace("\'", "\"")
        returned = returned.replace("song = ", "")
        returned = json.loads(returned)
        if returned["lyrics"] != "Not found":
            return returned["url"]
        return None

    def _get_lyrics_from_url(self, url):
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text)
        soup = soup.find("div", {"class": "lyricbox"})
        [elem.extract() for elem in soup.findAll('div')]
        [elem.replaceWith('\n') for elem in soup.findAll('br')]
        #with old BeautifulSoup the following is needed..? For recent versions, this isn't needed/doesn't work
        try:
            soup = BeautifulSoup(str(soup), convertEntities=BeautifulSoup.HTML_ENTITIES)
        except:
            pass
        soup = BeautifulSoup(re.sub(r'(<!--[.\s\S]*-->)', '', str(soup)))
        [elem.extract() for elem in soup.findAll('script')]
        return(soup.getText())
