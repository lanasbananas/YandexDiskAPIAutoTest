from utils.helpers import fill_trash, wait_for_async_operation, clear_trash, delete_file
from utils.assertions import assert_status_code, assert_status_in, assert_match, assert_is_not_in


def test_move_to_trash_and_clear_all(client, tmp_file, tmp_dir):
    fill_trash(client, tmp_dir, tmp_file)
    resp = client.trash.get(f"trash:/")
    data = resp.json()
    trash_files = [item["path"] for item in data["_embedded"]["items"]]
    trash_tmp_dir = trash_files[-2]
    trash_tmp_file = trash_files[-1]

    resp_trash = client.trash.clear()
    if resp_trash.status_code == 202:
        wait_for_async_operation(client, resp_trash)
    assert_status_in(resp_trash, (200, 202, 204))

    trash_resp = client.trash.get(trash_tmp_file)
    assert_status_code(trash_resp, 404)
    trash_resp = client.trash.get(trash_tmp_dir)
    assert_status_code(trash_resp, 404)

def test_move_to_trash_and_clear_file(client, tmp_file, tmp_dir):
    fill_trash(client, tmp_dir, tmp_file)
    resp = client.trash.get(f"trash:/")
    data = resp.json()
    trash_files = [item["path"] for item in data["_embedded"]["items"]]
    trash_tmp_dir = trash_files[-2]
    trash_tmp_file = trash_files[-1]

    resp_trash = client.trash.clear(trash_tmp_file)
    if resp_trash.status_code == 202:
        wait_for_async_operation(client, resp_trash)
    assert_status_in(resp_trash, (200, 202, 204))

    trash_resp = client.trash.get(trash_tmp_file)
    assert_status_code(trash_resp, 404)

    trash_resp = client.trash.get(trash_tmp_dir)
    assert_status_code(trash_resp, 200)
    clear_trash(client)

def test_get_trash_info(client, tmp_file, tmp_dir):
    clear_trash(client)
    fill_trash(client, tmp_dir, tmp_file)

    resp = client.trash.get(f"trash:/")
    data = resp.json()
    trash_files = [item["name"] for item in data["_embedded"]["items"]]
    assert_status_code(resp, 200)
    assert_match([tmp_dir, tmp_file], trash_files)
    clear_trash(client)

def test_restore_trash(client, tmp_file, tmp_dir):
    clear_trash(client)
    fill_trash(client, tmp_dir, tmp_file)
    resp = client.trash.get(f"trash:/")
    data = resp.json()
    trash_files = [item["path"] for item in data["_embedded"]["items"]]
    trash_tmp_dir = trash_files[-2]
    trash_tmp_file = trash_files[-1]
    resp_restore = client.trash.restore(trash_tmp_file)
    if resp_restore.status_code == 202:
        wait_for_async_operation(client, resp_restore)
    assert_status_in(resp_restore, (200, 201, 202))
    resp = client.trash.get(f"trash:/")
    data = resp.json()
    trash_files = [item["name"] for item in data["_embedded"]["items"]]
    assert_is_not_in(tmp_file, trash_files)
    resp = client.resources.get_meta(tmp_file)
    assert_status_code(resp, 200)
    clear_trash(client)
    delete_file(client, tmp_file)
