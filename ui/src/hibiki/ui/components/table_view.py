#!/usr/bin/env python3
"""
Hibiki UI v4.0 TableView组件
基于NSTableView的表格组件实现
"""

from typing import Optional, Union, Callable, Any, List, Dict
from AppKit import (
    NSView,
    NSTableView,
    NSTableColumn,
    NSScrollView,
    NSRect,
    NSMakeRect,
    NSTableViewColumnAutoresizingStyle,
)
from Foundation import NSObject

# 导入核心架构
from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect
from ..core.logging import get_logger

# 导入objc
import objc

logger = get_logger("components.table_view")
logger.setLevel("INFO")


# ================================
# FlippedScrollView - 坐标系修复
# ================================

class FlippedScrollView(NSScrollView):
    """坐标系修复的NSScrollView
    
    确保TableView的滚动视图使用top-left坐标系，
    与框架的布局引擎保持一致。
    """
    
    def isFlipped(self) -> bool:
        """启用top-left坐标系"""
        return True


# ================================
# TableView 数据源和委托类
# ================================

class TableViewDataSource(NSObject):
    """TableView数据源类 - 处理数据显示"""
    
    def init(self):
        self = objc.super(TableViewDataSource, self).init()
        if self is None:
            return None
        self.data = []
        self.columns = []
        self.table_component = None
        return self
    
    # NSTableViewDataSource 必需方法
    def numberOfRowsInTableView_(self, table_view):
        """返回表格行数"""
        return len(self.data)
    
    def tableView_objectValueForTableColumn_row_(self, table_view, table_column, row):
        """返回指定单元格的值"""
        try:
            if row >= len(self.data):
                return ""
            
            column_id = table_column.identifier()
            row_data = self.data[row]
            
            # 支持字典和列表两种数据格式
            if isinstance(row_data, dict):
                return str(row_data.get(column_id, ""))
            elif isinstance(row_data, (list, tuple)):
                try:
                    col_index = int(column_id) if column_id.isdigit() else 0
                    return str(row_data[col_index] if col_index < len(row_data) else "")
                except (ValueError, IndexError):
                    return ""
            else:
                return str(row_data)
        except Exception as e:
            logger.error(f"⚠️ TableView数据获取错误: {e}")
            return ""
    
    def tableView_setObjectValue_forTableColumn_row_(self, table_view, value, table_column, row):
        """设置指定单元格的值（可编辑时）"""
        try:
            if row >= len(self.data):
                return
            
            column_id = table_column.identifier()
            
            # 更新数据
            if isinstance(self.data[row], dict):
                self.data[row][column_id] = value
            elif isinstance(self.data[row], list):
                try:
                    col_index = int(column_id) if column_id.isdigit() else 0
                    if col_index < len(self.data[row]):
                        self.data[row][col_index] = value
                except (ValueError, IndexError):
                    pass
            
            # 通知组件数据已更改
            if hasattr(self, "table_component") and self.table_component:
                if hasattr(self.table_component, "_on_data_change"):
                    self.table_component._on_data_change(row, column_id, value)
            
            logger.debug(f"📝 TableView数据更新: row={row}, col={column_id}, value={value}")
        except Exception as e:
            logger.error(f"⚠️ TableView数据设置错误: {e}")


class TableViewDelegate(NSObject):
    """TableView委托类 - 处理用户交互"""
    
    def init(self):
        self = objc.super(TableViewDelegate, self).init()
        if self is None:
            return None
        self.table_component = None
        return self
    
    # 选择变化事件
    def tableViewSelectionDidChange_(self, notification):
        """表格选择变化事件处理"""
        if hasattr(self, "table_component") and self.table_component:
            try:
                table_view = notification.object()
                selected_row = table_view.selectedRow()
                
                # 更新组件的选中状态
                if hasattr(self.table_component, "_selected_row"):
                    if hasattr(self.table_component._selected_row, "value"):
                        self.table_component._selected_row.value = selected_row
                    else:
                        self.table_component._selected_row = selected_row
                
                # 调用选择回调
                if hasattr(self.table_component, "on_selection_change") and self.table_component.on_selection_change:
                    self.table_component.on_selection_change(selected_row)
                
                logger.debug(f"📊 TableView选择变化: row={selected_row}")
            except Exception as e:
                logger.error(f"⚠️ TableView选择回调错误: {e}")
    
    # 双击事件
    def tableView_shouldSelectRow_(self, table_view, row):
        """是否允许选择指定行"""
        return True
        
    # 鼠标事件处理
    def tableViewDoubleClick_(self, table_view):
        """双击事件处理"""
        if hasattr(self, "table_component") and self.table_component:
            try:
                clicked_row = table_view.clickedRow()
                if clicked_row >= 0 and hasattr(self.table_component, "on_double_click") and self.table_component.on_double_click:
                    self.table_component.on_double_click(clicked_row)
                    logger.debug(f"📊 TableView双击: row={clicked_row}")
            except Exception as e:
                logger.error(f"⚠️ TableView双击回调错误: {e}")
    
    # 可编辑性控制
    def tableView_shouldEditTableColumn_row_(self, table_view, table_column, row):
        """是否允许编辑指定单元格"""
        if hasattr(self, "table_component") and self.table_component:
            return getattr(self.table_component, "editable", True)
        return True


