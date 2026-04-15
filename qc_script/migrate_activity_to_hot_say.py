#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
活动数据迁移脚本
将 wb_addons_activity 表的数据迁移到 hot_say 表
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional

import pymysql


class ActivityMigrator:
    """活动数据迁移器"""

    def __init__(self, db_config: Dict[str, Any], log_file: Optional[str] = None):
        """
        初始化迁移器

        Args:
            db_config: 数据库配置字典，包含 host, port, user, password, database
            log_file: 日志文件路径，None表示不记录日志文件
        """
        self.db_config = db_config
        self.connection: Optional[pymysql.Connection] = None
        self.logger = self._setup_logger(log_file)

    def _setup_logger(self, log_file: Optional[str]) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('ActivityMigrator')
        logger.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 文件处理器
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.db_config['host'],
                port=self.db_config.get('port', 3306),
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            msg = f"✓ 成功连接到数据库: {self.db_config['database']}"
            print(msg)
            self.logger.info(msg)
        except Exception as e:
            msg = f"✗ 数据库连接失败: {e}"
            print(msg)
            self.logger.error(msg)
            sys.exit(1)

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            msg = "✓ 数据库连接已关闭"
            print(msg)
            self.logger.info(msg)

    def fetch_activities(self, limit: Optional[int] = None) -> list:
        """
        从 wb_addons_activity 表获取活动数据

        Args:
            limit: 限制获取的记录数，None表示获取全部

        Returns:
            活动数据列表
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT
                        activity_id,
                        forum_id,
                        title,
                        content,
                        banner,
                        hot_banner,
                        location,
                        started_at,
                        ended_at,
                        views,
                        applies,
                        created_at,
                        updated_at,
                        deleted_at,
                        is_hide
                    FROM wb_addons_activity
                    WHERE deleted_at IS NULL
                """

                if limit:
                    sql += f" LIMIT {limit}"

                cursor.execute(sql)
                activities = cursor.fetchall()
                msg = f"✓ 从 wb_addons_activity 表获取到 {len(activities)} 条记录"
                print(msg)
                self.logger.info(msg)
                return activities
        except Exception as e:
            msg = f"✗ 获取活动数据失败: {e}"
            print(msg)
            self.logger.error(msg)
            return []

    def transform_activity_to_hot_say(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        将活动数据转换为热议数据格式

        Args:
            activity: 活动数据字典

        Returns:
            转换后的热议数据字典
        """
        # 处理 content 字段（可能是 bytes 类型）
        content = activity.get('content')
        if isinstance(content, bytes):
            try:
                content = content.decode('utf-8')
            except:
                content = ''
        elif content is None:
            content = ''

        # is_show 根据 is_hide 反转
        is_show = 0 if activity.get('is_hide', 0) == 1 else 1

        return {
            'source': 'fansquan',
            'type': 'offline',
            'forum_id': activity.get('forum_id', 0),
            'say_name': activity.get('title', ''),
            'logo': activity.get('banner', ''),
            'head_logo': activity.get('hot_banner', ''),
            'hot_spot_url': activity.get('banner', ''),  # 使用 banner 作为热点列表显示图片
            'description': content,
            'is_show': is_show,
            'is_top': 0,
            'participants': activity.get('applies', 0),
            'views': activity.get('views', 0),
            'replies': 0,
            'favorites': 0,
            'shares': 0,
            'likes': 0,
            'score': '',
            'created_at': activity.get('created_at'),
            'updated_at': activity.get('updated_at'),
            'deleted_at': activity.get('deleted_at')
        }

    def insert_hot_say(self, hot_say_data: Dict[str, Any]) -> bool:
        """
        插入数据到 hot_say 表

        Args:
            hot_say_data: 热议数据字典

        Returns:
            是否插入成功
        """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO hot_say (
                        source, type, forum_id, say_name, logo, head_logo,
                        hot_spot_url, description, is_show, is_top,
                        participants, views, replies, favorites, shares,
                        likes, score, created_at, updated_at, deleted_at
                    ) VALUES (
                        %(source)s, %(type)s, %(forum_id)s, %(say_name)s, %(logo)s, %(head_logo)s,
                        %(hot_spot_url)s, %(description)s, %(is_show)s, %(is_top)s,
                        %(participants)s, %(views)s, %(replies)s, %(favorites)s, %(shares)s,
                        %(likes)s, %(score)s, %(created_at)s, %(updated_at)s, %(deleted_at)s
                    )
                """
                cursor.execute(sql, hot_say_data)
                return True
        except Exception as e:
            msg = f"✗ 插入数据失败 (forum_id={hot_say_data.get('forum_id')}, say_name={hot_say_data.get('say_name')}): {e}"
            print(msg)
            self.logger.error(msg)
            return False

    def migrate(self, batch_size: int = 100, limit: Optional[int] = None, dry_run: bool = False):
        """
        执行数据迁移

        Args:
            batch_size: 批量提交的记录数
            limit: 限制迁移的记录数，None表示迁移全部
            dry_run: 是否为试运行模式（不实际插入数据）
        """
        print("\n" + "="*60)
        print("开始数据迁移: wb_addons_activity -> hot_say")
        print("="*60)

        if dry_run:
            print("⚠️  试运行模式：不会实际插入数据")

        # 获取活动数据
        activities = self.fetch_activities(limit)

        if not activities:
            print("⚠️  没有需要迁移的数据")
            return

        total = len(activities)
        success_count = 0
        fail_count = 0

        print(f"\n开始迁移 {total} 条记录...")
        print("-" * 60)

        for idx, activity in enumerate(activities, 1):
            # 转换数据格式
            hot_say_data = self.transform_activity_to_hot_say(activity)

            # 插入数据
            if not dry_run:
                if self.insert_hot_say(hot_say_data):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                success_count += 1

            # 批量提交
            if not dry_run and idx % batch_size == 0:
                self.connection.commit()
                print(f"进度: {idx}/{total} ({idx*100//total}%) - 成功: {success_count}, 失败: {fail_count}")

        # 最后提交剩余的数据
        if not dry_run:
            self.connection.commit()

        # 输出统计信息
        print("-" * 60)
        print(f"\n迁移完成！")
        print(f"  总记录数: {total}")
        print(f"  成功: {success_count}")
        print(f"  失败: {fail_count}")
        print("="*60 + "\n")


def main():
    """主函数"""
    import argparse

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='活动数据迁移工具: wb_addons_activity -> hot_say')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式，不实际插入数据')
    parser.add_argument('--limit', type=int, default=None, help='限制迁移的记录数')
    parser.add_argument('--batch-size', type=int, default=100, help='批量提交的记录数')
    parser.add_argument('--log-file', type=str, default=None, help='日志文件路径')
    args = parser.parse_args()

    # 如果没有指定日志文件，使用默认文件名
    if args.log_file is None and not args.dry_run:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.log_file = f'migration_{timestamp}.log'

    # 尝试导入配置文件
    try:
        from db_config import DB_CONFIG
        db_config = DB_CONFIG
    except ImportError:
        print("⚠️  未找到 db_config.py 配置文件")
        print("请复制 db_config.example.py 为 db_config.py 并填入数据库配置")
        print("\n使用默认配置（需要手动修改脚本）...")

        # 默认配置
        db_config = {
            'host': 'v2.wezan.net',
            'port': 3306,
            'user': 'fansquan_dev',
            'password': 'webei95180',
            'database': 'data'
        }

    # 显示配置信息
    print("\n配置信息:")
    print(f"  数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    print(f"  批量大小: {args.batch_size}")
    print(f"  限制记录数: {args.limit if args.limit else '全部'}")
    print(f"  试运行模式: {'是' if args.dry_run else '否'}")
    if args.log_file:
        print(f"  日志文件: {args.log_file}")

    # 创建迁移器实例
    migrator = ActivityMigrator(db_config, log_file=args.log_file)

    try:
        # 连接数据库
        migrator.connect()

        # 执行迁移
        migrator.migrate(
            batch_size=args.batch_size,
            limit=args.limit,
            dry_run=args.dry_run
        )

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 迁移过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 关闭连接
        migrator.close()


if __name__ == '__main__':
    main()
