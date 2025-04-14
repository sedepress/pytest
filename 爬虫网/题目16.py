import datetime
import time

import execjs
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    's': '51b351b351b351b370b0d030d030507090d0f030f0',
    'v': 'QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744484789',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://stu.tulingpyton.cn',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/16/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; s=51b351b351b351b370b0d030d030507090d0f030f0; v=QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744484789',
}


def get_v(t):
    with open('./js/PcSign.js', 'r') as f:
        url = execjs.compile(f.read()).call('getM',
                                            {'page': page, 't': t})
        return url


while True:
    t = int(datetime.datetime.now().timestamp() * 1000)
    h5 = get_v(t)
    data = f'{{"page":"{page}","t":"{t}","h5":"{h5}"}}'

    time.sleep(1)
    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/16/data/', cookies=cookies,
                             headers=headers, data=data)

    if response.status_code != 200:
        break

    data = response.json()

    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
