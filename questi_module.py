"""
Módulo Questi - Wrapper para questionary con manejo de errores y validaciones.

Este módulo proporciona una interfaz simplificada para questionary con:
- Manejo automático de salidas (Ctrl+C, ESC, etc.)
- Validaciones predefinidas para enteros y flotantes
- Mensajes personalizados por módulo
- Callbacks de salida personalizables

Ejemplo:
    >>> from questi_module import questi
    >>> nombre = questi.text("¿Cuál es tu nombre?")
    >>> edad = questi.text("¿Cuál es tu edad?", validate_user=2.0, inicio_rango=0, fin_rango=120)
"""

from functools import wraps
import sys
import time
import inspect
from typing import Callable, Union, Optional, Dict, Any, NoReturn
import questionary


class Questi:
    """
    Wrapper para questionary que añade manejo de errores y validaciones predefinidas.

    Esta clase proporciona métodos simplificados para crear interfaces de línea
    de comandos interactivas con validación automática y manejo de salidas elegante.

    Attributes:
        modulo_mensajes: Diccionario con mensajes personalizados por archivo.
    """

    modulo_mensajes: Dict[str, str] = {
        "calculadora_de_calificaciones.py": "¡Gracias por usar la calculadora de calificaciones!",
        "generador_de_contrasenas.py": "¡Gracias por usar el generador de contraseñas!",
    }

    def _questi_handler(
        self,
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Decorador interno para manejar salidas (Ctrl+C, ESC) en funciones questionary.

        Cuando el usuario cancela una pregunta (retorna None), ejecuta el callback
        de salida o termina el programa elegantemente.

        Args:
            exit_callback: Función a ejecutar antes de salir. Si es None, usa self.exit().

        Returns:
            Decorador que maneja las salidas de questionary.
        """

        def decorator(questionary_func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(questionary_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                if resultado := questionary_func(*args, **kwargs):
                    return resultado
                if exit_callback:
                    return exit_callback()
                return questi.exit()

            return wrapper

        return decorator

    def text(
        self,
        mensaje: str = "Ingrese algun valor:",
        validate_user: Union[float, Callable[[str], bool]] = 1.0,
        inicio_rango: float = float("-inf"),
        fin_rango: float = float("inf"),
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> str:
        """Solicita entrada de texto al usuario con validación personalizable.

        Este método proporciona una interfaz para obtener input del usuario con diferentes
        tipos de validación predefinidas o personalizadas, incluyendo validación de texto,
        enteros y flotantes con rangos opcionales.

        Args:
            mensaje (str, optional): Mensaje que se muestra al usuario para solicitar
                la entrada. Defaults to "Ingrese algun valor:".
            validate_user (Union[float, Callable[[str], bool]], optional): Tipo de
                validación a aplicar. Puede ser:
                - 1.0: Texto no vacío
                - 2.0: Entero dentro del rango [inicio_rango, fin_rango]
                - 2.1: Entero >= inicio_rango
                - 2.2: Entero <= fin_rango
                - 3.0: Float dentro del rango [inicio_rango, fin_rango]
                - 3.1: Float >= inicio_rango
                - 3.2: Float <= fin_rango
                - Callable: Función personalizada de validación
                Defaults to 1.0.
            inicio_rango (float, optional): Valor mínimo para validaciones numéricas.
                Defaults to float("-inf").
            fin_rango (float, optional): Valor máximo para validaciones numéricas.
                Defaults to float("inf").
            exit_callback (Optional[Callable[[], Any]], optional): Función callback
                a ejecutar en caso de salida. Defaults to None.

        Returns:
            str: El texto ingresado por el usuario que ha pasado la validación.

        Raises:
            ValueError: Si validate_user no es un tipo de validación válido.

        Examples:
            >>> # Solicitar texto no vacío
            >>> texto = self.text("Ingrese su nombre:")

            >>> # Solicitar entero en rango específico
            >>> edad = self.text("Ingrese su edad:", 2.0, 0, 120)

            >>> # Solicitar float mayor a cero
            >>> precio = self.text("Ingrese el precio:", 3.1, 0.01)

            >>> # Validación personalizada
            >>> email = self.text("Email:", lambda x: "@" in x and "." in x)
        """

        def validate_int_range(
            x: str, min_val: float = float("-inf"), max_val: float = float("inf")
        ) -> bool:
            """Valida que una cadena sea un entero dentro del rango especificado.

            Args:
                x (str): Cadena a validar.
                min_val (float, optional): Valor mínimo permitido.
                    Defaults to float("-inf").
                max_val (float, optional): Valor máximo permitido.
                    Defaults to float("inf").

            Returns:
                bool: True si la cadena es un entero válido dentro del rango,
                    False en caso contrario.
            """
            x = x.strip()
            return is_int(x) and min_val <= int(x) <= max_val

        def is_int(x: str) -> bool:
            """Verifica si una cadena representa un número entero.

            Args:
                x (str): Cadena a verificar.

            Returns:
                bool: True si la cadena representa un entero, False en caso contrario.
            """
            return x.lstrip("-").isdigit()

        def validate_float_range(
            x: str, min_val: float = float("-inf"), max_val: float = float("inf")
        ) -> bool:
            """Valida que una cadena sea un float dentro del rango especificado.

            Args:
                x (str): Cadena a validar.
                min_val (float, optional): Valor mínimo permitido.
                    Defaults to float("-inf").
                max_val (float, optional): Valor máximo permitido.
                    Defaults to float("inf").

            Returns:
                bool: True si la cadena es un float válido dentro del rango,
                    False en caso contrario.
            """
            x = x.strip()
            return is_float(x) and min_val <= float(x) <= max_val

        def is_float(x: str) -> bool:
            """Verifica si una cadena representa un número flotante.

            Args:
                x (str): Cadena a verificar.

            Returns:
                bool: True si la cadena representa un float, False en caso contrario.
            """
            return x.lstrip("-").replace(".", "", 1).isdigit() and x.count(".") <= 1

        @self._questi_handler(exit_callback)
        def _questi_text() -> Optional[str]:
            """Función interna que maneja la lógica de solicitud de texto.

            Returns:
                Optional[str]: El texto ingresado por el usuario o None si se cancela.

            Raises:
                ValueError: Si el tipo de validación no es reconocido.
            """
            validaciones: Dict[float, Callable[[str], bool]] = {
                1.0: lambda x: x.strip() != "",
                2.0: lambda x: validate_int_range(x, inicio_rango, fin_rango),
                2.1: lambda x: validate_int_range(x, inicio_rango),
                2.2: lambda x: validate_int_range(x, max_val=fin_rango),
                3.0: lambda x: validate_float_range(x, inicio_rango, fin_rango),
                3.1: lambda x: validate_float_range(x, inicio_rango),
                3.2: lambda x: validate_float_range(x, max_val=fin_rango),
            }

            # Mucha comprobacion sin necesidad ya que validate_user lo da el programador no el usuario pero bueno. Lo pide Pylance
            if isinstance(validate_user, float) and validate_user in validaciones:
                return questionary.text(
                    mensaje, validate=validaciones[validate_user]
                ).ask()
            if callable(validate_user):
                return questionary.text(mensaje, validate=validate_user).ask()
            return questi.exit_error(
                "Revise las validaciones disponibles; Ingrese su propio lambda si asi lo desea."
            )

        return _questi_text()

    def exit(self, mensaje: str = "¡Gracias por usar!") -> NoReturn:
        """
        Termina el programa elegantemente con un mensaje personalizado.

        Busca un mensaje específico para el archivo actual en modulo_mensajes,
        si no lo encuentra usa el mensaje por defecto.

        Args:
            mensaje: Mensaje por defecto si no hay uno específico para el módulo.

        Raises:
            SystemExit: Siempre, con código 0 (salida exitosa).

        Example:
            >>> questi.exit("¡Hasta la vista!")
        """
        print(
            "\n",
            questi.modulo_mensajes.get(
                inspect.stack()[1].filename.split("\\")[-1],
                mensaje,
            ),
        )
        time.sleep(1)
        sys.exit(0)

    def exit_error(self, reporte: str = "¡Algo salio mal!") -> NoReturn:
        """
        Termina el programa con un mensaje de error.

        Args:
            reporte: Mensaje de error a mostrar.

        Raises:
            SystemExit: Siempre, con código 1 (error).

        Example:
            >>> questi.exit_error("Error: No se pudo conectar a la base de datos")
        """
        print(f"\n{reporte}")
        time.sleep(1)
        sys.exit(1)

    def select(
        self,
        mensaje: str = "Elija alguna de las siguientes opciones:",
        opciones: list[str] | None = None,
        indice: int = 0,
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> str:
        """
        Muestra un menú de selección y retorna la opción elegida.

        Args:
            mensaje: Texto a mostrar arriba del menú.
            opciones: Lista de opciones disponibles. Si es None, usa opciones por defecto.
            indice: Índice del carácter a retornar de la opción seleccionada (por defecto 0).
            exit_callback: Función a ejecutar si el usuario cancela.

        Returns:
            str: El carácter en la posición 'indice' de la opción seleccionada.

        Example:
            >>> opciones = ["1. Crear usuario", "2. Eliminar usuario", "3. Salir"]
            >>> eleccion = questi.select("¿Qué desea hacer?", opciones, indice=0)
            >>> # Retorna "1", "2" o "3"
        """

        @self._questi_handler(exit_callback)
        def _questi_select() -> Optional[str]:
            choices = opciones if opciones else ["A.", "B.", "C."]
            return (questionary.select(mensaje, choices=choices).ask())[indice]

        return _questi_select()

    def confirm(
        self,
        mensaje: str,
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> bool:
        """
        Solicita confirmación del usuario (Sí/No).

        Args:
            mensaje: Pregunta de confirmación a mostrar.
            exit_callback: Función a ejecutar si el usuario cancela.

        Returns:
            bool: True si el usuario confirma, False si no.

        Example:
            >>> if questi.confirm("¿Está seguro de eliminar el archivo?"):
            ...     eliminar_archivo()
        """

        @self._questi_handler(exit_callback)
        def _questi_confirm() -> Optional[bool]:
            return questionary.confirm(mensaje).ask()

        return _questi_confirm()


# Instancia global para facilitar el uso
questi: Questi = Questi()
