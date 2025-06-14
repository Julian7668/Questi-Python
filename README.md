# 🎯 Questi - Wrapper Inteligente para Questionary

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)

Un wrapper elegante y poderoso para `questionary` que simplifica la creación de interfaces de línea de comandos interactivas con manejo automático de errores, validaciones predefinidas y callbacks personalizables.

## ✨ Características Principales

- 🛡️ **Manejo automático de salidas**: Captura Ctrl+C, ESC y otras interrupciones elegantemente
- ✅ **Validaciones predefinidas**: Para enteros, flotantes y strings con rangos personalizables
- 🎨 **Mensajes personalizados**: Por módulo/archivo para una experiencia más pulida
- 🔧 **Callbacks de salida**: Ejecuta funciones personalizadas antes de terminar
- 📝 **Documentación completa**: Docstrings detallados y ejemplos de uso
- 🚀 **Fácil de usar**: Una sola instancia global `questi` para todas tus necesidades

## 🚀 Instalación Rápida

```bash
# Clona el repositorio
git clone https://github.com/tu-usuario/questi-module.git
cd questi-module

# Instala la dependencia
pip install questionary
```

## 💡 Uso Básico

```python
from questi_module import questi

# Entrada de texto simple
nombre = questi.text("¿Cuál es tu nombre?")

# Validación de enteros con rango
edad = questi.text(
    "¿Cuál es tu edad?", 
    validate_user=2.0,  # Validar entero
    inicio_rango=0, 
    fin_rango=120
)

# Validación de flotantes
peso = questi.text(
    "¿Cuál es tu peso en kg?",
    validate_user=3.0,  # Validar flotante
    inicio_rango=0.0,
    fin_rango=300.0
)

# Menú de selección
opciones = ["1. Crear usuario", "2. Eliminar usuario", "3. Salir"]
eleccion = questi.select("¿Qué desea hacer?", opciones)

# Confirmación
if questi.confirm("¿Está seguro de continuar?"):
    print("¡Continuando!")
```

## 🎯 Ejemplos Avanzados

### Validación Personalizada

```python
def validar_email(email):
    return "@" in email and "." in email

email = questi.text(
    "Ingrese su email:",
    validate_user=validar_email
)
```

### Callback de Salida Personalizado

```python
def guardar_y_salir():
    print("Guardando datos...")
    # Lógica de guardado aquí
    questi.exit("¡Datos guardados exitosamente!")

nome = questi.text(
    "Ingrese el nombre del proyecto:",
    exit_callback=guardar_y_salir
)
```

### Conversión de Tipos Automática

```python
# Retorna automáticamente como entero
numero = questi.text(
    "Ingrese un número:",
    validate_user=2.0,
    what_return=int
)

# Retorna automáticamente como flotante
precio = questi.text(
    "Ingrese el precio:",
    validate_user=3.0,
    what_return=float
)
```

## 📚 API Reference

### `questi.text()`

Solicita entrada de texto con validaciones opcionales.

**Parámetros:**
- `mensaje` (str): Mensaje a mostrar al usuario
- `validate_user` (Union[float, Callable]): Tipo de validación:
  - `1.0`: String no vacío
  - `2.0`: Entero válido
  - `3.0`: Flotante válido
  - `Callable`: Función personalizada
- `inicio_rango` (float): Valor mínimo para números
- `fin_rango` (float): Valor máximo para números
- `exit_callback` (Callable): Función a ejecutar al cancelar
- `what_return` (type): Tipo de retorno (str, int, float, bool)
- `use_strip` (bool): Aplicar strip() al resultado

### `questi.select()`

Muestra un menú de selección.

**Parámetros:**
- `mensaje` (str): Texto del menú
- `opciones` (list[str]): Lista de opciones
- `indice` (slice): Índice del carácter a retornar
- `exit_callback` (Callable): Función a ejecutar al cancelar
- `what_return` (type): Tipo de retorno

### `questi.confirm()`

Solicita confirmación (Sí/No).

**Parámetros:**
- `mensaje` (str): Pregunta de confirmación
- `exit_callback` (Callable): Función a ejecutar al cancelar

### `questi.exit()` y `questi.exit_error()`

Terminan el programa elegantemente con mensajes personalizados.

## 🎨 Personalización

### Mensajes por Módulo

```python
questi.modulo_mensajes.update({
    "mi_app.py": "¡Gracias por usar Mi App Increíble!",
    "calculadora.py": "¡Cálculos completados!"
})
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0 (2024)
- ✨ Lanzamiento inicial
- 🛡️ Manejo automático de interrupciones
- ✅ Validaciones para enteros, flotantes y strings
- 🎨 Sistema de mensajes personalizados
- 📚 Documentación completa

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ve el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [questionary](https://github.com/tmbo/questionary) - La increíble librería base
- A todos los desarrolladores que hacen que Python sea genial

---

**Desarrollado con ❤️ para simplificar las interfaces de línea de comandos**

¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!
