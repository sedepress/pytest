#!/usr/bin/env python3
"""
微信回调转发服务器
在测试服务器上运行，接收微信回调并转发到本地开发环境
"""

import logging
from datetime import datetime

import requests
from flask import Flask, request, Response

app = Flask(__name__)

# 配置
LOCAL_URL = "http://192.168.0.102:8000"  # 修改为你的本地地址
FORWARD_PATH = "/b/wechat/callback"  # 本地接收路径

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wechat_forwarder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    """接收微信回调并转发"""

    # 记录请求信息
    logger.info(f"收到请求: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")

    try:
        if request.method == 'GET':
            # 微信服务器验证
            signature = request.args.get('signature', '')
            timestamp = request.args.get('timestamp', '')
            nonce = request.args.get('nonce', '')
            echostr = request.args.get('echostr', '')

            logger.info(f"GET验证请求 - signature: {signature}, timestamp: {timestamp}, nonce: {nonce}")

            # 转发到本地
            forward_url = f"{LOCAL_URL}{FORWARD_PATH}"
            response = requests.get(
                forward_url,
                params={
                    'signature': signature,
                    'timestamp': timestamp,
                    'nonce': nonce,
                    'echostr': echostr
                },
                timeout=10
            )

            logger.info(f"本地响应: {response.status_code} - {response.text}")
            return Response(response.text, status=response.status_code)

        elif request.method == 'POST':
            # 微信消息回调
            data = request.data
            content_type = request.content_type

            logger.info(f"POST回调 - Content-Type: {content_type}")
            logger.info(f"数据长度: {len(data)} bytes")
            logger.info(f"数据内容: {data.decode('utf-8', errors='ignore')[:500]}")

            # 转发到本地
            forward_url = f"{LOCAL_URL}{FORWARD_PATH}"
            response = requests.post(
                forward_url,
                data=data,
                headers={
                    'Content-Type': content_type or 'application/xml'
                },
                params=request.args,
                timeout=10
            )

            logger.info(f"本地响应: {response.status_code} - {response.text[:200]}")
            return Response(response.text, status=response.status_code, content_type=response.headers.get('Content-Type'))

    except requests.exceptions.RequestException as e:
        logger.error(f"转发失败: {str(e)}")
        return Response("success", status=200)  # 返回success避免微信重试
    except Exception as e:
        logger.error(f"处理异常: {str(e)}", exc_info=True)
        return Response("success", status=200)


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return {
        'status': 'ok',
        'time': datetime.now().isoformat(),
        'forward_to': f"{LOCAL_URL}{FORWARD_PATH}"
    }


@app.route('/config', methods=['GET', 'POST'])
def config():
    """动态配置转发地址"""
    global LOCAL_URL, FORWARD_PATH

    if request.method == 'POST':
        data = request.get_json()
        if 'local_url' in data:
            LOCAL_URL = data['local_url']
        if 'forward_path' in data:
            FORWARD_PATH = data['forward_path']
        logger.info(f"配置已更新: LOCAL_URL={LOCAL_URL}, FORWARD_PATH={FORWARD_PATH}")

    return {
        'local_url': LOCAL_URL,
        'forward_path': FORWARD_PATH,
        'full_url': f"{LOCAL_URL}{FORWARD_PATH}"
    }


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("微信回调转发服务器启动")
    logger.info(f"转发目标: {LOCAL_URL}{FORWARD_PATH}")
    logger.info("=" * 60)

    # 生产环境建议使用 gunicorn 或 uwsgi
    app.run(host='0.0.0.0', port=5000, debug=False)
