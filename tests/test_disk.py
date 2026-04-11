from utils.assertions import assert_status_code, assert_key_in_data

def test_get_disk_info(client):
    resp = client.disk.get_info()
    assert_status_code(resp, 200)
    data = resp.json()
    assert_key_in_data("total_space", data)