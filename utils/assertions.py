def assert_status_code(response, expected):
    assert response.status_code == expected, \
        f"Ожидалось: {expected}, получено: {response.status_code}, \nОтвет сервера: {response.text}"

def assert_match(actual, expected):
    assert actual == expected, \
        f"Ожидалось: {expected}, получено: {actual}"

def assert_key_in_data(key, data):
    assert key in data, \
    f"{key} не найден. Поиск осуществлен в: {data}"

def assert_status_in(response, expected_codes):
    assert response.status_code in expected_codes, \
        f"Ожидалось: {expected_codes}, получено: {response.status_code}, \nОтвет сервера: {response.text}"

def assert_is_key_not_none(key):
    assert key, \
    f"{key} отсутствует."

def assert_is_not_in(key, data):
    assert key not in data, \
    f"{key} есть в {data}"