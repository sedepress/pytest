import pymysql

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

cursor.execute("SELECT * FROM `wb_containers` WHERE `root_saas_id` = '118344500'")

shops = cursor.fetchall()

for shop in shops:
    cursor.execute("")

connection.commit()
cursor.close()
connection.close()

if __name__ == '__main__':
    print("创建完成")
