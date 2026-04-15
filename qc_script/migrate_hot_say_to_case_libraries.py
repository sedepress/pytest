#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热议话题迁移脚本

功能：
1. 从 data.hot_say 中查询 highlight、summary 非空的数据
2. 迁移全部符合条件的热议话题和线下活动数据
3. 按类型映射写入 luyi_ai.wb_activity_case_libraries
4. 将 highlight 按换行拆分为 JSON 字符串
5. 将统计字段聚合为 stats_json，参与人数单独存储
6. 随机为每条数据分配标签

类型映射：
- hot_say -> category_id = 1
- offline -> category_id = 3
"""

import argparse
import json
import random
import sys
from contextlib import contextmanager
from typing import Dict, Iterable, List, Optional

import pymysql

TYPE_TO_CATEGORY_ID = {
    "hot_say": 1,
    "offline": 3,
}

TAG_OPTIONS = ["爆款", "热门", "经典", "推荐"]

DEFAULT_DB_CONFIG = {
    "host": "192.168.0.249",
    "port": 3306,
    "user": "fansquan_dev",
    "password": "webei95180",
    "charset": "utf8mb4",
}


@contextmanager
def get_connection(db_config: Dict[str, object]):
    """获取数据库连接"""
    connection = pymysql.connect(
        host=db_config["host"],
        port=int(db_config["port"]),
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        charset=db_config["charset"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        yield connection
    finally:
        connection.close()


def fetch_hot_say_records_by_type(connection, activity_type: str, limit: Optional[int] = None) -> List[Dict[str, object]]:
    """按类型查询待迁移的热议话题数据"""
    sql = """
        SELECT
            id,
            type,
            say_name,
            logo,
            hot_spot_url,
            description,
            participants,
            views,
            replies,
            favorites,
            shares,
            likes,
            highlight,
            summary
        FROM hot_say
        WHERE deleted_at IS NULL
          AND type = %s
          AND highlight IS NOT NULL
          AND summary IS NOT NULL
          AND TRIM(highlight) != ''
          AND TRIM(summary) != ''
        ORDER BY id DESC
    """

    params = [activity_type]
    if limit is not None:
        sql += "\n        LIMIT %s"
        params.append(limit)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return list(cursor.fetchall())


def fetch_hot_say_records(connection, limit_per_type: Optional[int] = None) -> List[Dict[str, object]]:
    """查询全部待迁移的热议话题数据"""
    records: List[Dict[str, object]] = []
    for activity_type in TYPE_TO_CATEGORY_ID:
        records.extend(fetch_hot_say_records_by_type(connection, activity_type, limit_per_type))
    return records


def format_highlight_as_json(highlight_text: object, max_items: int = 3) -> str:
    """将亮点文本按换行拆分为 JSON 字符串"""
    lines = [line.strip() for line in str(highlight_text or "").splitlines() if line.strip()]
    if max_items > 0:
        lines = lines[:max_items]
    return json.dumps(lines, ensure_ascii=False)


def random_stat_value() -> int:
    """生成随机统计值"""
    return random.randint(1000, 10000)


def normalize_stat_value(value: object) -> int:
    """规范化统计值，为空时返回随机值"""
    try:
        numeric_value = int(value or 0)
    except (TypeError, ValueError):
        numeric_value = 0
    return numeric_value if numeric_value > 0 else random_stat_value()


def build_stats_json(record: Dict[str, object], source_type: str) -> str:
    """构建统计 JSON 字符串"""
    if source_type == "hot_say":
        stats = [
            {"label": "浏览量", "value": str(normalize_stat_value(record.get("views")))},
            {"label": "访客数", "value": str(random_stat_value())},
            {"label": "点赞数", "value": str(normalize_stat_value(record.get("likes")))},
            {"label": "评论数", "value": str(normalize_stat_value(record.get("replies")))},
        ]
    elif source_type == "offline":
        stats = [
            {"label": "浏览量", "value": str(normalize_stat_value(record.get("views")))},
            {"label": "访客数", "value": str(random_stat_value())},
            {"label": "核销数", "value": str(random_stat_value())},
        ]
    else:
        raise ValueError(f"不支持的 type: {source_type}")

    return json.dumps(stats, ensure_ascii=False)


def transform_record(record: Dict[str, object], highlight_limit: int) -> Dict[str, object]:
    """将 hot_say 记录转换为案例库记录"""
    source_type = str(record.get("type") or "").strip()
    if source_type not in TYPE_TO_CATEGORY_ID:
        raise ValueError(f"不支持的 type: {source_type}")

    cover_url = record.get("logo") or ""
    head_url = record.get("hot_spot_url") or cover_url

    return {
        "category_id": TYPE_TO_CATEGORY_ID[source_type],
        "title": record.get("say_name") or "",
        "cover_url": cover_url,
        "head_url": head_url,
        "description": record.get("description") or "",
        "participants": normalize_stat_value(record.get("participants")),
        "stats_json": build_stats_json(record, source_type),
        "highlight": format_highlight_as_json(record.get("highlight"), max_items=highlight_limit),
        "summary": record.get("summary") or "",
        "tag": random.choice(TAG_OPTIONS),
    }


def insert_case_library_records(connection, records: Iterable[Dict[str, object]]) -> int:
    """写入案例库表"""
    sql = """
        INSERT INTO wb_activity_case_libraries (
            category_id,
            title,
            cover_url,
            head_url,
            description,
            participants,
            stats_json,
            highlight,
            summary,
            tag,
            created_at,
            updated_at
        ) VALUES (
            %(category_id)s,
            %(title)s,
            %(cover_url)s,
            %(head_url)s,
            %(description)s,
            %(participants)s,
            %(stats_json)s,
            %(highlight)s,
            %(summary)s,
            %(tag)s,
            NOW(),
            NOW()
        )
    """

    record_list = list(records)
    if not record_list:
        return 0

    with connection.cursor() as cursor:
        cursor.executemany(sql, record_list)

    connection.commit()
    return len(record_list)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="将 data.hot_say 中 highlight、summary 非空的数据迁移到 luyi_ai.wb_activity_case_libraries"
    )
    parser.add_argument("--host", default=DEFAULT_DB_CONFIG["host"], help="数据库主机")
    parser.add_argument("--port", type=int, default=DEFAULT_DB_CONFIG["port"], help="数据库端口")
    parser.add_argument("--user", default=DEFAULT_DB_CONFIG["user"], help="数据库用户名")
    parser.add_argument("--password", default=DEFAULT_DB_CONFIG["password"], help="数据库密码")
    parser.add_argument("--source-db", default="data", help="源数据库名")
    parser.add_argument("--target-db", default="luyi_ai", help="目标数据库名")
    parser.add_argument("--limit", type=int, default=None, help="每种类型迁移条数，默认迁移全部")
    parser.add_argument("--highlight-limit", type=int, default=3, help="亮点最多保留几条，默认 3")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际写入")
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    if args.limit is not None and args.limit <= 0:
        print("✗ --limit 必须大于 0")
        sys.exit(1)
    if args.highlight_limit <= 0:
        print("✗ --highlight-limit 必须大于 0")
        sys.exit(1)

    source_db_config = {
        **DEFAULT_DB_CONFIG,
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "password": args.password,
        "database": args.source_db,
    }
    target_db_config = {
        **DEFAULT_DB_CONFIG,
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "password": args.password,
        "database": args.target_db,
    }

    print("=" * 60)
    print("热议话题迁移到案例库")
    print("=" * 60)
    print(f"源库: {args.source_db}.hot_say")
    print(f"目标库: {args.target_db}.wb_activity_case_libraries")
    print("条件: highlight、summary 非空")
    print(f"每种类型条数: {args.limit if args.limit is not None else '全部'}")
    print(f"亮点保留条数: {args.highlight_limit}")
    print(f"试运行: {'是' if args.dry_run else '否'}")
    print("-" * 60)

    try:
        with get_connection(source_db_config) as source_conn:
            source_records = fetch_hot_say_records(source_conn, args.limit)

        if not source_records:
            print("⚠️ 未查询到符合条件的数据")
            return

        transformed_records = [transform_record(record, args.highlight_limit) for record in source_records]

        type_counts = {activity_type: 0 for activity_type in TYPE_TO_CATEGORY_ID}
        for record in source_records:
            source_type = str(record.get("type") or "").strip()
            if source_type in type_counts:
                type_counts[source_type] += 1

        print(f"✓ 已查询到 {len(source_records)} 条待迁移数据")
        for activity_type, count in type_counts.items():
            print(f"  - {activity_type}: {count} 条")

        for index, record in enumerate(source_records, start=1):
            source_type = record.get("type") or ""
            category_id = TYPE_TO_CATEGORY_ID.get(source_type, "未知")
            highlight_json = format_highlight_as_json(record.get("highlight"), args.highlight_limit)
            assigned_record = transformed_records[index - 1]
            print(
                f"{index:02d}. hot_say.id={record['id']} | "
                f"type={source_type} -> category_id={category_id} | "
                f"title={record.get('say_name') or ''} | "
                f"tag={assigned_record['tag']} | "
                f"participants={assigned_record['participants']} | "
                f"stats_json={assigned_record['stats_json']} | "
                f"highlight={highlight_json}"
            )

        if args.dry_run:
            print("-" * 60)
            print("试运行结束，未执行写入")
            return

        with get_connection(target_db_config) as target_conn:
            inserted_count = insert_case_library_records(target_conn, transformed_records)

        print("-" * 60)
        print(f"✓ 迁移完成，成功写入 {inserted_count} 条数据")
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as error:
        print(f"✗ 执行失败: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
