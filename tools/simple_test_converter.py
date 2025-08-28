#!/usr/bin/env python3
"""
简化的测试转换器 - 用于调试和测试转换逻辑
"""

import re
from pathlib import Path

def convert_one_file(file_path: Path):
    """转换单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 查找print语句
    found_prints = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if 'print(' in stripped and not stripped.startswith('#'):
            found_prints.append((i, line))
    
    print(f"文件: {file_path}")
    print(f"找到 {len(found_prints)} 个print语句")
    
    if found_prints:
        print("前5个:")
        for i, (line_num, line) in enumerate(found_prints[:5]):
            print(f"  {line_num+1}: {line.strip()}")
    
    # 查找现有导入
    has_logger_import = any('get_logger' in line for line in lines)
    has_logger_var = any(re.match(r'\s*logger\s*=', line) for line in lines)
    
    print(f"已有logger导入: {has_logger_import}")
    print(f"已有logger变量: {has_logger_var}")
    
    if not has_logger_import or not has_logger_var:
        # 改进的导入位置查找（只查找开头导入块，正确处理多行导入）
        last_import_line = -1
        in_import_block = True
        in_multiline_import = False
        paren_depth = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 跳过文件头部的注释和文档字符串
            if i < 10 and (not stripped or stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''")):
                continue
            
            # 处理多行导入的括号计数
            if in_multiline_import:
                paren_depth += line.count('(') - line.count(')')
                if paren_depth <= 0:
                    in_multiline_import = False
                    if in_import_block:
                        last_import_line = i
                continue
                
            if stripped.startswith('from ') or stripped.startswith('import '):
                if in_import_block:
                    last_import_line = i
                    # 检查是否是多行导入
                    if '(' in line and ')' not in line:
                        in_multiline_import = True
                        paren_depth = line.count('(')
            else:
                # 遇到非空非注释非导入行，且已经有过导入，检查是否应该结束导入块
                if stripped and not stripped.startswith('#') and last_import_line >= 0 and not in_multiline_import:
                    # 如果是class, def, 或其他明显的非导入代码，结束导入块
                    if (stripped.startswith('class ') or stripped.startswith('def ') or 
                        stripped.startswith('if __name__') or stripped.startswith('@')):
                        in_import_block = False
                        break
        
        print(f"开头导入块最后一行: {last_import_line}")
        if last_import_line >= 0:
            print(f"  内容: {lines[last_import_line].strip()}")
            
            # 找插入位置
            insert_pos = last_import_line + 1
            print(f"建议插入位置: {insert_pos}")
            if insert_pos < len(lines):
                print(f"  插入位置的行: '{lines[insert_pos]}'")
            else:
                print("  插入位置：文件末尾")

if __name__ == "__main__":
    # 测试一个文件
    test_file = Path(__file__).parent.parent / "hibiki/components/basic.py"
    convert_one_file(test_file)