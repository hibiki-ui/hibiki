"""UI Components for macUI v3.0 - All Modern Components Based on Stretchable Layout Engine"""

# Export basic control components (Modern implementations)
from .basic_controls import Button, Label, TextField, LineBreakMode, LabelStyle

# Export input control components (Modern implementations)
from .input_controls import Slider, Switch, Checkbox, RadioButton, SegmentedControl

# Export selection control components (Modern implementations)
from .selection_controls import PopUpButton, ComboBox, Menu, ContextMenu

# Export display control components (Modern implementations with new TableView)
from .display_controls import ImageView, ProgressBar, TextArea
from .modern_display import ModernTableView, TableView  # Modern TableView

# Export picker control components (Modern implementations)
from .picker_controls import DatePicker, TimePicker

# Export Modern layout components (all based on Stretchable engine)
from .modern_layout import (
    ModernVStack, ModernHStack,
    CenteredVStack, CenteredHStack, FlexVStack, FlexHStack
)

# Export Modern control components (for explicit Modern usage)
from .modern_controls import ModernButton, ModernLabel, ModernTextField
from .modern_input import ModernSlider, ModernSwitch, ModernCheckbox, ModernSegmentedControl, ModernRadioButton
from .modern_display import ModernImageView, ModernProgressBar, ModernTextArea
from .modern_selection import ModernPopUpButton, ModernComboBox, ModernMenu
from .modern_time import ModernDatePicker, CalendarDatePicker

# Create compatibility aliases (VStack/HStack now point to Modern implementations)
VStack = ModernVStack
HStack = ModernHStack

__all__ = [
    # Basic control components
    "Button",
    "TextField", 
    "TextArea",
    "Label",
    "LineBreakMode",
    "LabelStyle",
    
    # Input control components
    "Slider",
    "Switch", 
    "Checkbox",
    "RadioButton",
    "SegmentedControl",
    
    # Selection control components
    "PopUpButton",
    "ComboBox",
    "Menu",
    "ContextMenu",
    
    # Display control components
    "ImageView",
    "ProgressBar",
    "TableView",  # Now points to ModernTableView
    
    # Time picker components
    "DatePicker",
    "TimePicker",
    
    # Layout components (all Modern/Stretchable-based)
    "VStack",         # -> ModernVStack
    "HStack",         # -> ModernHStack
    "ModernVStack",
    "ModernHStack", 
    "CenteredVStack",
    "CenteredHStack",
    "FlexVStack",
    "FlexHStack",
    
    # Explicit Modern components (for advanced usage)
    "ModernButton",
    "ModernLabel", 
    "ModernTextField",
    "ModernSlider",
    "ModernSwitch",
    "ModernCheckbox",
    "ModernRadioButton",
    "ModernSegmentedControl",
    "ModernImageView",
    "ModernProgressBar",
    "ModernTextArea",
    "ModernTableView",
    "ModernPopUpButton",
    "ModernComboBox",
    "ModernMenu",
    "ModernDatePicker",
    "CalendarDatePicker",
]