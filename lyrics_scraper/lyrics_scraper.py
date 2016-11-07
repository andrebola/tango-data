import os
import json

import lyricswikia
import lyricsmania
import minilyrics
import musixmatch
import songlyrics

class LyricsScraper(object):
    def get_lyrics(self, works, artists):
        '''lyrics_tango_server = json.load(open('../data/lyric.json'))
        for lyric in lyrics_tango_server:
            lyric_str = ""
            offset = 1
            cont = True
            for line in lyric['body'].split('\n')[1:]:
                if len(line) == 0 or cont and ('Letra de ' in line or 'Musica de ' in line
                        or 'Compuesto en ' in line or 'Matriz ' in line):
                    cont = True
                    offset += 1

                else:
                    cont = False
                    lyric_str += line + '\n'
        '''
        sources = {
                'lyricswikia': lyricswikia.Lyricswikia(),
                'lyricsmania': lyricsmania.Lyricsmania(),
                'minilyrics': minilyrics.Minilyrics(),
                'musixmatch': musixmatch.Musixmatch(),
                'songlyrics': songlyrics.Songlyrics()
                }
        for w in works:
            for source in sources.keys():
                directory = "../data/lyrics/%d" % (w['id'])
                if not os.path.exists(directory):
                    os.makedirs(directory)
                location = os.path.join(directory, source+'.json')
                if not os.path.exists(location):
                    lyrics = []
                    search_artists = set(w['lyricists'] + w['composers'])
                    for a in search_artists:
                        ret = sources[source].get_data(artists[a]['name'], w['title'])
                        if len(ret):
                            lyrics.append(ret)
                    with open(location, 'w') as fp:
                        json.dump(lyrics, fp)


