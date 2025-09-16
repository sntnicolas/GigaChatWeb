import os
import pytest
import shutil
import allure
from qa_agent.chain import build_chain
from qa_agent.analyzer import generate_recommendation


# pytest-playwright provides 'page' fixture already.
# Мы добавим базовый url и вспомогательные фикстуры.

@pytest.fixture(scope="session")
def base_url():
    # Можно переопределить через env GIGA_BASE
    return os.getenv("GIGA_BASE", "https://giga.chat")


def pytest_sessionstart(session):
    """
    Перед стартом прогонов чистим allure-results.
    """
    allure_dir = os.path.join(os.getcwd(), "allure-results")
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
    os.makedirs(allure_dir)


# hook для прикрепления рекомендаций прямо во время выполнения теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук вызывается после каждого теста.
    Если тест упал → пробуем получить рекомендацию через LLM.
    """
    outcome = yield
    rep = outcome.get_result()

    # проверяем только фазу call (исполнение теста)
    if rep.when == "call" and rep.failed:
        try:
            # 🚀 используем LLM-цепочку
            chain = build_chain()
            result = chain.invoke({"error_message": error_message})
            recommendation = result["text"]

        except Exception as e:
            # если LLM не отработал → fallback на простой анализатор
            recommendation = generate_recommendation(
                test_name=item.name,
                status="failed",
                # message=error_message
                message=str(rep.longrepr)

            )
            recommendation = f"[Fallback] {recommendation}\nОшибка LLM: {e}"

        # прикрепляем к текущему тесту в Allure
        allure.attach(
            recommendation,
            name=f"Recommendation: {item.name}",
            attachment_type=allure.attachment_type.TEXT
        )
