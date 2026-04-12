from utils.helpers import extract_operation_id, delete_file, random_string
from utils.assertions import assert_is_key_not_none, assert_status_code

def test_get_operation_id_async(client):
    file_path = random_string()
    resp = client.resources.upload(file_path, "https://yandex.ru/")
    operation_id = extract_operation_id(resp)
    resp = client.operations.get_status(operation_id)
    data = resp.json()
    status = data.get("status")
    assert_is_key_not_none(status)
    assert_status_code(resp, 200)
    delete_file(client, file_path)

