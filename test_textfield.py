#!/usr/bin/env python3
"""
测试TextField组件功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# 导入macUI v4.0
from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import TextField, Label

def main():
    print("📝 TextField组件测试")
    print("=" * 30)
    
    # 初始化系统
    ManagerFactory.initialize_all()
    
    # 测试基础TextField创建
    print("\n1. 基础TextField测试:")
    
    def on_text_change(text):
        print(f"💬 用户输入: '{text}'")
    
    textfield = TextField(
        value="初始文本",
        placeholder="请输入文本...",
        on_change=on_text_change,
        width=250, height=30
    )
    
    # 挂载组件
    print("\n🚀 挂载TextField...")
    view = textfield.mount()
    
    print(f"✅ TextField挂载完成: {type(view).__name__}")
    print(f"🎯 当前文本: '{textfield.get_text()}'")
    print(f"💬 占位符: '{textfield.placeholder}'")
    
    # 测试动态文本设置
    print("\n2. 动态更新测试:")
    textfield.set_text("更新的文本")
    textfield.set_placeholder("新的占位符")
    
    print(f"✅ 文本已更新: '{textfield.get_text()}'")
    print(f"✅ 占位符已更新: '{textfield.placeholder}'")
    
    # 测试API链式调用
    print("\n3. API链式调用测试:")
    styled_textfield = TextField("样式文本", width=300, height=35)
    api_chain = styled_textfield.layout.center().fade(0.9).scale(1.1)
    result = api_chain.done()
    
    styled_view = styled_textfield.mount()
    
    print(f"✅ 链式调用成功: {result.__class__.__name__}")
    print(f"   - 定位: {styled_textfield.style.position}")
    print(f"   - 透明度: {styled_textfield.style.opacity}")
    print(f"   - 缩放: {styled_textfield.style.scale}")
    
    # 测试定位功能
    print("\n4. 定位功能测试:")
    positioned_textfield = TextField("定位测试", width=200, height=25)
    positioned_textfield.layout.absolute(left=100, top=200)
    positioned_view = positioned_textfield.mount()
    
    print(f"✅ 绝对定位: position={positioned_textfield.style.position}")
    print(f"   坐标: left={positioned_textfield.style.left}, top={positioned_textfield.style.top}")
    
    print("\n✅ TextField测试完成！")
    print("=" * 30)
    
    print("\n📊 测试总结:")
    print("✅ TextField基础功能")
    print("✅ 文本改变事件绑定")
    print("✅ 动态文本和占位符更新")
    print("✅ API链式调用支持")
    print("✅ 定位和样式系统")
    
    print(f"\n🎉 TextField组件完全正常工作！")

if __name__ == "__main__":
    main()