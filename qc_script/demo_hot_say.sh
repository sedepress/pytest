#!/bin/bash
# 热议话题服务器 - 完整功能演示脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 打印函数
print_header() {
    echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  $1${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}\n"
}

print_section() {
    echo -e "\n${CYAN}┌──────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│  $1${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────┘${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 清屏
clear

# 显示欢迎信息
print_header "热议话题服务器 v2.0 - 功能演示"

echo -e "${MAGENTA}本演示将展示以下功能:${NC}"
echo "  1. 双维度筛选（活动类型 + 数据来源）"
echo "  2. 组合筛选"
echo "  3. 实时统计"
echo "  4. API 接口测试"
echo ""

read -p "按回车键开始演示..." dummy

# 检查服务器是否运行
print_section "检查服务器状态"

if curl -s "http://localhost:10086/api/hot-say/stats" > /dev/null 2>&1; then
    print_success "服务器正在运行"
else
    print_error "服务器未运行"
    echo ""
    print_info "请先启动服务器:"
    echo "  cd qc_script"
    echo "  python3 hot_say_server.py"
    echo ""
    exit 1
fi

# 演示1: 获取全部统计
print_section "演示1: 获取全部统计数据"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/stats\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/stats")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 演示2: 按活动类型筛选（线下活动）
print_section "演示2: 按活动类型筛选（线下活动）"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/stats?type=offline\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/stats?type=offline")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 演示3: 按数据来源筛选（粉丝圈）
print_section "演示3: 按数据来源筛选（粉丝圈）"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/stats?source=fansquan\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/stats?source=fansquan")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 演示4: 组合筛选（线下活动 + 粉丝圈）
print_section "演示4: 组合筛选（线下活动 + 粉丝圈）"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/stats?type=offline&source=fansquan\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/stats?type=offline&source=fansquan")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 演示5: 获取列表数据（前5条）
print_section "演示5: 获取列表数据（线下活动，前5条）"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/list?page=1&page_size=5&type=offline\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/list?page=1&page_size=5&type=offline")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 演示6: 关键词搜索 + 筛选
print_section "演示6: 关键词搜索 + 类型筛选"

echo "API 调用:"
echo -e "${CYAN}curl \"http://localhost:10086/api/hot-say/list?keyword=活动&type=offline&page_size=3\"${NC}"
echo ""

response=$(curl -s "http://localhost:10086/api/hot-say/list?keyword=活动&type=offline&page_size=3")
echo "响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"

read -p "按回车键继续..." dummy

# 显示总结
print_header "演示完成"

echo -e "${GREEN}✓ 所有功能演示完成！${NC}"
echo ""
echo "功能清单:"
echo "  ✅ 活动类型筛选（热议话题/线下活动）"
echo "  ✅ 数据来源筛选（粉丝圈/有赞/微盟）"
echo "  ✅ 组合筛选（类型 + 来源）"
echo "  ✅ 关键词搜索"
echo "  ✅ 实时统计"
echo ""
echo "下一步:"
echo "  1. 访问 Web 界面: ${CYAN}http://localhost:10086${NC}"
echo "  2. 查看完整文档: ${CYAN}cat HOT_SAY_GUIDE.md${NC}"
echo "  3. 运行完整测试: ${CYAN}python3 test_hot_say_api.py${NC}"
echo ""
