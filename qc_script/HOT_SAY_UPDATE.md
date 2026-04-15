# 热议话题服务器 - 功能更新说明

## 📋 更新内容

### 版本：v2.0
### 更新日期：2026-02-05

---

## ✨ 新增功能

### 1. 活动类型筛选 ⭐⭐⭐

**功能说明**：
- 支持按活动类型筛选数据
- 两种类型：热议话题（hot_say）、线下活动（offline）

**使用方式**：
- 前端：在页面顶部选择"活动类型"下拉框
- API：`GET /api/hot-say/list?type=offline`
- API：`GET /api/hot-say/stats?type=hot_say`

**视觉标识**：
- 热议话题：粉红色标签 🎀
- 线下活动：蓝色标签 🎯

---

### 2. 数据来源筛选 ⭐⭐⭐

**功能说明**：
- 支持按数据来源筛选
- 三种来源：粉丝圈（fansquan）、有赞（youzan_fansquan）、微盟（weimob_fansquan）

**使用方式**：
- 前端：在页面顶部选择"数据来源"下拉框
- API：`GET /api/hot-say/list?source=fansquan`
- API：`GET /api/hot-say/stats?source=youzan_fansquan`

**视觉标识**：
- 粉丝圈：绿色标签 🟢
- 有赞：橙色标签 🟠
- 微盟：蓝色标签 🔵

---

### 3. 组合筛选 ⭐⭐⭐

**功能说明**：
- 支持多条件组合筛选
- 可同时使用：活动类型 + 数据来源 + 关键词搜索

**使用示例**：
```
# 筛选粉丝圈的线下活动
GET /api/hot-say/list?type=offline&source=fansquan

# 筛选有赞的热议话题，包含"活动"关键词
GET /api/hot-say/list?type=hot_say&source=youzan_fansquan&keyword=活动

# 筛选粉丝圈的所有数据
GET /api/hot-say/list?source=fansquan
```

---

### 4. 智能统计 ⭐⭐

**功能说明**：
- 统计数据根据筛选条件实时更新
- 显示当前筛选条件的记录数、浏览量、参与数、点赞数

**显示效果**：
```
全部：共 1,234 条记录
热议话题：共 567 条记录（热议话题）
线下活动 + 粉丝圈：共 123 条记录（线下活动 - 粉丝圈）
```

---

## 🎨 界面更新

### 筛选栏布局
```
┌─────────────────────────────────────────────────────┐
│  [活动类型: 全部 ▼]  [数据来源: 全部 ▼]  [🔍 搜索...]  │
└─────────────────────────────────────────────────────┘
```

### 表格新增列
- 在"话题名称"和"来源"之间新增"活动类型"列
- 显示带颜色标签的活动类型

---

## 🔧 API 更新

### 列表接口
```
GET /api/hot-say/list

参数：
  - page: 页码（默认1）
  - page_size: 每页大小（默认50）
  - keyword: 搜索关键词
  - type: 活动类型（hot_say/offline）⭐ 新增
  - source: 数据来源（fansquan/youzan_fansquan/weimob_fansquan）⭐ 新增
  - sort_key: 排序字段
  - sort_dir: 排序方向（asc/desc）

返回：
  {
    "code": 1,
    "data": {
      "list": [
        {
          "id": 123,
          "say_name": "活动名称",
          "type": "offline",           ⭐ 新增
          "type_name": "线下活动",      ⭐ 新增
          "source": "fansquan",
          "source_name": "粉丝圈",
          ...
        }
      ],
      "total": 1234,
      "page": 1,
      "page_size": 50,
      "total_pages": 25
    }
  }
```

### 统计接口
```
GET /api/hot-say/stats

参数：
  - type: 活动类型（hot_say/offline）⭐ 新增
  - source: 数据来源（fansquan/youzan_fansquan/weimob_fansquan）⭐ 新增

返回：
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

## 📊 使用场景

### 场景1：查看所有线下活动
1. 选择"活动类型" → "线下活动"
2. 自动刷新列表和统计数据

### 场景2：查看粉丝圈的热议话题
1. 选择"活动类型" → "热议话题"
2. 选择"数据来源" → "粉丝圈"
3. 查看筛选结果

### 场景3：搜索特定活动
1. 选择筛选条件（可选）
2. 在搜索框输入关键词
3. 实时显示搜索结果

---

## 🚀 快速开始

### 启动服务器
```bash
cd qc_script
python3 hot_say_server.py
```

### 访问页面
```
http://localhost:10086
```

### 测试 API
```bash
# 运行测试脚本
python3 test_hot_say_api.py

# 或手动测试
curl "http://localhost:10086/api/hot-say/stats?type=offline&source=fansquan"
```

---

## 🔍 测试验证

### 自动化测试
```bash
# 确保服务器已启动
python3 hot_say_server.py

# 在另一个终端运行测试
python3 test_hot_say_api.py
```

### 手动测试清单
- [ ] 活动类型筛选（全部/热议话题/线下活动）
- [ ] 数据来源筛选（全部/粉丝圈/有赞/微盟）
- [ ] 组合筛选（类型 + 来源）
- [ ] 关键词搜索 + 筛选
- [ ] 统计数据更新
- [ ] 表格数据显示
- [ ] 分页功能
- [ ] 排序功能

---

## 📝 技术细节

### 后端修改
- `fetch_hot_say_list()` 函数新增 `source` 参数
- `fetch_statistics()` 函数新增 `source` 参数
- SQL WHERE 子句支持多条件筛选
- 返回数据包含 `type` 和 `type_name` 字段

### 前端修改
- 新增 `sourceFilter` 变量
- 新增 `handleSourceFilter()` 函数
- 更新 `loadStats()` 函数，支持组合筛选
- 更新 `loadData()` 函数，传递 source 参数
- 新增来源筛选器 UI 和事件监听

### 数据库查询
```sql
-- 组合筛选示例
SELECT * FROM hot_say
WHERE deleted_at IS NULL
  AND type = 'offline'
  AND source = 'fansquan'
ORDER BY id DESC
LIMIT 50 OFFSET 0
```

---

## ⚠️ 注意事项

1. **数据库字段**：确保 `hot_say` 表包含 `type` 和 `source` 字段
2. **数据迁移**：线下活动数据的 `type` 应为 `offline`，`source` 应为 `fansquan`
3. **性能优化**：建议在 `type` 和 `source` 字段上创建索引
4. **兼容性**：保持向后兼容，不传筛选参数时显示全部数据

---

## 🎉 总结

本次更新新增了**活动类型**和**数据来源**两个筛选维度，支持**组合筛选**，大大提升了数据查询的灵活性和用户体验。

**核心改进**：
- ✅ 双维度筛选（类型 + 来源）
- ✅ 组合筛选支持
- ✅ 实时统计更新
- ✅ 视觉标识优化
- ✅ API 完整支持
- ✅ 测试脚本完善

---

**版本**: v2.0
**作者**: Claude Code
**更新日期**: 2026-02-05
