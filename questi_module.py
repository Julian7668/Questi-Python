"""
Módulo Questi - Wrapper para questionary con manejo de errores y validaciones.

Este módulo proporciona una interfaz simplificada para questionary con:
- Manejo automático de salidas (Ctrl+C, ESC, etc.)
- Validaciones predefinidas para enteros y flotantes
- Mensajes personalizados por módulo
- Callbacks de salida personalizables

Example:
    >>> from questi_module import questi
    >>> nombre = questi.text("¿Cuál es tu nombre?")
    >>> edad = questi.text("¿Cuál es tu edad?", validate_user=int, inicio_rango=0, fin_rango=120)
"""

import sys
import time
import inspect
from functools import wraps
from typing import Callable, Union, Optional, Dict, Any, NoReturn
import questionary


class Questi:
    """
    Wrapper para questionary que añade manejo de errores y validaciones predefinidas.

    Esta clase proporciona métodos simplificados para crear interfaces de línea
    de comandos interactivas con validación automática y manejo de salidas elegante.

    Attributes:
        modulo_mensajes (Dict[str, str]): Diccionario con mensajes personalizados por archivo.
    """

    modulo_mensajes: Dict[str, str] = {
        "calculadora_de_calificaciones.py": "¡Gracias por usar la calculadora de calificaciones!",
        "generador_de_contrasenas.py": "¡Gracias por usar el generador de contraseñas!",
        "generador_de_excusas.py": "¡Gracias por usar el generador de excusas!",
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
            exit_callback (Optional[Callable[[], Any]]): Función a ejecutar antes de salir.
                Si es None, usa self.exit().

        Returns:
            Callable[[Callable[..., Any]], Callable[..., Any]]: Decorador que maneja las salidas de questionary.
        """

        def decorator(questionary_func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(questionary_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                if not (resultado := questionary_func(*args, **kwargs)):
                    if exit_callback:
                        return exit_callback()
                    return self.exit()
                return resultado

            return wrapper

        return decorator

    def text(
        self,
        mensaje: str = "Ingrese algun valor:",
        validate_user: type = str,
        inicio_rango: float = float("-inf"),
        fin_rango: float = float("inf"),
        what_return: type = str,
        use_strip: bool = True,
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> Union[str, int, float, bool]:
        """
        Solicita entrada de texto del usuario con validaciones opcionales.

        Este método permite solicitar texto, enteros o flotantes con validación automática
        según el tipo especificado en validate_user.

        Args:
            mensaje (str): Mensaje a mostrar al usuario. Defaults to "Ingrese algun valor:".
            validate_user (type): Tipo de validación a aplicar:
                - str: Validar que no esté vacío (string no vacío)
                - int: Validar entero dentro del rango especificado
                - float: Validar flotante dentro del rango especificado
                - Callable: Función personalizada de validación que recibe str y retorna bool
                Defaults to str.
            inicio_rango (float): Valor mínimo permitido para números. Defaults to float("-inf").
            fin_rango (float): Valor máximo permitido para números. Defaults to float("inf").
            what_return (type): Tipo de dato a retornar (str, int, float, bool). Defaults to str.
            use_strip (bool): Si aplicar strip() al resultado. Defaults to True.
            exit_callback (Optional[Callable[[], Any]]): Función a ejecutar si el usuario cancela.
                Defaults to None.

        Returns:
            Union[str, int, float, bool]: El valor ingresado convertido al tipo especificado.

        Raises:
            ValueError: Si el tipo de validación o retorno no es soportado.

        Example:
            >>> # Solicitar string no vacío
            >>> nombre = questi.text("¿Tu nombre?", validate_user=str)
            >>>
            >>> # Solicitar entero en rango específico
            >>> edad = questi.text("¿Tu edad?", validate_user=int, inicio_rango=0, fin_rango=120)
            >>>
            >>> # Solicitar flotante con rango
            >>> peso = questi.text("¿Tu peso (kg)?", validate_user=float, inicio_rango=0.0, fin_rango=300.0)
            >>>
            >>> # Usar validación personalizada
            >>> email = questi.text("¿Tu email?", validate_user=lambda x: "@" in x and "." in x)
        """

        def convert_result(
            resultado: str, what_return: type, use_strip: bool
        ) -> Union[str, int, float, bool]:
            """
            Convierte el resultado a el tipo especificado.

            Args:
                resultado (str): Cadena de texto a convertir.
                what_return (type): Tipo objetivo de conversión.
                use_strip (bool): Si aplicar strip() antes de convertir.

            Returns:
                Union[str, int, float, bool]: Resultado convertido al tipo especificado.

            Raises:
                ValueError: Si el tipo de retorno no es soportado.
            """
            if use_strip:
                resultado = resultado.strip()

            if what_return is str:
                return resultado
            if what_return in [int, float, bool]:
                return what_return(resultado)
            raise ValueError("Tipo de retorno no soportado")

        class Validates:
            """Clase interna con métodos de validación estáticos."""

            @staticmethod
            def validate_int(
                x: str,
                inicio_rango: float = float("-inf"),
                fin_rango: float = float("inf"),
            ) -> bool:
                """
                Valida que una cadena sea un entero válido dentro del rango especificado.

                Args:
                    x (str): Cadena a validar.
                    inicio_rango (float): Valor mínimo permitido. Defaults to float("-inf").
                    fin_rango (float): Valor máximo permitido. Defaults to float("inf").

                Returns:
                    bool: True si es un entero válido dentro del rango, False en caso contrario.
                """
                return (x.lstrip("-").isdigit()) and inicio_rango <= int(x) <= fin_rango

            @staticmethod
            def validate_float(
                x: str,
                inicio_rango: float = float("-inf"),
                fin_rango: float = float("inf"),
            ) -> bool:
                """
                Valida que una cadena sea un flotante válido dentro del rango especificado.

                Args:
                    x (str): Cadena a validar.
                    inicio_rango (float): Valor mínimo permitido. Defaults to float("-inf").
                    fin_rango (float): Valor máximo permitido. Defaults to float("inf").

                Returns:
                    bool: True si es un flotante válido dentro del rango, False en caso contrario.
                """
                return (
                    x.lstrip("-").replace(".", "", 1).isdigit() and x.count(".") <= 1
                ) and inicio_rango <= float(x) <= fin_rango

        @self._questi_handler(exit_callback)
        def _questi_text() -> Optional[Union[str, int, float]]:
            """
            Función interna que maneja la lógica de entrada de texto.

            Returns:
                Optional[Union[str, int, float]]: El valor ingresado o None si se cancela.
            """
            nonlocal what_return
            validaciones: Dict[type, Callable[[str], bool]] = {
                str: lambda x: x.strip() != "",
                int: lambda x: Validates.validate_int(
                    x.strip(), inicio_rango, fin_rango
                ),
                float: lambda x: Validates.validate_float(
                    x.strip(), inicio_rango, fin_rango
                ),
            }

            if isinstance(validate_user, type) and validate_user in validaciones:
                if resultado := questionary.text(
                    mensaje, validate=validaciones[validate_user]
                ).ask():
                    if validate_user in [int, float]:
                        what_return = validate_user

                    return convert_result(resultado, what_return, use_strip)
                return None  # en este punto, resultado y None son si o si iguales.

            if callable(validate_user):
                return questionary.text(mensaje, validate=validate_user).ask()

            raise ValueError("Tipo de validación no soportado")

        return _questi_text()

    def exit(self, mensaje: str = "¡Gracias por usar!") -> NoReturn:
        """
        Termina el programa elegantemente con un mensaje personalizado.

        Busca un mensaje específico para el archivo actual en modulo_mensajes,
        si no lo encuentra usa el mensaje por defecto.

        Args:
            mensaje (str): Mensaje por defecto si no hay uno específico para el módulo.
                Defaults to "¡Gracias por usar!".

        Raises:
            SystemExit: Siempre, con código 0 (salida exitosa).

        Example:
            >>> questi.exit("¡Hasta la vista!")
        """
        print(
            "\n",
            self.modulo_mensajes.get(
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
            reporte (str): Mensaje de error a mostrar. Defaults to "¡Algo salio mal!".

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
        opciones: Optional[list[str]] = None,
        what_return: type = str,
        indice: slice = slice(0, 1),
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> Union[str, int, float, bool]:
        """
        Muestra un menú de selección y retorna la opción elegida.

        Args:
            mensaje (str): Texto a mostrar arriba del menú.
                Defaults to "Elija alguna de las siguientes opciones:".
            opciones (Optional[list[str]]): Lista de opciones disponibles.
                Si es None, usa opciones por defecto ["A.", "B.", "C."]. Defaults to None.
            indice (slice): Índice del carácter a retornar de la opción seleccionada.
                Defaults to slice(0, 1).
            what_return (type): Tipo de dato a retornar (str, int, float, bool). Defaults to str.
            exit_callback (Optional[Callable[[], Any]]): Función a ejecutar si el usuario cancela.
                Defaults to None.

        Returns:
            Union[str, int, float, bool]: El carácter en la posición 'indice' de la opción
                seleccionada, convertido al tipo especificado.

        Raises:
            ValueError: Si el tipo de retorno no es soportado.

        Example:
            >>> opciones = ["1. Crear usuario", "2. Eliminar usuario", "3. Salir"]
            >>> eleccion = questi.select("¿Qué desea hacer?", opciones, slice(0, 1))
            >>> # Retorna "1", "2" o "3"
            >>>
            >>> # Para retornar como entero
            >>> opcion_num = questi.select("Elija:", opciones, what_return=int, indice=slice(0, 1))
        """

        def convert_result(
            resultado: str, what_return: type
        ) -> Union[str, int, float, bool]:
            """
            Convierte el resultado a el tipo especificado.

            Args:
                resultado (str): Cadena de texto a convertir.
                what_return (type): Tipo objetivo de conversión.

            Returns:
                Union[str, int, float, bool]: Resultado convertido al tipo especificado.

            Raises:
                ValueError: Si el tipo de retorno no es soportado.
            """
            if what_return == str:
                return resultado
            if what_return in [int, float, bool]:
                return what_return(resultado)
            raise ValueError("Tipo de retorno no soportado")

        @self._questi_handler(exit_callback)
        def _questi_select() -> Optional[Union[str, int, float, bool]]:
            """
            Función interna que maneja la lógica de selección.

            Returns:
                Optional[Union[str, int, float, bool]]: La opción seleccionada o None si se cancela.
            """
            choices = opciones if opciones else ["A.", "B.", "C."]
            if resultado := (questionary.select(mensaje, choices=choices).ask())[
                indice
            ]:
                return convert_result(resultado, what_return)
            return None  # en este punto, resultado y None son si o si iguales.

        return _questi_select()

    def confirm(
        self,
        mensaje: str,
        exit_callback: Optional[Callable[[], Any]] = None,
    ) -> bool:
        """
        Solicita confirmación del usuario (Sí/No).

        Args:
            mensaje (str): Pregunta de confirmación a mostrar.
            exit_callback (Optional[Callable[[], Any]]): Función a ejecutar si el usuario cancela.
                Defaults to None.

        Returns:
            bool: True si el usuario confirma, False si no.

        Example:
            >>> if questi.confirm("¿Está seguro de eliminar el archivo?"):
            ...     eliminar_archivo()
        """

        @self._questi_handler(exit_callback)
        def _questi_confirm() -> Optional[bool]:
            """
            Función interna que maneja la lógica de confirmación.

            Returns:
                Optional[bool]: True/False según la respuesta del usuario, None si se cancela.
            """
            return questionary.confirm(mensaje).ask()

        return _questi_confirm()


# Instancia global para facilitar el uso
questi: Questi = Questi()
