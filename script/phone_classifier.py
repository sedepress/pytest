#!/usr/bin/env python3
"""
电话号码分类脚本
功能：从ZIP压缩包中读取JSON文件，根据电话号码分类并检查是否为美国实体卡
"""

import json
import os
import re
import shutil
import tkinter as tk
import zipfile
from datetime import datetime
from tkinter import filedialog

import requests


class PhoneClassifier:
    def __init__(self):
        self.us_area_codes = self.load_us_area_codes()
        self.session = requests.Session()
        
    def load_us_area_codes(self):
        """加载美国区号列表"""
        us_area_codes = set()
        # 从需求文件中提取的美国区号
        area_codes_list = [
            '205', '251', '256', '334', '938',  # Alabama
            '907',  # Alaska
            '480', '520', '602', '623', '928',  # Arizona
            '479', '501', '870',  # Arkansas
            '209', '213', '279', '310', '323', '341', '408', '415', '424', '442', '510', '530', '559', '562', '619', '626', '628', '650', '657', '661', '669', '707', '714', '747', '760', '805', '818', '820', '831', '858', '909', '916', '925', '949', '951',  # California
            '303', '719', '720', '970',  # Colorado
            '203', '475', '860', '959',  # Connecticut
            '302',  # Delaware
            '239', '305', '321', '352', '386', '407', '561', '727', '754', '772', '786', '813', '850', '863', '904', '941', '954',  # Florida
            '229', '404', '470', '478', '678', '706', '762', '770', '912',  # Georgia
            '808',  # Hawaii
            '208', '986',  # Idaho
            '217', '224', '309', '312', '331', '618', '630', '708', '773', '779', '815', '847', '872',  # Illinois
            '219', '260', '317', '463', '574', '765', '812', '930',  # Indiana
            '319', '515', '563', '641', '712',  # Iowa
            '316', '620', '785', '913',  # Kansas
            '270', '364', '502', '606', '859',  # Kentucky
            '225', '318', '337', '504', '985',  # Louisiana
            '207',  # Maine
            '240', '301', '410', '443', '667',  # Maryland
            '339', '351', '413', '508', '617', '774', '781', '857', '978',  # Massachusetts
            '231', '248', '269', '313', '517', '586', '616', '734', '810', '906', '947', '989',  # Michigan
            '218', '320', '507', '612', '651', '763', '952',  # Minnesota
            '228', '601', '662', '769',  # Mississippi
            '314', '417', '573', '636', '660', '816',  # Missouri
            '406',  # Montana
            '308', '402', '531',  # Nebraska
            '702', '725', '775',  # Nevada
            '603',  # New Hampshire
            '201', '551', '609', '640', '732', '848', '856', '862', '908', '973',  # New Jersey
            '505', '575',  # New Mexico
            '212', '315', '332', '347', '516', '518', '585', '607', '631', '646', '680', '716', '718', '838', '845', '914', '917', '929', '934',  # New York
            '252', '336', '704', '743', '828', '910', '919', '980', '984',  # North Carolina
            '701',  # North Dakota
            '216', '220', '234', '330', '380', '419', '440', '513', '567', '614', '740', '937',  # Ohio
            '405', '539', '580', '918',  # Oklahoma
            '458', '503', '541', '971',  # Oregon
            '215', '223', '267', '272', '412', '445', '484', '570', '610', '717', '724', '814', '878',  # Pennsylvania
            '401',  # Rhode Island
            '803', '843', '854', '864',  # South Carolina
            '605',  # South Dakota
            '423', '615', '629', '731', '865', '901', '931',  # Tennessee
            '210', '214', '254', '281', '325', '346', '361', '409', '430', '432', '469', '512', '682', '713', '726', '737', '806', '817', '830', '832', '903', '915', '936', '940', '956', '972', '979',  # Texas
            '385', '435', '801',  # Utah
            '802',  # Vermont
            '276', '434', '540', '571', '703', '757', '804',  # Virginia
            '206', '253', '360', '425', '509', '564',  # Washington
            '202',  # Washington DC
            '304', '681',  # West Virginia
            '262', '414', '534', '608', '715', '920',  # Wisconsin
            '307'  # Wyoming
        ]
        us_area_codes.update(area_codes_list)
        return us_area_codes
    
    def select_zip_file(self):
        """选择ZIP文件"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="选择ZIP压缩包",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        root.destroy()
        return file_path
    
    def extract_json_from_zip(self, zip_path):
        """从ZIP文件中提取JSON文件"""
        json_files = []
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('.json'):
                        with zip_ref.open(file_info) as json_file:
                            try:
                                data = json.load(json_file)
                                # 添加原始文件名信息
                                data['_original_filename'] = file_info.filename
                                json_files.append(data)
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            print(f"读取ZIP文件出错: {e}")
        return json_files
    
    def is_us_phone_number(self, phone):
        """判断是否为美国电话号码"""
        # 移除所有非数字字符
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # 美国电话号码通常为10位或11位（带国家代码1）
        if len(clean_phone) == 10:
            area_code = clean_phone[:3]
            return area_code in self.us_area_codes
        elif len(clean_phone) == 11 and clean_phone[0] == '1':
            area_code = clean_phone[1:4]
            return area_code in self.us_area_codes
        
        return False
    
    def setup_directories(self):
        """创建目录结构"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 创建主分类目录
        us_phones_dir = os.path.join(base_dir, "美国电话")
        non_us_phones_dir = os.path.join(base_dir, "非美国电话")
        
        os.makedirs(us_phones_dir, exist_ok=True)
        os.makedirs(non_us_phones_dir, exist_ok=True)
        
        # 创建美国电话的子目录
        physical_cards_dir = os.path.join(us_phones_dir, "实体卡")
        virtual_cards_dir = os.path.join(us_phones_dir, "非实体卡")
        
        os.makedirs(physical_cards_dir, exist_ok=True)
        os.makedirs(virtual_cards_dir, exist_ok=True)
        
        return us_phones_dir, non_us_phones_dir, physical_cards_dir, virtual_cards_dir
    
    def check_carrier_type(self, phone, proxy_info):
        """检查运营商类型（实体卡/虚拟卡）"""
        # 清理电话号码
        clean_phone = re.sub(r'[^\d]', '', str(phone))
        
        # 只有1开头的美国电话才进行检查
        if not clean_phone.startswith('1'):
            return False
        
        # 提取10位电话号码（去掉国家代码1）
        if len(clean_phone) == 11:
            phone_number = clean_phone[1:]
        elif len(clean_phone) == 10:
            phone_number = clean_phone
        else:
            return False
        
        # 设置代理
        proxies = None
        if proxy_info and len(proxy_info) >= 3:
            proxy_type = proxy_info[0]  # 3表示SOCKS5
            proxy_host = proxy_info[1]
            proxy_port = proxy_info[2]
            proxy_user = proxy_info[4] if len(proxy_info) > 4 else None
            proxy_pass = proxy_info[5] if len(proxy_info) > 5 else None
            
            try:
                if proxy_type == 3:  # SOCKS5代理
                    # 验证代理参数
                    if not proxy_host or not proxy_port:
                        print("代理主机或端口为空，跳过代理设置")
                        proxies = None
                    else:
                        # URL编码用户名和密码中的特殊字符
                        from urllib.parse import quote
                        encoded_user = quote(str(proxy_user)) if proxy_user else None
                        encoded_pass = quote(str(proxy_pass)) if proxy_pass else None
                        
                        # 设置SOCKS5代理
                        if encoded_user and encoded_pass:
                            proxy_url = f"socks5h://{encoded_user}:{encoded_pass}@{proxy_host}:{proxy_port}"
                        else:
                            proxy_url = f"socks5h://{proxy_host}:{proxy_port}"
                        
                        print(f"使用SOCKS5代理: {proxy_url.split('@')[-1] if '@' in proxy_url else proxy_url}")
                        # 配置requests使用SOCKS5代理
                        proxies = {
                            'http': proxy_url,
                            'https': proxy_url
                        }
                else:
                    # 其他类型的代理（HTTP/HTTPS）
                    if not proxy_host or not proxy_port:
                        print("代理主机或端口为空，跳过代理设置")
                        proxies = None
                    else:
                        from urllib.parse import quote
                        encoded_user = quote(str(proxy_user)) if proxy_user else None
                        encoded_pass = quote(str(proxy_pass)) if proxy_pass else None
                        
                        if encoded_user and encoded_pass:
                            proxy_url = f'socks5h://{encoded_user}:{encoded_pass}@{proxy_host}:{proxy_port}'
                        else:
                            proxy_url = f'socks5h://{proxy_host}:{proxy_port}'

                        print(f"使用HTTP代理: {proxy_url.split('@')[-1] if '@' in proxy_url else proxy_url}")
                        proxies = {
                            'http': proxy_url,
                            'https': proxy_url
                        }
            except Exception as e:
                print(f"设置代理时出错: {e}")
                proxies = None

        cookies = {
            'PHPSESSID': '78256ebt61le7vudq79d8bm907',
            '_ga': 'GA1.2.613962221.1755675688',
            '_gid': 'GA1.2.308913265.1755675688',
            'cf_clearance': 'UsNXOkAx1.5XAZeYeyJ4tD8kwe3KCEpjGAHzyFMKnu8-1755764967-1.2.1.1-Gt557Zs5aSZjv6m6FveHMcWDxn2hlclmWsyygXdgSPnedXOlbKTh.5yPJz7BbDwTehr80GRdet62NpH_lPpa2uoBOWuDC4VlmsFs.ZDFa2VgkUcofScjnERfjc2qJkSRFnohHBQ5YtcnuT0aD92Vv6t517nXM6SboqnmEV6oLEGa0pu.kuG1odJNnFebsXnTJ2i.cyMezYUbl56Basvfmih1s9uVNnF2VYPgT9OAGVU',
            '_ga_4JSC4GJHB3': 'GS2.2.s1755764968$o4$g0$t1755764968$j60$l0$h0',
            '__gads': 'ID=67ec3cd6a78a0163:T=1755675688:RT=1755764967:S=ALNI_MZm45eCmmymGlxPcxbBC0lkawLRkQ',
            '__gpi': 'UID=000011834b99d1e6:T=1755675688:RT=1755764967:S=ALNI_MZb7MpLEEnHqjbgkgsUUUBibpkcIw',
            '__eoi': 'ID=e0c330f59c61e8dd:T=1755675688:RT=1755764967:S=AA-AfjYbduvrDLcWZFsoxV1GzKvi',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://freecarrierlookup.com',
            'priority': 'u=0, i',
            'referer': 'https://freecarrierlookup.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            # 'cookie': 'PHPSESSID=78256ebt61le7vudq79d8bm907; _ga=GA1.2.613962221.1755675688; _gid=GA1.2.308913265.1755675688; cf_clearance=UsNXOkAx1.5XAZeYeyJ4tD8kwe3KCEpjGAHzyFMKnu8-1755764967-1.2.1.1-Gt557Zs5aSZjv6m6FveHMcWDxn2hlclmWsyygXdgSPnedXOlbKTh.5yPJz7BbDwTehr80GRdet62NpH_lPpa2uoBOWuDC4VlmsFs.ZDFa2VgkUcofScjnERfjc2qJkSRFnohHBQ5YtcnuT0aD92Vv6t517nXM6SboqnmEV6oLEGa0pu.kuG1odJNnFebsXnTJ2i.cyMezYUbl56Basvfmih1s9uVNnF2VYPgT9OAGVU; _ga_4JSC4GJHB3=GS2.2.s1755764968$o4$g0$t1755764968$j60$l0$h0; __gads=ID=67ec3cd6a78a0163:T=1755675688:RT=1755764967:S=ALNI_MZm45eCmmymGlxPcxbBC0lkawLRkQ; __gpi=UID=000011834b99d1e6:T=1755675688:RT=1755764967:S=ALNI_MZb7MpLEEnHqjbgkgsUUUBibpkcIw; __eoi=ID=e0c330f59c61e8dd:T=1755675688:RT=1755764967:S=AA-AfjYbduvrDLcWZFsoxV1GzKvi',
        }

        # 请求数据
        data = {
            'test': '456Tabo',
            'cc': '1',
            'phonenum': phone_number,
            'sessionlogin': '1'
        }
        
        def make_request(use_proxies=True):
            """内部函数：发送请求"""
            current_proxies = proxies if use_proxies else None
            
            try:
                # 首先检查代理设置是否正确
                if current_proxies:
                    proxy_display = {k: v.split('@')[-1] if '@' in v else v for k, v in current_proxies.items()}
                    print(f"使用代理请求: {proxy_display}")
                else:
                    print("不使用代理直接请求")

                response = self.session.post(
                    'https://freecarrierlookup.com/getcarrier_free.php',
                    headers=headers,
                    cookies=cookies,
                    data=data,
                    proxies=current_proxies,
                    timeout=20  # 增加超时时间
                )

                print(f"响应状态码: {response.status_code}")
                if response.status_code == 200:
                    response_text = response.text
                    print(f"  -> API响应: {response_text[:100]}...")
                    
                    # 解析响应 - 从JSON的html字段中提取Is Wireless信息
                    try:
                        response_data = json.loads(response_text)

                        print(f"  -> API响应数据: {response_data}")
                        # 检查status是否为success
                        if response_data.get('status') == 'success':
                            html_content = response_data.get('html', '')
                            
                            # 使用正则表达式从HTML中提取Is Wireless信息
                            # 匹配模式: Is Wireless:</strong> 后跟一些内容，然后在<p>标签中找到y/n值
                            wireless_pattern = r'Is Wireless:</strong>.*?<p>\s*([a-zA-Z])\s*</p>'
                            wireless_match = re.search(wireless_pattern, html_content, re.IGNORECASE | re.DOTALL)

                            print(f"  -> 正则匹配结果: {wireless_match}")
                            if wireless_match:
                                wireless_value = wireless_match.group(1).lower()
                                print(f"  -> 找到Is Wireless: {wireless_value}")
                                if wireless_value == 'y':
                                    return True
                            else:
                                print(f"  -> 未找到Is Wireless信息")
                                # 输出HTML片段用于调试
                                print(f"  -> HTML片段: {html_content[:300]}...")
                        else:
                            print(f"  -> API状态不是success: {response_data.get('status')}")
                            
                    except json.JSONDecodeError as e:
                        print(f"  -> JSON解析失败: {e}")
                        print(f"  -> 响应内容: {response_text[:200]}...")
                else:
                    print(f"  -> HTTP请求失败，状态码: {response.status_code}")
                    print(f"  -> 响应内容: {response.text[:200]}...")
                            
            except Exception as e:
                print(f"检查运营商类型时出错: {e}")
                return False
            
            return False
        
        # 首先尝试使用代理（如果有）
        if proxies:
            result = make_request(use_proxies=True)
            if result:
                return True
            
            # 如果代理失败，尝试不使用代理
            print("  -> 代理连接失败，尝试不使用代理重试...")
            result = make_request(use_proxies=False)
            if result:
                return True
        else:
            # 没有代理，直接请求
            result = make_request(use_proxies=False)
            if result:
                return True
        
        return False
    
    def save_json_file(self, data, file_path):
        """保存JSON文件"""
        try:
            # 移除内部字段后再保存
            save_data = data.copy()
            if '_original_filename' in save_data:
                del save_data['_original_filename']
            if '_session_file_content' in save_data:
                del save_data['_session_file_content']
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件出错: {e}")
    
    def extract_session_file_from_zip(self, zip_path, session_filename):
        """从ZIP文件中提取session文件"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename == session_filename:
                        with zip_ref.open(file_info) as session_file:
                            return session_file.read()
        except Exception as e:
            print(f"提取session文件出错: {e}")
        return None
    
    def save_session_file(self, content, file_path):
        """保存session文件"""
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
        except Exception as e:
            print(f"保存session文件出错: {e}")
    
    def create_zip_archive(self, source_dir, output_path):
        """创建ZIP压缩包"""
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
        except Exception as e:
            print(f"创建ZIP文件出错: {e}")
    
    def process_files(self):
        """主处理函数"""
        print("开始处理电话号码分类...")
        
        # 选择ZIP文件
        zip_path = self.select_zip_file()
        if not zip_path:
            print("未选择文件，程序退出")
            return
        
        print(f"选择的文件: {zip_path}")
        
        # 提取JSON文件
        json_files = self.extract_json_from_zip(zip_path)
        if not json_files:
            print("ZIP文件中没有找到有效的JSON文件")
            return
        
        print(f"找到 {len(json_files)} 个JSON文件")
        
        # 创建目录结构
        us_dir, non_us_dir, physical_dir, virtual_dir = self.setup_directories()
        
        # 分类处理
        us_count = 0
        non_us_count = 0
        physical_count = 0
        virtual_count = 0
        
        for data in json_files:
            phone = data.get('phone', '')
            proxy_info = data.get('proxy', [])
            session_file = data.get('session_file', '')
            original_filename = data.get('_original_filename', '')
            
            if self.is_us_phone_number(phone):
                us_count += 1
                print(f"美国电话: {phone}")
                
                # 检查是否为实体卡
                is_physical = self.check_carrier_type(phone, proxy_info)
                
                if is_physical:
                    physical_count += 1
                    json_save_path = os.path.join(physical_dir, f"{session_file}.json")
                    print(f"  -> 实体卡: {phone}")
                    target_dir = physical_dir
                else:
                    virtual_count += 1
                    json_save_path = os.path.join(virtual_dir, f"{session_file}.json")
                    print(f"  -> 非实体卡: {phone}")
                    target_dir = virtual_dir
                
                # 保存JSON文件
                self.save_json_file(data, json_save_path)
                
                # 提取并保存session文件
                if session_file:
                    # 根据原始文件名推断session文件名
                    if original_filename:
                        # 从原始JSON文件名获取对应的session文件名
                        base_name = os.path.splitext(original_filename)[0]
                        session_filename = f"{base_name}.session"
                    else:
                        session_filename = f"{session_file}.session"
                    
                    session_content = self.extract_session_file_from_zip(zip_path, session_filename)
                    if session_content:
                        session_save_path = os.path.join(target_dir, f"{session_file}.session")
                        self.save_session_file(session_content, session_save_path)
                        print(f"  -> 已保存session文件: {session_file}.session")
                    
            else:
                non_us_count += 1
                json_save_path = os.path.join(non_us_dir, f"{session_file}.json")
                self.save_json_file(data, json_save_path)
                print(f"非美国电话: {phone}")
                
                # 提取并保存session文件
                if session_file:
                    # 根据原始文件名推断session文件名
                    if original_filename:
                        base_name = os.path.splitext(original_filename)[0]
                        session_filename = f"{base_name}.session"
                    else:
                        session_filename = f"{session_file}.session"
                    
                    session_content = self.extract_session_file_from_zip(zip_path, session_filename)
                    if session_content:
                        session_save_path = os.path.join(non_us_dir, f"{session_file}.session")
                        self.save_session_file(session_content, session_save_path)
                        print(f"  -> 已保存session文件: {session_file}.session")
        
        print(f"\n处理完成:")
        print(f"美国电话: {us_count} 个")
        print(f"  - 实体卡: {physical_count} 个")
        print(f"  - 非实体卡: {virtual_count} 个")
        print(f"非美国电话: {non_us_count} 个")
        
        # 创建最终的ZIP压缩包
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 压缩美国电话文件夹
        us_zip_path = os.path.join(os.path.dirname(zip_path), f"美国电话_{timestamp}.zip")
        self.create_zip_archive(us_dir, us_zip_path)
        print(f"已创建美国电话压缩包: {us_zip_path}")
        
        # 压缩非美国电话文件夹
        non_us_zip_path = os.path.join(os.path.dirname(zip_path), f"非美国电话_{timestamp}.zip")
        self.create_zip_archive(non_us_dir, non_us_zip_path)
        print(f"已创建非美国电话压缩包: {non_us_zip_path}")
        
        # 删除原始文件夹
        print("\n正在清理临时文件夹...")
        try:
            if os.path.exists(us_dir):
                shutil.rmtree(us_dir)
                print(f"已删除文件夹: {us_dir}")
            
            if os.path.exists(non_us_dir):
                shutil.rmtree(non_us_dir)
                print(f"已删除文件夹: {non_us_dir}")
                
        except Exception as e:
            print(f"删除文件夹时出错: {e}")
        
        print("所有处理完成！")


if __name__ == "__main__":
    classifier = PhoneClassifier()
    classifier.process_files()