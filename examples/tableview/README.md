# NSTableView 纯 PyObjC 实现示例

本目录包含严格按照 NSTableView 核心指南 + PyObjC 最佳实践实现的纯 PyObjC 示例，用于验证和理解 NSTableView 的正确用法。

## 🎯 PyObjC 最佳实践应用

所有示例都应用了 PyObjC 命令行启动的核心4要点：
1. **激活策略** - `app.setActivationPolicy_(NSApplicationActivationPolicyRegular)`
2. **菜单栏** - 创建包含退出功能的最小菜单栏
3. **AppHelper事件循环** - `AppHelper.runEventLoop(installInterrupt=True)`
4. **分离架构** - AppDelegate + WindowController 保持强引用链

## 文件说明

### 1. `simple_pure_tableview.py`
**简单的NSTableView实现 + PyObjC最佳实践**
- 基础的View-Based表格
- 正确实现数据源和代理模式
- 视图复用机制
- AppDelegate + WindowController 分离架构

**功能特性：**
- ✅ NSTableViewDataSource 正确实现
- ✅ NSTableViewDelegate 正确实现  
- ✅ View-Based 表格模式
- ✅ 视图复用队列 (`makeViewWithIdentifier_owner_`)
- ✅ PyObjC 最佳实践 (激活策略 + 菜单栏 + AppHelper + 分离架构)
- ✅ 强引用链防止对象回收

### 2. `advanced_pure_tableview_simple.py`
**高级NSTableView实现（简化版）+ PyObjC最佳实践**
- 完整的功能特性集合
- 动态数据操作
- 列排序功能
- 条件格式化
- AppDelegate + WindowController 分离架构

**功能特性：**
- ✅ 动态数据添加/删除/清空/重置
- ✅ 列标题排序（点击排序）
- ✅ 条件格式化（薪资颜色编码）
- ✅ 高性能视图复用
- ✅ 完整的用户交互
- ✅ PyObjC 最佳实践 (激活策略 + 菜单栏 + AppHelper + 分离架构)
- ✅ 强引用链防止对象回收

### 3. `advanced_pure_tableview.py`
**复杂自定义视图版本（存在问题）+ PyObjC最佳实践**
- 尝试使用自定义NSView和复杂布局
- 遇到objc关联对象和约束问题  
- 已应用PyObjC最佳实践架构
- 作为学习参考，展示了复杂实现的挑战
- **推荐使用简化版本**

## 核心实现要点

### 1. 数据源模式 (DataSource Pattern)
```python
class TableDataSource(NSObject):
    def numberOfRowsInTableView_(self, tableView):
        """必须实现：返回行数"""
        return len(self.data)
    
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        """兼容方法：用于排序等功能"""
        # 返回单元格数据
```

### 2. 代理模式 (Delegate Pattern)
```python
class TableDelegate(NSObject):
    def tableView_viewForTableColumn_row_(self, tableView, tableColumn, row):
        """核心方法：提供单元格视图"""
        # Step 1: 尝试从复用队列获取视图
        cell_view = tableView.makeViewWithIdentifier_owner_(identifier, self)
        
        # Step 2: 如果没有可复用的，创建新视图
        if cell_view is None:
            cell_view = NSTextField.alloc().init()
            cell_view.setIdentifier_(identifier)
        
        # Step 3: 配置视图内容
        cell_view.setStringValue_(data)
        
        return cell_view
```

### 3. 视图复用机制
这是NSTableView性能的关键：
- 使用 `makeViewWithIdentifier_owner_` 从复用队列获取视图
- 为每种单元格类型设置唯一的identifier
- 无论视图是复用的还是新创建的，都要重新配置数据

### 4. 排序功能
```python
# 创建列时设置排序描述符
sort_descriptor = NSSortDescriptor.alloc().initWithKey_ascending_(key, True)
column.setSortDescriptorPrototype_(sort_descriptor)

# 在代理中处理排序变化
def tableView_sortDescriptorsDidChange_(self, tableView, oldDescriptors):
    # 对数据进行排序
    # 调用tableView.reloadData()刷新显示
```

## 测试运行

```bash
# 运行简单示例（推荐开始）
python3 simple_pure_tableview.py

# 运行高级示例（功能完整）
python3 advanced_pure_tableview_simple.py

# 复杂版本（有问题，仅作参考）
python3 advanced_pure_tableview.py
```

### 操作说明
- 所有应用都支持 **Cmd+Q** 退出
- 窗口可以正常关闭、最小化、调整大小
- 应用会出现在Dock栏并获得前台焦点
- 点击列标题进行排序（高级版本）
- 使用按钮进行数据操作（高级版本）

## 验证结果

通过这些纯PyObjC + 最佳实践实现，我们验证了：

1. **NSTableView本身是稳定的** - 没有出现任何系统级崩溃
2. **关键在于正确实现协议** - 数据源和代理的正确实现是核心
3. **视图复用是性能关键** - 必须使用`makeViewWithIdentifier_owner_`
4. **View-Based模式是现代标准** - 不应使用已废弃的Cell-Based模式
5. **PyObjC最佳实践至关重要** - 激活策略、菜单栏、AppHelper、分离架构缺一不可
6. **强引用链防止对象回收** - AppDelegate → WindowController → 所有UI对象

## 与macUI封装的对比

这些纯PyObjC实现帮助我们理解：
- macUI的TableView封装在哪些地方可能存在问题
- 正确的NSTableView使用模式应该是什么样的
- 如何在保持简洁API的同时正确实现底层协议

## 总结

NSTableView的核心设计原则：
1. **分离关注点** - 视图不拥有数据，通过协议请求
2. **性能优化** - 视图复用机制是必须的
3. **灵活性** - View-Based模式提供最大的自定义能力
4. **稳定性** - 按照Apple的设计模式实现，组件本身极其稳定

这些示例为修复macUI的TableView实现提供了可靠的参考基础。