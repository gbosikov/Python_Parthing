import requests
import json


url = f'https://api.vk.com/method/groups.get'
params = {
    'access_token': '***TOKEN****',
    'user_id': '',
    'extended': 1,
    'filter': '',
    'fields': '',
    'offset': '',
    'count': 50
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = json.loads(response.text)
    for group in data['response']['items']:
        print(group['name'])
    with open('vk.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)
