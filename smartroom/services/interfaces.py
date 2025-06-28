from abc import ABC, abstractmethod

# ... interfaces de usuario ...

class IReservaCRUDService(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def update(self, reserva_id, **kwargs):
        pass

    @abstractmethod
    def delete(self, reserva_id):
        pass

class ISalaCRUDService(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, nombre, capacidad, estado):
        pass

    @abstractmethod
    def update(self, sala_id, nombre, capacidad, estado):
        pass

    @abstractmethod
    def delete(self, sala_id):
        pass

class IAutenticacionService(ABC):
    @abstractmethod
    def autenticar(self, username, password):
        pass

class IUsuarioCRUDService(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, username, password, role):
        pass

    @abstractmethod
    def update(self, user_id, username, role):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass