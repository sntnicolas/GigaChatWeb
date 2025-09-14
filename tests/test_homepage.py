import allure
import pytest
from pages.home_page import HomePage

@allure.feature("Главная страница")
@allure.story("Отображение элементов")
def test_home_page_elements_visible(page):
    home = HomePage(page, "https://giga.chat")
    home.goto()
    assert home.is_loaded()

    with allure.step("Проверяем обязательные элементы"):
        # кнопки
        elements = {
            "gigachat": home.btn_gigachat,
            "sidebar_toggle": home.btn_sidebar_toggle,
            "new_chat": home.btn_new_chat,
            "my_chats": home.btn_my_chats,
            "smart_editor": home.btn_smart_editor,
            "tools": home.btn_tools,
        }

        missing = []
        for name, selector in elements.items():
            if not page.is_visible(selector):
                missing.append(name)

        if missing:
            filename = "_".join(missing) + ".png"
            filepath = f"screenshots/{filename}"

            page.screenshot(path=filepath)
            allure.attach.file(filepath,
                               name=f"Скриншот отсутствующих элементов: {', '.join(missing)}",
                               attachment_type=allure.attachment_type.PNG)

            pytest.fail(f"Не найдены элементы: {', '.join(missing)}")