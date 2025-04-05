import time

import pywasm
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    's': '51b351b351b351b370b0d030d030507090d0f030f0',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743519865',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/10/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; s=51b351b351b351b370b0d030d030507090d0f030f0; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1743519865',
}

date = round(time.time())


def load_wasm(page):
    runtime = pywasm.core.Runtime()
    m = runtime.instance_from_file('./wasm/encrypt.wasm')
    r = runtime.invocate(m, 'encrypt', [page, date])
    return r


while True:
    r = load_wasm(page)

    params = {
        'page': page,
        'm': r[0],
        '_ts': date,
    }

    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/11/data/', params=params, cookies=cookies,
                            headers=headers)

    if response.status_code != 200:
        break

    data = response.json()

    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
