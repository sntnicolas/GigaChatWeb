# llm.py
from langchain_gigachat.chat_models import GigaChat
from .config import GIGACHAT_MODEL, GIGACHAT_SCOPE, GIGACHAT_CREDENTIALS, VERIFY_SSL

def get_llm() -> GigaChat:
    return GigaChat(
        model=GIGACHAT_MODEL,
        credentials=GIGACHAT_CREDENTIALS,
        scope=GIGACHAT_SCOPE,
        verify_ssl_certs=VERIFY_SSL
    )

if __name__ == "__main__":
    llm = get_llm()
    response = llm.invoke("Кто тебя создал?")
    print(response.content)
