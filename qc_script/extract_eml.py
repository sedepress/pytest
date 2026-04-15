#!/usr/bin/env python3
"""从ZIP压缩包中提取EML邮件文件内容到TXT"""

import zipfile
from email import policy
from email.parser import BytesParser
from pathlib import Path


def extract_eml_content(zip_path: str, output_txt: str) -> None:
    """
    从ZIP文件中读取所有EML文件并提取内容到TXT

    Args:
        zip_path: ZIP文件路径
        output_txt: 输出TXT文件路径
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        eml_files = [f for f in zip_file.namelist() if f.lower().endswith('.eml')]

        if not eml_files:
            print("ZIP中未找到EML文件")
            return

        with open(output_txt, 'w', encoding='utf-8') as output:
            for idx, eml_name in enumerate(eml_files, 1):
                output.write(f"{'='*80}\n")
                output.write(f"邮件 {idx}/{len(eml_files)}: {eml_name}\n")
                output.write(f"{'='*80}\n\n")

                # 读取并解析EML文件
                eml_data = zip_file.read(eml_name)
                msg = BytesParser(policy=policy.default).parsebytes(eml_data)

                # 提取邮件头信息
                output.write(f"主题: {msg.get('Subject', '无主题')}\n")
                output.write(f"发件人: {msg.get('From', '未知')}\n")
                output.write(f"收件人: {msg.get('To', '未知')}\n")
                output.write(f"日期: {msg.get('Date', '未知')}\n")
                output.write(f"\n{'-'*80}\n正文:\n{'-'*80}\n\n")

                # 提取邮件正文
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == 'text/plain':
                            body = part.get_content()
                            output.write(body)
                            output.write("\n")
                        elif content_type == 'text/html':
                            # 如果没有纯文本，使用HTML
                            if not any(p.get_content_type() == 'text/plain' for p in msg.walk()):
                                body = part.get_content()
                                output.write("[HTML内容]\n")
                                output.write(body)
                                output.write("\n")
                else:
                    body = msg.get_content()
                    output.write(body)
                    output.write("\n")

                output.write(f"\n\n")

        print(f"✓ 已处理 {len(eml_files)} 个EML文件")
        print(f"✓ 输出文件: {output_txt}")


if __name__ == "__main__":
    zip_path = "1.zip"
    output_txt = "邮件内容.txt"

    if not Path(zip_path).exists():
        print(f"错误: 找不到文件 {zip_path}")
        exit(1)

    extract_eml_content(zip_path, output_txt)
