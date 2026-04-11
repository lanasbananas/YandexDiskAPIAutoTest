from api.base_api import BaseAPI


class TrashAPI(BaseAPI):

    BASE_PATH = "/v1/disk/trash/resources"

    def get(self, path: str = None, limit: int = None, offset: int = None):
        params = {}
        if path:
            params["path"] = path
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self.request(
            "GET",
            self.BASE_PATH,
            params=params
        )

    def clear(self, path: str = None):
        params = {}
        if path:
            params["path"] = path

        return self.request(
            "DELETE",
            self.BASE_PATH,
            params=params
        )

    def restore(self, path: str, name: str = None, overwrite: bool = False):
        params = {"path": path}
        if name:
            params["name"] = name
        params["overwrite"] = overwrite

        return self.request(
            "PUT",
            f"{self.BASE_PATH}/restore",
            params=params
        )

    def restore_all(self, overwrite: bool = False):
        return self.restore(path="/", overwrite=overwrite)

    def get_size(self):
        response = self.get(limit=1)
        data = response.json()
        return data.get("total_size", 0)

    def get_count(self):
        response = self.get(limit=1)
        data = response.json()
        return data.get("total_count", 0)

    def delete_permanently(self, path: str):
        return self.request(
            "DELETE",
            self.BASE_PATH,
            params={"path": path, "permanently": True}
        )