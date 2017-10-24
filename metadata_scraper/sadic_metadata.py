import re
import requests
import json
from  bs4 import BeautifulSoup

def get_metadata():
    ret = []
    works_list = "https://tango.info/work/"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        r = requests.get(works_list+letter, timeout=15)
        soup = BeautifulSoup(r.text)
        links = soup.findAll('a', href=True, text='info')
        url = "https://tango.info"
        for link in links:
            url + link['href']

            r = requests.get(url + link['href'], timeout=15)
            soup = BeautifulSoup(r.text)
            sadic = soup.find('a', href=True, text='SADAIC work number')

            todotango_id = None
            sadic_id = None

            if sadic != None:
                sadic_links = list(sadic.parents)[1].findAll('a')
                sadic_link = list(sadic_links)[1]
                sadic_href = sadic_link['href']
                sadic_id = sadic_link.string
            todotango = soup.find('td', text='Todotango.com work number:')
            if todotango != None:
                todotango_a = list(todotango.parents)[0].find('a')
                todotango_href = todotango_a['href']
                todotango_id  = todotango_a.string
            if todotango_id and sadic_id:
                r = requests.get(sadic_href, timeout=15)
                soup = BeautifulSoup(r.text)
                sadic_items = soup.findAll('span', {'class': 'detalle-busqueda'})
                date = None
                for item in list(sadic_items):
                    content = item.prettify()
                    if 'Registrada el ' in content:
                        date = content.split('\n')[1].replace('Registrada el ', '')
                ret.append({'url': todotango_href, 'todotango': todotango_id, 'sadic_url': sadic_href, 'sadic_id': sadic_id, 'date': date})
    return ret


if __name__ == "__main__":
    ret = get_metadata()
    json.dump(ret, open('../data/sadic_metadata.json', 'w'))
