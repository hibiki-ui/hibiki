#!/usr/bin/env python3
"""
安全的日志转换工具 - 将print语句转换为logger调用

改进策略：
1. 更精确的AST解析，避免破坏语法
2. 分批处理，每次只处理几个文件
3. 备份和验证机制
4. 支持手动确认模式
"""

import ast
import re
import os
import shutil
from pathlib import Path
from typing import List, Tuple, Set
import argparse

class SafeLoggingConverter:
    def __init__(self, hibiki_root: Path):
        self.hibiki_root = hibiki_root
        self.backup_dir = hibiki_root / "tools" / "backup"
        self.processed_files: Set[Path] = set()
        
    def find_print_statements(self, file_path: Path) -> List[Tuple[int, str, str]]:
        """查找文件中的print语句，返回 (行号, 原始行, 建议替换)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")
            return []
            
        results = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line.rstrip()
            stripped = line.strip()
            
            # 跳过注释行
            if stripped.startswith('#'):
                continue
                
            # 检测print语句的几种模式
            print_patterns = [
                r'print\s*\(\s*f"([^"]*)"',     # f-string
                r'print\s*\(\s*"([^"]*)"',      # 普通字符串
                r'print\s*\(\s*f\'([^\']*)\'',  # f-string单引号
                r'print\s*\(\s*\'([^\']*)\'',   # 普通字符串单引号
            ]
            
            for pattern in print_patterns:
                match = re.search(pattern, stripped)
                if match:
                    message = match.group(1)
                    
                    # 确定日志级别
                    if any(marker in message.lower() for marker in ['error', '错误', '❌']):
                        log_level = 'error'
                    elif any(marker in message.lower() for marker in ['warn', '警告', '⚠️']):
                        log_level = 'warning'
                    elif any(marker in message.lower() for marker in ['debug', '调试', '🐛']):
                        log_level = 'debug'
                    else:
                        log_level = 'info'
                    
                    # 生成替换建议
                    if stripped.startswith('print(f"') or stripped.startswith("print(f'"):
                        suggested = stripped.replace('print(f"', f'logger.{log_level}(f"').replace("print(f'", f"logger.{log_level}(f'")
                    else:
                        suggested = stripped.replace('print("', f'logger.{log_level}("').replace("print('", f"logger.{log_level}('")
                    
                    results.append((line_num, original_line, suggested))
                    break
                    
        return results

    def backup_file(self, file_path: Path) -> Path:
        """备份文件"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建相对路径的备份结构
        relative_path = file_path.relative_to(self.hibiki_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_path)
        return backup_path

    def add_logger_import(self, file_path: Path, content: str) -> str:
        """添加logger导入语句"""
        lines = content.split('\n')
        
        # 查找是否已有logger相关导入
        has_logger_import = any('get_logger' in line for line in lines)
        has_logger_var = any(re.match(r'\s*logger\s*=', line) for line in lines)
        
        if has_logger_import and has_logger_var:
            return content
            
        # 找到导入语句的位置 - 更精确的查找
        import_insert_line = 0
        last_import_line = -1
        
        # 找到开头导入块的最后一行（避免文件末尾的测试导入）
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
        
        # 如果找到导入语句，找到导入块的结束位置
        if last_import_line >= 0:
            import_insert_line = last_import_line + 1
            
            # 寻找导入块后第一个空行的位置
            for i in range(last_import_line + 1, len(lines)):
                line = lines[i].strip()
                # 遇到第一个非导入、非空行时停止
                if line and not line.startswith('from ') and not line.startswith('import ') and not line.startswith('#'):
                    import_insert_line = i
                    break
                # 如果是空行，这是插入的好位置
                if not line:
                    import_insert_line = i
                    break
        else:
            # 没有导入语句，在文件开头插入
            # 跳过文档字符串和注释
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
                    import_insert_line = i
                    break
        
        # 计算模块名称 
        relative_path = file_path.relative_to(self.hibiki_root)
        parts = relative_path.parts
        
        # 构建简化的模块名称
        if len(parts) >= 2 and parts[0] == 'hibiki':
            # hibiki/components/basic.py -> components.basic
            module_name = '.'.join(parts[1:-1] + (parts[-1].replace('.py', ''),))
        else:
            module_name = parts[-1].replace('.py', '')
        
        # 确定正确的导入路径
        if parts[0] == 'hibiki' and len(parts) >= 3:
            if parts[1] == 'core':
                # hibiki/core内的文件使用相对导入
                import_statement = "from .logging import get_logger"
            else:
                # hibiki/components等使用绝对导入
                import_statement = "from hibiki.core.logging import get_logger"
        else:
            # 默认使用相对导入
            import_statement = "from ..core.logging import get_logger"
        
        # 添加导入和logger初始化
        new_imports = []
        if not has_logger_import:
            new_imports.append(import_statement)
        if not has_logger_var:
            new_imports.append(f"logger = get_logger('{module_name}')")
        
        if new_imports:
            lines.insert(import_insert_line, "")
            for imp in reversed(new_imports):
                lines.insert(import_insert_line, imp)
            lines.insert(import_insert_line, "")
            
        return '\n'.join(lines)

    def process_file(self, file_path: Path, dry_run: bool = True, auto_confirm: bool = False) -> bool:
        """处理单个文件"""
        print_statements = self.find_print_statements(file_path)
        
        if not print_statements:
            return True
            
        print(f"\n📁 处理文件: {file_path.relative_to(self.hibiki_root)}")
        print(f"找到 {len(print_statements)} 个print语句:")
        
        for line_num, original, suggested in print_statements:
            print(f"  {line_num:3d}: {original}")
            print(f"       -> {suggested}")
        
        if dry_run:
            print("  (预览模式，未实际修改)")
            return True
            
        # 确认是否继续
        if auto_confirm:
            print("  (自动确认模式，继续处理)")
            response = 'y'
        else:
            response = input("\n是否处理此文件？ (y/n/q): ").strip().lower()
            if response == 'q':
                return False
            if response != 'y':
                return True
            
        # 备份文件
        backup_path = self.backup_file(file_path)
        print(f"✅ 已备份到: {backup_path.relative_to(self.hibiki_root)}")
        
        try:
            # 读取原文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 添加logger导入
            content = self.add_logger_import(file_path, content)
            
            # 逐行替换
            lines = content.split('\n')
            for line_num, original, suggested in print_statements:
                if line_num <= len(lines):
                    lines[line_num - 1] = lines[line_num - 1].replace(
                        original.strip(), suggested
                    )
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
            # 验证语法
            try:
                with open(file_path, 'r') as f:
                    ast.parse(f.read())
                print(f"✅ 语法检查通过")
                self.processed_files.add(file_path)
                return True
            except SyntaxError as e:
                print(f"❌ 语法错误: {e}")
                # 恢复备份
                shutil.copy2(backup_path, file_path)
                print(f"⚠️  已恢复原文件")
                return True
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            return True

    def find_library_files(self) -> List[Path]:
        """查找需要处理的库文件（排除examples）"""
        library_files = []
        
        # 扫描hibiki目录下的Python文件
        hibiki_dir = self.hibiki_root / "hibiki"
        if hibiki_dir.exists():
            for py_file in hibiki_dir.rglob("*.py"):
                if py_file.name != "__init__.py":
                    library_files.append(py_file)
        
        return sorted(library_files)

    def run(self, dry_run: bool = True, batch_size: int = 5, auto_confirm: bool = False):
        """执行转换"""
        files = self.find_library_files()
        
        if not files:
            print("没有找到需要处理的文件")
            return
            
        print(f"找到 {len(files)} 个库文件需要检查")
        
        # 分批处理
        for i in range(0, len(files), batch_size):
            batch = files[i:i+batch_size]
            print(f"\n{'='*50}")
            print(f"处理批次 {i//batch_size + 1}: {len(batch)} 个文件")
            print('='*50)
            
            for file_path in batch:
                if not self.process_file(file_path, dry_run, auto_confirm):
                    print("用户退出")
                    break
            else:
                continue
            break
        
        print(f"\n处理完成。共处理 {len(self.processed_files)} 个文件")
        if self.processed_files and not dry_run:
            print(f"备份位置: {self.backup_dir}")

def main():
    parser = argparse.ArgumentParser(description="安全的日志转换工具")
    parser.add_argument("--run", action="store_true", help="实际执行转换（默认为预览模式）")
    parser.add_argument("--batch-size", type=int, default=3, help="批次大小")
    parser.add_argument("--auto", action="store_true", help="自动确认所有文件")
    
    args = parser.parse_args()
    
    hibiki_root = Path(__file__).parent.parent
    converter = SafeLoggingConverter(hibiki_root)
    
    print(f"Hibiki UI 安全日志转换工具")
    print(f"根目录: {hibiki_root}")
    print(f"模式: {'实际执行' if args.run else '预览模式'}")
    print(f"批次大小: {args.batch_size}")
    print(f"自动确认: {args.auto}")
    
    converter.run(dry_run=not args.run, batch_size=args.batch_size, auto_confirm=args.auto)

if __name__ == "__main__":
    main()