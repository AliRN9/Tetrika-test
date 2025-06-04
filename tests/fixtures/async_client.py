from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def async_client_mock():
    return AsyncMock()
