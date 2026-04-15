#!/usr/bin/env python3
"""
电话号码分类脚本 - 优化版本（修复pickle错误）
功能：从ZIP压缩包中读取JSON文件，根据电话号码分类并检查是否为美国实体卡
优化：多进程处理、多浏览器窗口、连接复用
"""

import json
import multiprocessing as mp
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from datetime import datetime

from DrissionPage import ChromiumPage


def init_worker():
    """初始化工作进程"""
    # 全局变量，每个进程独立创建
    global browser
    browser = None
    
    # 注册进程退出时的清理函数
    import atexit
    atexit.register(cleanup_worker)
    
    # 预先创建浏览器实例
    get_browser()


def cleanup_worker():
    """清理工作进程资源"""
    global browser
    try:
        if browser:
            print(f"进程 {os.getpid()}: 正在关闭浏览器...")
            browser.quit()
            browser = None
            print(f"进程 {os.getpid()}: 浏览器已关闭")
    except Exception as e:
        print(f"进程 {os.getpid()}: 关闭浏览器时出错: {e}")
        browser = None


def cleanup_chrome_processes():
    """强制清理所有Chrome进程"""
    try:
        if sys.platform == 'win32':
            # Windows系统
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe', '/T'], 
                         capture_output=True, text=True)
            subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe', '/T'], 
                         capture_output=True, text=True)
        else:
            # macOS和Linux系统
            subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True)
        
        print("已清理所有Chrome进程")
    except Exception as e:
        print(f"清理Chrome进程时出错: {e}")


def signal_handler(signum, frame):
    """信号处理器，用于优雅退出"""
    print(f"\n收到信号 {signum}，正在清理资源...")
    cleanup_chrome_processes()
    sys.exit(0)


def load_us_area_codes():
    """加载美国区号列表"""
    us_area_codes = set()
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


def is_us_phone_number(phone, us_area_codes):
    """判断是否为美国电话号码"""
    clean_phone = re.sub(r'[^\d]', '', str(phone))
    
    if len(clean_phone) == 10:
        area_code = clean_phone[:3]
        return area_code in us_area_codes
    elif len(clean_phone) == 11 and clean_phone[0] == '1':
        area_code = clean_phone[1:4]
        return area_code in us_area_codes
    
    return False


def get_browser():
    """获取浏览器实例（每个进程独立）"""
    global browser
    if browser is None:
        try:
            browser = ChromiumPage()
            browser.set.auto_handle_alert()
            print(f"进程 {os.getpid()}: 浏览器初始化成功")
        except Exception as e:
            print(f"进程 {os.getpid()}: 浏览器初始化失败: {e}")
            raise
    return browser


def check_carrier_type(phone):
    """检查运营商类型（实体卡/虚拟卡）"""
    clean_phone = re.sub(r'[^\d]', '', str(phone))
    
    if not clean_phone.startswith('1'):
        return False
    
    if len(clean_phone) == 11:
        phone_number = clean_phone[1:]
    elif len(clean_phone) == 10:
        phone_number = clean_phone
    else:
        return False
    
    global browser
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 确保浏览器可用
            if browser is None:
                browser = get_browser()
            
            # 每次检查都重新加载页面，确保页面状态正确
            browser.get('https://freecarrierlookup.com/')
            time.sleep(1)  # 等待页面加载
            
            # 填充表单数据
            input_element = browser.ele('tag:input')
            input_element.input(phone_number, True)
            
            submit_button = browser.ele('tag:button[type=submit]')
            submit_button.click()
            
            # 等待结果加载
            time.sleep(1)
            
            # 查找结果元素
            result_element = browser.ele('tag:div', timeout=5)
            result = result_element.text
            print(f"进程 {os.getpid()}: 检查 {phone_number} 结果: {result}")
            return result.lower() == 'y'
            
        except Exception as e:
            print(f"进程 {os.getpid()}: 检查 {phone_number} 时出错 (尝试 {attempt + 1}/{max_retries}): {e}")
            
            # 如果不是最后一次尝试，尝试重新初始化浏览器
            if attempt < max_retries - 1:
                try:
                    if browser:
                        browser.quit()
                except:
                    pass
                browser = None
                time.sleep(1)  # 等待一秒后重试
            else:
                # 最后一次尝试失败，返回False
                return False
    
    return False


