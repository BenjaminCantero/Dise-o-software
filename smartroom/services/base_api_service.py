from abc import ABC, abstractmethod

class BaseApiService(ABC):
    API_URL = "http://127.0.0.1:8000"
    HEADERS = {"Authorization": "Bearer secrettoken"}

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, id, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, id):
        pass