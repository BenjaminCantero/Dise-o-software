from abc import ABC, abstractmethod

# ... interfaces de usuario ...

class IReservaCRUDService(ABC):
    @abstractmethod
    def get_reservas(self):
        pass

    @abstractmethod
    def create_reserva(self, usuario_id, sala_id, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def update_reserva(self, reserva_id, usuario_id, sala_id, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def delete_reserva(self, reserva_id):
        pass

class ISalaCRUDService(ABC):
    @abstractmethod
    def get_salas(self):
        pass

    @abstractmethod
    def create_sala(self, nombre, capacidad, estado):
        pass

    @abstractmethod
    def update_sala(self, sala_id, nombre, capacidad, estado):
        pass

    @abstractmethod
    def delete_sala(self, sala_id):
        pass

class IAutenticacionService(ABC):
    @abstractmethod
    def autenticar(self, username, password):
        pass

class IUsuarioCRUDService(ABC):
    @abstractmethod
    def get_usuarios(self):
        pass

    @abstractmethod
    def create_usuario(self, username, password, role):
        pass

    @abstractmethod
    def update_usuario(self, user_id, username, role):
        pass

    @abstractmethod
    def delete_usuario(self, user_id):
        pass