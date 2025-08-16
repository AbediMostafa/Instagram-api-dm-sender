
import os
import pytest


@pytest.fixture
def credentials():
    return {
        'username': os.getenv('TEST_USERNAME'),
        'username': os.getenv('TEST_USERNAME'),
    }