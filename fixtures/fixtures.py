import pytest
from utils.helpers import wait_for_async_operation, random_string


TEST_URL = "https://yandex.ru/"

@pytest.fixture(scope="function")
def tmp_file(client):
    filename = random_string()
    resp = client.resources.upload(filename, TEST_URL)
    if resp.status_code == 202:
        wait_for_async_operation(client, resp)

    yield filename
    delete_resp = client.resources.delete(filename)
    if delete_resp.status_code == 202:
        wait_for_async_operation(client, delete_resp)

@pytest.fixture(scope="function")
def tmp_dir(client):
    dirname = random_string()
    client.resources.create_folder(dirname)

    yield dirname
    delete_resp = client.resources.delete(dirname)
    if delete_resp.status_code == 202:
        wait_for_async_operation(client, delete_resp)

