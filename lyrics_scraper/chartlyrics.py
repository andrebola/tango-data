import json
import sys
import urllib
from collections import Counter
from operator import itemgetter
import xml.etree.ElementTree as ET

BASE = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?'

class Chartlyrics(object):

    def get_data(self, artist, title):
        qs_args = {
            'artist': artist.encode('utf-8'),
            'song': title.encode('utf-8'),
        }
        url = BASE + urllib.urlencode(qs_args)
        response = urllib.urlopen(url)
        if response.getcode() == 500:
            return []
        content = response.read()
        data = ET.fromstring(content)
        lyric_elem = data.find('{http://api.chartlyrics.com/}Lyric')
        lyric = lyric_elem.text
        id_elem = data.find('{http://api.chartlyrics.com/}TrackId')
        lyricid_elem = data.find('{http://api.chartlyrics.com/}LyricId')
        song_elem = data.find('{http://api.chartlyrics.com/}LyricSong')
        artist_elem = data.find('{http://api.chartlyrics.com/}LyricArtist')
        url_elem = data.find('{http://api.chartlyrics.com/}LyricUrl')
        rank_elem = data.find('{http://api.chartlyrics.com/LyricRank')

        if lyric != None:
            ret = {
                'track_id': id_elem.text,
                'lyric_id': lyricid_elem.text,
                'song': song_elem.text,
                'artist': artist_elem.text,
                'url': url_elem.text,
                'lyric': lyric}
            if rank_elem != None:
                ret['rank'] = rank_elem.text
            return [ret]
        return []