# ================================
# 列定义类
# ================================

class TableColumn:
    """表格列定义"""
    
    def __init__(
        self,
        identifier: str,
        title: str,
        width: Optional[float] = None,
        min_width: Optional[float] = None,
        max_width: Optional[float] = None,
        resizable: bool = True,
        sortable: bool = False,
        editable: bool = True,
    ):
        """初始化表格列
        
        Args:
            identifier: 列标识符（用于数据映射）
            title: 列标题
            width: 列宽度
            min_width: 最小宽度
            max_width: 最大宽度
            resizable: 是否可调整大小
            sortable: 是否可排序
            editable: 是否可编辑
        """
        self.identifier = identifier
        self.title = title
        self.width = width or 100.0
        self.min_width = min_width or 50.0
        self.max_width = max_width or 500.0
        self.resizable = resizable
        self.sortable = sortable
        self.editable = editable
    
    def to_ns_table_column(self) -> NSTableColumn:
        """转换为NSTableColumn"""
        column = NSTableColumn.alloc().initWithIdentifier_(self.identifier)
        column.headerCell().setStringValue_(self.title)
        column.setWidth_(self.width)
        column.setMinWidth_(self.min_width)
        column.setMaxWidth_(self.max_width)
        column.setResizingMask_(1 if self.resizable else 0)  # NSTableColumnAutoresizingMask
        column.setEditable_(self.editable)
        
        return column


# ================================
# TableView 主组件类
# ================================

