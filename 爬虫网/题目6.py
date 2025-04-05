import json

import execjs
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743128910',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/6/',
    's': '8101900bc03d472f21c1ac058caa19de',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'tt': '1743128909596',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}


def header_encrypt():
    with open('./js/6.js', 'r') as f:
        r = execjs.compile(f.read()).call('s')
        return r


def response_decrypt(t):
    with open('./js/6.js', 'r') as f:
        r = execjs.compile(f.read()).call('xxxxoooo', t)
        return r


while True:
    r = header_encrypt()
    headers['s'] = r['s']
    headers['tt'] = str(r['tt'])

    response = requests.get(f'https://stu.tulingpyton.cn/api/problem-detail/6/data/?page={page}', cookies=cookies,
                            headers=headers)

    if response.status_code != 200:
        break

    t = response.json()['t']
    data = json.loads(response_decrypt(t))

    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
