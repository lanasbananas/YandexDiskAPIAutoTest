from config.config import Config
from api.disk_api import DiskAPI
from api.resources_api import ResourcesAPI
from api.trash_api import TrashAPI
from api.public_resources_api import PublicResourcesAPI
from api.operations_api import OperationsAPI


class Client:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.token = Config.API_TOKEN

        # инициализация всех клиентов
        self.disk = DiskAPI(self.base_url, self.token)
        self.resources = ResourcesAPI(self.base_url, self.token)
        self.trash = TrashAPI(self.base_url, self.token)
        self.public = PublicResourcesAPI(self.base_url, self.token)
        self.operations = OperationsAPI(self.base_url, self.token)