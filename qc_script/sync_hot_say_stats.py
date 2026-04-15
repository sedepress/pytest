#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热议话题统计同步脚本

功能：从 wb_forum_thread 表统计帖子数据，更新到 hot_say 表

表关系：
- hot_say.id = wb_forum_say_threads.say_id
- wb_forum_say_threads.thread_id = wb_forum_thread.thread_id
- 统计字段：likes, favorites, shares, replies
"""

from contextlib import contextmanager
from typing import Dict, List, Tuple

import pymysql

# ==================== 数据库配置 ====================
DB_CONFIG = {
    "host": "v2.wezan.net",
    "port": 3306,
    "user": "fansquan_dev",
    "password": "webei95180",
    "database": "data",
    "charset": "utf8mb4",
}


@contextmanager
def get_connection(db_config: Dict):
    """获取数据库连接的上下文管理器"""
    conn = pymysql.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()


def fetch_thread_stats() -> Dict[int, Dict[str, int]]:
    """
    通过中间表 wb_forum_say_threads 关联查询，统计每个 say_id 的数据

    返回格式：{say_id: {likes, favorites, shares, replies}}
    """
    sql = """
        SELECT
            st.say_id,
            SUM(t.likes) AS total_likes,
            SUM(t.favorites) AS total_favorites,
            SUM(t.shares) AS total_shares,
            SUM(t.replies) AS total_replies,
            SUM(t.views) AS total_views
        FROM wb_forum_say_threads st
        INNER JOIN wb_forum_thread t ON st.thread_id = t.thread_id
        GROUP BY st.say_id
    """

    stats = {}
    with get_connection(DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                say_id = row[0]
                stats[say_id] = {
                    "likes": int(row[1] or 0),
                    "favorites": int(row[2] or 0),
                    "shares": int(row[3] or 0),
                    "replies": int(row[4] or 0),
                    "views": int(row[5] or 0),
                }

    print(f"[INFO] 统计到 {len(stats)} 个热议话题的帖子数据")
    return stats


def fetch_hot_say_ids() -> List[int]:
    """获取 hot_say 表中所有未删除的记录 ID"""
    sql = "SELECT id FROM hot_say"

    ids = []
    with get_connection(DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            ids = [row[0] for row in cursor.fetchall()]

    print(f"[INFO] hot_say 表中有 {len(ids)} 条有效记录")
    return ids


def update_hot_say_stats(stats: Dict[int, Dict[str, int]], hot_say_ids: List[int]) -> Tuple[int, int]:
    """
    批量更新 hot_say 表的统计字段

    返回：(更新成功数, 跳过数)
    """
    sql = """
        UPDATE hot_say
        SET likes = %s,
            favorites = %s,
            shares = %s,
            replies = %s,
            views = %s,
            updated_at = NOW()
        WHERE id = %s
    """

    updated = 0
    skipped = 0

    # 只更新 hot_say 表中存在且有统计数据的记录
    matched_ids = set(hot_say_ids) & set(stats.keys())

    with get_connection(DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            for say_id in matched_ids:
                stat = stats[say_id]
                try:
                    cursor.execute(sql, (
                        stat["likes"],
                        stat["favorites"],
                        stat["shares"],
                        stat["replies"],
                        stat["views"],
                        say_id
                    ))
                    updated += 1
                except Exception as e:
                    print(f"[ERROR] 更新 id={say_id} 失败: {e}")
                    skipped += 1

            conn.commit()

    not_matched = len(hot_say_ids) - len(matched_ids)
    print(f"[INFO] 更新完成: 成功={updated}, 失败={skipped}, 无关联帖子={not_matched}")

    return updated, skipped


def preview_changes(limit: int = 10):
    """预览将要更新的数据变化"""
    stats = fetch_thread_stats()

    sql = """
        SELECT id, say_name, likes, favorites, shares, replies, views
        FROM hot_say
        ORDER BY id DESC
        LIMIT %s
    """

    print("\n" + "=" * 100)
    print(f"数据变化预览（最近 {limit} 条）")
    print("=" * 100)
    print(f"{'ID':<8} {'话题名称':<35} {'字段':<12} {'当前值':<10} {'新值':<10}")
    print("-" * 100)

    with get_connection(DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()

            for row in rows:
                say_id = row[0]
                say_name = (row[1][:30] + "...") if row[1] and len(row[1]) > 30 else (row[1] or "N/A")
                current = {
                    "likes": row[2],
                    "favorites": row[3],
                    "shares": row[4],
                    "replies": row[5],
                    "views": row[6],
                }

                if say_id in stats:
                    new_stats = stats[say_id]
                    has_change = False
                    for field in ["likes", "favorites", "shares", "replies", "views"]:
                        if current[field] != new_stats[field]:
                            print(f"{say_id:<8} {say_name:<35} {field:<12} {current[field]:<10} {new_stats[field]:<10}")
                            has_change = True
                    if not has_change:
                        print(f"{say_id:<8} {say_name:<35} {'(无变化)'}")
                else:
                    print(f"{say_id:<8} {say_name:<35} {'(无关联帖子)'}")

    print("=" * 100)


def main():
    """主函数"""
    print("=" * 60)
    print("热议话题统计同步脚本")
    print("=" * 60)
    print(f"数据库: {DB_CONFIG['host']} / {DB_CONFIG['database']}")
    print("=" * 60)

    # 验证数据库配置
    if not DB_CONFIG["host"]:
        print("[ERROR] 请先填写数据库配置信息！")
        return

    # Step 1: 预览变化
    print("\n[Step 1] 预览数据变化...")
    preview_changes(limit=10)

    # Step 2: 确认执行
    confirm = input("\n是否继续执行更新？(yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("[INFO] 已取消操作")
        return

    # Step 3: 执行更新
    print("\n[Step 2] 开始统计并更新数据...")

    # 获取统计数据
    stats = fetch_thread_stats()

    # 获取 hot_say 表的 ID 列表
    hot_say_ids = fetch_hot_say_ids()

    # 执行更新
    updated, skipped = update_hot_say_stats(stats, hot_say_ids)

    print("\n" + "=" * 60)
    print("同步完成!")
    print(f"  - 成功更新: {updated} 条")
    print(f"  - 更新失败: {skipped} 条")
    print("=" * 60)


if __name__ == "__main__":
    main()
