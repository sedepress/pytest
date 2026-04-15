# 热议话题服务器 - 完整使用指南

## 🎯 快速开始

### 方式一：使用启动脚本（推荐）⭐⭐⭐

```bash
cd qc_script
./start_hot_say_server.sh
```

### 方式二：直接启动

```bash
cd qc_script
python3 hot_say_server.py
```

### 方式三：后台运行

```bash
cd qc_script
nohup python3 hot_say_server.py > hot_say_server.log 2>&1 &
```

---

## 📋 功能清单

### ✅ 已实现的功能

#### 1. 双维度筛选
- **活动类型筛选**
  - 全部
  - 热议话题（hot_say）
  - 线下活动（offline）

- **数据来源筛选**
  - 全部
  - 粉丝圈（fansquan）
  - 有赞（youzan_fansquan）
  - 微盟（weimob_fansquan）

#### 2. 组合筛选
- 支持活动类型 + 数据来源组合
- 支持筛选 + 关键词搜索组合
- 支持筛选 + 排序组合

#### 3. 实时统计
- 话题总数
- 总浏览量
- 总参与数
- 总点赞数
- 根据筛选条件动态更新

#### 4. 数据展示
- 分页显示（默认50条/页）
- 多字段排序
- 关键词搜索
- 详情查看
- 分数评级
- 删除操作

---

## 🎨 界面说明

### 筛选栏
```
┌──────────────────────────────────────────────────────────┐
│  [活动类型: 全部 ▼]  [数据来源: 全部 ▼]  [🔍 搜索话题...]  │
└──────────────────────────────────────────────────────────┘
```

### 统计栏
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  话题总数   │  总浏览量   │  总参与数   │  总点赞数   │
│    1,234    │   567,890   │   12,345    │    6,789    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 表格列
| ID | Logo | 话题名称 | 活动类型 | 来源 | 描述 | 参与数 | 浏览量 | ... | 操作 |
|----|------|---------|---------|------|------|--------|--------|-----|------|

---

## 🔧 API 接口文档

### 1. 获取列表

**请求**：
```
GET /api/hot-say/list
```

**参数**：
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| page | int | 否 | 页码 | 1 |
| page_size | int | 否 | 每页大小 | 50 |
| keyword | string | 否 | 搜索关键词 | 活动 |
| type | string | 否 | 活动类型 | offline |
| source | string | 否 | 数据来源 | fansquan |
| sort_key | string | 否 | 排序字段 | views |
| sort_dir | string | 否 | 排序方向 | desc |

**响应**：
```json
{
  "code": 1,
  "data": {
    "list": [
      {
        "id": 123,
        "say_name": "活动名称",
        "logo": "https://cdn.example.com/logo.jpg",
        "description": "活动描述",
        "type": "offline",
        "type_name": "线下活动",
        "source": "fansquan",
        "source_name": "粉丝圈",
        "participants": 100,
        "views": 1000,
        "replies": 50,
        "favorites": 20,
        "shares": 10,
        "likes": 80,
        "score": "A",
        "created_at": "2026-02-05 10:00"
      }
    ],
    "total": 1234,
    "page": 1,
    "page_size": 50,
    "total_pages": 25
  }
}
```

---

### 2. 获取统计

**请求**：
```
GET /api/hot-say/stats
```

**参数**：
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| type | string | 否 | 活动类型 | offline |
| source | string | 否 | 数据来源 | fansquan |

**响应**：
```json
{
  "code": 1,
  "data": {
    "total": 1234,
    "total_views": 567890,
    "total_participants": 12345,
    "total_likes": 6789
  }
}
```

---

### 3. 更新分数

**请求**：
```
POST /api/hot-say/update-score
Content-Type: application/json
```

**请求体**：
```json
{
  "id": 123,
  "score": "A"
}
```

**响应**：
```json
{
  "code": 1,
  "message": "更新成功"
}
```

---

### 4. 删除话题

**请求**：
```
POST /api/hot-say/delete
Content-Type: application/json
```

**请求体**：
```json
{
  "id": 123
}
```

