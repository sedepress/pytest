#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热议话题 API 服务器

功能：提供分页 API 接口，支持前端滚动加载
"""

import json
from contextlib import contextmanager
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import pymysql

# ==================== 数据库配置 ====================
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "fansquan_dev",
    "password": "webei95180",
    "database": "data",
    "charset": "utf8mb4",
}

# CDN 域名配置
CDN_CONFIG = {
    "default": "https://cdn.myfans.cc/",
    "youzan_fansquan": "https://youzan.myfans.cc/",
    "weimob_fansquan": "https://youzan.myfans.cc/",
}

# 来源映射
SOURCE_MAP = {
    "fansquan": "粉丝圈",
    "youzan_fansquan": "有赞",
    "weimob_fansquan": "微盟",
}

# 活动类型映射
TYPE_MAP = {
    "hot_say": "热议话题",
    "offline": "线下活动",
}

# 服务配置
HOST = "0.0.0.0"
PORT = 10086


@contextmanager
def get_connection():
    """获取数据库连接"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


def process_logo_url(logo: str, source: str = "") -> str:
    """处理 logo URL，根据来源使用不同 CDN"""
    if not logo:
        return ""
    if logo.startswith("https"):
        return logo

    # 根据来源选择 CDN
    cdn_base = CDN_CONFIG.get(source, CDN_CONFIG["default"])
    return f"{cdn_base}{logo}"


def update_review_notes(hot_say_id: int, highlight: str, summary: str):
    """更新热议话题的亮点和总结"""
    if hot_say_id <= 0:
        return {"code": 0, "message": "无效的记录 ID"}

    sql = """
        UPDATE hot_say
        SET `highlight` = %s, `summary` = %s
        WHERE id = %s AND deleted_at IS NULL
    """

    try:
        clean_highlight = highlight.strip()
        clean_summary = summary.strip()

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (clean_highlight, clean_summary, hot_say_id))
                conn.commit()

                if cursor.rowcount == 0:
                    return {"code": 0, "message": "记录不存在或已删除"}

        return {"code": 1, "message": "保存成功"}
    except Exception as e:
        print(f"[ERROR] 保存备注失败: {e}")
        return {"code": 0, "message": str(e)}


