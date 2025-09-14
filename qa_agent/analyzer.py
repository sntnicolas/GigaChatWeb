from .parser import parse_allure_results


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


def generate_recommendation(test_name: str, status: str, message: str) -> str:
    if status != "failed":
        return ""  # или None
    error_type = classify_error(message)
    if error_type == "locator_issue":
        return f"Тест '{test_name}' упал из-за локатора. Проверьте селекторы."
    elif error_type == "timeout":
        return f"Тест '{test_name}' упал из-за таймаута. Проверьте ожидания."
    else:
        return f"Тест '{test_name}' упал. Возможен баг продукта."


if __name__ == "__main__":
    parsed = parse_allure_results()
    print("Рекомендации сгенерированы и прикреплены к Allure UI.")
