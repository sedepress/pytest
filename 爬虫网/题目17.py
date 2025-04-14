import requests

page = 1
total = 0
cookies = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    's': '51b351b351b351b370b0d030d030507090d0f030f0',
    'v': 'QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1744593529',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/17/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1742952358; HMACCOUNT=F8D55D100B06DC65; sessionid=vmaeexrf3cnbsy6o76brm9pkgy302z33; s=51b351b351b351b370b0d030d030507090d0f030f0; v=QTJ4b3BBdk1KN3lsLVRQN3UtNXhSbEhrTzBHYkpSTDhFc3NrazhhdGVRMjY5Z0pfN2pYZ1gyTFo5Q0FWMTc0NDM1ODc3MTkzOA==; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1744593529',
}


def get_font(k):
    font_dict = {
        'ꙮ': '0',
        'ઊ': '1',
        'સ': '2',
        'ત': '3',
        'ধ': '4',
        'ન': '5',
        'પ': '6',
        'ફ': '7',
        'બ': '8',
        'ભ': '9'
    }

    return font_dict[k]


while True:
    params = {
        'page': page,
    }

    response = requests.get('https://stu.tulingpyton.cn/api/problem-detail/17/data/', cookies=cookies,
                            headers=headers, params=params)

    if response.status_code != 200:
        break

    data = response.json()
    current_array = []
    for item in data['current_array']:
        new_str = ''
        for i in range(len(item)):
            new_str += get_font(item[i])
        current_array.append(int(new_str))

    total += sum(current_array)
    page += 1

    if not data['pagination']['has_next']:
        break

if __name__ == '__main__':
    print(total)
