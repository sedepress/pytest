# Phone Classifier Windows 构建指南

## 概述
此目录包含将 `phone_classifier.py` 打包成 Windows 可执行文件的配置和脚本。

## 文件说明

### 主要文件
- `phone_classifier.py` - 主程序脚本
- `phone_classifier_windows.spec` - PyInstaller 配置文件
- `build_windows_simple.bat` - Windows 批处理构建脚本
- `build_windows_updated.py` - Python 构建脚本

### 构建产物
- `dist/phone_classifier.exe` - 单文件可执行程序
- `dist/phone_classifier/` - 文件夹版本（包含所有依赖）

## 构建方法

### 方法一：使用批处理脚本（推荐）
1. 双击运行 `build_windows_simple.bat`
2. 等待构建完成
3. 在 `dist` 目录找到生成的 EXE 文件

### 方法二：使用Python脚本
```bash
python build_windows_updated.py
```

### 方法三：手动构建
```bash
# 安装依赖
pip install pyinstaller drissionpage

# 使用spec文件构建
pyinstaller phone_classifier_windows.spec --clean --noconfirm
```

## 系统要求

### 开发环境
- Python 3.8+
- PyInstaller
- DrissionPage

### 运行环境
- Windows 10/11
- Chrome 浏览器（必需）
- 网络连接

## 配置说明

### Spec文件特点
- 包含所有必要的隐藏导入
- 排除不必要的科学计算库
- 支持GUI和命令行界面
- 自动处理Chrome浏览器依赖

### 主要依赖
- `DrissionPage` - 浏览器自动化
- `tkinter` - GUI文件选择器
- `requests` - HTTP请求
- `selenium` - WebDriver支持

## 使用说明

### 运行EXE文件
1. 双击 `phone_classifier.exe`
2. 在弹出的文件选择器中选择包含JSON文件的ZIP压缩包
3. 等待程序处理完成
4. 查看生成的分类结果

### 命令行使用
```bash
phone_classifier.exe 文件路径.zip
```

## 故障排除

### 常见问题
1. **Chrome浏览器未找到**
   - 确保已安装Chrome浏览器
   - 检查Chrome是否在系统PATH中

2. **缺少依赖库**
   - 使用spec文件重新构建
   - 检查 `hiddenimports` 配置

3. **GUI无法显示**
   - 确保系统支持tkinter
   - 检查Windows显示设置

4. **网络连接问题**
   - 检查防火墙设置
   - 确保可以访问 `freecarrierlookup.com`

### 调试方法
1. 使用 `--debug` 参数构建调试版本
2. 检查控制台输出错误信息
3. 在开发环境中测试脚本功能

## 更新日志

### v1.0 (2024-08-22)
- 初始Windows版本
- 支持GUI文件选择
- 包含所有必要依赖
- 优化打包大小