from gigachat import GigaChat
from . import config


class GigaChatAgent:
    def __init__(self):
        self.giga = GigaChat(
            credentials=config.GIGACHAT_CREDENTIALS,
            scope=config.GIGACHAT_SCOPE,
            model=config.GIGACHAT_MODEL,
            verify_ssl_certs=config.VERIFY_SSL
        )

    def get_models(self):
        return self.giga.get_models()

    def ask(self, prompt: str):
        return self.giga.ask(prompt)


# Пример использования
if __name__ == "__main__":
    agent = GigaChatAgent()
    token = agent.get_token()
    models = agent.get_models()

    print(token)
    print(models)

giga = GigaChat(
    credentials="MjYzZDVhY2MtMmYyNi00ZDY5LThkMDItYzk4N2YxZTI0ZDdiOmVlYmI2OTExLWVkYjUtNDNlYy04MTU3LWE3YjY0YjRkZTllZg==",
    # scope="GIGACHAT_API_PERS",
    # model="GigaChat",
    verify_ssl_certs=False  # отключаем проверку сертификатов
)

token = giga.get_token()
models = giga.get_models()

print(token, models)

from langchain_gigachat.chat_models import GigaChat

llm = GigaChat(model="GigaChat-2-Max", top_p=0, timeout=120)
response = llm.invoke("Кто тебя создал?")
print(response.content)
