import pymysql
import requests


# 连锁店创建
page = 1

connection = pymysql.connect(
        host='rm-bp18a15df76b6s7xao.mysql.rds.aliyuncs.com',
        port=3306,
        user='webei_production',
        password='webei95180',
        database='guider_assistant',
    )
cursor = connection.cursor()
while True:
    params = {
        'page_size': 50,
        'page_num': page
    }
    response = requests.post('https://open.youzanyun.com/api/youzan.shop.chain.descendent.organization.list/1.0.1?access_token=789b206c266e82198dd5d1891e1924a', json=params)
    data = response.json()

    if len(data['data']['organization_list']) > 0:
        for organization in data['data']['organization_list']:
            sql = "INSERT INTO `guider_assistant`.`wb_containers` (`saas_id`, `phone`, `name`, `logo`, `root_saas_id`, `expired_at`, `created_at`, `updated_at`, `version`) VALUES (%s, '17891971802', %s, 'https://img.yzcdn.cn/upload_files/2025/03/12/FqO6PV59yVG5oPHnYVaB0FoWMxOA.jpg', %s, '2025-06-17 09:25:29', '2025-06-10 09:26:57', '2025-06-10 09:26:57', 0);"
            cursor.execute(sql, (organization['kdt_id'], organization['name'], '118344500'))

    if len(data['data']['organization_list']) == 0:
        break

    page += 1

connection.commit()
cursor.close()
connection.close()

if __name__ == '__main__':
    print("创建完成")
