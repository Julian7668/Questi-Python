"""
Instancia global de la clase Questi para uso directo en aplicaciones.

Esta instancia permite usar las funcionalidades de Questi sin necesidad de crear
una nueva instancia cada vez. Es la forma recomendada de usar la clase en la
mayoría de casos.

Examples:
    >>> from questi_module import questi
    >>> nombre = questi.text("Su nombre:")
    >>> confirmado = questi.confirm("¿Continuar?")
    >>> questi.exit()
"""

from functools import wraps
import sys
import time
import inspect
from typing import Callable, Union, Optional, Dict, Any, NoReturn
import questionary


class Questi:
    """
    Una clase wrapper para questionary que proporciona validaciones automáticas y manejo elegante de salidas.

    Esta clase encapsula las funcionalidades de questionary añadiendo validaciones predefinidas,
    manejo automático de errores y salidas personalizadas según el módulo que la utilice.
    Simplifica la creación de interfaces de línea de comandos interactivas con validación robusta.

    Attributes:
        modulo_mensajes (Dict[str, str]): Diccionario que mapea nombres de archivos Python
            a mensajes de despedida personalizados. Permite mostrar mensajes específicos
            según el módulo que esté utilizando la clase.

    Examples:
        Uso básico:
            >>> questi = Questi()
            >>> nombre = questi.text("Ingrese su nombre:")
            >>> edad = questi.text("Ingrese su edad:", validate_user=2.0, inicio_rango=0, fin_rango=120)
            >>> confirmacion = questi.confirm("¿Está seguro?")

        Con validaciones personalizadas:
            >>> email = questi.text("Email:", validate_user=lambda x: "@" in x and "." in x)
            >>> opcion = questi.select("Elija una opción:", ["Opción 1", "Opción 2", "Opción 3"])
    """

    modulo_mensajes: Dict[str, str] = {
        "calculadora_de_calificaciones.py": "¡Gracias por usar la calculadora de calificaciones!",
        "generador_de_contrasenas.py": "¡Gracias por usar el generador de contraseñas!",
    }

    def _questi_handler(
        self, questionary_func: Callable[..., Any]
    ) -> Callable[..., Any]:
        """
        Decorador interno que maneja las respuestas de questionary y las salidas automáticas.

        Este método privado envuelve las funciones de questionary para proporcionar un
        comportamiento consistente: si el usuario cancela la operación (Ctrl+C o ESC),
        automáticamente llama al método exit() para terminar el programa elegantemente.

        Args:
            questionary_func (Callable[..., Any]): Función de questionary a envolver.
                Debe ser una función que retorne un valor o None si es cancelada.

        Returns:
            Callable[..., Any]: Función wrapper que maneja automáticamente las salidas.
                Si la función original retorna un valor válido, lo devuelve tal como está.
                Si retorna None (cancelación), ejecuta exit() y termina el programa.

        Note:
            Este es un método privado y no debe ser llamado directamente por el usuario.
            Se utiliza internamente para envolver todas las funciones de entrada.
        """

        @wraps(questionary_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if entrada := questionary_func(*args, **kwargs):
                return entrada
            return Questi().exit()

        return wrapper

    def text(
        self,
        mensaje: str,
        validate_user: Union[float, Callable[[str], bool]] = 1.0,
        inicio_rango: float = float("-inf"),
        fin_rango: float = float("inf"),
    ) -> str:
        """
        Solicita entrada de texto del usuario con validaciones predefinidas o personalizadas.

        Este método proporciona una interfaz simplificada para obtener entrada de texto
        con múltiples tipos de validación incorporados. Soporta validaciones para texto
        simple, números enteros, números decimales, y rangos específicos.

        Args:
            mensaje (str): El mensaje/prompt que se mostrará al usuario.
                Debe ser descriptivo y claro sobre qué se espera.
            validate_user (Union[float, Callable[[str], bool]], optional):
                Tipo de validación a aplicar. Defaults to 1.0.
                Opciones predefinidas:
                - 1.0: Texto no vacío (solo espacios no cuenta como válido)
                - 2.0: Número entero dentro del rango [inicio_rango, fin_rango]
                - 2.1: Número entero mayor o igual a inicio_rango
                - 2.2: Número entero menor o igual a fin_rango
                - 3.0: Número decimal dentro del rango [inicio_rango, fin_rango]
                - 3.1: Número decimal mayor o igual a inicio_rango
                - 3.2: Número decimal menor o igual a fin_rango
                - Callable: Función personalizada que recibe str y retorna bool
            inicio_rango (float, optional): Límite inferior para validaciones numéricas.
                Defaults to float("-inf"). Solo aplica para validaciones 2.x y 3.x.
            fin_rango (float, optional): Límite superior para validaciones numéricas.
                Defaults to float("inf"). Solo aplica para validaciones 2.x y 3.x.

        Returns:
            str: La entrada del usuario validada. Garantiza que cumple con los criterios
                especificados en validate_user.

        Raises:
            SystemExit: Si validate_user no es un valor válido o función callable.
                También se ejecuta si el usuario cancela la entrada (Ctrl+C).

        Examples:
            Validaciones básicas:
                >>> name = questi.text("Nombre completo:")  # Solo texto no vacío
                >>> age = questi.text("Edad:", 2.0, 0, 120)  # Entero entre 0 y 120
                >>> price = questi.text("Precio:", 3.1, 0)  # Decimal mayor a 0

            Validación personalizada:
                >>> email = questi.text("Email:", lambda x: "@" in x and len(x) > 5)
                >>> codigo = questi.text("Código:", lambda x: x.upper().startswith("ABC"))

        Note:
            Los números decimales deben usar punto (.) como separador decimal.
            La validación de rangos es inclusiva en ambos extremos.
        """

        @self._questi_handler
        def _questi_text() -> Optional[str]:
            validaciones: Dict[float, Callable[[str], bool]] = {
                1.0: lambda x: x.strip() != "",
                2.0: lambda x: x.strip() != ""
                and x.isdigit()
                and inicio_rango <= int(x) <= fin_rango,
                2.1: lambda x: x.strip() != ""
                and x.isdigit()
                and inicio_rango <= int(x),
                2.2: lambda x: x.strip() != "" and x.isdigit() and int(x) <= fin_rango,
                3.0: lambda x: x.strip() != ""
                and x.replace(".", "", 1).isdigit()
                and x.count(".") <= 1
                and inicio_rango <= float(x) <= fin_rango,
                3.1: lambda x: x.strip() != ""
                and x.replace(".", "", 1).isdigit()
                and x.count(".") <= 1
                and inicio_rango <= float(x),
                3.2: lambda x: x.strip() != ""
                and x.replace(".", "", 1).isdigit()
                and x.count(".") <= 1
                and float(x) <= fin_rango,
            }
            # Mucha comprobacion sin necesidad ya que validate_user lo da el progamador no el usuario pero bueno. Lo pide Pylance
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

    def exit(self, mensaje="¡Gracias por usar!") -> NoReturn:
        """
        Termina el programa de manera elegante con un mensaje de despedida personalizado.

        Este método proporciona una salida limpia del programa, mostrando un mensaje
        personalizado según el módulo que esté ejecutándose. Si el módulo actual está
        registrado en modulo_mensajes, usa ese mensaje; de lo contrario, usa el mensaje
        por defecto proporcionado.

        Args:
            mensaje (str, optional): Mensaje de despedida por defecto si no se encuentra
                un mensaje específico para el módulo actual. Defaults to "¡Gracias por usar!".

        Returns:
            NoReturn: Esta función nunca retorna ya que termina el programa con sys.exit(0).

        Note:
            - Añade una pausa de 1 segundo antes de terminar para que el usuario pueda leer el mensaje.
            - Utiliza inspect.stack() para determinar automáticamente el nombre del archivo que llama.
            - La salida es con código 0 (éxito).

        Examples:
            Salida con mensaje por defecto:
                >>> questi.exit()  # Muestra "¡Gracias por usar!"

            Salida con mensaje personalizado:
                >>> questi.exit("¡Hasta la vista!")

            Salida automática (desde calculadora_de_calificaciones.py):
                >>> questi.exit()  # Muestra "¡Gracias por usar la calculadora de calificaciones!"
        """
        print(
            "\n",
            Questi().modulo_mensajes.get(
                inspect.stack()[1].filename.split("\\")[-1],
                mensaje,
            ),
        )
        time.sleep(1)
        sys.exit(0)

    def exit_error(self, reporte="¡Algo salio mal!") -> NoReturn:
        """
        Termina el programa con un mensaje de error y código de salida de falla.

        Este método se utiliza para terminar el programa cuando ocurre un error
        irrecuperable. Muestra el mensaje de error y termina con código de salida 1,
        indicando que el programa terminó debido a un error.

        Args:
            reporte (str, optional): Mensaje de error a mostrar al usuario.
                Debe ser descriptivo del problema ocurrido.
                Defaults to "¡Algo salio mal!".

        Returns:
            NoReturn: Esta función nunca retorna ya que termina el programa con sys.exit(1).

        Note:
            - Añade una pausa de 1 segundo antes de terminar para que el usuario pueda leer el error.
            - La salida es con código 1 (error).
            - Se utiliza internamente cuando las validaciones fallan o hay errores de configuración.

        Examples:
            Error genérico:
                >>> questi.exit_error()  # Muestra "¡Algo salio mal!"

            Error específico:
                >>> questi.exit_error("Archivo de configuración no encontrado")
                >>> questi.exit_error("Formato de datos inválido en línea 15")
        """
        print(f"\n{reporte}")
        time.sleep(1)
        sys.exit(1)

    def select(
        self,
        mensaje: str = "Elija alguna de las siguientes opciones:",
        opciones: list[str] | None = None,
    ) -> str:
        """
        Presenta una lista de opciones al usuario para que seleccione una usando las flechas del teclado.

        Este método crea un menú interactivo donde el usuario puede navegar entre las opciones
        usando las flechas del teclado y seleccionar con Enter. Proporciona una interfaz
        más intuitiva que escribir texto para selecciones múltiples. Si no se proporcionan
        opciones, utiliza opciones por defecto ["A.", "B.", "C."].

        Args:
            mensaje (str, optional): El mensaje/prompt que se mostrará encima de las opciones.
                Debe explicar claramente qué se está seleccionando.
                Defaults to "Elija alguna de las siguientes opciones:".
            opciones (list[str] | None, optional): Lista de strings que representan las opciones
                disponibles. Cada string será una opción seleccionable en el menú.
                Si es None, se usarán opciones por defecto ["A.", "B.", "C."].
                Defaults to None.

        Returns:
            str: El primer carácter de la opción seleccionada por el usuario.
                Por ejemplo, si selecciona "Crear archivo", retorna "C".
                Si usa opciones por defecto y selecciona "A.", retorna "A".

        Raises:
            SystemExit: Si el usuario cancela la selección (Ctrl+C o ESC).

        Examples:
            Menú con opciones por defecto:
                >>> opcion = questi.select()  # Usa mensaje y opciones por defecto
                >>> print(f"Seleccionó: {opcion}")  # Imprime "A", "B", o "C"

            Menú simple personalizado:
                >>> opcion = questi.select("Seleccione una opción:", ["Crear", "Editar", "Eliminar"])
                >>> print(f"Seleccionó: {opcion}")  # Imprime "C", "E", o "E"

            Menú de configuración:
                >>> tema = questi.select(
                ...     "Elija el tema de la aplicación:",
                ...     ["Claro", "Oscuro", "Automático"]
                ... )  # Retorna "C", "O", o "A"

            Menú solo con mensaje personalizado:
                >>> nivel = questi.select("Seleccione el nivel:")
                # Muestra ["A.", "B.", "C."] y retorna "A", "B", o "C"

        Note:
            - El usuario navega con las flechas arriba/abajo del teclado.
            - Se selecciona con Enter.
            - Se puede cancelar con Ctrl+C o ESC (esto termina el programa).
            - La primera opción aparece seleccionada por defecto.
            - IMPORTANTE: Solo retorna el primer carácter de la opción seleccionada, no la opción completa.
            - Si no proporciona opciones, automáticamente usa ["A.", "B.", "C."].
        """

        @self._questi_handler
        def _questi_select() -> Optional[str]:
            choices = opciones if opciones else ["A.", "B.", "C."]
            return (questionary.select(mensaje, choices=choices).ask())[0]

        return _questi_select()

    def confirm(self, mensaje: str) -> bool:
        """
        Solicita una confirmación sí/no del usuario.

        Este método presenta una pregunta de confirmación al usuario que debe responder
        con 'y' (yes/sí) o 'n' (no). Es útil para confirmar acciones importantes,
        eliminar datos, o cualquier operación que requiera confirmación explícita.

        Args:
            mensaje (str): La pregunta de confirmación a mostrar al usuario.
                Debe estar formulada de manera que una respuesta "sí" indique
                confirmación y "no" indique cancelación.

        Returns:
            bool: True si el usuario confirma (responde 'y'), False si rechaza (responde 'n').

        Raises:
            SystemExit: Si el usuario cancela la confirmación (Ctrl+C o ESC).

        Examples:
            Confirmación de eliminación:
                >>> if questi.confirm("¿Está seguro de que desea eliminar este archivo?"):
                ...     eliminar_archivo()
                ... else:
                ...     print("Operación cancelada")

            Confirmación de guardado:
                >>> guardar = questi.confirm("¿Desea guardar los cambios?")
                >>> if guardar:
                ...     guardar_documento()

            Confirmación de salida:
                >>> if questi.confirm("¿Desea salir del programa?"):
                ...     questi.exit("¡Hasta luego!")

        Note:
            - El usuario responde con 'y' para sí o 'n' para no.
            - Por defecto, 'n' (no) está seleccionado.
            - Se puede cambiar la selección con las flechas y confirmar con Enter.
            - Cancelar con Ctrl+C o ESC termina el programa.
        """

        @self._questi_handler
        def _questi_confirm() -> Optional[bool]:
            return questionary.confirm(mensaje).ask()

        return _questi_confirm()


# Instancia global para uso directo
questi: Questi = Questi()
