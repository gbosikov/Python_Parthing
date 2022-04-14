from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup as bs
import hashlib as hs
import requests as rq
import Lesson_03.errors as err
from pprint import pprint

user = 'admin'
passw = '5moHizn3JvYLTDPY'
client = MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.uxlpm.mongodb.net/vacancy?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client['Lesson_03']  # создаю базу данных
vacancy = db.vacancy  # создаю коллекцию


base_url = f'https://hh.ru/vacancies'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
key_word = input('Enter keyword: \n').replace(' ', '-')
url = f'{base_url}/{key_word}'
response = rq.get(url, headers=headers)
dom = bs(response.text, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})


def max_num():
    max_num = 0
    for item in dom.find_all('a', {'data-qa': 'pager-page'}):
        max_num = list(item.strings)[0].split(" ")[-1]
    return int(max_num)


def data_collect(pages: int):
    vacancies_list = []
    for page in range(pages):
        url2 = f'{base_url}/{key_word}?page={page}'
        response2 = rq.get(url2, headers=headers)
        dom2 = bs(response2.text, 'html.parser')
        vacancies2 = dom2.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies2:
            vacancy_data = {}
            vacancy_title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text.strip()
            vacancy_employer = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.replace("\xa0", ' ').strip()
            vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_salary_data = {'min_salary': '', 'max_salary': '', 'currency': ''}
            if vacancy_salary is None:
                vacancy_salary_data['min_salary'] = 'None'
                vacancy_salary_data['max_salary'] = 'None'
                vacancy_salary_data['currency'] = 'None'
            else:
                vacancy_salary = vacancy_salary.text.replace("\u202f", '').split()
                if 'от' in vacancy_salary:
                    if 'руб' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = 'None'
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['max_salary'] = 'None'
                        vacancy_salary_data['currency'] = 'USD'
                if 'до' in vacancy_salary:
                    if 'руб' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = 'None'
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = 'None'
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'USD'
                if 'от' not in vacancy_salary and 'до' not in vacancy_salary:
                    if 'руб' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'USD'
            encoding = vacancy_link.encode()
            vacancy_data['_id'] = hs.md5(encoding).hexdigest()
            vacancy_data['vacancy_title'] = vacancy_title
            vacancy_data['vacancy_employer'] = vacancy_employer
            vacancy_data['vacancy_link'] = vacancy_link
            vacancy_data['vacancy_salary'] = vacancy_salary_data
            vacancies_list.append(vacancy_data)
            try:
                vacancy.insert_one(vacancy_data)
            except err.DuplicateKeyError:
                print(f'Collection with _id: {hs.md5(encoding).hexdigest()} already exists')
    pass

data_collect(max_num())


