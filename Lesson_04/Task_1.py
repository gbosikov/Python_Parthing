from lxml import html
import requests
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import hashlib
from pprint import pprint
from pymongo.server_api import ServerApi

user = 'admin'
passw = '5moHizn3JvYLTDPY'
client = MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.uxlpm.mongodb.net/vacancy?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client['Lesson_04']  # создаю базу данных
news = db.news  # создаю коллекцию


url = 'https://lenta.ru'
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
top_news = dom.xpath(".//div[@class='topnews__first-topic']//@href")[0]
other_news_links = dom.xpath("//a[@class='card-mini _topnews']//@href")
other_news_links.append(top_news)
# print(other_news_links)

for links in other_news_links:
    if links[0] == '/':
        news_link = f'{url}{links}'
        # print(news_link)
        news_dict = {}
        response_to_news = requests.get(news_link, headers=header)
        news_link_dom = html.fromstring(response_to_news.text)
        news_source = news_link_dom.xpath(".//a[@class='topic-header__item topic-header__rubric']//text()")
        news_title = news_link_dom.xpath(".//span[@class='topic-body__title']//text()")
        news_date = news_link_dom.xpath(".//time[@class='topic-header__item topic-header__time'][position() < 2]//text")

        encoding = news_link.encode()

        news_dict['_id'] = hashlib.md5(encoding).hexdigest()
        news_dict['news_source'] = news_source
        news_dict['news_title'] = news_title
        news_dict['news_date'] = news_date
        news_dict['link'] = news_link

        try:
            news.insert_one(news_dict)
        except DuplicateKeyError:
            print(f"Document {news_dict['_id']} already exists")

all_news = list(news.find({}))
pprint(all_news)
