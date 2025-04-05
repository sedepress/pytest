import json

import execjs
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743386268',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'm': '3e75efe6bc1945c560ce9d2fadd965da',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/7/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'ts': '1743386283975',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1743386268',
}


def header_encrypt():
    with open('./js/7.js', 'r') as f:
        r = execjs.compile(f.read()).call('getHeader')
        return r


def response_decrypt(t):
    with open('./js/7.js', 'r') as f:
        r = execjs.compile(f.read()).call('xxxxoooo', t)
        return r


while True:
    h = header_encrypt()

    params = {
        'page': page,
        'x': h['headers']['x'],
    }

    headers['m'] = h['headers']['m']
    headers['ts'] = str(h['headers']['ts'])

    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/7/data/', params=params, cookies=cookies,
                            headers=headers)

    if response.status_code != 200:
        break

    t = response.json()
    data = json.loads(response_decrypt(t['r']))
    print(data)

    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
