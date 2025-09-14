from langchain_gigachat.chat_models import GigaChat

llm = GigaChat(model="GigaChat-2-Max", top_p=0, timeout=120)
response = llm.invoke("Кто тебя создал?")
print(response.content)
