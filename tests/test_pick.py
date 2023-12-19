from unittest.mock import Mock
from src.picombo import PickWindow

mock = Mock()
item_num = 100
items = [str(i) for i in range(1, item_num + 1)]


def init_pw():
    return PickWindow(search_items=items)


def test_filtered_items():
    pw = init_pw()
    filtered_items = pw._get_filtered_items('2')
    items_include_2 = [i for i in items if '2' in i]
    assert filtered_items == items_include_2


def test_move_cursor_down():
    pw = init_pw()

    # カーソルの初期位置を確認
    assert pw._selected_index == 0

    # カーソルが移動することを確認
    pw._move_cursor_down(None)
    assert pw._selected_index == 1

    # ページ送りが正常に進むことを確認
    count = pw._page_size
    while count != 0:
        count -= 1
        pw._move_cursor_down(None)
    assert pw._selected_index == 1
    assert pw._current_page == 1

    # カーソルが画面外まで進まないことを確認
    pw = init_pw()
    count = len(items)
    while count != 0:
        count -= 1
        pw._move_cursor_down(None)
    print(pw._selected_index)
    assert pw._selected_index == 0
    assert pw._current_page == 0


def test_move_cursor_up():
    # カーソルをテストの初期位置まで移動
    pw = init_pw()
    count = pw._page_size + 1
    while count != 0:
        count -= 1
        pw._move_cursor_down(None)
        print(pw._selected_index)

    # カーソルが移動することを確認
    pw._move_cursor_up(None)
    assert pw._selected_index == 0

    # ページ送りが正常に戻ることを確認
    pw._move_cursor_up(None)
    assert pw._selected_index == pw._page_size - 1
    assert pw._current_page == 0

    # カーソルが画面外まで戻らないことを確認
    pw = init_pw()
    pw._move_cursor_up(None)
    assert pw._selected_index == item_num % pw._page_size - 1
    assert pw._current_page == item_num // pw._page_size


def test_select_item():
    pw = init_pw()
    count = pw._page_size
    while count != 0:
        count -= 1
        pw._move_cursor_down(None)
    pw._select_item(mock)
    assert pw._selected_item == str(23)