class TableView(UIComponent):
    """现代化TableView表格组件
    
    基于Hibiki UI v4.0新架构的表格组件。
    支持完整的布局API、响应式数据绑定和用户交互。
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 响应式数据绑定
    - 多列显示和自定义列配置
    - 行选择和双击事件
    - 可编辑单元格支持
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        data: Union[List[Dict], List[List], Any] = None,
        columns: Optional[List[TableColumn]] = None,
        column_titles: Optional[List[str]] = None,
        style: Optional[ComponentStyle] = None,
        editable: bool = False,
        allows_multiple_selection: bool = False,
        on_selection_change: Optional[Callable[[int], None]] = None,
        on_double_click: Optional[Callable[[int], None]] = None,
        on_data_change: Optional[Callable[[int, str, Any], None]] = None,
        **style_kwargs,
    ):
        """🏗️ CORE METHOD: TableView component initialization
        
        Args:
            data: 表格数据，支持字典列表、嵌套列表或Signal
            columns: 列定义列表
            column_titles: 简单列标题列表（当未提供columns时使用）
            style: 组件样式对象
            editable: 是否允许编辑单元格
            allows_multiple_selection: 是否允许多选
            on_selection_change: 选择变化回调函数
            on_double_click: 双击行回调函数
            on_data_change: 数据变化回调函数
            **style_kwargs: 样式快捷参数
        """
        # 确保有合适的默认尺寸
        if style is None:
            from ..core.styles import px
            style = ComponentStyle(width=px(400), height=px(300))
        
        super().__init__(style, **style_kwargs)
        
        # 数据处理
        self.data = data or []
        self._is_reactive_data = isinstance(data, (Signal, Computed))
        
        # 列配置
        if columns:
            self.columns = columns
        elif column_titles:
            self.columns = [
                TableColumn(identifier=str(i), title=title)
                for i, title in enumerate(column_titles)
            ]
        else:
            # 自动生成列（基于第一行数据）
            self.columns = self._auto_generate_columns()
        
        # 配置参数
        self.editable = editable
        self.allows_multiple_selection = allows_multiple_selection
        
        # 事件回调
        self.on_selection_change = on_selection_change
        self.on_double_click = on_double_click
        self._on_data_change = on_data_change
        
        # 选中状态
        self._selected_row = -1  # -1表示未选中
        
        # 内部组件引用
        self._table_view = None
        self._scroll_view = None
        self._data_source = None
        self._delegate = None
        self._bindings = []
        
        logger.debug(
            f"📊 TableView创建: rows={len(self.data) if not self._is_reactive_data else '响应式'}, "
            f"cols={len(self.columns)}, editable={editable}"
        )
    
    def _auto_generate_columns(self) -> List[TableColumn]:
        """自动生成列定义"""
        columns = []
        
        if not self.data:
            return columns
        
        # 获取实际数据（处理响应式数据）
        actual_data = self.data
        if self._is_reactive_data and hasattr(self.data, "value"):
            actual_data = self.data.value
        
        if not actual_data:
            return columns
        
        first_row = actual_data[0]
        
        if isinstance(first_row, dict):
            # 字典格式：使用键作为列标识和标题
            for key in first_row.keys():
                columns.append(TableColumn(identifier=key, title=str(key)))
        elif isinstance(first_row, (list, tuple)):
            # 列表格式：生成Column 0, Column 1等
            for i in range(len(first_row)):
                columns.append(TableColumn(identifier=str(i), title=f"Column {i}"))
        else:
            # 其他格式：单列显示
            columns.append(TableColumn(identifier="0", title="Value"))
        
        return columns
    
    def _create_nsview(self) -> NSView:
        """🔧 修复坐标系Bug：使用FlippedScrollView确保top-left坐标系"""
        
        # 创建flipped滚动视图容器（确保坐标系一致性）
        scroll_view = FlippedScrollView.alloc().initWithFrame_(
            NSMakeRect(0, 0, 400, 300)
        )
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setHasHorizontalScroller_(True)
        scroll_view.setAutohidesScrollers_(False)
        scroll_view.setBorderType_(1)  # NSBezelBorder
        
        # 创建表格视图
        table_view = NSTableView.alloc().init()
        table_view.setUsesAlternatingRowBackgroundColors_(True)
        table_view.setAllowsMultipleSelection_(self.allows_multiple_selection)
        table_view.setAllowsColumnSelection_(False)
        table_view.setAllowsEmptySelection_(True)
        
        # 设置表格视图尺寸模式
        table_view.setColumnAutoresizingStyle_(1)  # NSTableViewUniformColumnAutoresizingStyle
        
        # 设置行高
        table_view.setRowHeight_(20.0)
        
        # 添加列
        for column_def in self.columns:
            ns_column = column_def.to_ns_table_column()
            table_view.addTableColumn_(ns_column)
        
        # 创建数据源
        self._data_source = TableViewDataSource.alloc().init()
        self._data_source.table_component = self
        self._data_source.columns = self.columns
        self._update_data_source()
        table_view.setDataSource_(self._data_source)
        
        # 创建委托
        self._delegate = TableViewDelegate.alloc().init()
        self._delegate.table_component = self
        table_view.setDelegate_(self._delegate)
        
        # 设置双击事件
        if self.on_double_click:
            table_view.setTarget_(self._delegate)
            table_view.setDoubleAction_("tableViewDoubleClick:")
        
        # 将表格视图添加到滚动视图
        scroll_view.setDocumentView_(table_view)
        
        # 保存引用
        self._table_view = table_view
        self._scroll_view = scroll_view
        
        # 建立响应式绑定
        if self._is_reactive_data:
            self._bind_reactive_data()
        
        logger.info(f"📊 TableView NSView创建完成: {len(self.columns)}列, {len(self._data_source.data)}行数据")
        logger.info(f"📊 表格列标识: {[col.identifier for col in self.columns]}")
        logger.info(f"📊 数据样本: {self._data_source.data[:2] if self._data_source.data else '无数据'}")
        
        return scroll_view
    
    def _update_data_source(self):
        """更新数据源数据"""
        if self._data_source:
            # 获取实际数据
            actual_data = self.data
            if self._is_reactive_data and hasattr(self.data, "value"):
                actual_data = self.data.value
            
            self._data_source.data = actual_data or []
    
    def _bind_reactive_data(self):
        """建立响应式数据绑定"""
        if not hasattr(self.data, "value"):
            return
        
        def update_data():
            if self._table_view and self._data_source:
                self._update_data_source()
                
                # 如果列结构发生变化，重新生成列
                if not self.columns or (hasattr(self.data, "value") and self.data.value):
                    new_columns = self._auto_generate_columns()
                    if len(new_columns) != len(self.columns):
                        self._rebuild_columns(new_columns)
                
                # 刷新表格显示
                self._table_view.reloadData()
                logger.debug(f"📊 TableView响应式数据更新: {len(self._data_source.data)}行")
        
        # 使用Effect建立响应式绑定
        effect = Effect(update_data)
        self._bindings.append(effect)
    
    def _rebuild_columns(self, new_columns: List[TableColumn]):
        """重建表格列"""
        if not self._table_view:
            return
        
        # 移除现有列
        for column in list(self._table_view.tableColumns()):
            self._table_view.removeTableColumn_(column)
        
        # 添加新列
        self.columns = new_columns
        for column_def in self.columns:
            ns_column = column_def.to_ns_table_column()
            self._table_view.addTableColumn_(ns_column)
        
        # 更新数据源列信息
        if self._data_source:
            self._data_source.columns = self.columns
    
    
    # ================================
    # 公共API方法
    # ================================
    
    def get_selected_row(self) -> int:
        """获取当前选中行"""
        if self._table_view:
            return self._table_view.selectedRow()
        return self._selected_row
    
    def set_selected_row(self, row: int) -> "TableView":
        """设置选中行
        
        Args:
            row: 要选中的行索引，-1表示清除选择
        """
        if self._table_view:
            if row >= 0:
                self._table_view.selectRowIndexes_byExtendingSelection_(
                    {row}, False
                )
            else:
                self._table_view.deselectAll_(None)
        
        self._selected_row = row
        logger.debug(f"📊 TableView选择设置: row={row}")
        return self
    
    def get_data(self) -> List:
        """获取当前数据"""
        if self._is_reactive_data and hasattr(self.data, "value"):
            return self.data.value
        return self.data
    
    def set_data(self, data: Union[List[Dict], List[List], Any]) -> "TableView":
        """设置表格数据
        
        Args:
            data: 新的表格数据
        """
        self.data = data
        self._is_reactive_data = isinstance(data, (Signal, Computed))
        
        if self._table_view:
            self._update_data_source()
            
            # 重新生成列（如果需要）
            if not self.columns:
                new_columns = self._auto_generate_columns()
                if new_columns:
                    self._rebuild_columns(new_columns)
            
            self._table_view.reloadData()
            logger.debug(f"📊 TableView数据更新: {len(self.get_data())}行")
        
        return self
    
    def add_row(self, row_data: Union[Dict, List]) -> "TableView":
        """添加新行
        
        Args:
            row_data: 行数据
        """
        if self._is_reactive_data:
            if hasattr(self.data, "value"):
                current_data = list(self.data.value)
                current_data.append(row_data)
                self.data.value = current_data
        else:
            if isinstance(self.data, list):
                self.data.append(row_data)
                if self._table_view:
                    self._update_data_source()
                    self._table_view.reloadData()
        
        logger.debug(f"📊 TableView添加行: {row_data}")
        return self
    
    def remove_row(self, row_index: int) -> "TableView":
        """删除指定行
        
        Args:
            row_index: 要删除的行索引
        """
        if self._is_reactive_data:
            if hasattr(self.data, "value") and 0 <= row_index < len(self.data.value):
                current_data = list(self.data.value)
                removed = current_data.pop(row_index)
                self.data.value = current_data
                logger.debug(f"📊 TableView删除行: {row_index} -> {removed}")
        else:
            if isinstance(self.data, list) and 0 <= row_index < len(self.data):
                removed = self.data.pop(row_index)
                if self._table_view:
                    self._update_data_source()
                    self._table_view.reloadData()
                logger.debug(f"📊 TableView删除行: {row_index} -> {removed}")
        
        return self
    
    def reload_data(self) -> "TableView":
        """刷新表格数据显示"""
        if self._table_view:
            self._update_data_source()
            self._table_view.reloadData()
            logger.debug(f"📊 TableView数据刷新")
        return self
    
    def cleanup(self):
        """组件清理"""
        for binding in self._bindings:
            if hasattr(binding, "cleanup"):
                binding.cleanup()
        self._bindings.clear()
        super().cleanup()


# ================================
# 使用示例和测试
# ================================

if __name__ == "__main__":
    logger.debug("Hibiki UI v4.0 TableView组件测试\n")
    
    # 测试数据
    sample_data = [
        {"name": "张三", "age": 25, "city": "北京"},
        {"name": "李四", "age": 30, "city": "上海"},
        {"name": "王五", "age": 28, "city": "深圳"},
    ]
    
    # 创建列定义
    columns = [
        TableColumn("name", "姓名", width=100),
        TableColumn("age", "年龄", width=80),
        TableColumn("city", "城市", width=120),
    ]
    
    logger.debug("🧪 TableView创建测试:")
    
    # 创建TableView
    def on_selection(row):
        logger.debug(f"🎯 选中行: {row}")
    
    def on_double_click(row):
        logger.debug(f"🖱️ 双击行: {row}")
    
    table_view = TableView(
        data=sample_data,
        columns=columns,
        on_selection_change=on_selection,
        on_double_click=on_double_click,
    )
    
    logger.debug(f"TableView创建完成: {table_view.__class__.__name__}")
    logger.debug(f"数据行数: {len(table_view.get_data())}")
    logger.debug(f"列数: {len(table_view.columns)}")
    
    logger.info("\n✅ TableView组件测试完成！")