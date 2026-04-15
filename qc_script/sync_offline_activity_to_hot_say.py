#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线下活动数据同步到hot_say表

功能：从有赞粉圈线下活动接口获取活动数据，插入到hot_say表
"""

import pymysql
import requests


def fetch_activities(page=1):
    """获取指定页的活动数据"""
    url = f'https://fansquan.app.weimobcloud.com/remote/offline-activity/list?page={page}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[错误] 获取第{page}页数据失败: {e}")
        return None


def insert_activity(cursor, activity):
    """插入单条活动数据到hot_say表"""
    sql = """
    INSERT INTO hot_say (
        source, type, forum_id, say_name, logo, head_logo,
        description, is_show, is_top, participants, views,
        replies, favorites, shares, likes, score,
        created_at, updated_at
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON DUPLICATE KEY UPDATE
        say_name = VALUES(say_name),
        logo = VALUES(logo),
        head_logo = VALUES(head_logo),
        description = VALUES(description),
        participants = VALUES(participants),
        views = VALUES(views),
        updated_at = VALUES(updated_at)
    """

    # 字段映射
    values = (
        'youzan_fansquan',  # source: 数据来源
        'offline',  # type: 活动类型
        activity.get('forumId', 0),  # forum_id: 论坛ID
        activity.get('title', ''),  # say_name: 活动名称
        activity.get('banner', ''),  # logo: 活动横幅（限制60字符）
        activity.get('headBanner', ''),  # head_logo: 头部横幅
        activity.get('content', ''),  # description: 活动描述
        1,  # is_show: 默认显示
        0,  # is_top: 默认不置顶
        activity.get('applies', 0),  # participants: 报名人数
        activity.get('views', 0),  # views: 浏览量
        0,  # replies: 回复数（活动无此数据）
        0,  # favorites: 收藏数（活动无此数据）
        0,  # shares: 分享数（活动无此数据）
        0,  # likes: 点赞数（活动无此数据）
        '',  # score: 评分
        activity.get('created_at'),  # created_at: 创建时间
        activity.get('updated_at')  # updated_at: 更新时间
    )

    cursor.execute(sql, values)


def main():
    """主函数"""
    # 数据库连接配置
    connection = pymysql.connect(
        host='v2.wezan.net',
        port=3306,
        user='fansquan_dev',
        password='webei95180',
        database='data',
    )

    try:
        cursor = connection.cursor()

        # 获取第一页数据以确定总页数
        print("=" * 60)
        print("线下活动数据同步到hot_say表")
        print("=" * 60)
        print("\n[步骤1] 获取活动数据...")

        first_page = fetch_activities(1)

        if not first_page or first_page.get('code') != 1:
            print("[错误] 获取数据失败，请检查API接口")
            return

        total_pages = first_page['data']['last_page']
        total_count = first_page['data']['total']
        per_page = first_page['data']['per_page']

        print(f"总共{total_count}条活动数据，每页{per_page}条，共{total_pages}页")

        # 确认执行
        confirm = input("\n是否开始同步数据？(yes/no): ").strip().lower()
        if confirm not in ('yes', 'y'):
            print("[信息] 已取消操作")
            return

        print("\n[步骤2] 开始同步数据...")
        total_inserted = 0
        total_failed = 0

        # 遍历所有页面
        for page in range(1, total_pages + 1):
            print(f"\n正在处理第{page}/{total_pages}页...")

            # 第一页已经获取过了
            if page == 1:
                data = first_page
            else:
                data = fetch_activities(page)

            if not data or data.get('code') != 1:
                print(f"  [错误] 第{page}页数据获取失败，跳过")
                continue

            activities = data['data']['data']

            # 插入每条活动数据
            for activity in activities:
                activity_id = activity.get('activityId')
                title = activity.get('title', '')[:30]

                try:
                    insert_activity(cursor, activity)
                    total_inserted += 1
                    print(f"  [成功] 活动ID: {activity_id} - {title}")
                except Exception as e:
                    total_failed += 1
                    print(f"  [失败] 活动ID: {activity_id} - {title} | 错误: {e}")

            # 每页提交一次
            connection.commit()
            print(f"第{page}页完成，成功{len(activities)}条")

        # 完成统计
        print("\n" + "=" * 60)
        print("同步完成！")
        print(f"  - 成功插入/更新: {total_inserted} 条")
        print(f"  - 失败: {total_failed} 条")
        print("=" * 60)

    except Exception as e:
        print(f"\n[错误] 执行失败: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()
