"""UI Components for macUI v2"""

# Export basic control components
from .basic_controls import Button, Label, TextField, LineBreakMode, LabelStyle

# Export input control components  
from .input_controls import Slider, Switch, Checkbox, RadioButton, SegmentedControl

# Export selection control components
from .selection_controls import PopUpButton, ComboBox, Menu, ContextMenu

# Export display control components
from .display_controls import ImageView, ProgressBar, TextArea

# Export picker control components
from .picker_controls import DatePicker, TimePicker

# Export layout components (traditional implementations)
from .layout import (
    HStack, OutlineView, ResponsiveStack, ScrollView, SplitView, TableView, TabView, VStack, ZStack
)

# Export modern layout components (recommended)
from .modern_layout import (
    ModernVStack, ModernHStack,
    VStack as ModernVStackCompat, HStack as ModernHStackCompat,  # Modern implementations with compatibility names
    CenteredVStack, CenteredHStack, FlexVStack, FlexHStack
)

__all__ = [
    # Control components
    "Button",
    "TextField",
    "TextArea", 
    "Label",
    "LineBreakMode",
    "LabelStyle",
    "Slider",
    "ProgressBar",
    "Checkbox",
    "RadioButton",
    "Switch",
    "SegmentedControl",
    "PopUpButton",
    "ComboBox",
    "Menu",
    "ContextMenu",
    "DatePicker",
    "TimePicker",
    "ImageView",

    # Layout components (traditional)
    "VStack",
    "HStack", 
    "ZStack",
    "ScrollView",
    "ResponsiveStack",
    "TabView",
    "SplitView",
    "TableView",
    "OutlineView",
    
    # Modern layout components (recommended)
    "ModernVStack",
    "ModernHStack",
    "ModernVStackCompat",
    "ModernHStackCompat", 
    "CenteredVStack",
    "CenteredHStack",
    "FlexVStack", 
    "FlexHStack",
]
