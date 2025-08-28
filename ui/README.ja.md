# Hibiki UI

*他の言語で読む: [English](README.md) | [简体中文](README.zh-CN.md)*

[![PyPI version](https://badge.fury.io/py/hibiki-ui.svg)](https://badge.fury.io/py/hibiki-ui)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python と PyObjC を使用してネイティブ macOS アプリケーションを構築するための、モダンなリアクティブ UI フレームワークです。Hibiki UI はシグナルベースのリアクティブシステムとネイティブ macOS コンポーネントを組み合わせ、レスポンシブなユーザーインターフェースを作成するためのクリーンで強力な API を提供します。

## 🎯 主要機能

- **🔄 シグナルベースのリアクティブシステム** - Signal、Computed、Effect プリミティブを使用したきめ細かいリアクティブ更新
- **🍎 ネイティブ macOS 統合** - AppKit コンポーネントとの直接的な PyObjC 統合
- **⚡ 高パフォーマンス** - Core Animation API のみを使用した GPU 加速アニメーション
- **🧩 コンポーネントアーキテクチャ** - ライフサイクル管理を備えたモダンなコンポーネントベース開発
- **📐 プロフェッショナルレイアウトシステム** - 精密制御を備えた Flexbox スタイルのレイアウトエンジン
- **🎨 完全な UI ツールキット** - ネイティブ macOS コントロールとウィジェットの完全セット
- **🔧 タイプセーフ** - 優れた IDE サポートを備えた完全な型注釈

## 🚀 クイックスタート

### インストール

```bash
# uv を使用（推奨）
uv add hibiki-ui

# pip を使用
pip install hibiki-ui
```

### Hello World の例

```python
from hibiki import Signal, Computed
from hibiki import Label, Button, Container, ComponentStyle, px
from hibiki import ManagerFactory

# リアクティブ状態を作成
count = Signal(0)

# リアクティブバインディングを持つ UI コンポーネントを作成
button = Button(
    "クリックして",
    style=ComponentStyle(width=px(120), height=px(32)),
    on_click=lambda: setattr(count, 'value', count.value + 1)
)

label = Label(
    Computed(lambda: f"{count.value} 回クリックしました"),
    style=ComponentStyle(height=px(25))
)

# レイアウトコンテナを作成
app_ui = Container(
    children=[label, button],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        gap=px(10),
        padding=px(20)
    )
)

# アプリケーションを作成して実行
app_manager = ManagerFactory.get_app_manager()
window = app_manager.create_window("Hello Hibiki UI", 300, 150)
window.set_content(app_ui)
app_manager.run()
```

## 🏗️ アーキテクチャ

```
あなたのアプリケーションコード
       ↓
コンポーネントシステム（Label、Button、Container）
       ↓
リアクティブシステム（Signal、Computed、Effect）← コア
       ↓
バインディングレイヤー（ReactiveBinding、イベント処理）
       ↓
AppKit/PyObjC（NSView、NSButton など）
```

## 🔄 リアクティブシステム

### Signals - リアクティブ状態

```python
from hibiki import Signal, Effect

# 可変なリアクティブ状態を作成
user_name = Signal("太郎")
user_age = Signal(25)

# Signals は変更時に自動的にオブザーバーに通知
user_name.value = "花子"  # 依存する計算と副作用をトリガー
```

### Computed - 派生値

```python
from hibiki import Computed

# Computed 値は依存関係が変更されると自動的に再計算
full_info = Computed(lambda: f"{user_name.value}は{user_age.value}歳です")
is_adult = Computed(lambda: user_age.value >= 18)

print(full_info.value)  # "花子は25歳です"
```

### Effects - 副作用

```python
# Effects はリアクティブな依存関係が変更されたときに実行
def log_changes():
    print(f"ユーザー情報が更新されました: {full_info.value}")

effect = Effect(log_changes)  # 即座に実行され、各変更時に実行
user_age.value = 30  # 副作用をトリガー
```

## 🧩 コンポーネントシステム

### 基本コンポーネント

```python
from hibiki import (
    Label, Button, TextField, Slider, Switch,
    ProgressBar, ImageView, Checkbox, RadioButton
)

# リアクティブコンテンツを持つテキスト表示
status_label = Label(
    Computed(lambda: f"状態: {'オンライン' if connected.value else 'オフライン'}"),
    style=ComponentStyle(color="green" if connected.value else "red")
)

# 動的状態を持つインタラクティブボタン
action_button = Button(
    title=Computed(lambda: "切断" if connected.value else "接続"),
    enabled=Computed(lambda: not is_loading.value),
    on_click=toggle_connection
)

# テキスト入力との双方向データバインディング
username_field = TextField(
    value=username_signal,  # 自動双方向バインディング
    placeholder="ユーザー名を入力...",
    style=ComponentStyle(width=px(200))
)
```

### レイアウトコンポーネント

```python
from hibiki import Container

# Flexbox スタイルレイアウト
header = Container(
    children=[logo, title, menu_button],
    style=ComponentStyle(
        display="flex",
        flex_direction="row",
        justify_content="space-between",
        align_items="center",
        padding=px(15)
    )
)

sidebar = Container(
    children=[nav_menu, user_profile],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        width=px(250),
        background_color="lightgray"
    )
)

main_content = Container(
    children=[content_area],
    style=ComponentStyle(
        flex=1,  # 残りのスペースを占有
        padding=px(20)
    )
)

app_layout = Container(
    children=[header, Container(children=[sidebar, main_content])],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        height=px(600)
    )
)
```

## 🎨 高度な機能

### フォーム処理

```python
from hibiki import Form, FormField, RequiredValidator, EmailValidator

# バリデーション付きフォームを作成
contact_form = Form([
    FormField("name", TextField(), [RequiredValidator("名前は必須です")]),
    FormField("email", TextField(), [EmailValidator(), RequiredValidator()]),
    FormField("age", TextField(), [NumberValidator(min_value=0, max_value=120)])
])

# フォーム送信を処理
def submit_form():
    if contact_form.is_valid():
        data = contact_form.get_data()
        print(f"送信データ: {data}")
    else:
        print("フォームにエラーがあります:", contact_form.get_errors())
```

### アニメーション

```python
from hibiki import animate, fade_in, bounce

# シンプルな宣言的アニメーション
animate(my_button, duration=0.3, scale=1.1, opacity=0.9)

# プリセットアニメーション効果
fade_in(welcome_label, duration=1.0)
bounce(notification_view, scale=1.05)

# リアクティブアニメーション
effect = Effect(lambda: animate(
    status_indicator,
    opacity=1.0 if is_online.value else 0.3,
    duration=0.2
))
```

### カスタムコンポーネント

```python
from hibiki import UIComponent

class CounterWidget(UIComponent):
    def __init__(self, initial_value=0):
        super().__init__()
        self.count = Signal(initial_value)
        self.count_text = Computed(lambda: f"カウント: {self.count.value}")
    
    def _create_nsview(self):
        # ラベルとボタンを含むコンテナを作成
        container = Container(
            children=[
                Button("-", on_click=lambda: setattr(self.count, 'value', self.count.value - 1)),
                Label(self.count_text, style=ComponentStyle(min_width=px(60))),
                Button("+", on_click=lambda: setattr(self.count, 'value', self.count.value + 1))
            ],
            style=ComponentStyle(
                display="flex",
                flex_direction="row",
                gap=px(5),
                align_items="center"
            )
        )
        return container.mount()

# 使用方法
counter = CounterWidget(initial_value=10)
```

## 🎭 完全なアプリケーションの例

```python
from hibiki import *

class TodoApp:
    def __init__(self):
        self.todos = Signal([])
        self.new_todo_text = Signal("")
        self.filter_mode = Signal("all")  # "all", "active", "completed"
    
    def add_todo(self):
        text = self.new_todo_text.value.strip()
        if text:
            new_todo = {"id": len(self.todos.value), "text": text, "completed": False}
            self.todos.value = [*self.todos.value, new_todo]
            self.new_todo_text.value = ""
    
    def toggle_todo(self, todo_id):
        todos = self.todos.value
        updated_todos = []
        for todo in todos:
            if todo["id"] == todo_id:
                updated_todos.append({**todo, "completed": not todo["completed"]})
            else:
                updated_todos.append(todo)
        self.todos.value = updated_todos
    
    def create_ui(self):
        # 計算値
        active_count = Computed(lambda: sum(1 for todo in self.todos.value if not todo["completed"]))
        filtered_todos = Computed(lambda: self._filter_todos())
        
        # UI コンポーネント
        header = Container([
            Label("Todo アプリ", style=ComponentStyle(font_size=px(24), font_weight="bold")),
            TextField(
                value=self.new_todo_text,
                placeholder="何をする必要がありますか？",
                on_enter=self.add_todo
            ),
            Button("Todo を追加", on_click=self.add_todo)
        ], style=ComponentStyle(gap=px(10)))
        
        # 動的 Todo リスト
        todo_list = Container([
            *[self._create_todo_item(todo) for todo in filtered_todos.value]
        ], style=ComponentStyle(gap=px(5)))
        
        footer = Container([
            Label(Computed(lambda: f"残り {active_count.value} 項目")),
            Container([
                Button("すべて", on_click=lambda: setattr(self.filter_mode, 'value', "all")),
                Button("進行中", on_click=lambda: setattr(self.filter_mode, 'value', "active")),
                Button("完了済み", on_click=lambda: setattr(self.filter_mode, 'value', "completed"))
            ], style=ComponentStyle(display="flex", flex_direction="row", gap=px(5)))
        ], style=ComponentStyle(display="flex", justify_content="space-between"))
        
        return Container([header, todo_list, footer], style=ComponentStyle(
            padding=px(20),
            gap=px(15),
            min_height=px(400)
        ))
    
    def _filter_todos(self):
        todos = self.todos.value
        if self.filter_mode.value == "active":
            return [todo for todo in todos if not todo["completed"]]
        elif self.filter_mode.value == "completed":
            return [todo for todo in todos if todo["completed"]]
        return todos
    
    def _create_todo_item(self, todo):
        return Container([
            Checkbox(
                checked=Signal(todo["completed"]),
                on_change=lambda checked: self.toggle_todo(todo["id"])
            ),
            Label(todo["text"], style=ComponentStyle(
                text_decoration="line-through" if todo["completed"] else "none"
            ))
        ], style=ComponentStyle(display="flex", flex_direction="row", gap=px(10)))

def main():
    app = TodoApp()
    
    # アプリケーションを作成
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window("Hibiki UI Todo アプリ", 500, 600)
    window.set_content(app.create_ui())
    
    app_manager.run()

if __name__ == "__main__":
    main()
```

## 📦 開発

### プロジェクトセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/hibiki-ui/hibiki-ui.git
cd hibiki-ui

# 開発環境をセットアップ
uv sync --all-extras
uv run pre-commit install
```

### 開発コマンド

```bash
# ショーケースデモを実行
uv run python showcase.py

# テストを実行
uv run pytest

# コード品質
uv run ruff check .
uv run ruff check --fix .
uv run black .
uv run isort .
uv run mypy hibiki

# パッケージをビルド
uv build
```

## 🎯 なぜ Hibiki UI を選ぶのか？

### 他の macOS GUI フレームワークとの比較

| 機能 | Hibiki UI | Tkinter | PyQt/PySide | Kivy |
|------|-----------|---------|-------------|------|
| ネイティブ macOS | ✅ 完全な AppKit | ❌ エミュレート | ⚠️ テーマ化 | ❌ カスタム |
| リアクティブ更新 | ✅ 自動 | ❌ 手動 | ❌ シグナル/スロット | ❌ 手動 |
| パフォーマンス | ✅ ネイティブ | ⚠️ 中程度 | ⚠️ 良好 | ✅ 良好 |
| macOS 統合 | ✅ 完全 | ❌ なし | ⚠️ 限定的 | ❌ なし |
| 学習曲線 | ✅ モダン | ✅ シンプル | ❌ 複雑 | ⚠️ 中程度 |
| バンドルサイズ | ✅ 小さい | ✅ 小さい | ❌ 大きい | ⚠️ 中程度 |
| アニメーションサポート | ✅ GPU 加速 | ❌ 限定的 | ⚠️ 基本的 | ✅ 良好 |

### 主な利点

- **🍎 ネイティブパフォーマンス**：直接的な AppKit 統合でゼロ抽象化オーバーヘッド
- **🔄 リアクティブ設計**：自動 UI 更新、手動 DOM 操作不要
- **🚀 モダンな開発者体験**：型ヒント、IDE サポート、現代的なツール
- **🎨 プロフェッショナルアニメーション**：GPU 加速の Core Animation 統合
- **📱 本番環境対応**：適切なメモリ管理とライフサイクル処理

## 📄 ライセンス

MIT ライセンス - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- **SolidJS** - リアクティブシステム設計のインスピレーション
- **PyObjC** - これを可能にする基盤
- **AppKit** - ネイティブ macOS UI フレームワーク
- **Core Animation** - GPU 加速アニメーションシステム

---

**Hibiki UI** - ネイティブ macOS アプリケーションにリアクティブでモダンな UI 開発をもたらします。🍎✨