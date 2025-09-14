import os
import pytest
import shutil
from qa_agent.analyzer import generate_recommendation


# pytest-playwright provides 'page' fixture already.
# Мы добавим базовый url и вспомогательные фикстуры.

@pytest.fixture(scope="session")
def base_url():
    # Можно переопределить через env GIGA_BASE
    return os.getenv("GIGA_BASE", "https://giga.chat")


def pytest_sessionstart(session):
    allure_dir = os.path.join(os.getcwd(), "allure-results")
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
    os.makedirs(allure_dir)


# hook для прикрепления рекомендаций прямо во время выполнения теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # выполняем тест
    outcome = yield
    rep = outcome.get_result()

    # проверяем только фазу call (исполнение теста)
    if rep.when == "call" and rep.failed:
        recommendation = generate_recommendation(
            test_name=item.name,
            status='failed',
            message=str(rep.longrepr)
        )
        # прикрепляем к текущему тесту в Allure
        import allure
        allure.attach(
            recommendation,
            name=f"Recommendation: {item.name}",
            attachment_type=allure.attachment_type.TEXT
        )
