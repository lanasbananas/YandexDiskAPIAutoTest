import requests

class BaseAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"OAuth {token}"}

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return requests.request(method, url, headers=self.headers, **kwargs)