import os
import pytest

# pytest-playwright provides 'page' fixture already.
# Мы добавим базовый url и вспомогательные фикстуры.

@pytest.fixture(scope="session")
def base_url():
    # Можно переопределить через env GIGA_BASE
    return os.getenv("GIGA_BASE", "https://giga.chat")
