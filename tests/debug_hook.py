from types import SimpleNamespace
import allure
from qa_agent.chain import build_chain
from qa_agent.analyzer import generate_recommendation

def simulate_failed_test():
    """
    Симуляция падения теста для проверки генерации рекомендаций.
    """
    # фейковый объект item (как будто pytest передал)
    fake_item = SimpleNamespace(name="test_fake_failure")

    # фейковый отчет о падении
    fake_rep = SimpleNamespace(
        when="call",
        failed=True,
        longrepr="Не найдены элементы: sidebar_toggle"
    )

    error_message = str(fake_rep.longrepr)

    try:
        # пробуем LLM
        chain = build_chain()
        result = chain.invoke({"error_message": error_message})
        recommendation = result["text"]
    except Exception as e:
        # fallback
        recommendation = generate_recommendation(
            test_name=fake_item.name,
            status="failed",
            message=error_message
        )
        recommendation = f"[Fallback] {recommendation}\nОшибка LLM: {e}"

    print("=== Recommendation ===")
    print(recommendation)

    # Чтобы увидеть в Allure:
    allure.attach(
        recommendation,
        name=f"Recommendation: {fake_item.name}",
        attachment_type=allure.attachment_type.TEXT
    )


if __name__ == "__main__":
    simulate_failed_test()
