"""PyObjC Mock 系统

用于单元测试，完全模拟 PyObjC 的行为，不依赖真实的 macOS 环境。
包含所有 AppKit 和 Foundation 类的 Mock 实现。
"""

from typing import Any, Callable, Dict, List, Optional
from unittest.mock import MagicMock, Mock
import weakref


class MockNSObject:
    """NSObject 的基础 Mock 类"""
    
    def __init__(self, *args, **kwargs):
        self._mock_id = id(self)
        self._mock_properties = {}
        self._mock_associated_objects = {}
        self._mock_method_calls = []
    
    def init(self):
        return self
    
    def alloc(self):
        return self.__class__()
    
    @classmethod
    def new(cls):
        return cls().init()


class MockNSView(MockNSObject):
    """NSView Mock 类"""
    
    def __init__(self):
        super().__init__()
        self._subviews = []
        self._superview = None
        self._frame = (0, 0, 100, 100)  # (x, y, width, height)
        self._hidden = False
        self._alpha = 1.0
        
    def addSubview_(self, subview):
        self._subviews.append(subview)
        subview._superview = self
        self._mock_method_calls.append(('addSubview_', subview))
        
    def removeFromSuperview(self):
        if self._superview:
            self._superview._subviews.remove(self)
            self._superview = None
        self._mock_method_calls.append(('removeFromSuperview',))
    
    def setFrame_(self, frame):
        self._frame = frame
        self._mock_method_calls.append(('setFrame_', frame))
    
    def frame(self):
        return self._frame
    
    def setHidden_(self, hidden):
        self._hidden = hidden
        self._mock_method_calls.append(('setHidden_', hidden))
    
    def isHidden(self):
        return self._hidden
    
    def setAlphaValue_(self, alpha):
        self._alpha = alpha
        self._mock_method_calls.append(('setAlphaValue_', alpha))
    
    def alphaValue(self):
        return self._alpha


class MockNSButton(MockNSView):
    """NSButton Mock 类"""
    
    def __init__(self):
        super().__init__()
        self._title = ""
        self._button_type = 0
        self._enabled = True
        self._target = None
        self._action = None
        self._tooltip = None
        
    def setTitle_(self, title):
        self._title = str(title)
        self._mock_method_calls.append(('setTitle_', title))
    
    def title(self):
        return self._title
    
    def setButtonType_(self, button_type):
        self._button_type = button_type
        self._mock_method_calls.append(('setButtonType_', button_type))
        
    def setEnabled_(self, enabled):
        self._enabled = bool(enabled)
        self._mock_method_calls.append(('setEnabled_', enabled))
    
    def isEnabled(self):
        return self._enabled
    
    def setTarget_(self, target):
        self._target = target
        self._mock_method_calls.append(('setTarget_', target))
    
    def target(self):
        return self._target
    
    def setAction_(self, action):
        self._action = action
        self._mock_method_calls.append(('setAction_', action))
    
    def action(self):
        return self._action
    
    def setToolTip_(self, tooltip):
        self._tooltip = str(tooltip) if tooltip else None
        self._mock_method_calls.append(('setToolTip_', tooltip))
    
    def toolTip(self):
        return self._tooltip
    
    def performClick_(self, sender):
        """模拟按钮点击"""
        if self._target and self._action and hasattr(self._target, self._action.rstrip(':')):
            method_name = self._action.rstrip(':') + '_'
            if hasattr(self._target, method_name):
                method = getattr(self._target, method_name)
                method(self)
        self._mock_method_calls.append(('performClick_', sender))


class MockNSTextField(MockNSView):
    """NSTextField Mock 类"""
    
    def __init__(self):
        super().__init__()
        self._string_value = ""
        self._placeholder = ""
        self._editable = True
        self._selectable = True
        self._bezeled = True
        self._draws_background = True
        self._delegate = None
        
    def setStringValue_(self, value):
        self._string_value = str(value)
        self._mock_method_calls.append(('setStringValue_', value))
    
    def stringValue(self):
        return self._string_value
    
    def setPlaceholderString_(self, placeholder):
        self._placeholder = str(placeholder)
        self._mock_method_calls.append(('setPlaceholderString_', placeholder))
    
    def setEditable_(self, editable):
        self._editable = bool(editable)
        self._mock_method_calls.append(('setEditable_', editable))
    
    def setSelectable_(self, selectable):
        self._selectable = bool(selectable)
        self._mock_method_calls.append(('setSelectable_', selectable))
    
    def setBezeled_(self, bezeled):
        self._bezeled = bool(bezeled)
        self._mock_method_calls.append(('setBezeled_', bezeled))
    
    def setDrawsBackground_(self, draws_background):
        self._draws_background = bool(draws_background)
        self._mock_method_calls.append(('setDrawsBackground_', draws_background))
    
    def setDelegate_(self, delegate):
        self._delegate = delegate
        self._mock_method_calls.append(('setDelegate_', delegate))


