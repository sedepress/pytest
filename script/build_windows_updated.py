#!/usr/bin/env python3
"""
Windows 构建脚本
用于将phone_classifier.py打包成Windows可执行文件
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller安装成功")
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller安装失败: {e}")
        return False
    return True

def install_drissionpage():
    """安装DrissionPage"""
    print("正在安装DrissionPage...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "drissionpage"], check=True)
        print("✓ DrissionPage安装成功")
    except subprocess.CalledProcessError as e:
        print(f"✗ DrissionPage安装失败: {e}")
        return False
    return True

def build_exe():
    """构建EXE文件"""
    print("开始构建EXE文件...")
    
    # 切换到script目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # 使用spec文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "phone_classifier_windows.spec", "--clean", "--noconfirm"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✓ 构建成功！")
        print("构建输出:")
        print(result.stdout)
        
        if result.stderr:
            print("构建警告/错误:")
            print(result.stderr)
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        print("错误输出:")
        print(e.stderr)
        return False

def create_build_info():
    """创建构建信息文件"""
    build_info = """Phone Classifier Windows Build
===================================

构建时间: {timestamp}
Python版本: {python_version}
操作系统: {platform}

使用说明:
1. 运行 phone_classifier.exe
2. 选择包含JSON文件的ZIP压缩包
3. 程序会自动分类电话号码并输出结果

依赖组件:
- DrissionPage (浏览器自动化)
- tkinter (GUI文件选择)
- 标准库模块

注意事项:
- 需要Chrome浏览器已安装
- 需要网络连接访问查询API
- 建议在Windows 10/11上运行
""".format(
    timestamp=__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    python_version=sys.version,
    platform=sys.platform
    )
    
    with open("dist/build_info.txt", "w", encoding="utf-8") as f:
        f.write(build_info)
    print("✓ 构建信息文件已创建")

def main():
    """主函数"""
    print("Phone Classifier Windows 构建工具")
    print("=" * 40)
    
    # 检查是否在Windows上
    if not sys.platform.startswith('win'):
        print("警告: 此脚本设计用于Windows环境")
        response = input("是否继续构建? (y/N): ")
        if response.lower() != 'y':
            print("构建已取消")
            return
    
    # 安装依赖
    if not install_pyinstaller():
        return
    
    if not install_drissionpage():
        return
    
    # 构建EXE
    if not build_exe():
        return
    
    # 创建构建信息
    create_build_info()
    
    print("\n" + "=" * 40)
    print("构建完成!")
    print("EXE文件位置: dist/phone_classifier.exe")
    print("文件夹版本: dist/phone_classifier/")
    print("=" * 40)

if __name__ == "__main__":
    main()