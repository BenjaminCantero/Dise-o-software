from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def crear(self, db, *args, **kwargs):
        pass

    @abstractmethod
    def obtener(self, db, id):
        pass

    @abstractmethod
    def actualizar(self, db, id, *args, **kwargs):
        pass

    @abstractmethod
    def eliminar(self, db, id):
        pass