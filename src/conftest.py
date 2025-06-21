import os
import pytest
# import pytest_asyncio
# from httpx import AsyncClient

from main import create_app

os.environ["APP_ENV"] = "test"


@pytest.fixture(scope="session")
def unit_app():
    app = create_app()
    app.title = "Unit Test"
    yield app
