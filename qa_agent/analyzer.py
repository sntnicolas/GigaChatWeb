from .parser import parse_allure_results
from .chain import build_chain


def classify_error(message: str) -> str:
    """
    Простая классификация ошибки по тексту.
    """
    msg_lower = message.lower()
    if "не найдены элементы" in msg_lower:
        return "locator_issue"
    elif "timeout" in msg_lower or "ожидание" in msg_lower:
        return "timeout"
    else:
        return "product_bug"


def generate_simple_recommendation(test_name: str, status: str, message: str) -> str:
    """Базовые рекомендации без LLM (фолбэк)."""
    if status != "failed":
        return ""
    error_type = classify_error(message)
    if error_type == "locator_issue":
        return f"Тест '{test_name}' упал из-за локатора. Проверьте селекторы."
    elif error_type == "timeout":
        return f"Тест '{test_name}' упал из-за таймаута. Проверьте ожидания."
    else:
        return f"Тест '{test_name}' упал. Возможен баг продукта."


def generate_ai_recommendation(message: str) -> str:
    """
    Генерация рекомендации через GigaChat (цепочку).
    """
    try:
        chain = build_chain()
        result = chain.invoke({"error_message": message})
        return result["text"].strip()
    except Exception as e:
        return f"[LLM недоступен: {e}]"


def generate_recommendation(test_name: str, status: str, message: str) -> str:
    """
    Универсальная функция — сначала пробуем AI, если не вышло, берём fallback.
    """
    if status != "failed":
        return ""

    ai_response = generate_ai_recommendation(message)
    if ai_response and not ai_response.startswith("[LLM недоступен"):
        return f"🤖 AI-рекомендация: {ai_response}"
    else:
        return generate_simple_recommendation(test_name, status, message)


if __name__ == "__main__":
    parsed = parse_allure_results()
    for r in parsed:
        rec = generate_recommendation(r["name"], r["status"], r["message"])
        print(f"{r['name']}: {rec}")


# if __name__ == "__main__":
#     parsed = parse_allure_results()
#     print("Рекомендации сгенерированы и прикреплены к Allure UI.")

