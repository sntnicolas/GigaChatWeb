from gigachat import GigaChat
from config import GIGACHAT_MODEL, GIGACHAT_SCOPE, GIGACHAT_CREDENTIALS, VERIFY_SSL


class GigaChatAgent:
    def __init__(self):
        self.giga = GigaChat(
            credentials=GIGACHAT_CREDENTIALS,
            scope=GIGACHAT_SCOPE,
            model=GIGACHAT_MODEL,
            verify_ssl_certs=VERIFY_SSL
        )

    def get_token(self):
        return self.giga.get_token()

    def get_models(self):
        return self.giga.get_models()

    # def ask(self, prompt: str):
    #     return self.giga.ask(prompt)


# Пример использования
if __name__ == "__main__":
    agent = GigaChatAgent()
    token = agent.get_token()
    models = agent.get_models()

    print(token)
    print(models)
