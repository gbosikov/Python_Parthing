import requests
import json


login = 'gbosikov'
url = f'https://api.github.com/users/{login}/repos'
response = requests.get(url)
print(response.json())
if response.status_code == 200:
    for val in response.json():
        print(f'{val["name"]} - {val["url"]}')

data = json.loads(response.text)
with open(login + '.json', 'w', encoding='utf-8') as file:
    json.dump(data, file)
