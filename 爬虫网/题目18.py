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
    '_nano_fp': 'XpmYn0EoX5PxX5dxno_SEWXzUnt~HLUABpTu5fic',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744621513',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'client-version': '1.0.0',
    'm': '0arWtxUk6_VePpxynyKGpFKccXEXqb1jpO1YuSnpqRKXnSTyyoQyqNKqF4GpuJzdvFcpuYnydWyy6AwTRErqG62CYLPZ3qZKD6-OmMkOmM2Ze6tFe7xHI635eMkFD61KkM2O7z9VyTsw8T8obMzMkEBrXnpGF1iNLOquJfpivJjg2wyC2Qdn4lGNKOYH2vNNy1puxp99VHRawK_0Ke6NeDMNWDD0KbB2dM1bD-tJ1F-RIm63SH6kVKDJZbZoUbL0UMk8DFGrISt8CMD0Obk_CM3ICI6xF2Ywz9ZQgscOpVdIIz2fLfVlYXTagv4aUpVfOfy1pfoTYreldq5GUpo1nrgtid_Ip0FjgwcnrMgDtvH6muxdUThJSCM9OnlxVAnd9giDMKt8nOOWa4bHVvZ2UxNzQ0NjIxNTE2MDM5',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/18/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'timestamp': '1744621516039',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; s=51b351b351b351b370b0d030d030507090d0f030f0; v=QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==; _nano_fp=XpmYn0EoX5PxX5dxno_SEWXzUnt~HLUABpTu5fic; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744621513',
}

def get_header():
    with open('./js/18.js', 'r') as f:
        headers = execjs.compile(f.read()).call('aaa', [{}, {}, {}])
        return headers

while True:
    params = {
        'page': page,
    }

    h = get_header()
    h['headers']['timestamp'] = str(h['headers']['timestamp'])
    headers.update(h['headers'])

    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/18/data/', cookies=cookies,
                            headers=headers, params=params)

    if response.status_code != 200:
        break

    data = response.json()

    total += sum(data['current_array'])
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
