#!/usr/bin/env python3
"""
内存管理器 - 替代 objc.setAssociatedObject 的安全方案
"""

import weakref
from typing import Dict, Any, Set
from threading import Lock


class MemoryManager:
    """全局内存管理器 - 管理对象生命周期和引用关系"""
    
    def __init__(self):
        self._object_refs: Dict[int, Dict[str, Any]] = {}
        self._weak_refs: Dict[int, weakref.ref] = {}
        self._lock = Lock()
    
    def associate_object(self, owner: Any, key: str, associated_obj: Any):
        """关联对象到拥有者
        
        Args:
            owner: 拥有者对象
            key: 关联键
            associated_obj: 要关联的对象
        """
        owner_id = id(owner)
        
        with self._lock:
            # 如果这是第一次为这个拥有者关联对象
            if owner_id not in self._object_refs:
                self._object_refs[owner_id] = {}
                
                # 创建弱引用来监控拥有者的生命周期
                def cleanup_callback(ref):
                    self._cleanup_owner(owner_id)
                
                try:
                    weak_ref = weakref.ref(owner, cleanup_callback)
                    self._weak_refs[owner_id] = weak_ref
                except TypeError:
                    # 某些对象不支持弱引用
                    pass
            
            # 关联对象
            self._object_refs[owner_id][key] = associated_obj
    
    def get_associated_object(self, owner: Any, key: str) -> Any:
        """获取关联对象
        
        Args:
            owner: 拥有者对象
            key: 关联键
            
        Returns:
            关联的对象，如果不存在则返回 None
        """
        owner_id = id(owner)
        
        with self._lock:
            if owner_id in self._object_refs:
                return self._object_refs[owner_id].get(key)
            return None
    
    def remove_associated_object(self, owner: Any, key: str):
        """移除关联对象
        
        Args:
            owner: 拥有者对象
            key: 关联键
        """
        owner_id = id(owner)
        
        with self._lock:
            if owner_id in self._object_refs:
                self._object_refs[owner_id].pop(key, None)
                
                # 如果没有更多关联对象，清理拥有者记录
                if not self._object_refs[owner_id]:
                    self._cleanup_owner(owner_id)
    
    def _cleanup_owner(self, owner_id: int):
        """清理拥有者的所有关联对象"""
        if owner_id in self._object_refs:
            print(f"🗑️  清理内存管理器中的对象关联: owner_id={owner_id}")
            del self._object_refs[owner_id]
        
        if owner_id in self._weak_refs:
            del self._weak_refs[owner_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取内存管理统计信息"""
        with self._lock:
            return {
                "tracked_owners": len(self._object_refs),
                "total_associations": sum(len(refs) for refs in self._object_refs.values()),
                "weak_refs": len(self._weak_refs)
            }


# 全局内存管理器实例
memory_manager = MemoryManager()


def associate_object(owner, key: str, obj):
    """关联对象的便捷函数"""
    memory_manager.associate_object(owner, key, obj)


def get_associated_object(owner, key: str):
    """获取关联对象的便捷函数"""
    return memory_manager.get_associated_object(owner, key)


def remove_associated_object(owner, key: str):
    """移除关联对象的便捷函数"""
    memory_manager.remove_associated_object(owner, key)


def get_memory_stats():
    """获取内存统计信息的便捷函数"""
    return memory_manager.get_stats()