#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热议话题数据同步脚本（微盟渠道API版）

功能：
1. 从微盟 API 分页获取热议话题列表
2. 获取每个热议话题下的所有帖子
3. 聚合帖子统计数据
4. 插入到 hot_say 表
"""

import time
from contextlib import contextmanager
from typing import Dict, List, Optional

import pymysql
import requests

# ==================== 配置 ====================
# API 地址
API_BASE_URL = "https://fansquan.app.weimobcloud.com/remote"
API_HOT_SAY_LIST = f"{API_BASE_URL}/hot-say/list"
API_THREAD_LIST = f"{API_BASE_URL}/hot-say/thread/list"

# 数据库配置
DB_CONFIG = {
    "host": "v2.wezan.net",
    "port": 3306,
    "user": "fansquan_dev",
    "password": "webei95180",
    "database": "data",
    "charset": "utf8mb4",
}

# 数据来源标识
DEFAULT_SOURCE = "weimob_fansquan"

# 请求配置
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 0.2  # 请求间隔（秒），避免请求过快


@contextmanager
def get_connection(db_config: Dict):
    """获取数据库连接"""
    conn = pymysql.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()


def fetch_hot_say_list(page: int = 1) -> Optional[Dict]:
    """获取热议话题列表（单页）"""
    try:
        resp = requests.get(
            API_HOT_SAY_LIST,
            params={"page": page},
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] 获取热议话题列表失败 (page={page}): {e}")
        return None


def fetch_all_hot_says() -> List[Dict]:
    """获取所有热议话题"""
    all_items = []
    page = 1

    while True:
        print(f"[INFO] 获取热议话题列表 page={page}...")
        result = fetch_hot_say_list(page)

        if not result or result.get("code") != 1:
            print(f"[ERROR] API 返回异常: {result}")
            break

        # 解析返回数据
        data = result.get("data", {})
        items = data.get("data", [])

        if not items:
            break

        all_items.extend(items)
        print(f"[INFO] 获取到 {len(items)} 条，累计 {len(all_items)} 条")

        # 检查是否有下一页
        current_page = data.get("current_page", 1)
        last_page = data.get("last_page", 1)
        if current_page >= last_page:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    print(f"[INFO] 共获取 {len(all_items)} 个热议话题")
    return all_items


def fetch_thread_list(hot_say_id: int) -> Optional[Dict]:
    """获取热议话题下的帖子列表"""
    try:
        resp = requests.get(
            API_THREAD_LIST,
            params={"hot_say_id": hot_say_id},
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] 获取帖子列表失败 (hot_say_id={hot_say_id}): {e}")
        return None


def fetch_all_threads(hot_say_id: int) -> List[Dict]:
    """获取热议话题下的所有帖子"""
    result = fetch_thread_list(hot_say_id)

    if not result or result.get("code") != 1:
        return []

    # 微盟API返回的data直接是数组
    data = result.get("data", [])

    if isinstance(data, list):
        return data

    return []


def aggregate_thread_stats(threads: List[Dict]) -> Dict[str, int]:
    """聚合帖子统计数据"""
    stats = {
        "likes": 0,
        "replies": 0,  # 对应 API 中的 comments
        "views": 0,
        "shares": 0,
        "favorites": 0,
        "participants": len(threads),  # 帖子数作为参与数
    }

    for thread in threads:
        statistics = thread.get("statistics", {})
        if statistics:
            stats["likes"] += statistics.get("likes", 0) or 0
            stats["replies"] += statistics.get("comments", 0) or 0
            stats["views"] += statistics.get("views", 0) or 0
            stats["shares"] += statistics.get("shares", 0) or 0
            # 微盟API中没有favorites字段，保持为0

    return stats


def insert_hot_say(hot_say: Dict, stats: Dict[str, int]) -> bool:
    """插入 hot_say 表"""
    sql = """
        INSERT INTO hot_say (
            source, forum_id, say_name, logo, head_logo, hot_spot_url,
            description, is_show, is_top, participants, views, replies,
            favorites, shares, likes, created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, NOW()
        )
    """

    # 从 API 数据提取字段（微盟使用驼峰命名）
    say_id = hot_say.get("sayId")
    forum_id = hot_say.get("forumId", 0) or 0
    say_name = hot_say.get("sayName", "")
    logo = hot_say.get("logo", "")
    head_logo = hot_say.get("headLogo", "")
    hot_spot_url = ""  # API 没有此字段
    description = hot_say.get("description", "")
    is_show = hot_say.get("isShow", 1) or 0
    is_top = 0  # API 没有此字段
    created_at = hot_say.get("createdAt")

    try:
        with get_connection(DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (
                    DEFAULT_SOURCE,
                    forum_id,
                    say_name,
                    logo[:60] if logo else "",  # logo 字段限制 60 字符
                    head_logo,
                    hot_spot_url,
                    description,
                    is_show,
                    is_top,
                    stats["participants"],
                    stats["views"],
                    stats["replies"],
                    stats["favorites"],
                    stats["shares"],
                    stats["likes"],
                    created_at
                ))
                conn.commit()
                return True
    except Exception as e:
        print(f"[ERROR] 插入 hot_say 失败 (say_id={say_id}): {e}")
        return False


def process_hot_says(hot_says: List[Dict], dry_run: bool = False):
    """处理所有热议话题"""
    total = len(hot_says)
    success = 0
    failed = 0

    for i, item in enumerate(hot_says, 1):
        say_id = item.get("sayId")
        say_name = item.get("sayName", "")

        print(f"\n[{i}/{total}] 处理热议话题: {say_id} - {say_name[:30]}...")

        # 获取该话题下所有帖子
        threads = fetch_all_threads(say_id)
        print(f"  - 获取到 {len(threads)} 个帖子")

        # 聚合统计数据
        stats = aggregate_thread_stats(threads)
        print(f"  - 统计: views={stats['views']}, likes={stats['likes']}, "
              f"replies={stats['replies']}, favorites={stats['favorites']}, "
              f"shares={stats['shares']}, participants={stats['participants']}")

        # 插入数据库
        if dry_run:
            print(f"  - [DRY RUN] 跳过数据库插入")
            success += 1
        else:
            if insert_hot_say(item, stats):
                print(f"  - 插入成功")
                success += 1
            else:
                print(f"  - 插入失败")
                failed += 1

        time.sleep(REQUEST_DELAY)

    return success, failed


def main():
    """主函数"""
    print("=" * 60)
    print("热议话题数据同步脚本（微盟渠道API版 - 插入模式）")
    print("=" * 60)
    print(f"数据来源标识: {DEFAULT_SOURCE}")

    # 是否为试运行模式
    dry_run = False

    # Step 1: 获取所有热议话题
    print("\n[Step 1] 获取热议话题列表...")
    hot_says = fetch_all_hot_says()

    if not hot_says:
        print("[ERROR] 未获取到热议话题数据")
        return

    # Step 2: 确认执行
    print(f"\n共获取 {len(hot_says)} 个热议话题")
    if dry_run:
        print("[DRY RUN 模式] 不会实际插入数据库")

    confirm = input("\n是否开始处理？(yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("[INFO] 已取消操作")
        return

    # Step 3: 处理每个热议话题
    print("\n[Step 2] 开始处理热议话题...")
    success, failed = process_hot_says(hot_says, dry_run)

    # 完成
    print("\n" + "=" * 60)
    print("同步完成!")
    print(f"  - 成功插入: {success}")
    print(f"  - 插入失败: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
