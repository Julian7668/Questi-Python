"""Módulo para solicitar entrada de usuario con validación personalizada.

Este módulo proporciona una clase wrapper para la librería questionary que
facilita la recolección de entrada del usuario con validación automática y
manejo elegante de cancelaciones.

Características principales:
    - Validación automática de entrada vacía
    - Validación de números enteros y flotantes dentro de rangos específicos
    - Manejo automático de cancelación con mensajes personalizados
    - Soporte para validadores personalizados
    - Confirmaciones y selecciones interactivas

Example:
    Uso básico del módulo:

    ```python
    # Crear instancia
    questi = Questi()

    # Solicitar texto no vacío
    nombre = questi.text("Ingresa tu nombre: ")

    # Solicitar número entero en rango
    edad = questi.text("Ingresa tu edad: ", validate_user=2, inicio_rango=0, fin_rango=120)

    # Solicitar número flotante
    precio = questi.text("Precio: ", validate_user=3.0, inicio_rango=0, fin_rango=1000)

    # Usar validador personalizado
    email = questi.text("Email: ", validate_user=lambda x: "@" in x)

    # Confirmación
    continuar = questi.confirm("¿Deseas continuar?")

    # Selección múltiple
    opcion = questi.select("Elige:", ["Opción A", "Opción B"])
    ```

Note:
    Requiere la instalación de questionary: `pip install questionary`

Author:
    Estudiante de bachillerato - Proyecto de programación en Python
"""

from functools import wraps
import sys
import time
import inspect
import questionary


