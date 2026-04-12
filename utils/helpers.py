import string
import random

def extract_operation_id(response):
    try:
        data = response.json()
        href = data.get("href")
        if not href:
            raise ValueError(f"В ответе нет ссылки: {data}")
        return href.split("/")[-1]
    except Exception as e:
        raise ValueError(f"Не удалось извлечь operation_id: {e}")

def wait_for_async_operation(client, resp):
    operation_id = extract_operation_id(resp)
    result = client.operations.wait(operation_id)
    assert result["status"] == "success", "Некорректный статус "

def get_public_key(client, file_path, public_settings):
    client.resources.publish(file_path, public_settings)
    resp = client.resources.get_meta(file_path)
    public_key = resp.json()["public_key"]
    return public_key

def fill_trash(client, path_dir, path_file):
    resp_del_dir = client.resources.delete(path_dir)
    if resp_del_dir.status_code == 202:
     wait_for_async_operation(client, resp_del_dir)

    resp_del_file = client.resources.delete(path_file)
    if resp_del_file.status_code == 202:
     wait_for_async_operation(client, resp_del_file)

def clear_trash(client):
    resp_trash = client.trash.clear()
    if resp_trash.status_code == 202:
        wait_for_async_operation(client, resp_trash)

def delete_file(client, file_path):
    resp = client.resources.delete(file_path)
    if resp.status_code == 202:
        wait_for_async_operation(client, resp)

def upload_file(client, file_path):
    resp = client.resources.upload(file_path, "https://yandex.ru/")
    if resp.status_code == 202:
        wait_for_async_operation(client, resp)

def random_string(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))