import requests
from bs4 import BeautifulSoup as bs
import re

poisk = 'грабеж'

def get_url():
    page = set()
    url = f"https://tuva.sledcom.ru/search/?q={poisk}&sort=date&page="
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    pag = soup.findAll('div', {'class':'b-pagination'})[0]
    page_count = len([x for x in pag.find_all('a') if x.text])
    for i in range(1, page_count):
        page.add(url+str(i))
    return page

for get in get_url():
    r = requests.get(get,timeout=15)
    soup = bs(r.text, 'lxml')
    for t in soup.findAll('div',{'class':'bl-item-title'}):
        tit = (t.text)
        tit = re.sub(r'[\ \n]{2,}', '', tit)
        print(tit)
