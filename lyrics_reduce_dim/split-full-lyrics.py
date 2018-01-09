import json
import os.path
import time
from langdetect import detect, lang_detect_exception

max_lyric = 2400000
min_lyric = 1310000

lyrics_location = "/home/andres/projects/tango-data/data/test-full-lyrics/"

for lyric_num in range(min_lyric, max_lyric):
    filename = "%s%i.txt" % (lyrics_location, lyric_num)
    if os.path.isfile(filename):
        content = json.load(open(filename))
        try:
            lang = detect('\n'.join(content))
            if lang in ('en', 'es'):
                dest = "%s%s/%i.txt" % (lyrics_location, lang, lyric_num)
                if not os.path.isfile(dest):
                    json.dump(content, open(dest, "w"))
        except lang_detect_exception.LangDetectException:
            continue

