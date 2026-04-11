from api.base_api import BaseAPI

class DiskAPI(BaseAPI):

    BASE_PATH = "/v1/disk"

    def get_info(self):
        return self.request(
            "GET",
            self.BASE_PATH
        )