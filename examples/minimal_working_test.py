#!/usr/bin/env python3
"""
最小工作测试 - 只用 Label 和 Button，不包含 TableView
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import VStack, Label, Button
from macui.app import MacUIApp

set_log_level("INFO")

class MinimalWorkingApp(Component):
    """最小工作应用"""
    
    def __init__(self):
        super().__init__()
        self.message = self.create_signal("Ready")
        self.counter = self.create_signal(0)
        
        self.status_text = self.create_computed(
            lambda: f"Status: {self.message.value}"
        )
        self.counter_text = self.create_computed(
            lambda: f"Count: {self.counter.value}"
        )
    
    def increment(self):
        self.counter.value += 1
        self.message.value = f"Clicked {self.counter.value} times"
        print(f"Button clicked: {self.counter.value}")
    
    def mount(self):
        return VStack(spacing=15, padding=20, children=[
            Label("Minimal Working Test"),
            Label(self.status_text),
            Label(self.counter_text),
            Button("Click Me", on_click=self.increment),
        ])

def main():
    print("🚀 Minimal Working Test Starting...")
    
    app = MacUIApp("Minimal Working Test")
    
    window = app.create_window(
        title="Minimal Working Test",
        size=(300, 200),
        resizable=True,
        content=MinimalWorkingApp()
    )
    
    window.show()
    print("✅ Window should be visible now")
    
    app.run()

if __name__ == "__main__":
    main()