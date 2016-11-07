import hashlib
import json
import xmltodict
import requests

from xml.parsers.expat import ExpatError

class Minilyrics(object):

    def _search(self, artist, title):
        search_url = "http://search.crintsoft.com/searchlyrics.htm"
        search_md5watermark = b"Mlv1clt4.0"
        search_query_base = u"<?xml version='1.0' encoding='utf-8' standalone='yes' ?><searchV1 client=\"ViewLyricsOpenSearcher\" artist=\"{artist}\" title=\"{title}\" OnlyMatched=\"1\" />"
        data = self._vl_enc(search_query_base.format(artist=artist, title=title).encode("utf-8"), search_md5watermark)
        headers = {"User-Agent": "{ua}".format(ua="MiniLyrics"),
                   "Content-Length": "{content_length}".format(content_length=len(data)),
                   "Connection": "Keep-Alive",
                   "Expect": "100-continue",
                   "Content-Type": "application/x-www-form-urlencoded"
                   }
        fail_count = 0
        ret = ""
        while (ret == "") and (fail_count < 5):
            try:
                r = requests.post(search_url, data=data, headers=headers)
                ret = r.text
                return ret
            except Exception as exceptio:
                print(exceptio)
            fail_count += 1
        return None

    def _hexToStr(self, hexx):
        string = ''
        i = 0
        while (i < (len(hexx) - 1)):
            string += chr(int(hexx[i] + hexx[i + 1], 16))
            i += 2
        return (string)

    def _vl_enc(self, data, md5_extra):
        datalen = len(data)
        md5 = hashlib.md5()
        md5.update(data + md5_extra)
        hasheddata = self._hexToStr(md5.hexdigest())
        j = 0
        i = 0
        while (i < datalen):
            try:
                j += data[i]
            except TypeError:
                j += ord(data[i])
            i += 1
        magickey = chr(int(round(float(j) / float(datalen))))
        encddata = list(range(len(data)))
        if isinstance(magickey, int):
            pass
        else:
            magickey = ord(magickey)
        for i in range(datalen):
            # Python doesn't do bitwise operations with characters, so we need to convert them to integers first.
            # It also doesn't like it if you put integers in the ord() to be translated to integers, that's what the IF, ELSE is for.
            if isinstance(data[i], int):
                encddata[i] = data[i] ^ magickey
            else:
                encddata[i] = ord(data[i]) ^ magickey
        try:
            result = "\x02" + chr(magickey) + "\x04\x00\x00\x00" + str(hasheddata) + bytearray(encddata).decode("utf-8")
        except UnicodeDecodeError:
            result = "\x02" + chr(magickey) + "\x04\x00\x00\x00" + str(hasheddata) + bytearray(encddata)
        return (result)

    def get_data(self, artist, title):
        s = self._search(artist, title)
        if s:
            return self._get_lyrics_from_url(s)
        return []

    def _get_lyrics_from_url(self, search_result):
        xml = self._vl_dec(search_result)
        try:
            xml = xmltodict.parse(xml)
        except ExpatError:
            #This happends when the output is in plain text
            return []
        server_url = str(xml["return"]["@server_url"])
        results = []
        i = 0
        if "fileinfo" in xml["return"]:
            if isinstance(xml["return"]["fileinfo"], list):
                for item in xml["return"]["fileinfo"]:
                    # because the rating will sometimes not be filled, it could give an error, so the rating will be 0 for unrated items
                    try:
                        rating = item["@rate"]
                    except:
                        rating = 0
                    try:
                        artist = item["@artist"]
                    except:
                        artist = None
                    try:
                        title = item["@title"]
                    except:
                        title = None
                    lyric_url = server_url + item["@link"]
                    req = requests.get(lyric_url)
                    lyrics = req.text
                    results.append({'artist': artist, 'title': title, 'rating': float(rating),
                                    'filetype': item["@link"].split(".")[-1],
                                    'lyric': lyrics})
                    i += 1
                results = sorted(results, key=lambda result: (result["rating"]))
                results.reverse()
            else:
                # because the rating will sometimes not be filled, it could give an error, so the rating will be 0 for unrated items
                try:
                    rating = xml["return"]["fileinfo"]["@rate"]
                except:
                    rating = 0
                try:
                    artist = xml["return"]["fileinfo"]["@artist"]
                except:
                    artist = None
                try:
                    title = xml["return"]["fileinfo"]["@title"]
                except:
                    title = None
                lyric_url = server_url + xml["return"]["fileinfo"]["@link"]
                req = requests.get(lyric_url)
                lyrics = req.text
                results.append({'artist': artist, 'title': title, 'rating': float(rating),
                                'filetype': xml["return"]["fileinfo"]["@link"].split(".")[-1],
                                'lyric': lyrics})
        return(results)

    def _vl_dec(self, data):
        magickey = data[1]
        result = ""
        i = 22
        datalen = len(data)
        if isinstance(magickey, int):
            pass
        else:
            magickey = ord(magickey)
        for i in range(22, datalen):
            # python doesn't do bitwise operations with characters, so we need to convert them to integers first.
            if isinstance(data[i], int):
                result += unichr(data[i] ^ magickey)
            else:
                result += unichr(ord(data[i]) ^ magickey)
        return (result)
