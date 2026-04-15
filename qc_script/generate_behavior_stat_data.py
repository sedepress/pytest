#!/usr/bin/env python3
"""
行为统计测试数据生成脚本。

用法示例:
    python3 tools/generate_behavior_stat_data.py --kind hot-say --id 32
    python3 tools/generate_behavior_stat_data.py --kind activity --id 17 --days 7 --logs 24 --seed 20260324
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / "env.local.yaml"


@dataclass(frozen=True)
class TargetConfig:
    kind: str
    table: str
    id_column: str
    target_type: int
    cumulative_type: int
    daily_type: int


HOT_SAY = TargetConfig(
    kind="hot-say",
    table="wb_hot_saies",
    id_column="say_id",
    target_type=1,
    cumulative_type=7,
    daily_type=8,
)

ACTIVITY = TargetConfig(
    kind="activity",
    table="wb_activity",
    id_column="activity_id",
    target_type=2,
    cumulative_type=9,
    daily_type=10,
)

TARGETS = {
    HOT_SAY.kind: HOT_SAY,
    ACTIVITY.kind: ACTIVITY,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成行为统计测试数据并直接写入数据库")
    parser.add_argument("--kind", choices=sorted(TARGETS.keys()), required=True, help="目标类型")
    parser.add_argument("--id", type=int, required=True, dest="target_id", help="目标 id")
    parser.add_argument("--days", type=int, default=7, help="生成最近 N 天日统计，默认 7")
    parser.add_argument("--logs", type=int, default=24, help="生成当天行为日志条数，默认 24")
    parser.add_argument("--seed", type=int, default=None, help="随机种子，便于复现")
    return parser.parse_args()


def load_simple_env(path: Path) -> Dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"未找到配置文件: {path}")

    config: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        config[key.strip()] = value.strip()

    return config


def import_pymysql():
    try:
        import pymysql  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "缺少 PyMySQL 依赖，请先执行: python3 -m pip install PyMySQL"
        ) from exc

    return pymysql


def connect_mysql(config: Dict[str, str]):
    pymysql = import_pymysql()
    return pymysql.connect(
        host=config["mysql.host"],
        port=int(config["mysql.port"]),
        user=config["mysql.username"],
        password=config["mysql.password"],
        database=config["mysql.database"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def ensure_positive(name: str, value: int) -> None:
    if value <= 0:
        raise SystemExit(f"{name} 必须大于 0，当前值: {value}")


def random_string(rng: random.Random, length: int) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))


def unique_ticket_check_no(cursor, rng: random.Random) -> str:
    while True:
        code = "kb" + random_string(rng, 10)
        cursor.execute(
            "SELECT 1 FROM wb_activity_applies WHERE ticket_check_no=%s LIMIT 1",
            (code,),
        )
        if not cursor.fetchone():
            return code


def unique_ticket_id(cursor, rng: random.Random) -> str:
    while True:
        ticket_id = random_string(rng, 10)
        cursor.execute(
            "SELECT 1 FROM wb_activity_tickets WHERE ticket_id=%s LIMIT 1",
            (ticket_id,),
        )
        if not cursor.fetchone():
            return ticket_id


def load_target(cursor, target: TargetConfig, target_id: int) -> Dict[str, object]:
    sql = (
        f"SELECT {target.id_column} AS target_id, forum_id "
        f"FROM {target.table} "
        f"WHERE {target.id_column}=%s AND deleted_at IS NULL LIMIT 1"
    )
    cursor.execute(sql, (target_id,))
    row = cursor.fetchone()
    if not row:
        raise SystemExit(f"{target.kind} id={target_id} 不存在或已删除")
    return row


def load_users(cursor, limit: int = 20) -> List[Dict[str, object]]:
    cursor.execute(
        "SELECT user_id, nickname, avatar FROM wb_users WHERE user_id > 0 ORDER BY user_id ASC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    if len(rows) < 4:
        raise SystemExit("可用用户数量不足，至少需要 4 个用户来生成测试数据")
    return rows


def load_activity_verifier(
    cursor, activity_id: int, fallback_user: Dict[str, object]
) -> Dict[str, object]:
    cursor.execute(
        """
        SELECT v.user_id, u.nickname
        FROM wb_activity_verify v
        LEFT JOIN wb_users u ON v.user_id = u.user_id
        WHERE v.activity_id=%s
        ORDER BY v.id ASC
        LIMIT 1
        """,
        (activity_id,),
    )
    row = cursor.fetchone()
    if row:
        return row
    return {
        "user_id": int(fallback_user["user_id"]),
        "nickname": str(fallback_user.get("nickname") or "测试核销员"),
    }


def allocate_counts(
    total: int,
    weights: Dict[str, float],
    minimums: Optional[Dict[str, int]] = None,
) -> Dict[str, int]:
    minimums = minimums or {}
    counts = {key: minimums.get(key, 0) for key in weights}
    remaining = total - sum(counts.values())
    if remaining < 0:
        raise ValueError("最小分配数量超过总数")

    weight_sum = sum(weights.values())
    raw: Dict[str, float] = {}
    for key, weight in weights.items():
        raw[key] = 0 if weight_sum == 0 else remaining * weight / weight_sum
        counts[key] += int(raw[key])

    allocated = sum(counts.values())
    left = total - allocated
    if left > 0:
        fractions = sorted(
            weights.keys(),
            key=lambda key: (raw[key] - int(raw[key])),
            reverse=True,
        )
        for index in range(left):
            counts[fractions[index % len(fractions)]] += 1

    return counts


def adjust_activity_action_counts(counts: Dict[str, int]) -> Dict[str, int]:
    if counts["verify"] > counts["apply"]:
        diff = counts["verify"] - counts["apply"]
        counts["apply"] += diff
        if counts["view"] >= diff:
            counts["view"] -= diff
        else:
            remain = diff - counts["view"]
            counts["view"] = 0
            counts["like"] = max(0, counts["like"] - remain)
    return counts


def bucket_time(
    today_start: datetime, bucket_index: int, position: int, bucket_count: int, rng: random.Random
) -> datetime:
    bucket_ranges: List[Tuple[int, int]] = [(0, 5), (6, 11), (12, 17), (18, 23)]
    start_hour, end_hour = bucket_ranges[bucket_index]
    hour = rng.randint(start_hour, end_hour)
    minute = (position * 11 + rng.randint(0, 8)) % 60
    second = rng.randint(0, 50)
    return today_start.replace(hour=hour, minute=minute, second=second, microsecond=0)


def build_logs(
    kind: str,
    total_logs: int,
    user_ids: Sequence[int],
    today_start: datetime,
    rng: random.Random,
) -> List[Dict[str, object]]:
    if kind == HOT_SAY.kind:
        counts = allocate_counts(
            total_logs,
            {"view": 0.5, "like": 0.22, "comment": 0.1, "publish_thread": 0.1, "share": 0.08},
            {"view": 6, "like": 3, "comment": 1, "publish_thread": 1, "share": 1} if total_logs >= 12 else None,
        )
    else:
        counts = adjust_activity_action_counts(
            allocate_counts(
                total_logs,
                {"view": 0.45, "like": 0.2, "apply": 0.2, "verify": 0.15},
                {"view": 6, "like": 2, "apply": 2, "verify": 1} if total_logs >= 12 else None,
            )
        )

    actions: List[str] = []
    for action, count in counts.items():
        actions.extend([action] * count)
    rng.shuffle(actions)

    logs: List[Dict[str, object]] = []
    for index, action in enumerate(actions):
        bucket_index = index % 4
        created_at = bucket_time(today_start, bucket_index, index, total_logs, rng)
        user_id = int(rng.choice(user_ids))
        logs.append(
            {
                "action": action,
                "user_id": user_id,
                "created_at": created_at,
            }
        )

    logs.sort(key=lambda item: item["created_at"])
    return logs


def build_today_metrics(kind: str, logs: Sequence[Dict[str, object]]) -> Dict[str, int]:
    view_users = {int(item["user_id"]) for item in logs if item["action"] == "view"}
    non_view_users = {int(item["user_id"]) for item in logs if item["action"] != "view"}

    metrics = {
        "pv": sum(1 for item in logs if item["action"] == "view"),
        "uv": len(view_users),
        "users": len(non_view_users),
        "comments": sum(1 for item in logs if item["action"] in ("comment", "share")),
        "threads": sum(1 for item in logs if item["action"] == "publish_thread"),
        "likes": sum(1 for item in logs if item["action"] == "like"),
    }

    if kind == ACTIVITY.kind:
        metrics["comments"] = 0
        metrics["threads"] = 0

    return metrics


def build_day_series(
    kind: str,
    days: int,
    today: date,
    today_metrics: Dict[str, int],
    rng: random.Random,
) -> List[Dict[str, object]]:
    series: List[Dict[str, object]] = []
    for offset in range(days):
        current_date = today - timedelta(days=days - offset - 1)
        if offset == days - 1:
            metrics = dict(today_metrics)
        else:
            factor = 0.55 + 0.08 * offset
            metrics = {
                "pv": max(1, int(today_metrics["pv"] * factor) + rng.randint(0, 3)),
                "uv": max(1, int(today_metrics["uv"] * factor) + rng.randint(0, 2)),
                "users": max(1, int(today_metrics["users"] * factor) + rng.randint(0, 1)),
                "comments": max(0, int(today_metrics["comments"] * factor) + rng.randint(0, 1)),
                "threads": max(0, int(today_metrics["threads"] * factor) + (1 if offset % 3 == 0 and today_metrics["threads"] > 0 else 0)),
                "likes": max(0, int(today_metrics["likes"] * factor) + rng.randint(0, 1)),
            }
            if kind == ACTIVITY.kind:
                metrics["comments"] = 0
                metrics["threads"] = 0

        series.append({"date": current_date, "metrics": metrics})

    return series


def build_activity_apply_plan(
    day_series: Sequence[Dict[str, object]],
    today_apply_count: int,
    today_verify_count: int,
    rng: random.Random,
) -> List[Dict[str, object]]:
    plan: List[Dict[str, object]] = []
    total_days = len(day_series)
    for index, day in enumerate(day_series):
        current_date = day["date"]
        if index == total_days - 1:
            apply_count = today_apply_count
            verify_count = min(today_verify_count, apply_count)
        else:
            base = max(1, int(today_apply_count * (0.5 + index * 0.08)))
            apply_count = base + rng.randint(0, 2)
            verify_count = min(apply_count, max(0, int(apply_count * 0.5) + rng.randint(0, 1)))

        plan.append(
            {
                "date": current_date,
                "apply_count": apply_count,
                "verify_count": verify_count,
            }
        )

    return plan


def sum_metric_series(day_series: Sequence[Dict[str, object]]) -> Dict[str, int]:
    total = {"pv": 0, "uv": 0, "users": 0, "comments": 0, "threads": 0, "likes": 0}
    for day in day_series:
        metrics = day["metrics"]
        for key in total:
            total[key] += int(metrics[key])
    return total


def upsert_statistics_row(
    cursor,
    forum_id: int,
    stat_type: int,
    target_id: int,
    stat_date: Optional[date],
    metrics: Dict[str, int],
    now: datetime,
) -> str:
    if stat_date is None:
        cursor.execute(
            """
            SELECT id FROM wb_statistics
            WHERE fid=%s AND type=%s AND type_pk_id=%s AND date IS NULL
            ORDER BY id ASC
            LIMIT 1
            """,
            (forum_id, stat_type, target_id),
        )
    else:
        cursor.execute(
            """
            SELECT id FROM wb_statistics
            WHERE fid=%s AND type=%s AND type_pk_id=%s AND date=%s
            ORDER BY id ASC
            LIMIT 1
            """,
            (forum_id, stat_type, target_id, stat_date),
        )

    row = cursor.fetchone()
    if row:
        cursor.execute(
            """
            UPDATE wb_statistics
            SET pv = pv + %s,
                uv = uv + %s,
                users = users + %s,
                comments = comments + %s,
                threads = threads + %s,
                likes = likes + %s,
                updated_at = %s
            WHERE id=%s
            """,
            (
                metrics["pv"],
                metrics["uv"],
                metrics["users"],
                metrics["comments"],
                metrics["threads"],
                metrics["likes"],
                now,
                int(row["id"]),
            ),
        )
        return "updated"

    cursor.execute(
        """
        INSERT INTO wb_statistics
        (
            fid, type, type_pk_id, likes, comments, views, shares, pv, uv,
            coupon, goods_click, threads, publish_thread_users, new_users, users,
            orders, favorites, distribution_price, date, created_at, updated_at,
            mark_likes, mark_threads, mark_comments
        )
        VALUES
        (%s, %s, %s, %s, %s, 0, 0, %s, %s, 0, 0, %s, 0, 0, %s, 0, 0, 0, %s, %s, %s, 0, 0, 0)
        """,
        (
            forum_id,
            stat_type,
            target_id,
            metrics["likes"],
            metrics["comments"],
            metrics["pv"],
            metrics["uv"],
            metrics["threads"],
            metrics["users"],
            stat_date,
            now,
            now,
        ),
    )
    return "inserted"


def insert_behavior_logs(
    cursor,
    forum_id: int,
    target: TargetConfig,
    target_id: int,
    logs: Sequence[Dict[str, object]],
) -> int:
    sql = """
        INSERT INTO wb_behavior_logs
        (forum_id, user_id, target_type, target_id, action, extra, created_at)
        VALUES (%s, %s, %s, %s, %s, NULL, %s)
    """
    params = [
        (
            forum_id,
            int(item["user_id"]),
            target.target_type,
            target_id,
            str(item["action"]),
            item["created_at"],
        )
        for item in logs
    ]
    cursor.executemany(sql, params)
    return len(params)


def ensure_activity_ticket(
    cursor,
    activity_id: int,
    forum_id: int,
    total_apply_count: int,
    now: datetime,
    rng: random.Random,
) -> Tuple[str, bool]:
    cursor.execute(
        """
        SELECT ticket_id FROM wb_activity_tickets
        WHERE activity_id=%s AND deleted_at IS NULL
        ORDER BY created_at ASC, ticket_id ASC
        LIMIT 1
        """,
        (activity_id,),
    )
    row = cursor.fetchone()
    if row:
        ticket_id = str(row["ticket_id"])
        cursor.execute(
            """
            UPDATE wb_activity_tickets
            SET sale_total = sale_total + %s,
                is_apply = 1,
                updated_at = %s
            WHERE ticket_id=%s
            """,
            (total_apply_count, now, ticket_id),
        )
        return ticket_id, False

    ticket_id = unique_ticket_id(cursor, rng)
    cursor.execute(
        """
        INSERT INTO wb_activity_tickets
        (ticket_id, activity_id, name, kind, price, sale_total, `limit`, is_forbid_sale, is_apply, created_at, updated_at, deleted_at)
        VALUES (%s, %s, %s, 1, 0, %s, 0, 0, 1, %s, %s, NULL)
        """,
        (ticket_id, activity_id, "测试票", total_apply_count, now, now),
    )
    return ticket_id, True


def insert_activity_applies(
    cursor,
    activity_id: int,
    forum_id: int,
    ticket_id: str,
    users: Sequence[Dict[str, object]],
    verifier: Dict[str, object],
    apply_plan: Sequence[Dict[str, object]],
    rng: random.Random,
) -> Dict[str, int]:
    inserted = 0
    verified = 0
    for day in apply_plan:
        current_date: date = day["date"]
        apply_count = int(day["apply_count"])
        verify_count = int(day["verify_count"])
        verify_indexes = set(rng.sample(range(apply_count), verify_count)) if verify_count > 0 else set()

        for index in range(apply_count):
            user = users[(index + rng.randint(0, len(users) - 1)) % len(users)]
            created_at = datetime.combine(current_date, datetime.min.time()).replace(
                hour=9 + (index % 9),
                minute=(index * 7) % 60,
                second=(index * 11) % 60,
            )

            verify_at = None
            verify_user_id = 0
            verify_name = None
            updated_at = created_at
            if index in verify_indexes:
                verify_at = created_at + timedelta(hours=2 + (index % 5))
                verify_user_id = int(verifier["user_id"])
                verify_name = str(verifier.get("nickname") or "测试核销员")[:20]
                updated_at = verify_at
                verified += 1

            name = str(user.get("nickname") or f"测试用户{user['user_id']}")[:40]
            phone = f"13{rng.randint(100000000, 999999999)}"[:11]
            cursor.execute(
                """
                INSERT INTO wb_activity_applies
                (
                    activity_id, forum_id, user_id, name, phone, email, ticket_id,
                    extend_fields, is_allow, ticket_check_no, verify_user_id, verify_name,
                    verify_at, created_at, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, '', %s, '{}', 1, %s, %s, %s, %s, %s, %s)
                """,
                (
                    activity_id,
                    forum_id,
                    int(user["user_id"]),
                    name,
                    phone,
                    ticket_id,
                    unique_ticket_check_no(cursor, rng),
                    verify_user_id,
                    verify_name,
                    verify_at,
                    created_at,
                    updated_at,
                ),
            )
            inserted += 1

    return {"applies": inserted, "verified": verified}


def update_activity_apply_total(cursor, activity_id: int, added_count: int, now: datetime) -> None:
    cursor.execute(
        """
        UPDATE wb_activity
        SET applies = applies + %s,
            updated_at = %s
        WHERE activity_id=%s
        """,
        (added_count, now, activity_id),
    )


def generate_hot_say_data(
    cursor,
    target: TargetConfig,
    target_id: int,
    forum_id: int,
    users: Sequence[Dict[str, object]],
    days: int,
    log_count: int,
    rng: random.Random,
) -> Dict[str, object]:
    now = datetime.now()
    today = now.date()
    today_start = datetime.combine(today, datetime.min.time())
    logs = build_logs(target.kind, log_count, [int(user["user_id"]) for user in users], today_start, rng)
    today_metrics = build_today_metrics(target.kind, logs)
    day_series = build_day_series(target.kind, days, today, today_metrics, rng)
    total_metrics = sum_metric_series(day_series)

    stat_result = {"inserted": 0, "updated": 0}
    for day in day_series:
        status = upsert_statistics_row(
            cursor,
            forum_id,
            target.daily_type,
            target_id,
            day["date"],
            day["metrics"],
            now,
        )
        stat_result[status] += 1

    status = upsert_statistics_row(
        cursor,
        forum_id,
        target.cumulative_type,
        target_id,
        None,
        total_metrics,
        now,
    )
    stat_result[status] += 1

    inserted_logs = insert_behavior_logs(cursor, forum_id, target, target_id, logs)

    return {
        "statistics": stat_result,
        "logs": inserted_logs,
        "day_series": day_series,
        "total_metrics": total_metrics,
    }


def generate_activity_data(
    cursor,
    target: TargetConfig,
    target_id: int,
    forum_id: int,
    users: Sequence[Dict[str, object]],
    days: int,
    log_count: int,
    rng: random.Random,
) -> Dict[str, object]:
    now = datetime.now()
    today = now.date()
    today_start = datetime.combine(today, datetime.min.time())
    logs = build_logs(target.kind, log_count, [int(user["user_id"]) for user in users], today_start, rng)
    today_metrics = build_today_metrics(target.kind, logs)
    today_apply_count = sum(1 for item in logs if item["action"] == "apply")
    today_verify_count = sum(1 for item in logs if item["action"] == "verify")
    day_series = build_day_series(target.kind, days, today, today_metrics, rng)
    apply_plan = build_activity_apply_plan(day_series, today_apply_count, today_verify_count, rng)
    total_metrics = sum_metric_series(day_series)

    total_apply_count = sum(int(item["apply_count"]) for item in apply_plan)
    ticket_id, ticket_created = ensure_activity_ticket(cursor, target_id, forum_id, total_apply_count, now, rng)
    verifier = load_activity_verifier(cursor, target_id, users[0])
    apply_result = insert_activity_applies(cursor, target_id, forum_id, ticket_id, users, verifier, apply_plan, rng)
    update_activity_apply_total(cursor, target_id, apply_result["applies"], now)

    stat_result = {"inserted": 0, "updated": 0}
    for day in day_series:
        status = upsert_statistics_row(
            cursor,
            forum_id,
            target.daily_type,
            target_id,
            day["date"],
            day["metrics"],
            now,
        )
        stat_result[status] += 1

    status = upsert_statistics_row(
        cursor,
        forum_id,
        target.cumulative_type,
        target_id,
        None,
        total_metrics,
        now,
    )
    stat_result[status] += 1

    inserted_logs = insert_behavior_logs(cursor, forum_id, target, target_id, logs)

    return {
        "statistics": stat_result,
        "logs": inserted_logs,
        "day_series": day_series,
        "total_metrics": total_metrics,
        "activity_apply_result": apply_result,
        "ticket_id": ticket_id,
        "ticket_created": ticket_created,
    }


def main() -> int:
    args = parse_args()
    ensure_positive("id", args.target_id)
    ensure_positive("days", args.days)
    ensure_positive("logs", args.logs)

    seed = args.seed if args.seed is not None else int(time.time())
    rng = random.Random(seed)
    target = TARGETS[args.kind]
    config = load_simple_env(ENV_FILE)
    conn = connect_mysql(config)

    try:
        with conn.cursor() as cursor:
            target_info = load_target(cursor, target, args.target_id)
            forum_id = int(target_info["forum_id"])
            users = load_users(cursor)

            if target.kind == HOT_SAY.kind:
                result = generate_hot_say_data(
                    cursor, target, args.target_id, forum_id, users, args.days, args.logs, rng
                )
            else:
                result = generate_activity_data(
                    cursor, target, args.target_id, forum_id, users, args.days, args.logs, rng
                )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    output = {
        "kind": target.kind,
        "target_id": args.target_id,
        "forum_id": forum_id,
        "seed": seed,
        "days": args.days,
        "logs": args.logs,
        "result": result,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
