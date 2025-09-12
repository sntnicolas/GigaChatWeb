from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Навигационные кнопки
        self.btn_sidebar_toggle = '.DesktopSidebar-styled__SidebarContainer svg[role="button"]:nth-of-type(1)' # кнопка гигачат
        self.btn_gigachat = '.DesktopSidebar-styled__SidebarContainer svg[role="button"]:nth-of-type(2)' # открытие/закрытие сайдбара
        self.btn_new_chat = '.get_by_role("button", name="Новый чат")'
        self.btn_my_chats = '.get_by_role("button", name="Мои чаты")'
        self.btn_smart_editor = '.get_by_role("button", name="Умный редактор")'
        self.btn_tools = '.get_by_role("button", name="Полезное")'

        # Основное содержимое
        self.login_text1 = '.get_by_text("Откройте все возможности")'  # блок с текстом часть 1
        self.login_text2 = '.get_by_text("Создавайте документы, загружайте картинки, включайте озвучивание ответов"))'  # блок с текстом часть 2
        self.btn_try_now = '.get_by_role("button", name="Попробовать")'  # кнопка "Попробовать"

        # Поле ввода и сопутствующие кнопки
        # Используем родителя или класс контейнера, чтобы избежать нестабильного плейсхолдера
        self.input_query = '#chat-input-textarea'
        self.btn_attach_file = '.get_by_role("button", name="Прикрепить")'
        self.btn_microphone = '.locator("label").get_by_role("button").nth(1)'

        # ====== Подсказки ======
        self.suggestion_selector = 'div[data-suggest-position]'



        # Tapbar
        self.tapbar_giga = '.get_by_role("button", name="Giga")'
        self.tapbar_search = '.get_by_role("button", name="Искать Добавлю в ответ свежую информацию")'
        self.tapbar_explore = '.get_by_role("button", name="Исследовать Предоставлю анализ с выводами и источниками")'
        self.tapbar_reason = '.get_by_role("button", name="Рассуждать Покажу процесс создания ответа")'

        # Куки
        self.cookies_text1 = '.get_by_text("На этом сайте используются")'
        self.cookies_text2 = '.get_by_text("Cookies").nth(1)'
        self.cookies_link = 'get_by_role("link", name="читайте здесь")'
        self.cookies_accept = '.get_by_role("button", name="Принять")'


    # ====== Навигация ======
    def goto(self):
        self.page.goto(self.base_url)

    def open_sidebar(self):
        self.page.click(self.btn_sidebar_toggle)

    def click_new_chat(self):
        self.page.click(self.btn_new_chat)

    def click_my_chats(self):
        self.page.click(self.btn_my_chats)

    def click_smart_editor(self):
        self.page.click(self.btn_smart_editor)

    def click_tools(self):
        self.page.click(self.btn_tools)

    def click_gigachat(self):
        self.page.click(self.btn_gigachat)

    def click_try_now(self):
        self.page.click(self.btn_try_now)

    # ====== Работа с запросом ======
    def enter_query(self, text: str):
        self.page.fill(self.input_query, text)

    def click_attach_file(self):
        self.page.click(self.btn_attach_file)

    def click_microphone(self):
        self.page.click(self.btn_microphone)

    def get_suggestions_count(self) -> int:
        """Возвращает количество подсказок на странице"""
        return self.page.locator(self.suggestion_selector).count()

    def get_suggestion_text(self, index: int) -> str:
        """
        Возвращает текст подсказки по её порядковому номеру.
           index: 1..6 (как в атрибуте data-suggest-position)
        """
        locator = self.page.locator(f'div[data-suggest-position="{index}"]')
        return locator.inner_text().strip()

    def click_suggestion(self, index: int):
        """
        Кликает по подсказке по её порядковому номеру.
        index: 1..6
        """
        locator = self.page.locator(f'div[data-suggest-position="{index}"]')
        locator.click()

    # ====== Tapbar ======
    def tap_giga(self):
        self.page.click(self.tapbar_giga)

    def tap_search(self):
        self.page.click(self.tapbar_search)

    def tap_explore(self):
        self.page.click(self.tapbar_explore)

    def tap_reason(self):
        self.page.click(self.tapbar_reason)

    # ====== Куки ======
    def accept_cookies(self):
        if self.page.is_visible(self.cookies_accept):
            self.page.click(self.cookies_accept)

    # ====== Проверки состояния ======
    def is_loaded(self):
        self.page.wait_for_selector(self.input_query, timeout=10000)
        return True