import execjs
import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743427416',
    's': '51b351b351b351b370b0d030d010b0d030f0705051',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'm': 'dedededededea0a6a3a2a3a1a6a3a2a4a09fa7a0',
    'origin': 'https://stu.tulingpyton.cn',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/8/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    't': 'MTc0MzQyNzQzNTEwOA==',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1743427416; s=51b351b351b351b370b0d030d010b0d030f0705051',
}


def header_encrypt(page):
    with open('./js/8.js', 'r') as f:
        r = execjs.compile(f.read()).call('getHeader', {"data": {'page': page}})
        return r


while True:
    h = header_encrypt(page)

    params = {
        'page': page,
    }

    headers['m'] = h['headers']['m']
    headers['t'] = str(h['headers']['t'])

    print(headers)

    response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/8/data/', json=params, cookies=cookies,
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
