import pytest
from utils.helpers import wait_for_async_operation

TEST_FOLDER_PATH = "test_folder"
TEST_FILE_NAME = "test.txt"
TEST_URL = "https://yandex.ru/"

@pytest.fixture(scope="function")
def tmp_file(client):
    resp = client.resources.upload(TEST_FILE_NAME, TEST_URL)
    wait_for_async_operation(client, resp)

    yield TEST_FILE_NAME
    delete_resp = client.resources.delete(TEST_FILE_NAME)
    if delete_resp.status_code == 202:
        wait_for_async_operation(client, delete_resp)

@pytest.fixture(scope="function")
def tmp_dir(client):
    client.resources.create_folder(TEST_FOLDER_PATH)

    yield TEST_FOLDER_PATH
    delete_resp = client.resources.delete(TEST_FOLDER_PATH)
    if delete_resp.status_code == 202:
        wait_for_async_operation(client, delete_resp)

