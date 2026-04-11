from api.base_api import BaseAPI


class PublicResourcesAPI(BaseAPI):

    BASE_PATH = "/v1/disk/public/resources"

    def get_public_meta(self, public_key: str):
        return self.request(
            "GET",
            self.BASE_PATH,
            params={"public_key": public_key}
        )

    def download(self, public_key: str):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/download",
            params={"public_key": public_key}
        )

    def update_public_settings(
            self,
            path: str,
            public_settings: dict
    ):
        return self.request(
            "PATCH",
            f"{self.BASE_PATH}/public-settings",
            params={"path": path},
            json=public_settings
        )

    def save_to_disk(self, public_key: str, save_path: str = None):
        params = {"public_key": public_key}
        if save_path:
            params["save_path"] = save_path

        return self.request(
            "POST",
            f"{self.BASE_PATH}/save-to-disk",
            params=params
        )

    def get_direct_link(self, public_key: str):
        response = self.download(public_key)
        return response.json().get("href")