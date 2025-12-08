import pytest

from tests.test_utils import create_test_app

@pytest.fixture(scope="session")
def client():
    client = create_test_app()
    return client