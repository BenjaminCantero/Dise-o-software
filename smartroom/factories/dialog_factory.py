# smartroom/factories/dialog_factory.py

from gui.nueva_reserva_dialog import NuevaReservaDialog
from gui.editar_reserva_dialog import EditarReservaDialog
from gui.nueva_sala_dialog import NuevaSalaDialog
from gui.editar_sala_dialog import EditarSalaDialog
from gui.editar_usuario_dialog import EditarUsuarioDialog
#trabajar
class DialogFactory:
    """
    Fábrica centralizada para la creación de diálogos en la aplicación.

    Esta clase implementa el patrón de diseño Factory para desacoplar la
    lógica de instanciación de los diálogos del resto de la interfaz de
    usuario (GUI). Su objetivo es simplificar la creación de nuevas
    ventanas de diálogo y mejorar la mantenibilidad del código.

    Beneficios:
    - Desacopla la lógica de creación de objetos.
    - Facilita la extensión para nuevos tipos de diálogos.
    - Mejora la claridad y la estructura arquitectónica del proyecto.
    """

    def __init__(self, sala_service=None, user_service=None, reserva_service=None):
        """
        Inicializa la fábrica con los servicios necesarios que serán
        inyectados como dependencias en los diálogos que los requieran.

        Args:
            sala_service: El servicio para la gestión de salas.
            user_service: El servicio para la gestión de usuarios.
            reserva_service: El servicio para la gestión de reservas.
        """
        self._sala_service = sala_service
        self._user_service = user_service
        self._reserva_service = reserva_service

        # El mapa de diálogos relaciona un tipo (string) con su clase concreta.
        # Para agregar un nuevo diálogo, solo es necesario añadir una entrada aquí.
        self._dialog_map = {
            "nueva_reserva": NuevaReservaDialog,
            "editar_reserva": EditarReservaDialog,
            "nueva_sala": NuevaSalaDialog,
            "editar_sala": EditarSalaDialog,
            "editar_usuario": EditarUsuarioDialog,
        }

    def create_dialog(self, dialog_type, parent, *args, **kwargs):
        """
        Crea y retorna una instancia del diálogo solicitado.

        Este método selecciona la clase de diálogo adecuada a partir del mapa
        interno, inyecta las dependencias de servicios necesarias y pasa
        los argumentos adicionales al constructor del diálogo.

        Args:
            dialog_type (str): El tipo de diálogo a crear (e.g., 'nueva_sala').
            parent: El widget padre para el diálogo.
            *args: Argumentos posicionales para el constructor del diálogo.
            **kwargs: Argumentos de palabra clave para el constructor.

        Returns:
            Una instancia del diálogo solicitado.

        Raises:
            ValueError: Si el `dialog_type` no se encuentra en el mapa.
        """
        dialog_class = self._dialog_map.get(dialog_type)
        if not dialog_class:
            raise ValueError(f"El tipo de diálogo '{dialog_type}' no es válido.")

        # Inyección de dependencias basada en el tipo de diálogo.
        # Esto asegura que cada diálogo reciba solo los servicios que necesita.
        injected_kwargs = self._get_injected_dependencies(dialog_type)
        injected_kwargs.update(kwargs)

        return dialog_class(parent, *args, **injected_kwargs)

    def _get_injected_dependencies(self, dialog_type):
        """
        Determina qué dependencias de servicio inyectar según el tipo de diálogo.

        Args:
            dialog_type (str): El tipo de diálogo.

        Returns:
            Un diccionario con los servicios que deben ser inyectados.
        """
        dependencies = {}
        if "reserva" in dialog_type:
            dependencies['reserva_service'] = self._reserva_service
            dependencies['sala_service'] = self._sala_service
            dependencies['user_service'] = self._user_service
        elif "sala" in dialog_type:
            dependencies['sala_service'] = self._sala_service
        elif "usuario" in dialog_type:
            dependencies['user_service'] = self._user_service
        return dependencies
