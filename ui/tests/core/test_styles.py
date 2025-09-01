"""
Tests for the Style System
==========================

Testing ComponentStyle, units, and responsive styles.
"""

import pytest
from unittest.mock import MagicMock, patch
from hibiki.ui.core.styles import (
    ComponentStyle,
    Display, FlexDirection, JustifyContent, AlignItems,
    px, percent, vw, vh,
    Length
)
from hibiki.ui.core.responsive import BreakpointName, responsive_style


class TestLengthUnits:
    """Test length unit creation functions."""
    
    def test_px_unit(self):
        """Test pixel unit creation."""
        unit = px(100)
        assert unit.value == 100
        assert unit.unit == "px"
        assert str(unit) == "100px"
    
    def test_percent_unit(self):
        """Test percentage unit creation."""
        unit = percent(50)
        assert unit.value == 50
        assert unit.unit == "%"
        assert str(unit) == "50%"
    
    def test_vw_unit(self):
        """Test viewport width unit creation."""
        unit = vw(75)
        assert unit.value == 75
        assert unit.unit == "vw"
        assert str(unit) == "75vw"
    
    def test_vh_unit(self):
        """Test viewport height unit creation."""
        unit = vh(100)
        assert unit.value == 100
        assert unit.unit == "vh"
        assert str(unit) == "100vh"
    
    # em, rem, pt units not yet implemented in styles module
    
    def test_length_unit_to_pixels(self):
        """Test converting units to pixels."""
        # Test with default viewport
        assert px(100).to_pixels() == 100
        assert percent(50).to_pixels(reference_value=200) == 100
        
        # vw/vh require viewport size
        assert vw(50).to_pixels(viewport_width=800) == 400
        assert vh(25).to_pixels(viewport_height=600) == 150
        
        # em/rem/pt units not yet implemented
    
    def test_length_unit_equality(self):
        """Test length unit equality comparison."""
        assert px(100) == px(100)
        assert px(100) != px(200)
        assert px(100) != percent(100)  # Different units
    
    def test_length_repr(self):
        """Test length string representation."""
        unit = px(42)
        assert str(unit) == "42px"


