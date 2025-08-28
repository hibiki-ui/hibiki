#!/usr/bin/env python3
"""
test-project - A Hibiki UI application
"""

from hibiki import HibikiApp, Signal, Computed
from hibiki.components import Button, Label, VStack

class Test-projectApp:
    def __init__(self):
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
    
    def increment(self):
        self.count.value += 1
    
    def create_ui(self):
        return VStack(children=[
            Label(self.count_text),
            Button("Click me", on_click=self.increment)
        ])

def main():
    app = HibikiApp("test-project")
    demo = Test-projectApp()
    window = app.create_window("test-project", content=demo.create_ui())
    window.show()
    app.run()

if __name__ == "__main__":
    main()
