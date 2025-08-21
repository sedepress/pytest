# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python 3.14 project for phone number classification and web scraping tasks. The main functionality includes:

1. **Phone Number Classification** (`script/phone_classifier.py`): A script that processes ZIP archives containing JSON files with phone numbers, classifies them as US/non-US numbers, and determines if US numbers are physical/virtual carrier lines using external API calls.

2. **Web Scraping Challenges** (`爬虫网/题目*.py`): A collection of 19 web scraping exercises that fetch data from various APIs.

3. **Database Operations** (`qc_script/`): Scripts for database operations including cleaning expired posts and managing resources.

## Key Commands

### Running the Phone Classifier
```bash
# Run the main phone classification script
python script/phone_classifier.py
```

### Running Individual Scripts
```bash
# Run specific web scraping challenges
python 爬虫网/题目1.py
python 爬虫网/题目2.py
# ... etc for 题目1.py through 题目19.py

# Run database operation scripts
python qc_script/清理过期帖子ES.py
python qc_script/有问必答店铺创建.py
python qc_script/有问必答店铺试用次数.py
python qc_script/清理2025年之前不续约圈子七牛资源.py
python qc_script/补签.py
```

### Running Main Database Script
```bash
python main.py
```

## Project Structure

- `script/` - Main phone classification tool with supporting JSON test data
- `爬虫网/` - 19 web scraping challenge scripts with associated JS/WASM files
- `qc_script/` - Database management and cleaning scripts
- `main.py` - Primary database operations script for lottery data
- `pyproject.toml` - Project configuration with Python 3.14 requirement

## Dependencies

The project uses uv for dependency management. Key dependencies include:
- `pymysql>=1.1.1` - MySQL database connectivity
- `pysocks>=1.7.1` - SOCKS proxy support
- `qiniu>=7.16.0` - Qiniu cloud storage SDK
- `requests>=2.32.4` - HTTP requests library

## Phone Classification Architecture

The `phone_classifier.py` implements a comprehensive phone number classification system:

1. **File Processing**: Extracts JSON files from ZIP archives, preserving session files
2. **US Phone Detection**: Uses a hardcoded list of US area codes to identify US numbers
3. **Carrier Type Detection**: Makes HTTP requests to freecarrierlookup.com via proxies to determine if numbers are physical/virtual
4. **File Organization**: Creates directory structure and generates output ZIP archives
5. **Proxy Support**: Handles SOCKS5 and HTTP proxies from JSON configuration

## Database Integration

Several scripts connect to MySQL databases for:
- Lottery data storage and retrieval (`main.py`)
- Post/thread management (`qc_script/清理过期帖子ES.py`)
- Qiniu resource management (`qc_script/清理2025年之前不续约圈子七牛资源.py`)

## Testing and Data

- Test JSON files are located in `script/` and `script/测试/` directories
- Session files (.session) are processed alongside JSON files
- The classifier uses freecarrierlookup.com API with hardcoded cookies for carrier detection

## Notes

- The project requires Python 3.14 or higher
- All scripts are designed to be cross-platform (Windows/macOS compatible)
- The phone classifier includes GUI file selection using tkinter
- Proxy configuration is extracted from JSON files for carrier lookup requests