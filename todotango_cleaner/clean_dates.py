import re
import json

def get_years():

    f = json.load(open('data/clean/works.json'))
    r  = json.load(open('data/clean/recordings.json'))

    works_years = {}

    for i in r:
        if i['description']:
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

    for i in f:
        if (len(i['date'])):
            works_years[i['id']] = int(i['date'][2])
    return works_years
