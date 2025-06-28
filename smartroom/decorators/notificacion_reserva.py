from abc import ABC, abstractmethod
from datetime import datetime

# 1. Interfaz base para los componentes
class Componente(ABC):
    @abstractmethod
    def operacion(self, datos):
        pass

# 2. Componente concreto
class ComponenteConcreto(Componente):
    def operacion(self, datos):
        print(f"Operacion principal ejecutada con datos: {datos}")
        return {"resultado": "exito", "datos": datos}

# 3. Decorador base
class Decorador(Componente):
    def __init__(self, componente: Componente):
        self._componente = componente

    def operacion(self, datos):
        return self._componente.operacion(datos)

# 4. Decorador de logging
class DecoradorLogging(Decorador):
    def operacion(self, datos):
        print(f"[{datetime.now()}] [LOG] Inicio de operacion con datos: {datos}")
        resultado = super().operacion(datos)
        print(f"[{datetime.now()}] [LOG] Fin de operacion. Resultado: {resultado}")
        return resultado

# 5. Decorador de validación
class DecoradorValidacion(Decorador):
    def operacion(self, datos):
        print("[VALIDACIÓN] Comprobando datos antes de la operacion")
        if not datos or not isinstance(datos, dict):
            raise ValueError("Los datos deben ser un diccionario no vacio")
        if "usuario" not in datos:
            raise ValueError("Falta el campo 'usuario' en los datos.")
        print("[VALIDACIÓN] Datos validos.")
        return super().operacion(datos)

# 6. Decorador de auditoría
class DecoradorAuditoria(Decorador):
    def operacion(self, datos):
        usuario = datos.get("usuario", "desconocido")
        print(f"[AUDITORIA] Usuario '{usuario}' está realizando una operacion.")
        resultado = super().operacion(datos)
        print(f"[AUDITORIA] Operacion registrada para el usuario '{usuario}'.")
        return resultado

# 7. Decorador de notificación (ejemplo adicional)
class DecoradorNotificacion(Decorador):
    def operacion(self, datos):
        resultado = super().operacion(datos)
        print(f"[NOTIFICACION] Se ha notificado al usuario '{datos.get('usuario', 'desconocido')}'.")
        return resultado

# Los decoradores están listos para ser usados en los servicios del sistema.