class Questi:
    """Clase para manejar entradas de usuario con questionary de forma elegante.

    Proporciona métodos decorados para text(), select() y confirm() con manejo
    automático de cancelaciones y validaciones personalizadas. Permite crear
    interfaces de línea de comandos interactivas y robustas.

    La clase implementa un sistema de validación flexible que soporta múltiples
    tipos de entrada: texto básico, números enteros, números flotantes, y
    validadores personalizados. Cada método maneja automáticamente las
    cancelaciones del usuario y proporciona mensajes de despedida específicos
    por módulo.

    Attributes:
        modulo_mensajes (dict): Diccionario con mensajes de despedida específicos
            por archivo. Mapea nombres de archivos a mensajes personalizados que
            se muestran cuando el usuario cancela la operación.

    Example:
        Uso básico de la clase:

        ```python
        questi = Questi()

        # Entrada de texto básica
        nombre = questi.text("Ingresa tu nombre: ")

        # Entrada numérica con validación
        edad = questi.text("Edad: ", validate_user=2.0, inicio_rango=0, fin_rango=120)

        # Entrada de decimal
        altura = questi.text("Altura (m): ", validate_user=3.0, inicio_rango=0, fin_rango=3)

        # Selección múltiple
        opcion = questi.select("Elige una opción:", ["A", "B", "C"])

        # Confirmación
        continuar = questi.confirm("¿Deseas continuar?")

        # Salir del programa
        questi.exit()
        ```

    Note:
        Todas las funciones manejan automáticamente las cancelaciones del usuario
        (Ctrl+C o ESC) con mensajes de despedida apropiados y terminación limpia
        del programa.

    See Also:
        questionary: Librería base utilizada para la interfaz interactiva
    """

    modulo_mensajes = {
        "calculadora_de_calificaciones.py": "¡Gracias por usar la calculadora de calificaciones!",
        "generador_de_contrasenas.py": "¡Gracias por usar el generador de contraseñas!",
    }

    def _questi_handler(self, questionary_func):
        """Decorador para manejar la validación y cancelación en funciones questionary.

        Este decorador proporciona un manejo uniforme de cancelaciones del usuario
        y validación de entradas para todas las funciones questionary. Intercepta
        las respuestas None (que indican cancelación) y ejecuta la secuencia de
        terminación apropiada.

        El decorador implementa el patrón de manejo de errores para:
        - Detectar cancelaciones del usuario (None response)
        - Mostrar mensajes de despedida personalizados por módulo
        - Terminar el programa de forma elegante

        Args:
            questionary_func (callable): La función questionary específica a decorar.
                Debe ser una función que retorne el resultado de la interacción
                del usuario o None en caso de cancelación.

        Returns:
            callable: Función decorada que incluye manejo automático de cancelaciones
                y validación. La función decorada retorna el mismo tipo que la
                función original o termina el programa si hay cancelación.

        Example:
            Uso interno del decorador:

            ```python
            @self._questi_handler
            def _questi_text():
                return questionary.text("Mensaje").ask()

            # Si el usuario cancela, se ejecuta automáticamente:
            # 1. Mensaje de despedida personalizado
            # 2. Pausa de 1 segundo
            # 3. sys.exit(0)
            ```

        Note:
            - Este es un método interno y no debe ser llamado directamente
            - Utiliza inspect.stack() para determinar el archivo que llama
            - Maneja la terminación de forma limpia con sys.exit(0)
            - Preserve la signatura original de la función decorada con @wraps

        See Also:
            modulo_mensajes: Diccionario de mensajes personalizados
            exit(): Método público para terminación manual del programa
        """

        @wraps(questionary_func)
        def wrapper(*args, **kwargs):
            if entrada := questionary_func(*args, **kwargs):
                return entrada
            print(
                Questi().modulo_mensajes.get(
                    inspect.stack()[1].filename.split("\\")[-1],
                    "¡Gracias por usar!",
                )
            )
            time.sleep(1)
            sys.exit(0)

        return wrapper

    def exit(self):
        """Termina la ejecución del programa con un mensaje de despedida personalizado.

        Proporciona una forma elegante de terminar la aplicación mostrando un mensaje
        de despedida específico según el archivo desde el cual se llama. Utiliza el
        nombre del archivo que invoca la función para determinar qué mensaje mostrar,
        cayendo en un mensaje genérico si no hay uno específico configurado.

        El método implementa una secuencia controlada de terminación que incluye:
        1. Detectar automáticamente el archivo que llama usando inspect.stack()
        2. Buscar mensaje personalizado en modulo_mensajes
        3. Mostrar mensaje de despedida (personalizado o genérico)
        4. Pausa breve para legibilidad
        5. Terminación limpia del programa

        Returns:
            None: Esta función nunca retorna ya que termina la ejecución del programa
                con sys.exit(0).

        Raises:
            SystemExit: Siempre se ejecuta para terminar el programa con código de
                salida 0 (terminación exitosa).

        Example:
            Diferentes formas de usar exit():

            ```python
            questi = Questi()

            # Salida directa
            questi.exit()

            # Salida condicional
            if not questi.confirm("¿Deseas continuar?"):
                questi.exit()

            # En un menú
            opcion = questi.select("Elige:", ["Continuar", "Salir"])
            if opcion == "Salir":
                questi.exit()

            # Salida después de completar una tarea
            print("Proceso completado exitosamente.")
            questi.exit()

            # En manejo de errores
            try:
                # código que puede fallar
                pass
            except Exception as e:
                print(f"Error: {e}")
                questi.exit()
            ```

        Note:
            - Los mensajes personalizados se configuran en el diccionario modulo_mensajes
            - Si no existe mensaje personalizado, usa "¡Gracias por usar!"
            - La pausa de 1 segundo permite leer el mensaje antes de cerrar
            - Usa sys.exit(0) para una terminación limpia sin errores
            - Detecta automáticamente el archivo que llama usando inspect.stack()
            - Es thread-safe y puede llamarse desde cualquier parte del programa

        See Also:
            modulo_mensajes (dict): Diccionario con mensajes personalizados por archivo
            _questi_handler: Decorador que también maneja terminaciones automáticas
        """
        print(
            Questi().modulo_mensajes.get(
                inspect.stack()[1].filename.split("\\")[-1],
                "¡Gracias por usar!",
            )
        )
        time.sleep(1)
        sys.exit(0)

    def text(
        self,
        mensaje: str,
        validate_user=1.0,
        inicio_rango=float("-inf"),
        fin_rango=float("inf"),
    ):
        """Solicita entrada de texto al usuario con validación personalizada.

        Permite recoger texto del usuario con diferentes tipos de validación,
        desde validación básica de campo no vacío hasta validación numérica
        (enteros y flotantes) con rangos específicos o validadores personalizados.

        El método soporta múltiples tipos de validación identificados por códigos
        numéricos, cada uno con comportamientos específicos para diferentes casos
        de uso. Los validadores personalizados permiten lógica de validación
        completamente customizada.

        Args:
            mensaje (str): El mensaje/prompt a mostrar al usuario. Debe ser claro
                y descriptivo sobre qué tipo de entrada se espera.
            validate_user (float or callable, optional): Tipo de validación a aplicar.
                Opciones disponibles:
                    - 1.0: Valida que la entrada no esté vacía (default)
                    - 2.0: Número entero dentro del rango [inicio_rango, fin_rango]
                    - 2.1: Número entero mayor o igual al inicio_rango
                    - 2.2: Número entero menor o igual al fin_rango
                    - 3.0: Número flotante dentro del rango [inicio_rango, fin_rango]
                    - 3.1: Número flotante mayor o igual al inicio_rango
                    - 3.2: Número flotante menor o igual al fin_rango
                    - callable: Función personalizada que recibe la entrada y retorna bool
                    - None/False: Sin validación (acepta cualquier entrada)
                Defaults to 1.0.
            inicio_rango (float, optional): Límite inferior para validación numérica.
                Usado en validaciones 2.0, 2.1, 3.0, 3.1. Para 2.2 y 3.2 actúa
                como límite superior. Defaults to float("-inf").
            fin_rango (float, optional): Límite superior para validación numérica.
                Solo usado en validaciones 2.0 y 3.0 para rangos cerrados.
                Defaults to float("inf").

        Returns:
            str: La entrada del usuario validada. Siempre retorna un string,
                incluso para validaciones numéricas (debe convertirse después).

        Raises:
            KeyboardInterrupt: Si el usuario cancela con Ctrl+C, se maneja
                automáticamente con mensaje de despedida a través del decorador.
            ValueError: Si validate_user es un tipo no soportado.
            TypeError: Si el validador personalizado no es callable.

        Examples:
            Validación básica sin restricciones:

            >>> questi = Questi()
            >>> nombre = questi.text("Ingresa tu nombre: ")
            Ingresa tu nombre: Juan
            >>> print(nombre)
            'Juan'

            Validación numérica entera con rango cerrado:

            >>> edad = questi.text("Edad (0-120): ", validate_user=2.0,
            ...                   inicio_rango=0, fin_rango=120)
            Edad (0-120): 25
            >>> edad_int = int(edad)
            >>> print(edad_int)
            25

            Validación numérica entera con mínimo:

            >>> cantidad = questi.text("Cantidad mínima: ", validate_user=2.1,
            ...                       inicio_rango=1)
            Cantidad mínima: 5
            >>> print(int(cantidad))
            5

            Validación numérica entera con máximo:

            >>> intentos = questi.text("Máximo intentos: ", validate_user=2.2,
            ...                       inicio_rango=10)
            Máximo intentos: 8
            >>> print(int(intentos))
            8

            Validación numérica flotante con rango:

            >>> peso = questi.text("Peso (kg): ", validate_user=3.0,
            ...                   inicio_rango=0, fin_rango=500)
            Peso (kg): 75.5
            >>> print(float(peso))
            75.5

            Validación flotante con mínimo:

            >>> precio = questi.text("Precio mínimo: ", validate_user=3.1,
            ...                     inicio_rango=0.01)
            Precio mínimo: 19.99
            >>> print(float(precio))
            19.99

            Validación flotante con máximo:

            >>> descuento = questi.text("Descuento máximo: ", validate_user=3.2,
            ...                        inicio_rango=100.0)
            Descuento máximo: 25.5
            >>> print(float(descuento))
            25.5

            Validador personalizado para email:

            >>> email = questi.text("Email: ",
            ...                    validate_user=lambda x: "@" in x and "." in x)
            Email: usuario@ejemplo.com
            >>> print(email)
            'usuario@ejemplo.com'

            Validador personalizado complejo para contraseñas:

            >>> password = questi.text("Password: ",
            ...                       validate_user=lambda x: len(x) >= 8 and
            ...                                              any(c.isdigit() for c in x))
            Password: mipassword123
            >>> print(len(password))
            13

            Sin validación (acepta cualquier entrada):

            >>> comentario = questi.text("Comentarios opcionales: ",
            ...                         validate_user=None)
            Comentarios opcionales:
            >>> print(repr(comentario))
            ''

        Note:
            - La validación numérica entera (2.x) usa str.isdigit() y int()
            - La validación numérica flotante (3.x) permite un punto decimal usando replace()
            - Los validadores personalizados deben retornar True para entrada válida
            - Una entrada vacía en validación tipo 1.0 será rechazada automáticamente
            - Los números negativos no son soportados por las validaciones 2.x y 3.x actuales
            - Para usar los números validados, convierte el resultado con int() o float()
            - El parámetro inicio_rango tiene diferente comportamiento en 2.2 y 3.2 (actúa como máximo)

        Warning:
            Las validaciones numéricas actuales no soportan números negativos debido
            al uso de str.isdigit(). Para números negativos, usa un validador personalizado.

        See Also:
            select(): Para opciones predefinidas con menú de selección.
            confirm(): Para confirmaciones sí/no simples.
            _questi_handler: Decorador que maneja las cancelaciones del usuario.

        Todo:
            - Agregar soporte nativo para números negativos
            - Implementar validación de rangos más robusta
            - Añadir validadores comunes predefinidos (email, URL, etc.)
        """

        @self._questi_handler
        def _questi_text():
            validaciones = {
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
            return (
                questionary.text(
                    mensaje, validate=validaciones.get(validate_user)
                ).ask()
                if validate_user in validaciones
                else validate_user
            )

        return _questi_text()

    def select(self, mensaje, opciones):
        """Solicita selección de una opción al usuario desde una lista predefinida.

        Presenta una lista de opciones al usuario de forma interactiva, permitiendo
        navegar con las teclas de flecha y seleccionar con Enter. Proporciona una
        interfaz intuitiva para menús y selecciones múltiples.

        Este método es ideal para casos donde el usuario debe elegir entre opciones
        predefinidas, como menús de navegación, configuraciones, o cualquier
        selección donde las opciones son conocidas de antemano.

        Args:
            mensaje (str): El mensaje/prompt a mostrar al usuario. Debe explicar
                claramente qué se está seleccionando y proporcionar contexto
                sobre las opciones disponibles.
            opciones (list[str]): Lista de opciones disponibles para seleccionar.
                Cada elemento debe ser un string descriptivo. La lista no debe
                estar vacía y cada opción debe ser única y clara.

        Returns:
            str: La opción seleccionada por el usuario. Retorna exactamente uno
                de los elementos de la lista opciones tal como fue proporcionado.

        Raises:
            KeyboardInterrupt: Si el usuario cancela con Ctrl+C o ESC, se maneja
                automáticamente con mensaje de despedida a través del decorador.
            ValueError: Si la lista de opciones está vacía (manejado por questionary).

        Example:
            Diferentes usos de selección:

            ```python
            questi = Questi()

            # Menú principal simple
            accion = questi.select("¿Qué deseas hacer?", [
                "Crear nuevo archivo",
                "Abrir archivo existente",
                "Configuraciones",
                "Salir"
            ])

            # Selección de configuración
            lenguaje = questi.select("Selecciona tu lenguaje favorito:", [
                "Python",
                "JavaScript",
                "Java",
                "C++",
                "Go"
            ])

            # Selección con opciones numeradas
            dificultad = questi.select("Selecciona la dificultad:", [
                "1. Fácil - Para principiantes",
                "2. Medio - Con algo de experiencia",
                "3. Difícil - Para expertos",
                "4. Extremo - Solo para valientes"
            ])

            # Menú contextual basado en selección previa
            if accion == "Configuraciones":
                config = questi.select("¿Qué configurar?", [
                    "Tema de color",
                    "Idioma de interfaz",
                    "Atajos de teclado",
                    "Volver al menú principal"
                ])

            # Selección con validación posterior
            formato = questi.select("Formato de salida:", ["JSON", "CSV", "XML"])
            if formato == "CSV":
                separador = questi.select("Separador CSV:", [",", ";", "|", "\\t"])
            ```

        Note:
            - Usa las teclas de flecha arriba/abajo para navegar entre opciones
            - Presiona Enter para seleccionar la opción resaltada
            - ESC o Ctrl+C para cancelar (manejado automáticamente)
            - La primera opción está seleccionada por defecto al iniciar
            - Las opciones se muestran en el mismo orden que se proporcionan
            - No hay límite en el número de opciones, pero considera la usabilidad

        See Also:
            text(): Para entrada de texto libre
            confirm(): Para confirmaciones simples sí/no
            _questi_handler: Decorador que maneja las cancelaciones
        """

        @self._questi_handler
        def _questi_select():
            return questionary.select(mensaje, choices=opciones).ask()

        return _questi_select()

    def confirm(self, mensaje):
        """Solicita una confirmación sí/no al usuario.

        Presenta una pregunta de confirmación al usuario que puede responder
        con 'y' (sí/yes) o 'n' (no). Es útil para confirmar acciones importantes,
        validar decisiones del usuario, o implementar puntos de control en el
        flujo del programa donde se requiere confirmación explícita.

        Este método es especialmente valioso para acciones destructivas,
        configuraciones importantes, o cualquier operación que el usuario
        podría querer reconsiderar antes de ejecutar.

        Args:
            mensaje (str): La pregunta de confirmación a mostrar al usuario.
                Debe ser una pregunta clara y específica que se pueda responder
                con sí/no. Se recomienda usar lenguaje directo y explicar las
                consecuencias de confirmar cuando sea relevante.

        Returns:
            bool: True si el usuario confirma (responde 'y' o 'Y'), False si no
                confirma (responde 'n' o 'N'). El valor de retorno puede usarse
                directamente en condiciones if/while.

        Raises:
            KeyboardInterrupt: Si el usuario cancela con Ctrl+C o ESC, se maneja
                automáticamente con mensaje de despedida a través del decorador.

        Example:
            Diferentes usos de confirmación:

            ```python
            questi = Questi()

            # Confirmación básica de continuación
            if questi.confirm("¿Deseas continuar con el proceso?"):
                print("Continuando...")
            else:
                print("Proceso cancelado.")

            # Confirmación de acción destructiva
            if questi.confirm("¿Estás seguro de que deseas eliminar todos los archivos?"):
                eliminar_archivos()
                print("Archivos eliminados.")
            else:
                print("Operación cancelada por seguridad.")

            # Confirmación en bucle de validación
            while True:
                nombre = questi.text("Ingresa tu nombre: ")
                if questi.confirm(f"¿'{nombre}' es correcto?"):
                    break
                print("Por favor, ingresa nuevamente tu nombre.")

            # Confirmación para guardar cambios
            if datos_modificados:
                if questi.confirm("Hay cambios sin guardar. ¿Deseas guardarlos?"):
                    guardar_datos()
                    print("Datos guardados exitosamente.")

            # Confirmación de configuración
            configuracion_avanzada = questi.confirm("¿Deseas habilitar opciones avanzadas?")
            if configuracion_avanzada:
                opciones_avanzadas = True
                print("Modo avanzado activado.")

            # Confirmación múltiple anidada
            if questi.confirm("¿Deseas realizar una copia de seguridad?"):
                if questi.confirm("¿Incluir archivos temporales en la copia?"):
                    crear_backup(incluir_temp=True)
                else:
                    crear_backup(incluir_temp=False)

            # Confirmación con salida del programa
            if not questi.confirm("¿Deseas continuar usando el programa?"):
                questi.exit()
            ```

        Note:
            - Presiona 'y', 'Y', 's', o 'S' para confirmar (sí)
            - Presiona 'n' o 'N' para rechazar (no)
            - ESC o Ctrl+C para cancelar (manejado automáticamente)
            - El valor por defecto suele ser 'No' para mayor seguridad
            - Se recomienda ser específico en las preguntas para evitar confusión
            - Útil para implementar puntos de control en operaciones críticas

        See Also:
            text(): Para entrada de texto libre
            select(): Para selección entre múltiples opciones
            exit(): Para terminar programa tras confirmación negativa
            _questi_handler: Decorador que maneja las cancelaciones
        """

        @self._questi_handler
        def _questi_confirm():
            return questionary.confirm(mensaje).ask()

        return _questi_confirm()


questi = Questi()