class TestComponentStyle:
    """Test the ComponentStyle class."""
    
    def test_style_initialization(self):
        """Test creating a component style."""
        style = ComponentStyle(
            display=Display.FLEX,
            width=100,
            height=200,
            padding=10
        )
        
        assert style.display == Display.FLEX
        assert style.width == 100
        assert style.height == 200
        assert style.padding == 10
    
    def test_style_with_units(self):
        """Test style with length units."""
        style = ComponentStyle(
            width=px(100),
            height=percent(50),
            margin=vw(5),
            padding=px(16)
        )
        
        assert style.width == px(100)
        assert style.height == percent(50)
        assert style.margin == vw(5)
        assert style.padding == px(16)
    
    def test_style_merge(self):
        """Test merging two styles."""
        base_style = ComponentStyle(
            width=100,
            height=200,
            background_color="#fff"
        )
        
        override_style = ComponentStyle(
            height=300,
            color="#000",
            padding=10
        )
        
        merged = base_style.merge(override_style)
        
        # Override values should take precedence
        assert merged.width == 100  # From base
        assert merged.height == 300  # Overridden
        assert merged.background_color == "#fff"  # From base
        assert merged.color == "#000"  # From override
        assert merged.padding == 10  # From override
    
    def test_style_to_dict(self):
        """Test converting style to dictionary."""
        style = ComponentStyle(
            display=Display.FLEX,
            width=px(100),
            height=200,
            padding=10,
            flex_direction=FlexDirection.COLUMN
        )
        
        style_dict = style.to_dict()
        
        assert style_dict["display"] == Display.FLEX
        assert style_dict["width"] == px(100)
        assert style_dict["height"] == 200
        assert style_dict["padding"] == 10
        assert style_dict["flex_direction"] == FlexDirection.COLUMN
    
    def test_style_copy(self):
        """Test copying a style."""
        original = ComponentStyle(
            width=100,
            height=200,
            background_color="#fff"
        )
        
        copied = original.copy()
        
        assert copied.width == original.width
        assert copied.height == original.height
        assert copied.background_color == original.background_color
        assert copied is not original
    
    def test_style_flexbox_properties(self):
        """Test flexbox-related style properties."""
        style = ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.STRETCH,
            gap=10
        )
        
        assert style.display == Display.FLEX
        assert style.flex_direction == FlexDirection.ROW
        assert style.justify_content == JustifyContent.CENTER
        assert style.align_items == AlignItems.STRETCH
        assert style.gap == 10
    
    def test_style_grid_properties(self):
        """Test CSS Grid style properties."""
        style = ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr 1fr",
            grid_template_rows="auto",
            grid_gap=20,
            grid_auto_flow="row"
        )
        
        assert style.display == Display.GRID
        assert style.grid_template_columns == "1fr 1fr 1fr"
        assert style.grid_template_rows == "auto"
        assert style.grid_gap == 20
        assert style.grid_auto_flow == "row"
    
    def test_style_text_properties(self):
        """Test text-related style properties."""
        style = ComponentStyle(
            color="#333",
            font_size=16,
            font_weight="bold",
            text_align="center",
            line_height=1.5,
            letter_spacing=0.5
        )
        
        assert style.color == "#333"
        assert style.font_size == 16
        assert style.font_weight == "bold"
        assert style.text_align == "center"
        assert style.line_height == 1.5
        assert style.letter_spacing == 0.5
    
    def test_style_border_properties(self):
        """Test border style properties."""
        style = ComponentStyle(
            border_width=2,
            border_color="#000",
            border_style="solid",
            border_radius=px(8)
        )
        
        assert style.border_width == 2
        assert style.border_color == "#000"
        assert style.border_style == "solid"
        assert style.border_radius == px(8)
    
    def test_style_position_properties(self):
        """Test position-related properties."""
        style = ComponentStyle(
            position="absolute",
            top=10,
            left=20,
            right=30,
            bottom=40,
            z_index=100
        )
        
        assert style.position == "absolute"
        assert style.top == 10
        assert style.left == 20
        assert style.right == 30
        assert style.bottom == 40
        assert style.z_index == 100
    
    def test_style_none_values(self):
        """Test style with None values."""
        style = ComponentStyle(
            width=None,
            height=None,
            padding=None
        )
        
        assert style.width is None
        assert style.height is None
        assert style.padding is None
    
    def test_style_shorthand_properties(self):
        """Test shorthand style properties."""
        style = ComponentStyle(
            margin=10,  # All sides
            padding=px(20)  # All sides with units
        )
        
        assert style.margin == 10
        assert style.padding == px(20)


class TestResponsiveStyles:
    """Test responsive style functionality."""
    
    def test_responsive_style_creation(self):
        """Test creating responsive styles."""
        base_style = ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN
        )
        
        responsive = responsive_style(base_style)
        
        assert responsive.base_style == base_style
        assert len(responsive.breakpoint_styles) == 0
    
    def test_responsive_style_with_breakpoints(self):
        """Test adding breakpoint-specific styles."""
        responsive = (
            responsive_style(ComponentStyle(
                display=Display.GRID,
                grid_template_columns="1fr"
            ))
            .at_breakpoint(BreakpointName.MD, ComponentStyle(
                grid_template_columns="1fr 1fr"
            ))
            .at_breakpoint(BreakpointName.LG, ComponentStyle(
                grid_template_columns="1fr 1fr 1fr"
            ))
        )
        
        assert len(responsive.breakpoint_styles) == 2
        assert BreakpointName.MD in responsive.breakpoint_styles
        assert BreakpointName.LG in responsive.breakpoint_styles
    
    def test_responsive_style_get_active_style(self):
        """Test getting the active style for a breakpoint."""
        base = ComponentStyle(columns=1)
        tablet = ComponentStyle(columns=2)
        desktop = ComponentStyle(columns=3)
        
        responsive = (
            responsive_style(base)
            .at_breakpoint(BreakpointName.MD, tablet)
            .at_breakpoint(BreakpointName.LG, desktop)
        )
        
        # Test different viewport widths
        assert responsive.get_active_style(400) == base  # Mobile
        assert responsive.get_active_style(800) == tablet  # Tablet
        assert responsive.get_active_style(1200) == desktop  # Desktop
    
    def test_responsive_style_inheritance(self):
        """Test that responsive styles inherit from base."""
        responsive = (
            responsive_style(ComponentStyle(
                display=Display.FLEX,
                padding=10,
                color="#000"
            ))
            .at_breakpoint(BreakpointName.MD, ComponentStyle(
                padding=20  # Override padding only
            ))
        )
        
        # At medium breakpoint, should have base properties + override
        active = responsive.get_active_style(800)
        assert active.display == Display.FLEX  # Inherited
        assert active.padding == 20  # Overridden
        assert active.color == "#000"  # Inherited


