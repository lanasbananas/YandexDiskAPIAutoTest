from api.base_api import BaseAPI
from utils.waiters import wait_operation

class OperationsAPI(BaseAPI):

    BASE_PATH = "/v1/disk/operations"

    def get_status(self, operation_id):
        return self.request(
            "GET",
            f"{self.BASE_PATH}/{operation_id}"
        )

    def wait(self, operation_id, timeout=15):
        return wait_operation(self, operation_id, timeout)