class MockNSApplication(MockNSObject):
    """NSApplication Mock 类"""
    
    _shared_application = None
    
    def __init__(self):
        super().__init__()
        self._delegate = None
        self._activation_policy = None
        self._main_menu = None
        
    @classmethod
    def sharedApplication(cls):
        if cls._shared_application is None:
            cls._shared_application = cls()
        return cls._shared_application
    
    def setDelegate_(self, delegate):
        self._delegate = delegate
        self._mock_method_calls.append(('setDelegate_', delegate))
    
    def setActivationPolicy_(self, policy):
        self._activation_policy = policy
        self._mock_method_calls.append(('setActivationPolicy_', policy))
    
    def setMainMenu_(self, menu):
        self._main_menu = menu
        self._mock_method_calls.append(('setMainMenu_', menu))
    
    def run(self):
        self._mock_method_calls.append(('run',))
    
    def terminate_(self, sender):
        self._mock_method_calls.append(('terminate_', sender))


class MockNSWindow(MockNSObject):
    """NSWindow Mock 类"""
    
    def __init__(self):
        super().__init__()
        self._title = ""
        self._content_view = None
        self._frame = (0, 0, 800, 600)
        self._delegate = None
        self._visible = False
        
    def initWithContentRect_styleMask_backing_defer_(self, rect, style_mask, backing, defer):
        self._frame = rect
        return self
    
    def setTitle_(self, title):
        self._title = str(title)
        self._mock_method_calls.append(('setTitle_', title))
    
    def title(self):
        return self._title
    
    def setContentView_(self, view):
        self._content_view = view
        self._mock_method_calls.append(('setContentView_', view))
    
    def contentView(self):
        return self._content_view or MockNSView()
    
    def setFrame_display_(self, frame, display):
        self._frame = frame
        self._mock_method_calls.append(('setFrame_display_', frame, display))
    
    def frame(self):
        return self._frame
    
    def makeKeyAndOrderFront_(self, sender):
        self._visible = True
        self._mock_method_calls.append(('makeKeyAndOrderFront_', sender))
    
    def orderOut_(self, sender):
        self._visible = False
        self._mock_method_calls.append(('orderOut_', sender))
    
    def close(self):
        self._visible = False
        self._mock_method_calls.append(('close',))
    
    def center(self):
        self._mock_method_calls.append(('center',))
    
    def setDelegate_(self, delegate):
        self._delegate = delegate
        self._mock_method_calls.append(('setDelegate_', delegate))


class MockFoundation:
    """Foundation 框架 Mock"""
    
    @staticmethod
    def NSMakeRect(x, y, width, height):
        return (x, y, width, height)
    
    @staticmethod
    def NSEdgeInsets(top, left, bottom, right):
        return {'top': top, 'left': left, 'bottom': bottom, 'right': right}


class MockObjC:
    """objc 模块 Mock"""
    
    _associated_objects = weakref.WeakKeyDictionary()
    
    @staticmethod
    def setAssociatedObject(obj, key, value, policy):
        """模拟 objc.setAssociatedObject"""
        if obj not in MockObjC._associated_objects:
            MockObjC._associated_objects[obj] = {}
        MockObjC._associated_objects[obj][key] = value
    
    @staticmethod
    def getAssociatedObject(obj, key):
        """模拟 objc.getAssociatedObject"""
        if obj in MockObjC._associated_objects:
            return MockObjC._associated_objects[obj].get(key)
        return None
    
    # objc 常量
    OBJC_ASSOCIATION_RETAIN = 1
    OBJC_ASSOCIATION_COPY = 3


# Mock 常量
NSButtonTypeMomentaryPushIn = 0
NSTextFieldRoundedBezel = 1
NSApplicationActivationPolicyRegular = 0
NSBackingStoreBuffered = 2
NSWindowStyleMaskTitled = 1
NSWindowStyleMaskClosable = 2
NSWindowStyleMaskMiniaturizable = 4
NSWindowStyleMaskResizable = 8


