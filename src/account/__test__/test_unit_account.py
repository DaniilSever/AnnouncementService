import pytest
import pytest_asyncio
# from unittest.mock import AsyncMock, patch

from __mock__.mock_repo import MockAccRepo

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_repo():
    return MockAccRepo()

@pytest_asyncio.fixture(autouse=True, scope=function)
async def override(unit_app, mock_repo):
    unit_app.dependency_overrides[]