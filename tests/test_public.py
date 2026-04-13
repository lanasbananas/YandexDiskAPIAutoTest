import pytest
from utils.helpers import get_public_key, wait_for_async_operation
from utils.assertions import assert_status_code, assert_match, assert_key_in_data, assert_status_in
from urllib.parse import urlparse, parse_qs

def test_get_public_meta(client, tmp_file):
    public_settings = {"read_only": True}
    public_key = get_public_key(client, tmp_file, public_settings)
    resp_get_meta = client.public.get_public_meta(public_key)
    assert_status_code(resp_get_meta, 200)
    data = resp_get_meta.json()
    assert_match(data["name"], tmp_file)

def test_get_download_link_public(client, tmp_file):
    public_settings = {"read_only": True}
    public_key = get_public_key(client, tmp_file, public_settings)
    resp = client.public.download(public_key)
    assert_status_code(resp, 200)
    data = resp.json()
    assert_key_in_data("https://downloader.disk.yandex.ru/disk", data["href"])

@pytest.mark.xfail(reason='404')
def test_update_public(client, tmp_file):
    public_settings_update = {
          "available_until": 7643934
        }
    public_settings = {"read_only": False}
    resp = client.resources.publish(tmp_file, public_settings)
    data = resp.json()
    path = data["href"].split('path=')[1]
    resp_upload = client.public.update_public_settings(path, public_settings_update)
    assert_status_code(resp_upload, 200)

def test_download_public(client, tmp_file):
    public_settings = {"read_only": True}
    public_key = get_public_key(client, tmp_file, public_settings)
    resp_download = client.public.download(public_key)
    if resp_download.status_code == 202:
        wait_for_async_operation(client, resp_download)
    assert_status_in(resp_download, (200, 201, 202))
    data = resp_download.json()
    assert_key_in_data("https://downloader.disk.yandex.ru/disk", data["href"])

