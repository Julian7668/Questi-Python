# 🎯 Questi

> Wrapper elegante para questionary con validaciones automáticas y manejo de errores

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)

## ✨ Características

- 🛡️ **Manejo automático de salidas** - Ctrl+C y ESC manejados elegantemente
- ✅ **Validaciones predefinidas** - Para enteros, flotantes y strings
- 🎨 **Mensajes personalizados** - Por módulo o función
- 🔧 **Callbacks configurables** - Funciones personalizadas al salir
- 📝 **Documentación completa** - Con ejemplos y tipos

## 🚀 Instalación

```bash
pip install questionary
```

Luego simplemente incluye `questi_module.py` en tu proyecto.

## 💡 Uso básico

```python
from questi_module import questi

# Solicitar texto simple
nombre = questi.text("¿Cuál es tu nombre?")

# Solicitar entero con validación
edad = questi.text("¿Tu edad?", validate_user=int, inicio_rango=0, fin_rango=120)

# Menú de selección
opciones = ["1. Crear", "2. Editar", "3. Salir"]
eleccion = questi.select("¿Qué deseas hacer?", opciones)

# Confirmación
if questi.confirm("¿Continuar?"):
    print("¡Continuando!")
```

## 📚 Métodos disponibles

### `text()` - Entrada de texto
Solicita entrada con validaciones automáticas:

```python
# String no vacío
nombre = questi.text("Nombre:", validate_user=str)

# Número flotante en rango
peso = questi.text("Peso (kg):", validate_user=float, inicio_rango=0.0, fin_rango=300.0)

# Validación personalizada
email = questi.text("Email:", validate_user=lambda x: "@" in x and "." in x)
```

### `select()` - Menú de opciones
Muestra menú interactivo:

```python
opciones = ["A. Opción 1", "B. Opción 2", "C. Salir"]
letra = questi.select("Elige:", opciones, indice=slice(0, 1))  # Retorna "A", "B" o "C"
```

### `confirm()` - Confirmación
Pregunta Sí/No:

```python
if questi.confirm("¿Eliminar archivo?"):
    eliminar_archivo()
```

## 🔧 Características avanzadas

### Callbacks personalizados
```python
def mi_salida():
    print("¡Saliendo de forma personalizada!")
    
nombre = questi.text("Nombre:", exit_callback=mi_salida)
```

### Mensajes por módulo
El sistema detecta automáticamente el archivo que llama y muestra mensajes personalizados:

```python
# En calculadora_de_calificaciones.py
questi.exit()  # Muestra: "¡Gracias por usar la calculadora de calificaciones!"
```

### Validaciones con rangos
```python
# Solo números entre 1 y 10
puntuacion = questi.text(
    "Puntuación (1-10):", 
    validate_user=int, 
    inicio_rango=1, 
    fin_rango=10
)
```

## 🎯 Casos de uso

- **Calculadoras interactivas** - Con validación numérica automática
- **Menús de aplicaciones** - Navegación clara y elegante  
- **Configuradores** - Recopilación de datos con validación
- **Scripts de utilidad** - Interfaces de línea de comandos amigables

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para detalles.

---

<div align="center">
  <strong>Hecho con ❤️ para hacer las CLI más amigables</strong>
</div>
