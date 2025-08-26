#!/usr/bin/env python3
"""
全局对象注册表 - 强制防止关键对象被垃圾回收
"""

import weakref
from threading import Lock
from typing import Dict, Set, Any, List
import gc


class GlobalObjectRegistry:
    """全局对象注册表 - 确保关键对象永不被垃圾回收"""
    
    def __init__(self):
        self._lock = Lock()
        self._strong_refs: Dict[str, List[Any]] = {}
        self._object_map: Dict[int, str] = {}
        self._categories: Set[str] = set()
        
    def register_critical_object(self, obj: Any, category: str = "default", identifier: str = None) -> str:
        """注册关键对象，确保它永不被垃圾回收
        
        Args:
            obj: 要保护的对象
            category: 对象分类 (如 "table_data_source", "delegates" 等)
            identifier: 可选的标识符
            
        Returns:
            对象的唯一标识符
        """
        with self._lock:
            obj_id = id(obj)
            key = f"{category}_{obj_id}"
            if identifier:
                key = f"{category}_{identifier}_{obj_id}"
            
            # 如果分类不存在，创建它
            if category not in self._strong_refs:
                self._strong_refs[category] = []
                self._categories.add(category)
            
            # 添加强引用
            self._strong_refs[category].append(obj)
            self._object_map[obj_id] = key
            
            print(f"🔒 注册关键对象: {key} (type: {type(obj).__name__})")
            
            # 如果是 NSObject，显示引用计数
            if hasattr(obj, 'retainCount'):
                try:
                    count = obj.retainCount()
                    print(f"   引用计数: {count}")
                except:
                    pass
            
            return key
    
    def unregister_object(self, obj_or_key: Any) -> bool:
        """取消注册对象（谨慎使用）"""
        with self._lock:
            if isinstance(obj_or_key, str):
                # 按键查找
                key = obj_or_key
                for category, objects in self._strong_refs.items():
                    for i, obj in enumerate(objects):
                        if self._object_map.get(id(obj)) == key:
                            del objects[i]
                            del self._object_map[id(obj)]
                            print(f"🔓 取消注册对象: {key}")
                            return True
            else:
                # 按对象查找
                obj = obj_or_key
                obj_id = id(obj)
                if obj_id in self._object_map:
                    key = self._object_map[obj_id]
                    for category, objects in self._strong_refs.items():
                        if obj in objects:
                            objects.remove(obj)
                            del self._object_map[obj_id]
                            print(f"🔓 取消注册对象: {key}")
                            return True
            
            return False
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """获取注册表统计信息"""
        with self._lock:
            stats = {
                'categories': list(self._categories),
                'total_objects': sum(len(objects) for objects in self._strong_refs.values()),
                'by_category': {
                    category: len(objects) 
                    for category, objects in self._strong_refs.items()
                }
            }
            return stats
    
    def force_retain_all(self):
        """强制保持所有已注册对象的引用"""
        with self._lock:
            total = 0
            for category, objects in self._strong_refs.items():
                count = len(objects)
                total += count
                print(f"🔒 分类 '{category}': {count} 个对象")
            
            print(f"🔒 总计保护 {total} 个对象")
    
    def check_object_status(self):
        """检查所有注册对象的状态"""
        with self._lock:
            print("\n=== 对象注册表状态检查 ===")
            
            for category, objects in self._strong_refs.items():
                print(f"\n📂 分类: {category} ({len(objects)} 个对象)")
                
                for i, obj in enumerate(objects):
                    try:
                        obj_type = type(obj).__name__
                        obj_id = id(obj)
                        key = self._object_map.get(obj_id, "未知")
                        
                        status = "✅ 有效"
                        if hasattr(obj, 'retainCount'):
                            try:
                                count = obj.retainCount()
                                status += f" (引用计数: {count})"
                            except:
                                status = "⚠️ 引用计数获取失败"
                        
                        print(f"  {i+1}. {key}: {obj_type} - {status}")
                        
                    except Exception as e:
                        print(f"  {i+1}. 对象检查失败: {e}")
    
    def clear_category(self, category: str):
        """清空指定分类的所有对象"""
        with self._lock:
            if category in self._strong_refs:
                count = len(self._strong_refs[category])
                # 清理对象映射
                for obj in self._strong_refs[category]:
                    obj_id = id(obj)
                    if obj_id in self._object_map:
                        del self._object_map[obj_id]
                
                self._strong_refs[category].clear()
                print(f"🧹 清空分类 '{category}': {count} 个对象")
    
    def clear_all(self):
        """清空所有注册的对象（危险操作）"""
        with self._lock:
            total = sum(len(objects) for objects in self._strong_refs.values())
            self._strong_refs.clear()
            self._object_map.clear()
            self._categories.clear()
            print(f"🧹 清空所有注册对象: {total} 个")


# 全局注册表实例
global_registry = GlobalObjectRegistry()


def register_table_data_source(data_source: Any, table_view: Any = None) -> str:
    """注册表格数据源对象"""
    key = global_registry.register_critical_object(
        data_source, 
        "table_data_source", 
        f"datasource_{id(table_view) if table_view else 'unknown'}"
    )
    
    # 如果有表格视图，也注册它
    if table_view:
        global_registry.register_critical_object(
            table_view,
            "table_view",
            f"tableview_{id(table_view)}"
        )
    
    return key


def register_delegate(delegate: Any, component_type: str, component: Any = None) -> str:
    """注册委托对象"""
    identifier = f"{component_type}_{id(component) if component else 'unknown'}"
    return global_registry.register_critical_object(
        delegate,
        "delegates",
        identifier
    )


def register_effect(effect: Any, component: Any = None) -> str:
    """注册 Effect 对象"""
    identifier = f"effect_{id(component) if component else 'unknown'}"
    return global_registry.register_critical_object(
        effect,
        "effects",
        identifier
    )


def get_registry_stats() -> Dict[str, Any]:
    """获取注册表统计信息"""
    return global_registry.get_registry_stats()


def check_all_objects():
    """检查所有注册对象的状态"""
    global_registry.check_object_status()


def force_retain_everything():
    """强制保持所有对象"""
    global_registry.force_retain_all()
    
    # 额外的保护措施：禁用垃圾回收
    gc.disable()
    print("🛡️ 垃圾回收已禁用")


def enable_gc_with_protection():
    """重新启用垃圾回收，但保持对象保护"""
    gc.enable()
    global_registry.force_retain_all()
    print("🔄 垃圾回收已重新启用，对象保护仍然有效")