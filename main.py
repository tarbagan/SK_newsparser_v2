import requests
from bs4 import BeautifulSoup as bs
import re

poisk = 'женщина'

def get_url():
    """Обрабатываем пагинацию и формируем ссылки"""
    page = set()
    url = f"https://tuva.sledcom.ru/search/?q={poisk}&sort=date&page="
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    pag = soup.findAll('div', {'class':'b-pagination'})[0]
    page_count = len([x for x in pag.find_all('a') if x.text])
    for i in range(1, page_count):
        page.add(url+str(i))
    return page


def parsing(soup):
    """Парсинг данных"""
    def clear(text):
        """Чистим текст"""
        return re.sub(r'[\ \n]{2,}', '', text)

    news_all = []
    for i in soup.findAll('div', {'class': 'bl-item-holder'}):
        title = i.find('div', {'class': 'bl-item-title'}).text
        date = i.find('div', {'class': 'bl-item-date'}).text
        title = clear(title)
        date = clear(date)[9:]
        news = {'date': date, 'title': title}
        news_all.append(news)
    return news_all


urls = get_url()
print (f'Начинаем парсинг {len(urls)} страниц\n----------------------------')
for get in urls:
    r = requests.get(get, timeout=15)
    soup = bs(r.text, 'lxml')
    for i in (parsing(soup)):
        print(i)