def fetch_hot_say_list(page: int = 1, page_size: int = 50, keyword: str = "", activity_type: str = "", source: str = "", sort_key: str = "id", sort_dir: str = "desc"):
    """分页查询热议话题"""

    # 允许的排序字段
    allowed_sort_keys = {"id", "participants", "views", "replies", "favorites", "shares", "likes", "score"}
    if sort_key not in allowed_sort_keys:
        sort_key = "id"
    if sort_dir not in ("asc", "desc"):
        sort_dir = "desc"

    offset = (page - 1) * page_size

    # 构建 SQL
    where_clause = "WHERE deleted_at IS NULL"
    params = []

    if keyword:
        where_clause += " AND say_name LIKE %s"
        params.append(f"%{keyword}%")

    # 活动类型筛选
    if activity_type:
        where_clause += " AND type = %s"
        params.append(activity_type)

    # 来源筛选
    if source:
        where_clause += " AND source = %s"
        params.append(source)

    # 查询总数
    count_sql = f"SELECT COUNT(*) FROM hot_say {where_clause}"

    # 查询数据
    data_sql = f"""
        SELECT
            id, say_name, logo, description, `highlight`, `summary`,
            participants, views, replies, favorites, shares, likes,
            created_at, source, score, type
        FROM hot_say
        {where_clause}
        ORDER BY {sort_key} {sort_dir}
        LIMIT %s OFFSET %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            # 获取总数
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]

            # 获取数据
            cursor.execute(data_sql, params + [page_size, offset])
            rows = cursor.fetchall()

    # 组装结果
    items = []
    for row in rows:
        source = row[13] or ""
        activity_type = row[15] or ""
        item_id = row[0]
        items.append({
            "id": item_id,
            "say_name": row[1] or "",
            "logo": process_logo_url(row[2] or "", source),  # 传入 source
            "description": row[3] or "",
            "highlight": row[4] or "",
            "summary": row[5] or "",
            "participants": row[6] or 0,
            "views": row[7] or 0,
            "replies": row[8] or 0,
            "favorites": row[9] or 0,
            "shares": row[10] or 0,
            "likes": row[11] or 0,
            "source": source,
            "source_name": SOURCE_MAP.get(source, source),
            "score": row[14] if row[14] is not None else 0,
            "type": activity_type,
            "type_name": TYPE_MAP.get(activity_type, activity_type),
        })

    return {
        "code": 1,
        "data": {
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    }


def update_score(hot_say_id: int, score: str):
    """更新热议话题的分数"""
    # 验证分数选项
    if score not in ("A", "B", "C", "D", ""):
        return {"code": 0, "message": "分数必须是 A、B、C、D 之一"}

    sql = "UPDATE hot_say SET score = %s WHERE id = %s"

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (score, hot_say_id))
                conn.commit()

                if cursor.rowcount == 0:
                    return {"code": 0, "message": "记录不存在"}

        return {"code": 1, "message": "更新成功"}
    except Exception as e:
        print(f"[ERROR] 更新分数失败: {e}")
        return {"code": 0, "message": str(e)}


def delete_hot_say(hot_say_id: int):
    """删除热议话题（软删除）"""
    sql = "UPDATE hot_say SET deleted_at = NOW() WHERE id = %s AND deleted_at IS NULL"

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (hot_say_id,))
                conn.commit()

                if cursor.rowcount == 0:
                    return {"code": 0, "message": "记录不存在或已删除"}

        return {"code": 1, "message": "删除成功"}
    except Exception as e:
        print(f"[ERROR] 删除失败: {e}")
        return {"code": 0, "message": str(e)}


def fetch_statistics(activity_type: str = "", source: str = ""):
    """获取统计数据"""
    where_clause = "WHERE deleted_at IS NULL"
    params = []

    # 活动类型筛选
    if activity_type:
        where_clause += " AND type = %s"
        params.append(activity_type)

    # 来源筛选
    if source:
        where_clause += " AND source = %s"
        params.append(source)

    sql = f"""
        SELECT
            COUNT(*) as total,
            COALESCE(SUM(views), 0) as total_views,
            COALESCE(SUM(participants), 0) as total_participants,
            COALESCE(SUM(likes), 0) as total_likes
        FROM hot_say
        {where_clause}
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()

        return {
            "code": 1,
            "data": {
                "total": int(row[0] or 0),
                "total_views": int(row[1] or 0),
                "total_participants": int(row[2] or 0),
                "total_likes": int(row[3] or 0),
            }
        }
    except Exception as e:
        print(f"[ERROR] 获取统计数据失败: {e}")
        return {
            "code": 0,
            "message": str(e),
            "data": {
                "total": 0,
                "total_views": 0,
                "total_participants": 0,
                "total_likes": 0,
            }
        }


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 获取参数的辅助函数
        def get_param(key, default=""):
            return query.get(key, [default])[0]

        try:
            if path == "/api/hot-say/list":
                # 分页列表接口
                page = int(get_param("page", "1"))
                page_size = int(get_param("page_size", "50"))
                keyword = get_param("keyword", "")
                activity_type = get_param("type", "")
                source = get_param("source", "")
                sort_key = get_param("sort_key", "id")
                sort_dir = get_param("sort_dir", "desc")

                result = fetch_hot_say_list(page, page_size, keyword, activity_type, source, sort_key, sort_dir)

            elif path == "/api/hot-say/stats":
                # 统计接口
                activity_type = get_param("type", "")
                source = get_param("source", "")
                result = fetch_statistics(activity_type, source)

            elif path == "/" or path == "/index.html":
                # 返回 HTML 页面
                self._set_headers("text/html; charset=utf-8")
                self.wfile.write(generate_html().encode("utf-8"))
                return

            else:
                result = {"code": 0, "message": "Not Found"}

            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            self._set_headers()
            result = {"code": 0, "message": str(e)}
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path == "/api/hot-say/update-score":
                # 读取请求体
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)

                hot_say_id = int(data.get("id", 0))
                score = str(data.get("score", ""))

                result = update_score(hot_say_id, score)

            elif path == "/api/hot-say/delete":
                # 删除接口
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)

                hot_say_id = int(data.get("id", 0))

                result = delete_hot_say(hot_say_id)

            elif path == "/api/hot-say/update-notes":
                # 更新亮点和总结
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)

                hot_say_id = int(data.get("id", 0))
                highlight = str(data.get("highlight", "") or "")
                summary = str(data.get("summary", "") or "")

                result = update_review_notes(hot_say_id, highlight, summary)

            else:
                result = {"code": 0, "message": "Not Found"}

            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            self._set_headers()
            result = {"code": 0, "message": str(e)}
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


