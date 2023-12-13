from shutil import get_terminal_size
from typing import Any, List, Optional
from dataclasses import dataclass, field
from prompt_toolkit import Application
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Window
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.formatted_text import to_formatted_text


@dataclass
class PickWindow:
    search_items: Optional[List[Any]]
    _input_field: TextArea = field(init=False, default=TextArea(prompt='', height=1)) # 検索バー
    _result_window: Window = field(init=False, default=None) # 結果表示のウィンドウ
    _result_control: FormattedTextControl = field(init=False, default=FormattedTextControl()) # 結果表示のウィンドウのスタイル制御
    _current_results: Optional[List[Any]] = field(init=False, default_factory=list) # 現在の絞り込み結果
    _selected_index: int = field(init=False, default=0) # 絞り込み結果のリストの内、現在選択しているもののインデックス
    _selected_item: Any = field(init=False, default=None) # 最終的に選択した項目
    _page_size: int = field(init=False, default=10)  # 1ページあたりの項目数
    _current_page: int = field(init=False, default=0)  # 現在のページ番号
    _app: Application = field(init=False, default=None)

    def __post_init__(self):
        self._result_window = Window(content=self._result_control)
        self._current_results = self.search_items
        # 入力フィールドにテキストが変更されたときのイベントハンドラ
        self._input_field.buffer.on_text_changed.add_handler(lambda _: self._update_search())

        # キーバインドの設定、各キー押下時の動作を関数で指定する
        bindings = KeyBindings()
        bindings.add(Keys.Down)(self._move_cursor_down)
        bindings.add(Keys.Up)(self._move_cursor_up)
        bindings.add(Keys.Enter)(self._select_item)
        bindings.add(Keys.ControlC)(self._exit)

        # レイアウト
        layout = Layout(HSplit([self._input_field, Window(height=1, char='-'), self._result_window]))  # result_area を result_window に変更
        # 検索結果の色付けに使うスタイル
        style = Style([
            ('selected-item', 'bg:#ffd700 #000000'),  # 選択された項目のスタイル
            ('keyword', 'fg:#1e90ff')  # マッチしたキーワードのスタイル
        ])

        # 検索ウィンドウを初期化する、初期状態ではリストの全てを表示する
        self._update_result_area()
        # アプリケーションの作成と実行
        self._app = Application(layout=layout, key_bindings=bindings, full_screen=True, style=style)

    # 絞り込んだリストを取得
    def _get_filtered_items(self, input_text):
        if not input_text.strip():
            return self.search_items  # 入力が空の場合は全ての項目を表示
        keywords = input_text.lower().split()
        filtered_items = [item for item in self.search_items if all(keyword in item.lower() for keyword in keywords)]
        return filtered_items
    
    # 絞り込み結果を更新
    def _update_search(self):
        self._current_results = self._get_filtered_items(self._input_field.text)
        self._update_result_area()

    # 絞り込み結果からフォーマットしたテキストを生成
    def _get_formatted_text(self, item, keywords, selected=False):
        tokens = []
        last_idx = 0
        item = str(item)
        for keyword in keywords:
            start_idx = item.lower().find(keyword.lower(), last_idx)
            if start_idx >= 0:
                end_idx = start_idx + len(keyword)
                if selected:
                    # 選択された行のスタイルを適用
                    tokens.append(('class:selected-item', item[last_idx:start_idx]))  # マッチしてないテキスト
                    tokens.append(('class:selected-item class:keyword', item[start_idx:end_idx]))  # マッチしたテキスト
                else:
                    # 通常の行のスタイルを適用
                    tokens.append(('', item[last_idx:start_idx]))  # マッチしてないテキスト
                    tokens.append(('class:keyword', item[start_idx:end_idx]))  # マッチしたテキスト
                last_idx = end_idx
        tokens.append(('class:selected-item' if selected else '', item[last_idx:]))  # 残りのテキスト
        return tokens
    
    # 絞り込み結果の表示の更新
    def _update_result_area(self):
        self._page_size = get_terminal_size().lines - 2  # 検索ウィンドウと区切行分
        if self._current_results:
            start_index = self._current_page * self._page_size
            end_index = start_index + self._page_size
            page_items = self._current_results[start_index:end_index]

            keywords = self._input_field.text.lower().split()
            formatted_results = []
            for i, item in enumerate(page_items):
                tokens = self._get_formatted_text(item, keywords, selected=(i == self._selected_index))
                formatted_results.extend(tokens + [('', '\n')])  # 各項目の後に改行を追加
            self._result_control.text = to_formatted_text(formatted_results)
        else:
            self._result_control.text = to_formatted_text([])

    def _move_cursor_down(self, event: KeyPressEvent):
        max_page = len(self._current_results) // self._page_size
        if self._current_results:
            self._selected_index = self._selected_index + 1
            if self._selected_index > self._page_size - 1 and self._current_page < max_page:
                self._current_page += 1
                self._selected_index = 0
            self._update_result_area()

    def _move_cursor_up(self, event: KeyPressEvent):
        if self._current_results:
            self._selected_index = self._selected_index - 1
            if self._selected_index < 0 and self._current_page > 0:
                self._current_page -= 1
                self._selected_index = self._page_size - 1
            self._update_result_area()

    def _select_item(self, event: KeyPressEvent):
        if self._current_results:
            absolute_selected_index = self._current_page * self._page_size + self._selected_index
            self._selected_item = self._current_results[absolute_selected_index]
            event.app.exit()

    def _exit(self, event: KeyPressEvent):
        event.app.exit()

    # 絞り込みの開始
    def search(self):
        self._app.run()
        return self._selected_item