def test_home_page_elements_visible(page):
    home = HomePage(page, "https://giga.chat")
    home.goto()
    assert home.is_loaded()

    # кнопки
    assert page.is_visible(home.btn_gigachat)
    assert page.is_visible(home.btn_sidebar_toggle)
    assert page.is_visible(home.btn_new_chat)
    assert page.is_visible(home.btn_my_chats)
    assert page.is_visible(home.btn_smart_editor)
    assert page.is_visible(home.btn_tools)