class TestStyleEnums:
    """Test style enumeration values."""
    
    def test_display_enum(self):
        """Test Display enum values."""
        assert Display.BLOCK.value == "block"
        assert Display.FLEX.value == "flex"
        assert Display.GRID.value == "grid"
        assert Display.NONE.value == "none"
        assert Display.INLINE.value == "inline"
        assert Display.INLINE_BLOCK.value == "inline-block"
    
    def test_flex_direction_enum(self):
        """Test FlexDirection enum values."""
        assert FlexDirection.ROW.value == "row"
        assert FlexDirection.COLUMN.value == "column"
        assert FlexDirection.ROW_REVERSE.value == "row-reverse"
        assert FlexDirection.COLUMN_REVERSE.value == "column-reverse"
    
    def test_justify_content_enum(self):
        """Test JustifyContent enum values."""
        assert JustifyContent.START.value == "flex-start"
        assert JustifyContent.END.value == "flex-end"
        assert JustifyContent.CENTER.value == "center"
        assert JustifyContent.SPACE_BETWEEN.value == "space-between"
        assert JustifyContent.SPACE_AROUND.value == "space-around"
        assert JustifyContent.SPACE_EVENLY.value == "space-evenly"
    
    def test_align_items_enum(self):
        """Test AlignItems enum values."""
        assert AlignItems.START.value == "flex-start"
        assert AlignItems.END.value == "flex-end"
        assert AlignItems.CENTER.value == "center"
        assert AlignItems.STRETCH.value == "stretch"
        assert AlignItems.BASELINE.value == "baseline"


class TestStyleUtilities:
    """Test style utility functions and edge cases."""
    
    def test_style_with_mixed_units(self):
        """Test style with mixed unit types."""
        style = ComponentStyle(
            width=px(100),
            height=percent(50),
            margin=10,  # Raw number
            padding=vw(5)
        )
        
        assert isinstance(style.width, Length)
        assert isinstance(style.height, Length)
        assert isinstance(style.margin, int)
        assert isinstance(style.padding, Length)
    
    def test_style_merge_with_none(self):
        """Test merging styles with None values."""
        base = ComponentStyle(width=100, height=200)
        override = ComponentStyle(width=None, padding=10)
        
        merged = base.merge(override)
        
        # None in override should not override base value
        assert merged.width == 100
        assert merged.height == 200
        assert merged.padding == 10
    
    def test_style_to_dict_excludes_none(self):
        """Test that to_dict excludes None values."""
        style = ComponentStyle(
            width=100,
            height=None,
            padding=10
        )
        
        style_dict = style.to_dict()
        
        assert "width" in style_dict
        assert "height" not in style_dict  # None values excluded
        assert "padding" in style_dict
    
    def test_empty_style(self):
        """Test creating an empty style."""
        style = ComponentStyle()
        
        assert style.to_dict() == {}
    
    def test_style_equality(self):
        """Test style equality comparison."""
        style1 = ComponentStyle(width=100, height=200)
        style2 = ComponentStyle(width=100, height=200)
        style3 = ComponentStyle(width=100, height=300)
        
        # Styles with same properties should be equal
        assert style1.to_dict() == style2.to_dict()
        assert style1.to_dict() != style3.to_dict()