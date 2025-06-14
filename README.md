# Questi Module 🎯

Un wrapper elegante y robusto para la librería `questionary` que simplifica la creación de interfaces de línea de comandos interactivas con manejo automático de errores y validaciones predefinidas.

## ✨ Características

- **Manejo automático de salidas**: Gestiona elegantemente las interrupciones del usuario (Ctrl+C, ESC)
- **Validaciones predefinidas**: Soporte para texto, enteros y flotantes con rangos personalizables
- **Mensajes personalizados**: Mensajes de despedida específicos por módulo
- **Callbacks customizables**: Funciones personalizadas para manejar salidas
- **Interfaz simplificada**: API intuitiva para entrada de texto, menús de selección y confirmaciones
- **Documentación completa**: Type hints y docstrings detallados

## 🚀 Instalación

```bash
pip install questionary
```

## 📖 Uso Básico

### Importar el módulo
```python
from questi_module import questi
```

### Entrada de texto simple
```python
nombre = questi.text("¿Cuál es tu nombre?")
```

### Validación de enteros con rango
```python
edad = questi.text("¿Cuál es tu edad?", validate_user=2.0, inicio_rango=0, fin_rango=120)
```

### Validación de flotantes
```python
precio = questi.text("Ingrese el precio:", validate_user=3.1, inicio_rango=0.01)
```

### Menú de selección
```python
opciones = ["1. Crear usuario", "2. Eliminar usuario", "3. Salir"]
eleccion = questi.select("¿Qué desea hacer?", opciones, indice=0)
```

### Confirmación
```python
if questi.confirm("¿Está seguro de continuar?"):
    print("Continuando...")
```

## 🔧 Tipos de Validación

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| `1.0` | Texto no vacío | `questi.text("Nombre:", 1.0)` |
| `2.0` | Entero en rango [min, max] | `questi.text("Edad:", 2.0, 0, 120)` |
| `2.1` | Entero >= min | `questi.text("Cantidad:", 2.1, 1)` |
| `2.2` | Entero <= max | `questi.text("Puntos:", 2.2, fin_rango=100)` |
| `3.0` | Float en rango [min, max] | `questi.text("Precio:", 3.0, 0.0, 999.99)` |
| `3.1` | Float >= min | `questi.text("Temperatura:", 3.1, -273.15)` |
| `3.2` | Float <= max | `questi.text("Porcentaje:", 3.2, fin_rango=100.0)` |
| `función` | Validación personalizada | `questi.text("Email:", lambda x: "@" in x)` |

## 🎨 Ejemplos Avanzados

### Validación personalizada
```python
def validar_email(email):
    return "@" in email and "." in email.split("@")[1]

email = questi.text("Ingrese su email:", validate_user=validar_email)
```

### Callback personalizado de salida
```python
def mi_callback():
    print("¡Operación cancelada!")
    return None

resultado = questi.text("Dato:", exit_callback=mi_callback)
```

### Configurar mensajes por módulo
```python
# Agregar mensaje personalizado para tu archivo
questi.modulo_mensajes["mi_script.py"] = "¡Gracias por usar mi aplicación!"
```

## 🏗️ Estructura del Código

```
questi_module.py
├── Classe Questi
│   ├── _questi_handler()    # Decorador para manejo de salidas
│   ├── text()              # Entrada de texto con validación
│   ├── select()            # Menú de selección
│   ├── confirm()           # Confirmación Sí/No
│   ├── exit()              # Salida elegante
│   └── exit_error()        # Salida con error
└── questi (instancia global)
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'feat: add nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [questionary](https://github.com/tmbo/questionary) - La excelente librería que hace posible este wrapper
- La comunidad de Python por sus herramientas increíbles

---

**¡Hecho con ❤️ para simplificar la creación de CLIs interactivas!**
