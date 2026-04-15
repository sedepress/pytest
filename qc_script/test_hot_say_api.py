#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热议话题服务器测试脚本
测试筛选功能是否正常工作
"""

import requests
import json


def test_api(base_url="http://localhost:10086"):
    """测试 API 接口"""

    print("="*60)
    print("热议话题 API 测试")
    print("="*60)

    # 测试1: 获取统计数据（全部）
    print("\n【测试1】获取全部统计数据")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/stats")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  总记录数: {data['total']}")
            print(f"  总浏览量: {data['total_views']}")
            print(f"  总参与数: {data['total_participants']}")
            print(f"  总点赞数: {data['total_likes']}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试2: 按活动类型筛选统计（热议话题）
    print("\n【测试2】获取热议话题统计数据")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/stats?type=hot_say")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  热议话题数: {data['total']}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试3: 按活动类型筛选统计（线下活动）
    print("\n【测试3】获取线下活动统计数据")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/stats?type=offline")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  线下活动数: {data['total']}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试4: 按来源筛选统计（粉丝圈）
    print("\n【测试4】获取粉丝圈来源统计数据")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/stats?source=fansquan")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  粉丝圈记录数: {data['total']}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试5: 组合筛选（线下活动 + 粉丝圈）
    print("\n【测试5】组合筛选（线下活动 + 粉丝圈）")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/stats?type=offline&source=fansquan")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  符合条件记录数: {data['total']}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试6: 获取列表数据（带筛选）
    print("\n【测试6】获取列表数据（线下活动，前5条）")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/list?page=1&page_size=5&type=offline")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  总记录数: {data['total']}")
            print(f"  当前页: {data['page']}")
            print(f"  每页大小: {data['page_size']}")
            print(f"  总页数: {data['total_pages']}")
            print(f"\n  前5条记录:")
            for idx, item in enumerate(data['list'], 1):
                print(f"    {idx}. ID={item['id']}, 名称={item['say_name'][:30]}..., 类型={item.get('type_name', 'N/A')}, 来源={item.get('source_name', 'N/A')}")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    # 测试7: 关键词搜索 + 筛选
    print("\n【测试7】关键词搜索 + 类型筛选")
    try:
        resp = requests.get(f"{base_url}/api/hot-say/list?page=1&page_size=5&keyword=活动&type=offline")
        result = resp.json()
        if result['code'] == 1:
            data = result['data']
            print(f"✓ 成功")
            print(f"  搜索结果数: {data['total']}")
            if data['list']:
                print(f"  示例记录: {data['list'][0]['say_name'][:50]}...")
        else:
            print(f"✗ 失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


def main():
    """主函数"""
    import sys

    base_url = "http://localhost:10086"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    print(f"\n测试服务器: {base_url}")
    print("确保服务器已启动: python3 hot_say_server.py\n")

    try:
        test_api(base_url)
    except requests.exceptions.ConnectionError:
        print("\n✗ 无法连接到服务器")
        print("请先启动服务器: python3 hot_say_server.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