def process_phone_batch(args):
    """处理电话号码批次（进程函数）"""
    phone_batch, worker_id = args
    us_area_codes = load_us_area_codes()
    
    # 预先初始化浏览器，避免在处理过程中重复创建
    get_browser()
    
    results = []
    for i, phone_data in enumerate(phone_batch):
        try:
            phone = phone_data.get('phone', '')
            
            if is_us_phone_number(phone, us_area_codes):
                is_physical = check_carrier_type(phone)
                print(is_physical, 'is_physical')
                results.append({
                    'data': phone_data,
                    'is_us': True,
                    'is_physical': is_physical
                })
                
                if i % 5 == 0:  # 每5个号码输出一次进度
                    print(f"工作器 {worker_id}: 已处理 {i+1}/{len(phone_batch)} 个号码")
            else:
                results.append({
                    'data': phone_data,
                    'is_us': False,
                    'is_physical': False
                })
                
        except Exception as e:
            print(f"工作器 {worker_id}: 处理 {phone_data.get('phone', 'unknown')} 时出错: {e}")
            results.append({
                'data': phone_data,
                'is_us': False,
                'is_physical': False
            })
    
    print(f"工作器 {worker_id}: 完成批次处理，共 {len(phone_batch)} 个号码")
    return results


class PhoneClassifierOptimized:
    """优化的电话号码分类器"""
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or min(mp.cpu_count(), 4)
        
    def select_zip_file(self):
        """选择ZIP文件"""
        # 在无头环境中，使用命令行参数或默认路径
        import sys
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                return file_path
        
        # 尝试在当前目录查找ZIP文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        zip_files = [f for f in os.listdir(current_dir) if f.endswith('.zip')]
        
        if zip_files:
            # 返回找到的第一个ZIP文件
            return os.path.join(current_dir, zip_files[0])
        
        print("错误：未找到ZIP文件。请提供ZIP文件路径作为参数。")
        print("使用方法：python3 script/phone_classifier_optimized.py <zip文件路径>")
        return None
    
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
                                data['_original_filename'] = file_info.filename
                                json_files.append(data)
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            print(f"读取ZIP文件出错: {e}")
        return json_files
    
    def setup_directories(self):
        """创建目录结构"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        us_phones_dir = os.path.join(base_dir, "美国电话")
        non_us_phones_dir = os.path.join(base_dir, "非美国电话")
        
        os.makedirs(us_phones_dir, exist_ok=True)
        os.makedirs(non_us_phones_dir, exist_ok=True)
        
        physical_cards_dir = os.path.join(us_phones_dir, "实体卡")
        virtual_cards_dir = os.path.join(us_phones_dir, "非实体卡")
        
        os.makedirs(physical_cards_dir, exist_ok=True)
        os.makedirs(virtual_cards_dir, exist_ok=True)
        
        return us_phones_dir, non_us_phones_dir, physical_cards_dir, virtual_cards_dir
    
    def save_json_file(self, data, file_path):
        """保存JSON文件"""
        try:
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
    
    def process_files_parallel(self, json_files):
        """并行处理文件"""
        # 将文件分批
        batch_size = max(1, len(json_files) // self.max_workers)
        batches = [json_files[i:i + batch_size] for i in range(0, len(json_files), batch_size)]
        
        print(f"将 {len(json_files)} 个文件分成 {len(batches)} 批，每批约 {batch_size} 个文件")
        
        # 准备参数
        task_args = [(batch, i) for i, batch in enumerate(batches)]
        
        # 使用进程池并行处理
        all_results = []
        executor = ProcessPoolExecutor(
            max_workers=self.max_workers,
            initializer=init_worker
        )
        
        try:
            # 提交任务
            future_to_batch = {
                executor.submit(process_phone_batch, args): args
                for args in task_args
            }
            
            # 收集结果
            for future in as_completed(future_to_batch):
                args = future_to_batch[future]
                batch, worker_id = args
                try:
                    batch_results = future.result()
                    all_results.extend(batch_results)
                    print(f"工作器 {worker_id}: 完成 {len(batch)} 个文件的处理")
                except Exception as e:
                    print(f"工作器 {worker_id}: 处理批次时出错: {e}")
                    # 将失败批次的结果标记为非美国电话
                    for phone_data in batch:
                        all_results.append({
                            'data': phone_data,
                            'is_us': False,
                            'is_physical': False
                        })
        
        finally:
            # 确保进程池正确关闭，这会触发工作进程的清理函数
            print("正在关闭进程池...")
            executor.shutdown(wait=True)
            print("进程池已关闭")
        
        return all_results
    
    def save_results(self, results, zip_path, us_dir, non_us_dir, physical_dir, virtual_dir):
        """保存结果"""
        us_count = 0
        non_us_count = 0
        physical_count = 0
        virtual_count = 0
        
        # 使用线程池并行保存文件
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            
            for result in results:
                data = result['data']
                phone = data.get('phone', '')
                session_file = data.get('session_file', '')
                original_filename = data.get('_original_filename', '')
                
                if result['is_us']:
                    us_count += 1
                    if result['is_physical']:
                        physical_count += 1
                        json_save_path = os.path.join(physical_dir, f"{session_file}.json")
                        target_dir = physical_dir
                    else:
                        virtual_count += 1
                        json_save_path = os.path.join(virtual_dir, f"{session_file}.json")
                        target_dir = virtual_dir
                    
                    # 提交保存任务
                    futures.append(executor.submit(self.save_result_file, data, json_save_path, 
                                                 zip_path, session_file, original_filename, target_dir))
                else:
                    non_us_count += 1
                    json_save_path = os.path.join(non_us_dir, f"{session_file}.json")
                    futures.append(executor.submit(self.save_result_file, data, json_save_path, 
                                                 zip_path, session_file, original_filename, non_us_dir))
            
            # 等待所有保存任务完成
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    if completed % 10 == 0:
                        print(f"已保存 {completed}/{len(futures)} 个文件")
                except Exception as e:
                    print(f"保存文件时出错: {e}")
        
        return us_count, non_us_count, physical_count, virtual_count
    
    def save_result_file(self, data, json_save_path, zip_path, session_file, original_filename, target_dir):
        """保存单个结果文件"""
        # 保存JSON文件
        self.save_json_file(data, json_save_path)
        
        # 提取并保存session文件
        if session_file:
            if original_filename:
                base_name = os.path.splitext(original_filename)[0]
                session_filename = f"{base_name}.session"
            else:
                session_filename = f"{session_file}.session"
            
            session_content = self.extract_session_file_from_zip(zip_path, session_filename)
            if session_content:
                session_save_path = os.path.join(target_dir, f"{session_file}.session")
                self.save_session_file(session_content, session_save_path)
    
    def process_files(self):
        """主处理函数"""
        print("开始处理电话号码分类...")
        print(f"使用 {self.max_workers} 个工作器并行处理")
        
        # 选择ZIP文件
        zip_path = self.select_zip_file()
        if not zip_path:
            print("未选择文件，程序退出")
            return
        
        print(f"选择的文件: {zip_path}")
        
        # 提取JSON文件
        start_time = time.time()
        json_files = self.extract_json_from_zip(zip_path)
        if not json_files:
            print("ZIP文件中没有找到有效的JSON文件")
            return
        
        print(f"找到 {len(json_files)} 个JSON文件")
        
        # 创建目录结构
        us_dir, non_us_dir, physical_dir, virtual_dir = self.setup_directories()
        
        # 并行处理文件
        print("开始并行处理...")
        results = self.process_files_parallel(json_files)
        
        # 保存结果
        print("保存结果...")
        us_count, non_us_count, physical_count, virtual_count = self.save_results(
            results, zip_path, us_dir, non_us_dir, physical_dir, virtual_dir
        )
        
        # 统计信息
        elapsed_time = time.time() - start_time
        print(f"\n处理完成 (耗时 {elapsed_time:.2f} 秒):")
        print(f"美国电话: {us_count} 个")
        print(f"  - 实体卡: {physical_count} 个")
        print(f"  - 非实体卡: {virtual_count} 个")
        print(f"非美国电话: {non_us_count} 个")
        print(f"平均处理速度: {len(json_files)/elapsed_time:.2f} 文件/秒")
        
        # 创建最终的ZIP压缩包
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        us_zip_path = os.path.join(os.path.dirname(zip_path), f"美国电话_{timestamp}.zip")
        self.create_zip_archive(us_dir, us_zip_path)
        print(f"已创建美国电话压缩包: {us_zip_path}")
        
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
        
        # 强制清理所有Chrome进程
        print("正在清理浏览器进程...")
        cleanup_chrome_processes()


if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 设置多进程启动方法
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        # 如果已经设置过，忽略错误
        pass
    
    classifier = PhoneClassifierOptimized(max_workers=4)
    try:
        classifier.process_files()
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        # 强制清理所有Chrome进程
        print("正在清理浏览器进程...")
        cleanup_chrome_processes()
        
        # 强制垃圾回收
        import gc
        gc.collect()
        print("程序结束")