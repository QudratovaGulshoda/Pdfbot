import json
import requests
from environs import Env
env = Env()
env.read_env()
URL = env.str('BASE_URL')
def create_user(name,telegram_id):
    url = f'{URL}/users/'
    requests.post(url=url,data={
        'name':name,
        "telegram_id":telegram_id
    })
    return 'Created'
def get_info():
    url = f'{URL}/info'
    response = requests.get(url)
    rest = json.loads(response.text)
    return rest['info']
def get_users():
    url = f'{URL}/count/'
    response = requests.get(url)
    rest = json.loads(response.text)
    return rest