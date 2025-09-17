from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from .llm import get_llm


def build_chain():
    """
    Создаёт простую цепочку (LLMChain), которая принимает текст ошибки
    и возвращает рекомендацию по её устранению.
    """
    llm = get_llm()

    # Шаблон для промпта
    prompt = ChatPromptTemplate.from_template(
        "Ты — QA помощник. "
        "Разбери сообщение об ошибке из автотеста и предложи рекомендацию.\n\n"
        "Ошибка:\n{error_message}\n\n"
        "Ответь кратко и по делу."
    )

    # Цепочка: {error_message} → llm → {text}
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


if __name__ == "__main__":
    chain = build_chain()
    result = chain.invoke({"error_message": "Не найдены элементы: sidebar_toggle"})
    print(result["text"])
