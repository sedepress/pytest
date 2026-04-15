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

cursor.execute("SELECT * FROM `wb_containers` WHERE `root_saas_id` = '180691302' or `saas_id` = '180691302'")

shops = cursor.fetchall()
package_no = 0
for shop in shops:
    requests.get(f"https://guider-assistant.isv.youzan.com/package/set/fix?saas_id={shop[1]}&package_no={package_no}")
    print(f"{shop}套餐增加完成")

connection.commit()
cursor.close()
connection.close()

if __name__ == '__main__':
    print("套餐增加完成")
