#!/usr/bin/env python3
"""
Hibiki UI Print转Logger工具

智能批量替换print语句为logger调用的工具
- 自动检测现有的logger导入
- 智能分析print内容，决定日志级别
- 保留examples目录不变
- 生成详细转换报告
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import ast

class PrintToLoggerConverter:
    """Print转Logger转换器"""
    
    def __init__(self, hibiki_root: str):
        self.hibiki_root = Path(hibiki_root)
        self.conversion_stats = {
            'files_processed': 0,
            'prints_converted': 0,
            'logger_imports_added': 0,
            'skipped_files': []
        }
        
        # 日志级别检测模式
        self.log_level_patterns = {
            'debug': [
                r'(?i)(调试|debug|创建|初始化|设置|绑定|计算|效果|布局)',
                r'🔍|🔧|⚙️|🚀|🎨|📐|🔗|✅|🎯|🏗️'
            ],
            'info': [
                r'(?i)(启动|完成|成功|运行|加载)',
                r'🚀|✅|📱|💡|🎉'
            ],
            'warning': [
                r'(?i)(警告|warning|⚠️|注意|缺少)',
                r'⚠️|⚡|🟡'
            ],
            'error': [
                r'(?i)(错误|error|失败|异常|❌)',
                r'❌|💥|🔥|⛔'
            ]
        }
    
    def detect_log_level(self, print_content: str) -> str:
        """智能检测应该使用的日志级别"""
        print_content = print_content.strip()
        
        # 检查各个级别的模式
        for level, patterns in self.log_level_patterns.items():
            for pattern in patterns:
                if re.search(pattern, print_content):
                    return level
        
        # 默认使用debug级别
        return 'debug'
    
    def has_logger_import(self, file_content: str) -> bool:
        """检查文件是否已有logger导入"""
        return ('get_logger' in file_content and 
                'logging import' in file_content)
    
    def add_logger_import_and_init(self, file_content: str, file_path: Path) -> str:
        """添加logger导入和初始化"""
        lines = file_content.split('\n')
        
        # 寻找合适的导入位置
        import_insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_insert_idx = i + 1
            elif line.strip() == '':
                continue
            elif not line.startswith('#') and line.strip():
                break
        
        # 确定相对导入路径
        rel_path = file_path.relative_to(self.hibiki_root)
        depth = len(rel_path.parts) - 1  # 减1因为文件本身不算
        import_prefix = '../' * depth if depth > 0 else './'
        
        # 构建导入语句
        if depth == 0:
            # 在hibiki根目录下
            logger_import = "from .core.logging import get_logger"
        else:
            # 在子目录中
            logger_import = f"from {'...' if depth > 1 else '..'}core.logging import get_logger"
        
        # 生成模块名
        module_parts = []
        for part in rel_path.parts:
            if part.endswith('.py'):
                part = part[:-3]  # 移除.py
            module_parts.append(part)
        module_name = '.'.join(module_parts)
        
        # 插入导入和初始化
        lines.insert(import_insert_idx, logger_import)
        lines.insert(import_insert_idx + 1, "")
        lines.insert(import_insert_idx + 2, "# 初始化日志器")
        lines.insert(import_insert_idx + 3, f"logger = get_logger('{module_name}')")
        lines.insert(import_insert_idx + 4, "")
        
        self.conversion_stats['logger_imports_added'] += 1
        return '\n'.join(lines)
    
    def convert_print_to_logger(self, match) -> str:
        """转换单个print调用为logger调用"""
        print_args = match.group(1)
        
        # 检测日志级别
        log_level = self.detect_log_level(print_args)
        
        # 清理print参数 - 移除f字符串前缀并保持原有格式
        if print_args.strip().startswith('f"') or print_args.strip().startswith("f'"):
            # f字符串保持不变
            logger_call = f"logger.{log_level}({print_args})"
        else:
            # 普通字符串也保持不变
            logger_call = f"logger.{log_level}({print_args})"
        
        return logger_call
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个文件"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 查找所有print调用
            print_pattern = r'print\(([^)]+(?:\([^)]*\)[^)]*)*)\)'
            print_matches = list(re.finditer(print_pattern, content))
            
            if not print_matches:
                return False  # 没有print调用
            
            print(f"🔍 处理文件: {file_path}")
            print(f"   发现 {len(print_matches)} 个print调用")
            
            # 检查是否需要添加logger导入
            if not self.has_logger_import(content):
                content = self.add_logger_import_and_init(content, file_path)
                print(f"   ✅ 已添加logger导入和初始化")
            
            # 转换所有print调用
            converted_count = 0
            for match in reversed(print_matches):  # 反向处理以保持位置正确
                start, end = match.span()
                new_call = self.convert_print_to_logger(match)
                content = content[:start] + new_call + content[end:]
                converted_count += 1
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ 已转换 {converted_count} 个print调用")
            
            self.conversion_stats['files_processed'] += 1
            self.conversion_stats['prints_converted'] += converted_count
            
            return True
            
        except Exception as e:
            print(f"❌ 处理文件失败 {file_path}: {e}")
            self.conversion_stats['skipped_files'].append(str(file_path))
            return False
    
    def should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        # 跳过examples目录
        if 'examples' in file_path.parts:
            return True
        
        # 跳过测试文件
        if 'test' in file_path.name.lower():
            return True
            
        # 跳过工具脚本本身
        if file_path.name == 'convert_prints_to_logging.py':
            return True
            
        return False
    
    def run_conversion(self):
        """运行批量转换"""
        print("🚀 开始批量转换print到logger...")
        print(f"📁 扫描目录: {self.hibiki_root}")
        
        # 查找所有Python文件
        py_files = list(self.hibiki_root.rglob("*.py"))
        
        for py_file in py_files:
            if self.should_skip_file(py_file):
                continue
                
            self.process_file(py_file)
        
        # 输出统计报告
        print("\n" + "="*50)
        print("📊 转换完成统计报告")
        print("="*50)
        print(f"处理文件数量: {self.conversion_stats['files_processed']}")
        print(f"转换print数量: {self.conversion_stats['prints_converted']}")
        print(f"添加logger导入: {self.conversion_stats['logger_imports_added']}")
        
        if self.conversion_stats['skipped_files']:
            print(f"\n⚠️ 跳过的文件:")
            for skipped in self.conversion_stats['skipped_files']:
                print(f"   - {skipped}")
        
        print("\n✅ 批量转换完成!")
        print("💡 建议运行测试确保转换后的代码正常工作")

def main():
    if len(sys.argv) != 2:
        print("使用方法: python convert_prints_to_logging.py <hibiki根目录>")
        sys.exit(1)
    
    hibiki_root = sys.argv[1]
    if not os.path.exists(hibiki_root):
        print(f"❌ 目录不存在: {hibiki_root}")
        sys.exit(1)
    
    converter = PrintToLoggerConverter(hibiki_root)
    converter.run_conversion()

if __name__ == "__main__":
    main()