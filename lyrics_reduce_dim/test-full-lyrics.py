import lxml.html
import requests
import json
import os.path
import time

artists = 54825
artist_url = "https://www.musica.com/letras.asp?letras="

max_lyric = 2400000
    #min_lyric = 139134
min_lyric = 2319269 

lyrics_url = "https://www.musica.com/imprimir.asp?letra="
selector = '//*[@id="printableArea"]/center/table/tr[2]/td/font/div/text()'

for lyric_num in range(min_lyric, max_lyric):
    done = False
    filename = "%s%i.txt" % ("/home/andres/projects/tango-data/data/test-full-lyrics/", lyric_num)
    if not os.path.isfile(filename):
        while not done:
            url = "%s%i" % (lyrics_url,lyric_num)
            try:
                r = requests.get(url, timeout=15)
                page = lxml.html.document_fromstring(r.text)
                links = page.xpath(selector)
                if links:
                    json.dump(links, open(filename, "w"))
                    print lyric_num
                    time.sleep(0.5)
                done = True
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print "error"
                time.sleep(60 * 5)
