#!/usr/bin/env python3
"""
测试NSTextField方法的正确性
验证各种方法名是否存在和可用
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_nstextfield_methods():
    """测试NSTextField和NSTextFieldCell的方法"""
    
    try:
        from AppKit import NSTextField, NSLineBreakByWordWrapping, NSLineBreakByClipping
        
        print("🧪 测试NSTextField方法存在性")
        print("=" * 50)
        
        # 创建NSTextField实例
        field = NSTextField.alloc().init()
        cell = field.cell()
        
        print(f"NSTextField实例: {field}")
        print(f"NSTextFieldCell实例: {cell}")
        print()
        
        # 测试NSTextField直接方法
        methods_to_test = [
            ('field.setUsesSingleLineMode_', 'field', 'setUsesSingleLineMode_'),
            ('field.setLineBreakMode_', 'field', 'setLineBreakMode_'), 
            ('field.setPreferredMaxLayoutWidth_', 'field', 'setPreferredMaxLayoutWidth_'),
            ('cell.setUsesSingleLineMode_', 'cell', 'setUsesSingleLineMode_'),
            ('cell.setLineBreakMode_', 'cell', 'setLineBreakMode_'),
            ('cell.setWraps_', 'cell', 'setWraps_'),
            ('cell.setScrollable_', 'cell', 'setScrollable_'),
        ]
        
        for description, obj_name, method_name in methods_to_test:
            obj = field if obj_name == 'field' else cell
            has_method = hasattr(obj, method_name)
            
            if has_method:
                print(f"✅ {description}: 存在")
                
                # 尝试调用方法（使用安全的参数）
                try:
                    if method_name == 'setUsesSingleLineMode_':
                        obj.setUsesSingleLineMode_(False)
                        print(f"   ✅ 调用成功")
                    elif method_name == 'setLineBreakMode_':
                        obj.setLineBreakMode_(NSLineBreakByWordWrapping)
                        print(f"   ✅ 调用成功")
                    elif method_name == 'setPreferredMaxLayoutWidth_':
                        obj.setPreferredMaxLayoutWidth_(400.0)
                        print(f"   ✅ 调用成功")
                    elif method_name in ['setWraps_', 'setScrollable_']:
                        obj.setWraps_(True) if method_name == 'setWraps_' else obj.setScrollable_(False)
                        print(f"   ✅ 调用成功")
                except Exception as e:
                    print(f"   ❌ 调用失败: {e}")
                        
            else:
                print(f"❌ {description}: 不存在")
        
        print()
        
        # 测试常量
        constants_to_test = [
            ('NSLineBreakByWordWrapping', NSLineBreakByWordWrapping),
            ('NSLineBreakByClipping', NSLineBreakByClipping),
        ]
        
        print("🔍 测试常量:")
        for name, value in constants_to_test:
            print(f"✅ {name} = {value}")
        
        print()
        print("🎉 方法测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_nstextfield_methods()
    sys.exit(0 if success else 1)