**响应**：
```json
{
  "code": 1,
  "message": "删除成功"
}
```

---

## 📊 使用场景示例

### 场景1：查看所有线下活动

**操作步骤**：
1. 打开页面 `http://localhost:10086`
2. 选择"活动类型" → "线下活动"
3. 查看筛选结果

**API 调用**：
```bash
curl "http://localhost:10086/api/hot-say/list?type=offline"
```

**预期结果**：
- 只显示 type='offline' 的记录
- 统计数据更新为线下活动的统计
- 页面提示：共 XXX 条记录（线下活动）

---

### 场景2：查看粉丝圈的热议话题

**操作步骤**：
1. 选择"活动类型" → "热议话题"
2. 选择"数据来源" → "粉丝圈"
3. 查看筛选结果

**API 调用**：
```bash
curl "http://localhost:10086/api/hot-say/list?type=hot_say&source=fansquan"
```

**预期结果**：
- 只显示 type='hot_say' 且 source='fansquan' 的记录
- 统计数据更新
- 页面提示：共 XXX 条记录（热议话题 - 粉丝圈）

---

### 场景3：搜索特定活动

**操作步骤**：
1. 选择筛选条件（可选）
2. 在搜索框输入"春节"
3. 查看搜索结果

**API 调用**：
```bash
curl "http://localhost:10086/api/hot-say/list?keyword=春节&type=offline"
```

**预期结果**：
- 显示标题包含"春节"的线下活动
- 实时搜索，无需点击按钮

---

### 场景4：按浏览量排序

**操作步骤**：
1. 点击表头"浏览量"
2. 再次点击切换升序/降序

**API 调用**：
```bash
curl "http://localhost:10086/api/hot-say/list?sort_key=views&sort_dir=desc"
```

**预期结果**：
- 按浏览量降序排列
- 表头显示排序图标（↓）

---

## 🧪 测试验证

### 自动化测试

```bash
# 1. 启动服务器（终端1）
cd qc_script
python3 hot_say_server.py

# 2. 运行测试（终端2）
cd qc_script
python3 test_hot_say_api.py
```

**测试内容**：
- ✅ 获取全部统计数据
- ✅ 按活动类型筛选（热议话题）
- ✅ 按活动类型筛选（线下活动）
- ✅ 按来源筛选（粉丝圈）
- ✅ 组合筛选（线下活动 + 粉丝圈）
- ✅ 获取列表数据（带筛选）
- ✅ 关键词搜索 + 筛选

---

### 手动测试清单

#### 基础功能
- [ ] 页面正常加载
- [ ] 统计数据显示正确
- [ ] 表格数据显示正确
- [ ] 分页功能正常

#### 筛选功能
- [ ] 活动类型筛选（全部）
- [ ] 活动类型筛选（热议话题）
- [ ] 活动类型筛选（线下活动）
- [ ] 数据来源筛选（全部）
- [ ] 数据来源筛选（粉丝圈）
- [ ] 数据来源筛选（有赞）
- [ ] 数据来源筛选（微盟）
- [ ] 组合筛选（类型 + 来源）

#### 搜索功能
- [ ] 关键词搜索
- [ ] 搜索 + 类型筛选
- [ ] 搜索 + 来源筛选
- [ ] 搜索 + 组合筛选

#### 排序功能
- [ ] 按ID排序
- [ ] 按参与数排序
- [ ] 按浏览量排序
- [ ] 按点赞数排序
- [ ] 升序/降序切换

#### 其他功能
- [ ] 查看详情
- [ ] 更新分数
- [ ] 删除话题
- [ ] 页码跳转

---

## 🔍 故障排查

### 问题1：无法连接到服务器

**症状**：
- 浏览器显示"无法访问此网站"
- API 测试返回连接错误

**解决方案**：
```bash
# 1. 检查服务器是否启动
ps aux | grep hot_say_server.py

# 2. 检查端口是否被占用
lsof -i :10086

# 3. 重新启动服务器
python3 hot_say_server.py
```

---

### 问题2：筛选无效果

