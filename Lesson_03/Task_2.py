from pymongo import MongoClient as mg
from pprint import pprint
from pymongo.server_api import ServerApi


user = 'admin'
passw = '5moHizn3JvYLTDPY'
client = mg(f"mongodb+srv://{user}:{passw}@cluster0.uxlpm.mongodb.net/vacancy?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client['Lesson_03']
vacancy = db.vacancy

user_input = int(input('Enter minimum salary'))

def min_salary_from_db(min_salary: str):
    for a in vacancy.find(
            {'$or': [{"vacancy_salary.min_salary": {'$gt': min_salary}},
                     {"vacancy_salary.max_salary": {'$gt': min_salary}}]}):
        pprint(a)

min_salary_from_db(user_input)


