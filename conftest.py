import pytest
from config.config import Config
from api.client import Client
from fixtures.fixtures import tmp_file, tmp_dir

@pytest.fixture(scope="session", autouse=True)
def validate_config():
    Config.validate()

@pytest.fixture(scope="session")
def client():
    return Client()