import os
import re
import json

def get_years():
    root_folder = os.path.dirname(os.path.realpath(__file__)) + '/../'
    f = json.load(open(os.path.join(root_folder, 'data/clean/works.json')))
    r  = json.load(open(os.path.join(root_folder, 'data/clean/recordings.json')))
    l  = json.load(open(os.path.join(root_folder, 'data/clean/lyrics.json')))
    a  = json.load(open(os.path.join(root_folder, 'data/clean/artists.json')))
    sadic =json.load(open(os.path.join(root_folder, 'data/sadic_metadata.json')))

    works_years = {}

    # Set dates with the value in the works from todotango
    for i in f:
        if (len(i['date'])):
            works_years[i['id']] = int(i['date'][2])

    # Get missing dates from sadic
    sadic_dates = {}
    for i in sadic:
        if i['date']:
            sadic_dates[i['url'].split('/')[5]] = int(i['date'].split('/')[2])

    for k in l.keys():
        if int(k) not in works_years:
            todotango_id = f[int(k)]['external_id']['todotango'].split('/')[5]
            if todotango_id in sadic_dates:
                works_years[int(k)] = sadic_dates[todotango_id]

    # Set missing dates to works from the date of the first recording
    for i in r:
        if i['work'] not in works_years and i['description']:
            set_date = None
            match = re.findall('(19\d{2})', i['description'])
            match20 = re.findall('(20\d{2})', i['description'])
            if len(match)==1:
                d = int(match[0])
                if i['work'] in works_years:
                    if works_years[i['work']] > d:
                        set_date = d
                else:
                    set_date = d
            elif len(match20) == 1:
                d = int(match20[0])
                if i['work'] in works_years:
                    if works_years[i['work']] > d:
                        set_date = d
                else:
                    set_date = d
            if set_date != None:
                works_years[i['work']] = set_date

    # Get missing dates from authors birth dates
    d = works_years.keys()
    for k in l.keys():
        if int(k) not in d:
            c = f[int(k)]['composers'] + f[int(k)]['lyricists']
            if c != None and len(c) > 0 :
                last_begin = 0
                last_end = 9999
                for i in c:
                    if a[i]["begin_date"] != None and len(a[i]["begin_date"]) ==3:
                        begin = int(a[i]["begin_date"][2])
                        if begin > last_begin:
                            last_begin = begin
                    if a[i]["end_date"] != None and len(a[i]["end_date"])==3: 
                        end = int(a[i]["end_date"][2])
                        if end < last_end:
                            last_end = end
                if last_begin > 0:
                    set_date = None
                    if last_end:
                        set_date = last_begin + ((last_end - last_begin) /2)
                    else:
                        set_date = last_begin + 30 # Sum 30 to the date of birth
                    works_years[int(k)] = set_date
                elif last_end < 9999:
                    set_date = last_end - 20
                    works_years[int(k)] = set_date

    return works_years
