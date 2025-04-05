import requests

page = 1
total = 0
cs = {
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1742952358',
    'HMACCOUNT': 'F8D55D100B06DC65',
    'sessionid': 'vmaeexrf3cnbsy6o76brm9pkgy302z33',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1742953042'
}

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/2/',
}

while True:
    response = requests.get(f'https://stu.tulingpyton.cn/api/problem-detail/2/data/?page={page}', cookies=cs, headers=headers)
    if response.status_code != 200:
        break
    data = response.json()
    total += sum(data['current_array'])
    page += 1


if __name__ == '__main__':
    print(total)