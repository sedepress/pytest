import json
import time

import execjs
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743124188',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://stu.tulingpyton.cn',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/5/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}


def aes_encrypt(data):
    with open('./js/5.js', 'r') as f:
        r = execjs.compile(f.read()).call('encrypt', data)
        return r


while True:
    data = {
        'page': page,
        '_ts': int(time.time() * 1000),
    }

    j = {
        'xl': aes_encrypt(json.dumps(data))
    }
    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/5/data/', json=j, cookies=cookies,
                             headers=headers)
    if response.status_code != 200:
        break

    data = response.json()

    print(data)
    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
