"""macUI CLI - Command line interface for macUI development tools
"""

import argparse
import sys
from pathlib import Path


def create_project(name: str, template: str = "basic") -> None:
    """Create a new macUI project from template."""
    project_dir = Path(name)

    if project_dir.exists():
        print(f"Error: Directory '{name}' already exists")
        sys.exit(1)

    project_dir.mkdir()
    print(f"Created macUI project: {name}")

    # Create basic project structure
    (project_dir / "main.py").write_text(f'''#!/usr/bin/env python3
"""
{name} - A macUI application
"""

from macui import MacUIApp, Signal, Computed
from macui.components import Button, Label, VStack

class {name.capitalize()}App:
    def __init__(self):
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {{self.count.value}}")
    
    def increment(self):
        self.count.value += 1
    
    def create_ui(self):
        return VStack(children=[
            Label(self.count_text),
            Button("Click me", on_click=self.increment)
        ])

def main():
    app = MacUIApp("{name}")
    demo = {name.capitalize()}App()
    window = app.create_window("{name}", content=demo.create_ui())
    window.show()
    app.run()

if __name__ == "__main__":
    main()
''')

    print("  ✅ Created main.py")
    print(f"  💡 Run with: python {name}/main.py")


def run_examples():
    """List and run example applications."""
    examples_dir = Path(__file__).parent.parent / "examples"

    if not examples_dir.exists():
        print("No examples directory found")
        return

    examples = list(examples_dir.glob("*.py"))

    if not examples:
        print("No examples found")
        return

    print("Available examples:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example.stem}")

    try:
        choice = int(input("Select example (number): ")) - 1
        if 0 <= choice < len(examples):
            import subprocess
            subprocess.run([sys.executable, str(examples[choice])])
        else:
            print("Invalid choice")
    except (ValueError, KeyboardInterrupt):
        print("Cancelled")


def show_info():
    """Show macUI version and system information."""
    from . import __version__

    print(f"macUI v{__version__}")
    print(f"Python: {sys.version}")

    try:
        import objc
        print(f"PyObjC: {getattr(objc, '__version__', 'installed')}")
    except ImportError:
        print("PyObjC: not installed ❌")
        print("Install with: uv add pyobjc-core pyobjc-framework-Cocoa")

    print(f"Platform: {sys.platform}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="macUI CLI - Tools for macUI development"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create new macUI project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--template", default="basic", help="Project template")

    # Examples command
    subparsers.add_parser("examples", help="Run example applications")

    # Info command
    subparsers.add_parser("info", help="Show version and system information")

    args = parser.parse_args()

    if args.command == "create":
        create_project(args.name, args.template)
    elif args.command == "examples":
        run_examples()
    elif args.command == "info":
        show_info()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
