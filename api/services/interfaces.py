from abc import ABC, abstractmethod

class ISalaCRUDService(ABC):
    @abstractmethod
    def listar_salas(self, db):
        pass

    @abstractmethod
    def crear_sala(self, db, nombre, capacidad, estado="disponible"):
        pass

    @abstractmethod
    def editar_sala(self, db, sala_id, nombre=None, capacidad=None, estado=None):
        pass

    @abstractmethod
    def eliminar_sala(self, db, sala_id):
        pass

class IUsuarioCRUDService(ABC):
    @abstractmethod
    def listar_usuarios(self, db):
        pass

    @abstractmethod
    def crear_usuario(self, db, username, password, role):
        pass

    @abstractmethod
    def editar_usuario(self, db, user_id, username=None, password=None, role=None):
        pass

    @abstractmethod
    def eliminar_usuario(self, db, user_id):
        pass

class IAutenticacionService(ABC):
    @abstractmethod
    def autenticar(self, db, username, password):
        pass

class IReservaCRUDService(ABC):
    @abstractmethod
    def listar_reservas(self, db):
        pass

    @abstractmethod
    def crear_reserva(self, db, usuario_id, sala_id, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def editar_reserva(self, db, reserva_id, usuario_id=None, sala_id=None, fecha_inicio=None, fecha_fin=None):
        pass

    @abstractmethod
    def eliminar_reserva(self, db, reserva_id):
        pass