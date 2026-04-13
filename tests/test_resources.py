import time
from datetime import datetime
import pytest
from utils.helpers import wait_for_async_operation, delete_file, upload_file, random_string
from utils.assertions import assert_status_code, assert_match, assert_key_in_data, assert_status_in, assert_is_not_in


def test_get_meta(client, tmp_file):
    resp = client.resources.get_meta(tmp_file)
    assert_status_code(resp, 200)
    data = resp.json()
    assert_match(data["name"], tmp_file)

def test_publish_file(client, tmp_file):
    public_settings = {"read_only": True}
    pub_resp = client.resources.publish(tmp_file, public_settings)
    assert_status_code(pub_resp, 200)
    resp = client.resources.get_meta(tmp_file)
    data = resp.json()
    assert_key_in_data("public_key", data)

def test_unpublish_file(client, tmp_file):
    public_settings = {"read_only": True}
    client.resources.publish(tmp_file, public_settings)
    unpub_resp = client.resources.unpublish(tmp_file)
    assert_status_code(unpub_resp, 200)

def test_copy_file(client, tmp_file):
    copy_path = random_string()
    copy_resp = client.resources.copy(tmp_file, copy_path)
    if copy_resp.status_code == 202:
        wait_for_async_operation(client, copy_resp)
    assert_status_in(copy_resp, (200, 201, 202))
    resp = client.resources.get_meta(copy_path)
    assert_status_code(resp, 200)
    resp = client.resources.get_meta(tmp_file)
    assert_status_code(resp, 200)
    delete_file(client, copy_path)

def test_move_file(client, tmp_file):
    move_path = random_string()
    moved_file_name = "/"+random_string()
    client.resources.create_folder(move_path)
    move_resp = client.resources.move(tmp_file, move_path+moved_file_name)
    if (move_resp.status_code == 202):
        wait_for_async_operation(client, move_resp)
    assert_status_in(move_resp, (200, 201, 202))
    resp_new = client.resources.get_meta(move_path+moved_file_name)
    assert_status_code(resp_new, 200)

    resp_old = client.resources.get_meta(tmp_file)
    assert_status_code(resp_old, 404)
    delete_file(client, move_path)

def test_create_folder(client):
    folder_path = random_string()
    resp = client.resources.create_folder(folder_path)
    assert_status_in(resp, (200, 201))

    check_resp = client.resources.get_meta(folder_path)
    assert_status_code(check_resp, 200)
    delete_file(client, folder_path)

def test_upload_file(client):
    content = "https://yandex.ru/"
    file_path = random_string()
    resp = client.resources.upload(file_path, content)
    wait_for_async_operation(client, resp)
    assert_status_in(resp, (200, 202))

    check_resp = client.resources.get_meta(file_path)
    assert_status_code(check_resp, 200)
    delete_file(client, file_path)

def test_delete_file(client, tmp_file):
    delete_resp = client.resources.delete(tmp_file)
    if delete_resp.status_code == 202:
        wait_for_async_operation(client, delete_resp)
    assert_status_in(delete_resp, (200, 202, 204))

    resp = client.resources.get_meta(tmp_file)
    assert_status_code(resp, 404)

def test_update_custom_properties(client, tmp_dir):
    custom_properties = {'color': 'red'}
    resp = client.resources.update_custom_properties(tmp_dir, custom_properties)
    assert_status_code(resp, 200)
    data = resp.json()
    assert_match(custom_properties, data["custom_properties"])

def test_get_download_link(client, tmp_file):
    resp = client.resources.download(tmp_file)
    data = resp.json()
    assert_status_code(resp, 200)
    assert_key_in_data("https://downloader.disk.yandex.ru", data["href"])

def test_get_files_sorted_by_name(client):
    examples = ['b', 'a', 'b_1', 'рус', 'в', '5', '0', '_']
    try:
        for name in examples:
            upload_file(client, name)
        resp = client.resources.get_files()
        assert_status_code(resp, 200)
        data = resp.json()
        assert_key_in_data("items", data)
        items = data["items"]
        names = [item["name"] for item in items]
        assert_match(names,sorted(names))
    finally:
        for name in examples:
            delete_file(client, name)

def test_files_sorted_by_created_asc(client):
    examples = ['1', '2', '3', '4']
    try:
        for name in examples:
            upload_file(client, name)
            time.sleep(1)
        resp = client.resources.get_last_uploaded()
        assert_status_code(resp, 200)
        items = resp.json().get("items", [])
        created_dates = [
            datetime.fromisoformat(item["created"].replace("Z", "+00:00"))
            for item in items
            if "created" in item
        ]
        assert_match(created_dates, sorted(created_dates, reverse=True))
    finally:
        for name in examples:
            delete_file(client, name)

def test_get_public_files(client):
    public_settings = {"read_only": True}
    examples = ['1', '2', '3']
    try:
        for name in examples:
            upload_file(client, name)
        client.resources.publish(examples[0], public_settings)
        client.resources.publish(examples[2], public_settings)
        resp = client.resources.get_public_resources()
        assert_status_code(resp, 200)
        data = resp.json()
        names = [item["name"] for item in data["items"]]
        assert_key_in_data(examples[0], names)
        assert_key_in_data(examples[2], names)
        assert_is_not_in(examples[1], names)
    finally:
        for name in examples:
            delete_file(client, name)

@pytest.mark.xfail(reason='401')
def test_get_short_info(client, tmp_file):
    public_settings = {"read_only": False}
    client.resources.publish(tmp_file, public_settings)
    resp = client.resources.get_short_info(tmp_file)
    assert_status_code(resp, 200)

def test_get_link_for_download(client):
    path = random_string()
    resp = client.resources.get_upload_link(path)
    assert_status_code(resp, 200)
    data = resp.json()
    assert_key_in_data("https://uploader", data["href"])