def generate_html():
    """生成 HTML 页面"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>热议话题列表</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            color: #333;
        }
        .container { max-width: 1800px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 10px; color: #2c3e50; }
        .meta { text-align: center; color: #7f8c8d; margin-bottom: 20px; font-size: 14px; }

        .stats-bar {
            display: flex; justify-content: center; gap: 30px;
            margin-bottom: 20px; flex-wrap: wrap;
        }
        .stat-item {
            background: #fff; padding: 15px 25px; border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;
        }
        .stat-item .value { font-size: 24px; font-weight: bold; color: #3498db; }
        .stat-item .label { font-size: 12px; color: #95a5a6; margin-top: 5px; }

        .filter-bar {
            display: flex; justify-content: center; align-items: center;
            gap: 15px; margin-bottom: 20px; flex-wrap: wrap;
        }
        .search-box {
            display: flex; align-items: center; gap: 10px;
        }
        .search-box input {
            padding: 10px 20px; width: 300px; border: 1px solid #ddd;
            border-radius: 25px; font-size: 14px; outline: none;
        }
        .search-box input:focus { border-color: #3498db; box-shadow: 0 0 5px rgba(52,152,219,0.3); }

        .type-filter {
            display: flex; align-items: center; gap: 10px;
            background: #fff; padding: 8px 15px; border-radius: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .type-filter label {
            font-size: 14px; color: #7f8c8d; font-weight: 500;
        }
        .type-filter select {
            padding: 6px 12px; border: 1px solid #ddd;
            border-radius: 15px; font-size: 14px; outline: none;
            cursor: pointer; background: #fff;
        }
        .type-filter select:focus { border-color: #3498db; }

        .table-container {
            background: #fff; border-radius: 10px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1); overflow: hidden;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #ecf0f1; }
        th { background: #3498db; color: white; font-weight: 500; position: sticky; top: 0; z-index: 10; }
        th.sortable { cursor: pointer; user-select: none; }
        th.sortable:hover { background: #2980b9; }
        th.asc, th.desc { color: #ff4444; }
        th .sort-icon { margin-left: 5px; font-size: 14px; }
        tr:hover { background: #f8f9fa; }

        .logo { width: 50px; height: 50px; border-radius: 8px; object-fit: cover; background: #ecf0f1; }
        .logo-placeholder {
            display: inline-block; width: 50px; height: 50px; line-height: 50px;
            background: #ecf0f1; border-radius: 8px; font-size: 10px; color: #95a5a6;
        }
        .title { text-align: left; font-weight: 500; max-width: 200px; }
        .desc {
            text-align: left; color: #7f8c8d; font-size: 13px; max-width: 250px;
            max-height: 60px; overflow: hidden; cursor: pointer;
        }
        .desc:hover { color: #3498db; }
        .note-cell { min-width: 230px; }
        .note-input {
            width: 100%;
            min-height: 78px;
            padding: 8px 10px;
            border: 1px solid #d9dee7;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.5;
            color: #2c3e50;
            resize: vertical;
            outline: none;
            font-family: inherit;
            background: #fbfcfe;
            transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
        }
        .note-input:focus {
            border-color: #3498db;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(52,152,219,0.12);
        }
        .note-input.saving {
            border-color: #f39c12;
            background: #fff8e8;
        }
        .note-input.success {
            border-color: #27ae60;
            background: #eefaf3;
        }
        .note-input.error {
            border-color: #e74c3c;
            background: #fdeeee;
        }
        td:nth-child(n+6) { font-weight: 500; }

        .source-tag { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .source-fansquan { background: #e8f5e9; color: #2e7d32; }
        .source-youzan { background: #fff3e0; color: #e65100; }
        .source-weimob { background: #e3f2fd; color: #1565c0; }
        .source-unknown { background: #f5f5f5; color: #757575; }

        .type-tag { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .type-hot_say { background: #fce4ec; color: #c2185b; }
        .type-offline { background: #e1f5fe; color: #0277bd; }

        .score-select {
            width: 70px; padding: 5px 8px; border: 1px solid #ddd;
            border-radius: 4px; text-align: center; font-size: 14px;
            cursor: pointer;
        }
        .score-select:focus { border-color: #3498db; outline: none; }
        .score-select.saving { background: #fff3cd; }
        .score-select.success { background: #d4edda; }
        .score-select.error { background: #f8d7da; }

        .delete-btn {
            padding: 5px 12px; background: #e74c3c; color: white;
            border: none; border-radius: 4px; cursor: pointer;
            font-size: 12px; transition: background 0.3s;
        }
        .delete-btn:hover { background: #c0392b; }
        .delete-btn:disabled { background: #95a5a6; cursor: not-allowed; }

        .loading { text-align: center; padding: 30px; color: #7f8c8d; }
        .page-info { text-align: center; margin: 15px 0; color: #7f8c8d; font-size: 14px; }

        .pagination {
            display: flex; justify-content: center; align-items: center;
            gap: 10px; margin: 20px 0; flex-wrap: wrap;
        }
        .pagination button {
            padding: 8px 16px; border: 1px solid #ddd; background: #fff;
            border-radius: 4px; cursor: pointer; font-size: 14px;
            transition: all 0.3s;
        }
        .pagination button:hover:not(:disabled) {
            background: #3498db; color: white; border-color: #3498db;
        }
        .pagination button:disabled {
            background: #f5f5f5; color: #ccc; cursor: not-allowed;
        }
        .pagination button.active {
            background: #3498db; color: white; border-color: #3498db;
            font-weight: bold;
        }
        .pagination .page-num {
            padding: 8px 12px; min-width: 40px; text-align: center;
        }
        .pagination .ellipsis {
            padding: 8px 12px; color: #7f8c8d; cursor: default;
        }
        .pagination .page-jump {
            display: flex; align-items: center; gap: 5px;
            margin-left: 10px;
        }
        .pagination .page-jump input {
            width: 60px; padding: 6px 10px; border: 1px solid #ddd;
            border-radius: 4px; text-align: center; font-size: 14px;
        }
        .pagination .page-jump input:focus {
            border-color: #3498db; outline: none;
        }
        .pagination .page-jump button {
            padding: 6px 12px;
        }

        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center;
        }
        .modal-overlay.show { display: flex; }
        .modal-content {
            background: #fff; border-radius: 12px; max-width: 600px; max-height: 80vh;
            width: 90%; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        .modal-header {
            padding: 15px 20px; background: #3498db; color: white;
            display: flex; justify-content: space-between; align-items: center;
        }
        .modal-header h3 { margin: 0; font-size: 16px; font-weight: 500; }
        .modal-close { background: none; border: none; color: white; font-size: 24px; cursor: pointer; }
        .modal-body { padding: 20px; max-height: 60vh; overflow-y: auto; line-height: 1.8; }
        .modal-body img { max-width: 100%; height: auto; }

        @media (max-width: 1200px) { .table-container { overflow-x: auto; } table { min-width: 1600px; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>热议话题列表</h1>
        <p class="meta" id="metaInfo">加载中...</p>

        <div class="stats-bar" id="statsBar">
            <div class="stat-item"><div class="value" id="statTotal">-</div><div class="label">话题总数</div></div>
            <div class="stat-item"><div class="value" id="statViews">-</div><div class="label">总浏览量</div></div>
            <div class="stat-item"><div class="value" id="statParticipants">-</div><div class="label">总参与数</div></div>
            <div class="stat-item"><div class="value" id="statLikes">-</div><div class="label">总点赞数</div></div>
        </div>

        <div class="filter-bar">
            <div class="type-filter">
                <label>活动类型:</label>
                <select id="typeFilter">
                    <option value="">全部</option>
                    <option value="hot_say">热议话题</option>
                    <option value="offline">线下活动</option>
                </select>
            </div>
            <div class="type-filter">
                <label>数据来源:</label>
                <select id="sourceFilter">
                    <option value="">全部</option>
                    <option value="fansquan">粉丝圈</option>
                    <option value="youzan_fansquan">有赞</option>
                    <option value="weimob_fansquan">微盟</option>
                </select>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索话题名称...">
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th class="sortable" data-key="id">ID <span class="sort-icon">⇅</span></th>
                        <th>Logo</th>
                        <th>话题名称</th>
                        <th>活动类型</th>
                        <th>来源</th>
                        <th>描述</th>
                        <th>亮点</th>
                        <th>总结</th>
                        <th class="sortable" data-key="participants">参与数 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="views">浏览量 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="replies">回复数 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="favorites">收藏数 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="shares">分享数 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="likes">点赞数 <span class="sort-icon">⇅</span></th>
                        <th class="sortable" data-key="score">分数 <span class="sort-icon">⇅</span></th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>

        <p class="page-info" id="pageInfo"></p>
        <div class="loading" id="loading" style="display:none;">加载中...</div>

        <div class="pagination" id="pagination"></div>
    </div>

    <div class="modal-overlay" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">描述详情</h3>
                <button class="modal-close" id="modalClose">&times;</button>
            </div>
            <div class="modal-body" id="modalBody"></div>
        </div>
    </div>

    <script>
        const API_BASE = '';
        const PAGE_SIZE = 50;

        let currentPage = 1;
        let totalPages = 1;
        let totalRecords = 0;
        let isLoading = false;
        let keyword = '';
        let activityType = '';
        let sourceFilter = '';
        let sortKey = 'id';
        let sortDir = 'desc';
        let allItems = [];
        const noteSaveTimers = {};

        // 格式化数字
        function formatNumber(num) { return (num || 0).toLocaleString(); }

        // 转义 HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text || '';
            return div.innerHTML;
        }

        // 截取描述
        function truncateDesc(desc, len) {
            if (!desc) return '';
            const text = desc.replace(/<[^>]*>/g, '');
            return text.length > len ? text.substring(0, len) + '...' : text;
        }

        // 加载统计数据
        async function loadStats() {
            try {
                const url = `${API_BASE}/api/hot-say/stats?type=${encodeURIComponent(activityType)}&source=${encodeURIComponent(sourceFilter)}`;
                const resp = await fetch(url);
                const result = await resp.json();
                console.log('统计数据:', result);
                if (result.code === 1) {
                    const data = result.data;
                    document.getElementById('statTotal').textContent = formatNumber(data.total);
                    document.getElementById('statViews').textContent = formatNumber(data.total_views);
                    document.getElementById('statParticipants').textContent = formatNumber(data.total_participants);
                    document.getElementById('statLikes').textContent = formatNumber(data.total_likes);

                    // 根据筛选条件更新提示文本
                    let filterText = '';
                    const filters = [];
                    if (activityType === 'hot_say') {
                        filters.push('热议话题');
                    } else if (activityType === 'offline') {
                        filters.push('线下活动');
                    }
                    if (sourceFilter === 'fansquan') {
                        filters.push('粉丝圈');
                    } else if (sourceFilter === 'youzan_fansquan') {
                        filters.push('有赞');
                    } else if (sourceFilter === 'weimob_fansquan') {
                        filters.push('微盟');
                    }
                    if (filters.length > 0) {
                        filterText = '（' + filters.join(' - ') + '）';
                    }
                    document.getElementById('metaInfo').textContent = `共 ${formatNumber(data.total)} 条记录${filterText}`;
                } else {
                    console.error('统计接口返回错误:', result);
                    document.getElementById('metaInfo').textContent = '统计数据加载失败';
                }
            } catch (e) {
                console.error('加载统计失败:', e);
                document.getElementById('metaInfo').textContent = '统计数据加载失败: ' + e.message;
            }
        }

        // 加载列表数据
        async function loadData() {
            if (isLoading) return;
            isLoading = true;
            document.getElementById('loading').style.display = 'block';

            try {
                const url = `${API_BASE}/api/hot-say/list?page=${currentPage}&page_size=${PAGE_SIZE}&keyword=${encodeURIComponent(keyword)}&type=${encodeURIComponent(activityType)}&source=${encodeURIComponent(sourceFilter)}&sort_key=${sortKey}&sort_dir=${sortDir}`;
                const resp = await fetch(url);
                const result = await resp.json();

                if (result.code === 1) {
                    const data = result.data;
                    totalPages = data.total_pages;
                    totalRecords = data.total;
                    allItems = data.list || [];

                    renderTable(allItems);
                    renderPagination();

                    const start = (currentPage - 1) * PAGE_SIZE + 1;
                    const end = Math.min(currentPage * PAGE_SIZE, totalRecords);
                    document.getElementById('pageInfo').textContent = `显示 ${formatNumber(start)}-${formatNumber(end)} / 共 ${formatNumber(totalRecords)} 条`;
                }
            } catch (e) {
                console.error('加载数据失败:', e);
            } finally {
                isLoading = false;
                document.getElementById('loading').style.display = 'none';
            }
        }

        // 渲染表格
        function renderTable(items) {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            items.forEach(item => {
                const tr = document.createElement('tr');

                const logoHtml = item.logo
                    ? `<img class="logo" src="${item.logo}" alt="logo" loading="lazy">`
                    : '<span class="logo-placeholder">无图片</span>';

                const sourceClass = item.source === 'fansquan' ? 'source-fansquan'
                    : item.source === 'youzan_fansquan' ? 'source-youzan'
                    : item.source === 'weimob_fansquan' ? 'source-weimob'
                    : 'source-unknown';

                const typeClass = item.type === 'hot_say' ? 'type-hot_say'
                    : item.type === 'offline' ? 'type-offline'
                    : 'source-unknown';

                tr.innerHTML = `
                    <td>${item.id}</td>
                    <td>${logoHtml}</td>
                    <td class="title">${escapeHtml(item.say_name)}</td>
                    <td><span class="type-tag ${typeClass}">${item.type_name || item.type || '未知'}</span></td>
                    <td><span class="source-tag ${sourceClass}">${item.source_name || item.source || '未知'}</span></td>
                    <td class="desc" data-id="${item.id}">${truncateDesc(item.description, 50)}</td>
                    <td class="note-cell">
                        <textarea class="note-input" data-id="${item.id}" data-field="highlight" placeholder="填写亮点...">${escapeHtml(item.highlight)}</textarea>
                    </td>
                    <td class="note-cell">
                        <textarea class="note-input" data-id="${item.id}" data-field="summary" placeholder="填写总结...">${escapeHtml(item.summary)}</textarea>
                    </td>
                    <td>${formatNumber(item.participants)}</td>
                    <td>${formatNumber(item.views)}</td>
                    <td>${formatNumber(item.replies)}</td>
                    <td>${formatNumber(item.favorites)}</td>
                    <td>${formatNumber(item.shares)}</td>
                    <td>${formatNumber(item.likes)}</td>
                    <td>
                        <select class="score-select" data-id="${item.id}">
                            <option value="" ${!item.score ? 'selected' : ''}>-</option>
                            <option value="A" ${item.score === 'A' ? 'selected' : ''}>A</option>
                            <option value="B" ${item.score === 'B' ? 'selected' : ''}>B</option>
                            <option value="C" ${item.score === 'C' ? 'selected' : ''}>C</option>
                            <option value="D" ${item.score === 'D' ? 'selected' : ''}>D</option>
                        </select>
                    </td>
                    <td><button class="delete-btn" data-id="${item.id}">删除</button></td>
                `;
                tbody.appendChild(tr);
            });
        }

        // 渲染分页组件
        function renderPagination() {
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = '';

            if (totalPages <= 1) return;

            // 首页按钮
            const firstBtn = document.createElement('button');
            firstBtn.textContent = '首页';
            firstBtn.disabled = currentPage === 1;
            firstBtn.onclick = () => goToPage(1);
            pagination.appendChild(firstBtn);

            // 上一页按钮
            const prevBtn = document.createElement('button');
            prevBtn.textContent = '上一页';
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => goToPage(currentPage - 1);
            pagination.appendChild(prevBtn);

            // 页码按钮
            const pageNumbers = getPageNumbers();
            pageNumbers.forEach(num => {
                if (num === '...') {
                    const ellipsis = document.createElement('span');
                    ellipsis.className = 'ellipsis';
                    ellipsis.textContent = '...';
                    pagination.appendChild(ellipsis);
                } else {
                    const pageBtn = document.createElement('button');
                    pageBtn.className = 'page-num';
                    pageBtn.textContent = num;
                    if (num === currentPage) {
                        pageBtn.classList.add('active');
                    }
                    pageBtn.onclick = () => goToPage(num);
                    pagination.appendChild(pageBtn);
                }
            });

            // 下一页按钮
            const nextBtn = document.createElement('button');
            nextBtn.textContent = '下一页';
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => goToPage(currentPage + 1);
            pagination.appendChild(nextBtn);

            // 尾页按钮
            const lastBtn = document.createElement('button');
            lastBtn.textContent = '尾页';
            lastBtn.disabled = currentPage === totalPages;
            lastBtn.onclick = () => goToPage(totalPages);
            pagination.appendChild(lastBtn);

            // 页码跳转输入框
            const jumpContainer = document.createElement('div');
            jumpContainer.className = 'page-jump';

            const jumpLabel = document.createElement('span');
            jumpLabel.textContent = '跳转到';
            jumpContainer.appendChild(jumpLabel);

            const jumpInput = document.createElement('input');
            jumpInput.type = 'number';
            jumpInput.min = '1';
            jumpInput.max = totalPages.toString();
            jumpInput.placeholder = '页码';
            jumpInput.id = 'pageJumpInput';
            jumpContainer.appendChild(jumpInput);

            const jumpBtn = document.createElement('button');
            jumpBtn.textContent = '跳转';
            jumpBtn.onclick = () => handlePageJump();
            jumpContainer.appendChild(jumpBtn);

            pagination.appendChild(jumpContainer);

            // 回车键跳转
            jumpInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    handlePageJump();
                }
            });
        }

        // 处理页码跳转
        function handlePageJump() {
            const input = document.getElementById('pageJumpInput');
            const page = parseInt(input.value);

            if (!page || isNaN(page)) {
                alert('请输入有效的页码');
                return;
            }

            if (page < 1 || page > totalPages) {
                alert(`页码必须在 1 到 ${totalPages} 之间`);
                return;
            }

            input.value = '';
            goToPage(page);
        }

        // 获取要显示的页码数组
        function getPageNumbers() {
            const pages = [];
            const maxVisible = 7; // 最多显示7个页码按钮

            if (totalPages <= maxVisible) {
                // 总页数少于最大显示数，显示所有页码
                for (let i = 1; i <= totalPages; i++) {
                    pages.push(i);
                }
            } else {
                // 总页数多于最大显示数，智能显示
                if (currentPage <= 4) {
                    // 当前页在前面
                    for (let i = 1; i <= 5; i++) pages.push(i);
                    pages.push('...');
                    pages.push(totalPages);
                } else if (currentPage >= totalPages - 3) {
                    // 当前页在后面
                    pages.push(1);
                    pages.push('...');
                    for (let i = totalPages - 4; i <= totalPages; i++) pages.push(i);
                } else {
                    // 当前页在中间
                    pages.push(1);
                    pages.push('...');
                    for (let i = currentPage - 1; i <= currentPage + 1; i++) pages.push(i);
                    pages.push('...');
                    pages.push(totalPages);
                }
            }

            return pages;
        }

        // 跳转到指定页
        function goToPage(page) {
            if (page < 1 || page > totalPages || page === currentPage) return;
            currentPage = page;
            loadData();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // 搜索
        function handleSearch() {
            keyword = document.getElementById('searchInput').value.trim();
            currentPage = 1;
            loadData();
        }

        // 类型筛选
        function handleTypeFilter() {
            activityType = document.getElementById('typeFilter').value;
            currentPage = 1;
            loadStats();
            loadData();
        }

        // 来源筛选
        function handleSourceFilter() {
            sourceFilter = document.getElementById('sourceFilter').value;
            currentPage = 1;
            loadStats();
            loadData();
        }

        // 排序
        function handleSort(key) {
            if (sortKey === key) {
                sortDir = sortDir === 'asc' ? 'desc' : 'asc';
            } else {
                sortKey = key;
                sortDir = 'desc';
            }

            // 更新表头样式
            document.querySelectorAll('th.sortable').forEach(th => {
                th.classList.remove('asc', 'desc');
                th.querySelector('.sort-icon').textContent = '⇅';
            });
            const activeTh = document.querySelector(`th[data-key="${key}"]`);
            activeTh.classList.add(sortDir);
            activeTh.querySelector('.sort-icon').textContent = sortDir === 'asc' ? '↑' : '↓';

            currentPage = 1;
            loadData();
        }

        // 模态框
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');

        function showModal(title, content) {
            modalTitle.textContent = title;
            modalBody.innerHTML = content || '<p style="color:#999;">暂无描述</p>';
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }

        function hideModal() {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }

        function setNoteInputState(textareas, state) {
            textareas.forEach(textarea => {
                textarea.classList.remove('saving', 'success', 'error');
                if (state) {
                    textarea.classList.add(state);
                }
            });
        }

        async function saveRowNotes(hotSayId) {
            delete noteSaveTimers[hotSayId];
            const noteInputs = Array.from(document.querySelectorAll(`.note-input[data-id="${hotSayId}"]`));
            if (noteInputs.length === 0) return;

            const highlightInput = noteInputs.find(input => input.dataset.field === 'highlight');
            const summaryInput = noteInputs.find(input => input.dataset.field === 'summary');

            setNoteInputState(noteInputs, 'saving');

            try {
                const resp = await fetch(`${API_BASE}/api/hot-say/update-notes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: hotSayId,
                        highlight: highlightInput ? highlightInput.value : '',
                        summary: summaryInput ? summaryInput.value : ''
                    })
                });
                const result = await resp.json();

                if (result.code !== 1) {
                    throw new Error(result.message || '保存失败');
                }

                const item = allItems.find(data => data.id === hotSayId);
                if (item) {
                    item.highlight = highlightInput ? highlightInput.value : '';
                    item.summary = summaryInput ? summaryInput.value : '';
                }

                setNoteInputState(noteInputs, 'success');
                setTimeout(() => setNoteInputState(noteInputs, ''), 1000);
            } catch (e) {
                console.error('保存亮点/总结失败:', e);
                setNoteInputState(noteInputs, 'error');
                setTimeout(() => setNoteInputState(noteInputs, ''), 2000);
            }
        }

        function queueSaveRowNotes(hotSayId, immediate = false) {
            if (noteSaveTimers[hotSayId]) {
                clearTimeout(noteSaveTimers[hotSayId]);
            }

            if (immediate) {
                delete noteSaveTimers[hotSayId];
                saveRowNotes(hotSayId);
                return;
            }

            noteSaveTimers[hotSayId] = setTimeout(() => {
                saveRowNotes(hotSayId);
                delete noteSaveTimers[hotSayId];
            }, 400);
        }

        // 事件绑定
        document.getElementById('modalClose').addEventListener('click', hideModal);
        modal.addEventListener('click', e => { if (e.target === modal) hideModal(); });
        document.addEventListener('keydown', e => { if (e.key === 'Escape') hideModal(); });

        document.getElementById('tableBody').addEventListener('click', e => {
            const descCell = e.target.closest('.desc');
            if (descCell) {
                const id = parseInt(descCell.dataset.id);
                const item = allItems.find(data => data.id === id);
                if (item) {
                    showModal(item.say_name || '描述详情', item.description);
                }
            }
        });

        let searchTimer = null;
        document.getElementById('searchInput').addEventListener('input', () => {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(handleSearch, 300);
        });

        // 类型筛选器事件监听
        document.getElementById('typeFilter').addEventListener('change', handleTypeFilter);

        // 来源筛选器事件监听
        document.getElementById('sourceFilter').addEventListener('change', handleSourceFilter);

        document.querySelectorAll('th.sortable').forEach(th => {
            th.addEventListener('click', () => handleSort(th.dataset.key));
        });

        // 分数下拉选择框事件处理
        document.getElementById('tableBody').addEventListener('change', async (e) => {
            const select = e.target;
            if (!select.classList.contains('score-select')) return;

            const id = parseInt(select.dataset.id);
            const score = select.value;

            // 设置保存状态
            select.classList.remove('success', 'error');
            select.classList.add('saving');

            try {
                const resp = await fetch(`${API_BASE}/api/hot-say/update-score`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id, score })
                });
                const result = await resp.json();

                select.classList.remove('saving');
                if (result.code === 1) {
                    select.classList.add('success');
                    setTimeout(() => select.classList.remove('success'), 1000);
                } else {
                    select.classList.add('error');
                    console.error('更新分数失败:', result.message);
                    setTimeout(() => select.classList.remove('error'), 2000);
                }
            } catch (e) {
                select.classList.remove('saving');
                select.classList.add('error');
                console.error('更新分数失败:', e);
                setTimeout(() => select.classList.remove('error'), 2000);
            }
        });

        document.getElementById('tableBody').addEventListener('input', (e) => {
            const textarea = e.target;
            if (!textarea.classList.contains('note-input')) return;

            queueSaveRowNotes(parseInt(textarea.dataset.id));
        });

        document.getElementById('tableBody').addEventListener('blur', (e) => {
            const textarea = e.target;
            if (!textarea.classList.contains('note-input')) return;

            queueSaveRowNotes(parseInt(textarea.dataset.id), true);
        }, true);

        // 删除按钮事件处理
        document.getElementById('tableBody').addEventListener('click', async (e) => {
            const deleteBtn = e.target.closest('.delete-btn');
            if (!deleteBtn) return;

            const id = parseInt(deleteBtn.dataset.id);
            const item = allItems.find(d => d.id === id);

            if (!item) return;

            // 确认删除
            if (!confirm(`确定要删除热议话题"${item.say_name}"吗？\n\n此操作不可恢复！`)) {
                return;
            }

            // 禁用按钮
            deleteBtn.disabled = true;
            deleteBtn.textContent = '删除中...';

            try {
                const resp = await fetch(`${API_BASE}/api/hot-say/delete`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id })
                });
                const result = await resp.json();

                if (result.code === 1) {
                    // 删除成功，从列表中移除该行
                    const row = deleteBtn.closest('tr');
                    row.style.opacity = '0.5';
                    row.style.transition = 'opacity 0.3s';

                    setTimeout(() => {
                        row.remove();
                        // 重新加载当前页数据
                        loadData();
                        // 重新加载统计数据
                        loadStats();
                    }, 300);
                } else {
                    alert('删除失败: ' + result.message);
                    deleteBtn.disabled = false;
                    deleteBtn.textContent = '删除';
                }
            } catch (e) {
                console.error('删除失败:', e);
                alert('删除失败: ' + e.message);
                deleteBtn.disabled = false;
                deleteBtn.textContent = '删除';
            }
        });

        // 初始化
        loadStats();
        loadData();
    </script>
</body>
</html>'''


def main():
    """启动服务器"""
    print("=" * 60)
    print("热议话题 API 服务器")
    print("=" * 60)
    print(f"访问地址: http://{HOST}:{PORT}")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)

    server = HTTPServer((HOST, PORT), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
