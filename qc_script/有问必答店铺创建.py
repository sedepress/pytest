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

token = '1e52e4a68bf7222b5b465b66b8924c6'
expired_at = '2026-03-18 09:46:23'
cursor = connection.cursor()
while True:
    rootResponse = requests.get(f"https://open.youzanyun.com/api/youzan.shop.basic.get/3.0.0?access_token={token}")
    rootData = rootResponse.json()

    cursor.execute("SELECT container_id FROM wb_containers WHERE saas_id = %s", (rootData['data']['sid'],))
    if not cursor.fetchone():
        sql = "INSERT INTO `guider_assistant`.`wb_containers` (`saas_id`, `phone`, `name`, `logo`, `root_saas_id`, `expired_at`, `created_at`, `updated_at`, `version`) VALUES (%s, %s, %s, %s, null, %s, NOW(), NOW(), 0);"
        cursor.execute(sql, (rootData['data']['sid'], rootData['data']['customer_service_phone_number']['phone_number'], rootData['data']['name'], rootData['data']['logo'], expired_at))

    params = {
        'page_size': 50,
        'page_num': page
    }
    response = requests.post(f"https://open.youzanyun.com/api/youzan.shop.chain.descendent.organization.list/1.0.1?access_token={token}", json=params)
    data = response.json()

    if len(data['data']['organization_list']) > 0:
        for organization in data['data']['organization_list']:
            # 1. 先查是否存在
            cursor.execute("SELECT container_id FROM wb_containers WHERE saas_id = %s", (organization['kdt_id'],))
            if cursor.fetchone():
                print(f"跳过已存在的 ID: {organization['kdt_id']}")
                continue

            sql = "INSERT INTO `guider_assistant`.`wb_containers` (`saas_id`, `phone`, `name`, `logo`, `root_saas_id`, `expired_at`, `created_at`, `updated_at`, `version`) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), 0);"
            cursor.execute(sql, (organization['kdt_id'], rootData['data']['customer_service_phone_number']['phone_number'] , organization['name'], rootData['data']['logo'], organization['parent_kdt_id'], expired_at))

    if len(data['data']['organization_list']) == 0:
        break

    page += 1

connection.commit()
cursor.close()
connection.close()

if __name__ == '__main__':
    print("创建完成")
