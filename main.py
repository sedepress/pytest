from datetime import datetime

import pymysql
import requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://6hch.com',
    'Referer': 'https://6hch.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

data = {
    'year': '2025',
    'type': '1',
}

response = requests.post('https://1680660.com/smallSix/findSmallSixHistory.do', headers=headers, data=data)
data = response.json()['result']['data']['bodyList']

connection = pymysql.connect(
        host='185.239.69.183',
        port=3306,
        user='root',
        password='hFy8XzyaeNXmjpja',
        database='hk_49tkcp_me',
    )

cursor = connection.cursor()
sorted_data = sorted(data, key=lambda k: k['issue'])

for item in sorted_data:
    dt_utc = datetime.strptime(item['preDrawDate'], "%Y-%m-%d")
    timestamp = int(dt_utc.timestamp())
    sql = "INSERT INTO `pc_data2` (`type`, `time`, `number`, `data`) VALUES (1, %s, %s, %s);"
    if len(str(item['issue'])) == 1:
        number = '202500'+str(item['issue'])
    else:
        number = '20250'+str(item['issue'])
    cursor.execute(sql, (timestamp, number, item['preDrawCode']))

connection.commit()
cursor.close()
connection.close()

if __name__ == "__main__":
    print(data)