def setup_mock_pyobjc():
    """设置完整的 PyObjC Mock 环境"""
    import sys
    from unittest.mock import MagicMock
    
    # Mock AppKit 模块
    mock_appkit = MagicMock()
    mock_appkit.NSView = MockNSView
    mock_appkit.NSButton = MockNSButton
    mock_appkit.NSTextField = MockNSTextField
    mock_appkit.NSApplication = MockNSApplication
    mock_appkit.NSWindow = MockNSWindow
    mock_appkit.NSButtonTypeMomentaryPushIn = NSButtonTypeMomentaryPushIn
    mock_appkit.NSTextFieldRoundedBezel = NSTextFieldRoundedBezel
    mock_appkit.NSApplicationActivationPolicyRegular = NSApplicationActivationPolicyRegular
    mock_appkit.NSBackingStoreBuffered = NSBackingStoreBuffered
    mock_appkit.NSWindowStyleMaskTitled = NSWindowStyleMaskTitled
    mock_appkit.NSWindowStyleMaskClosable = NSWindowStyleMaskClosable
    mock_appkit.NSWindowStyleMaskMiniaturizable = NSWindowStyleMaskMiniaturizable
    mock_appkit.NSWindowStyleMaskResizable = NSWindowStyleMaskResizable
    
    # Mock Foundation 模块
    mock_foundation = MagicMock()
    mock_foundation.NSMakeRect = MockFoundation.NSMakeRect
    mock_foundation.NSEdgeInsets = MockFoundation.NSEdgeInsets
    mock_foundation.NSObject = MockNSObject
    
    # Mock objc 模块
    mock_objc = MagicMock()
    mock_objc.setAssociatedObject = MockObjC.setAssociatedObject
    mock_objc.getAssociatedObject = MockObjC.getAssociatedObject
    mock_objc.OBJC_ASSOCIATION_RETAIN = MockObjC.OBJC_ASSOCIATION_RETAIN
    mock_objc.OBJC_ASSOCIATION_COPY = MockObjC.OBJC_ASSOCIATION_COPY
    
    # 注册到 sys.modules
    sys.modules['AppKit'] = mock_appkit
    sys.modules['Foundation'] = mock_foundation
    sys.modules['objc'] = mock_objc
    
    return mock_appkit, mock_foundation, mock_objc


def reset_mock_pyobjc():
    """重置 Mock 状态"""
    MockObjC._associated_objects.clear()
    MockNSApplication._shared_application = None


def get_mock_method_calls(mock_obj):
    """获取 Mock 对象的方法调用记录"""
    return getattr(mock_obj, '_mock_method_calls', [])


def assert_mock_method_called(mock_obj, method_name, *args):
    """断言 Mock 对象的方法被调用"""
    calls = get_mock_method_calls(mock_obj)
    for call in calls:
        if call[0] == method_name:
            if len(call) == 1 and len(args) == 0:
                return True
            elif len(call) > 1 and call[1:] == args:
                return True
    raise AssertionError(f"Method {method_name} was not called with args {args}. Actual calls: {calls}")


def assert_mock_method_not_called(mock_obj, method_name):
    """断言 Mock 对象的方法未被调用"""
    calls = get_mock_method_calls(mock_obj)
    for call in calls:
        if call[0] == method_name:
            raise AssertionError(f"Method {method_name} was called unexpectedly. Actual calls: {calls}")


def get_mock_property(mock_obj, property_name):
    """获取 Mock 对象的属性值"""
    return getattr(mock_obj, f'_{property_name}', None)


class MockNSSecureTextField(MockNSTextField):
    """NSSecureTextField Mock 类"""
    
    def __init__(self):
        super().__init__()
        self._secure = True


class MockReactiveBinding:
    """ReactiveBinding Mock 类"""
    
    call_history = []
    
    @classmethod
    def bind(cls, view, property_name, signal):
        cls.call_history.append(('bind', view, property_name, signal))
    
    @classmethod
    def reset(cls):
        cls.call_history.clear()


class MockTwoWayBinding:
    """TwoWayBinding Mock 类"""
    
    call_history = []
    
    @classmethod
    def bind(cls, view, property_name, signal):
        cls.call_history.append(('bind', view, property_name, signal))
    
    @classmethod
    def reset(cls):
        cls.call_history.clear()


class MockEventBinding:
    """EventBinding Mock 类"""
    
    call_history = []
    
    @classmethod
    def bind_click(cls, view, handler):
        cls.call_history.append(('bind_click', view, handler))
    
    @classmethod
    def reset(cls):
        cls.call_history.clear()


class MockEnhancedTextFieldDelegate(MockNSObject):
    """EnhancedTextFieldDelegate Mock 类"""
    
    def __init__(self):
        super().__init__()
        self.on_change = None
        self.on_enter = None