**症状**：
- 选择筛选条件后，数据没有变化
- 统计数据不更新

**解决方案**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 是否有错误
3. 查看 Network 标签，检查 API 请求
4. 确认数据库中有对应的数据

---

### 问题3：数据库连接失败

**症状**：
- 服务器启动后报错
- API 返回数据库错误

**解决方案**：
```bash
# 1. 检查数据库配置
vim hot_say_server.py
# 确认 DB_CONFIG 配置正确

# 2. 测试数据库连接
mysql -h 127.0.0.1 -u fansquan_dev -p data

# 3. 检查表结构
SHOW TABLES LIKE 'hot_say';
DESC hot_say;
```

---

### 问题4：中文乱码

**症状**：
- 页面显示乱码
- API 返回乱码

**解决方案**：
1. 确认数据库字符集为 utf8mb4
2. 确认表字符集为 utf8mb4
3. 确认连接字符集为 utf8mb4

```sql
-- 检查字符集
SHOW VARIABLES LIKE 'character%';

-- 修改表字符集
ALTER TABLE hot_say CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 📈 性能优化建议

### 1. 数据库索引

```sql
-- 为筛选字段创建索引
CREATE INDEX idx_type ON hot_say(type);
CREATE INDEX idx_source ON hot_say(source);
CREATE INDEX idx_deleted_at ON hot_say(deleted_at);

-- 组合索引
CREATE INDEX idx_type_source ON hot_say(type, source, deleted_at);
```

### 2. 分页优化

```python
# 使用游标分页（大数据量时）
# 当前使用 LIMIT OFFSET，数据量大时可能较慢
# 可改为基于 ID 的游标分页
```

### 3. 缓存策略

```python
# 统计数据可以缓存
# 使用 Redis 或内存缓存
# 设置合理的过期时间
```

---

## 🔒 安全建议

### 1. SQL 注入防护
- ✅ 已使用参数化查询
- ✅ 已验证排序字段白名单

### 2. XSS 防护
- ✅ 前端已转义 HTML
- ✅ 使用 textContent 而非 innerHTML

### 3. CSRF 防护
- ⚠️ 建议添加 CSRF Token
- ⚠️ 建议添加请求来源验证

### 4. 访问控制
- ⚠️ 建议添加身份验证
- ⚠️ 建议添加权限控制

---

## 📝 开发计划

### 短期计划（v2.1）
- [ ] 添加批量操作功能
- [ ] 添加导出功能（Excel/CSV）
- [ ] 添加数据可视化图表
- [ ] 优化移动端显示

### 中期计划（v2.2）
- [ ] 添加用户认证
- [ ] 添加操作日志
- [ ] 添加数据备份功能
- [ ] 添加 API 限流

### 长期计划（v3.0）
- [ ] 重构为前后端分离架构
- [ ] 使用 Vue/React 重写前端
- [ ] 使用 FastAPI 重写后端
- [ ] 添加 WebSocket 实时推送

---

## 📞 技术支持

### 获取帮助

**文档**：
- `HOT_SAY_UPDATE.md` - 功能更新说明
- `README.md` - 项目说明

**测试**：
- `test_hot_say_api.py` - API 测试脚本
- `start_hot_say_server.sh` - 启动脚本

**联系方式**：
- 查看代码注释
- 查看 Git 提交历史

---

## 🎉 总结

本服务器提供了完整的热议话题管理功能，支持：

- ✅ **双维度筛选**（活动类型 + 数据来源）
- ✅ **组合筛选**（多条件组合）
- ✅ **实时统计**（动态更新）
- ✅ **关键词搜索**（实时搜索）
- ✅ **多字段排序**（灵活排序）
- ✅ **分页显示**（大数据量支持）
- ✅ **详情查看**（弹窗显示）
- ✅ **分数评级**（A/B/C/D）
- ✅ **删除操作**（软删除）

**立即开始**：
```bash
cd qc_script
./start_hot_say_server.sh
```

祝使用愉快！🚀

---

**版本**: v2.0
**作者**: Claude Code
**更新日期**: 2026-02-05
