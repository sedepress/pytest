import concurrent
from concurrent.futures import ThreadPoolExecutor

import pymysql
import requests


def process_thread(thread_id):
    """封装单个删除请求的线程任务"""
    json_data = {
        'thread_id': thread_id,
        'callback_url': 'www.wb.com/callback/post/delete'
    }
    try:
        response = requests.delete(
            'http://118.178.140.128:8003/thread/delete',
            json=json_data,
            timeout=10  # 添加请求超时控制
        )
        return (thread_id, response.json(), None)
    except Exception as e:
        return (thread_id, None, str(e))


def main():
    # 数据库连接
    connection = pymysql.connect(
        host='rm-bp18a15df76b6s7xao.mysql.rds.aliyuncs.com',
        port=3306,
        user='nbwcy',
        password='nbwcy',
        database='weibei',
    )

    try:
        with connection.cursor() as cursor:
            # 获取有效的forumIds（已去重）
            forum_ids = set()

            # 查询订阅的forum_id
            cursor.execute('SELECT forum_id FROM wb_business_subscriptions WHERE ended_at > NOW()')
            forum_ids.update(row[0] for row in cursor.fetchall())

            # 查询来源为2的forum_id
            cursor.execute('SELECT forum_id FROM wb_forum WHERE source = 2')
            forum_ids.update(row[0] for row in cursor.fetchall())

            base_sql = '''
                SELECT thread_id 
                FROM wb_forum_thread 
                WHERE is_status = 1 
                {forum_condition}
                ORDER BY thread_id  # 新增排序确保分页稳定
            '''

            page_size = 1000
            last_id = 0

            while True:
                # 动态生成分页查询
                forum_condition = "AND forum_id NOT IN ({})".format(
                    ', '.join(['%s'] * len(forum_ids))
                )
                params = list(forum_ids) + [last_id]

                sql = base_sql.format(forum_condition=forum_condition) + \
                      " AND thread_id > %s LIMIT %s"  # 分页条件

                # 执行分页查询
                cursor.execute(sql, params + [page_size])

                # 获取当前批次数据
                batch = cursor.fetchall()
                if not batch:
                    break

                thread_ids = [row[0] for row in batch]
                last_id = thread_ids[-1]

                # 使用线程池并发处理（控制并发数为20）
                with ThreadPoolExecutor(max_workers=2) as executor:
                    futures = {executor.submit(process_thread, tid): tid for tid in thread_ids}

                    for future in concurrent.futures.as_completed(futures):
                        thread_id = futures[future]
                        try:
                            tid, response, error = future.result()
                            if error:
                                print(f'[失败] 帖子ID: {tid} | 错误: {error}')
                            else:
                                print(f'[成功] 帖子ID: {tid} | 响应: {response}')
                        except Exception as e:
                            print(f'[异常] 帖子ID: {thread_id} | 错误: {str(e)}')
    finally:
        connection.close()


if __name__ == "__main__":
    main()#