# Page Object Model для главной/чат страницы.
# Подставь реальные селекторы из разметки giga.chat.

class HomePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

        # === ОБЯЗАТЕЛЬНО проверь и при необходимости поправь ===
        self.selector_chat_input = 'textarea[name="message"]'        # пример
        self.selector_send_button = 'button[type="submit"]'         # пример
        self.selector_messages_list = '.messages'                   # пример
        self.selector_message_item = '.message'                     # пример
        self.selector_login_button = 'a[href*="login"]'             # пример
        self.selector_user_avatar = '.user-avatar'                  # пример

    async def goto(self):
        await self.page.goto(self.base_url)

    async def is_loaded(self):
        # проверка ключевого элемента на странице
        return await self.page.is_visible(self.selector_chat_input)

    async def send_message(self, text):
        await self.page.fill(self.selector_chat_input, text)
        # иногда отправка через Enter удобнее:
        await self.page.press(self.selector_chat_input, "Enter")
        # или клик по кнопке:
        # await self.page.click(self.selector_send_button)

    async def last_message_text(self):
        items = await self.page.query_selector_all(self.selector_message_item)
        if not items:
            return None
        last = items[-1]
        return (await last.inner_text()).strip()

    async def wait_for_new_message(self, prev_count, timeout=5000):
        await self.page.wait_for_function(
            "(sel, prev) => document.querySelectorAll(sel).length > prev",
            self.selector_message_item,
            prev_count,
            timeout=timeout
        )

    async def message_count(self):
        items = await self.page.query_selector_all(self.selector_message_item)
        return len(items)
