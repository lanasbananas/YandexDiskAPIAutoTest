from api.base_api import BaseAPI


class ResourcesAPI(BaseAPI):
    BASE_PATH = "/v1/disk/resources"

    def delete(self, path, permanently=False):
        return self.request(
            "DELETE",
            self.BASE_PATH,
            params={
                "path": path,
                "permanently": permanently
            }
        )

    def get_meta(self, path):
        return self.request(
            "GET",
            self.BASE_PATH,
            params={"path": path}
        )

    def update_custom_properties(self, path: str, custom_properties: dict):
        return self.request(
            "PATCH",
            self.BASE_PATH,
            params={"path": path},
            json={"custom_properties": custom_properties}
        )

    def create_folder(self, path):
        return self.request(
            "PUT",
            self.BASE_PATH,
            params={"path": path}
        )

    def copy(self, from_path, to_path):
        return self.request(
            "POST",
            f"{self.BASE_PATH}/copy",
            params={"from": from_path, "path": to_path}
        )

    def download(self, path):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/download",
            params={"path": path}
        )

    def get_files(self):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/files",
            params={"sort": "name" }
        )

    def get_last_uploaded(self):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/last-uploaded"
        )

    def move(self, from_path, to_path):
        return self.request(
            "POST",
            f"{self.BASE_PATH}/move",
            params={"from": from_path, "path": to_path}
        )

    def get_public_resources(self):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/public"
        )

    def publish(self, path: str, public_settings: dict):
        return self.request(
            "PUT",
            f"{self.BASE_PATH}/publish",
            params={"path": path},
            json={"public_settings": public_settings}
        )

    def get_short_info(self, path):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/short-info",
            params={"path": path}
        )

    def unpublish(self, path):
        return self.request(
            "PUT",
            f"{self.BASE_PATH}/unpublish",
            params={"path": path}
        )

    def get_upload_link(self, path):
        """Получить ссылку для загрузки файла"""
        return self.request(
            "GET",
            f"{self.BASE_PATH}/upload",
            params={"path": path}
        )

    def upload(self, path, url):
        return self.request(
            "POST",
            f"{self.BASE_PATH}/upload",
            params={"path": path, "url": url}
        )

