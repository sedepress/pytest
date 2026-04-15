#!/bin/bash
# 热议话题服务器快速启动脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header "热议话题服务器 - 快速启动"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "✗ 未找到 Python3"
    exit 1
fi

print_success "Python3 已安装"

# 检查依赖
print_info "检查依赖..."
if python3 -c "import pymysql" 2>/dev/null; then
    print_success "pymysql 已安装"
else
    echo "✗ pymysql 未安装"
    echo "安装命令: pip3 install pymysql"
    exit 1
fi

# 检查文件
if [ ! -f "hot_say_server.py" ]; then
    echo "✗ 未找到 hot_say_server.py"
    exit 1
fi

print_success "服务器文件存在"

# 显示功能说明
print_header "功能说明"
echo "1. 活动类型筛选：热议话题 / 线下活动"
echo "2. 数据来源筛选：粉丝圈 / 有赞 / 微盟"
echo "3. 组合筛选：支持多条件组合"
echo "4. 关键词搜索：实时搜索话题名称"
echo "5. 排序功能：支持多字段排序"
echo "6. 分页功能：支持大数据量分页"

# 显示访问信息
print_header "访问信息"
echo "服务器地址: http://localhost:10086"
echo "API 文档: 查看 HOT_SAY_UPDATE.md"
echo ""
echo "API 示例:"
echo "  - 列表: http://localhost:10086/api/hot-say/list"
echo "  - 统计: http://localhost:10086/api/hot-say/stats"
echo "  - 筛选: http://localhost:10086/api/hot-say/list?type=offline&source=fansquan"

# 询问是否启动
echo ""
read -p "是否启动服务器? [Y/n]: " confirm
if [ "$confirm" = "n" ] || [ "$confirm" = "N" ]; then
    print_info "已取消启动"
    exit 0
fi

# 启动服务器
print_header "启动服务器"
print_info "按 Ctrl+C 停止服务器"
echo ""

python3 hot_say_server.py
