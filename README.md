# Questi-Python 🐍

Un wrapper elegante para la librería `questionary` que facilita la recolección de entrada del usuario con validación automática y manejo elegante de cancelaciones en Python.

## 🚀 Características

- ✅ **Validación automática** de entrada vacía
- 🔢 **Validación numérica** para enteros y flotantes con rangos específicos
- ❌ **Manejo automático** de cancelaciones del usuario (Ctrl+C)
- 🎯 **Validadores personalizados** para casos específicos
- 📋 **Selecciones interactivas** y confirmaciones
- 💬 **Mensajes de despedida personalizados** por módulo

## 📦 Instalación

Primero, instala la dependencia requerida:

```bash
pip install questionary
```

Luego, descarga el archivo `questi.py` y colócalo en tu proyecto, o clona este repositorio:

```bash
git clone https://github.com/Julian7568/Questi-Python.git
```

## 🔧 Uso Básico

```python
from questi import questi

# Entrada de texto básica
nombre = questi.text("Ingresa tu nombre: ")

# Número entero con validación de rango
edad = questi.text("Ingresa tu edad: ", validate_user=2.0, inicio_rango=0, fin_rango=120)

# Número flotante
peso = questi.text("Peso (kg): ", validate_user=3.0, inicio_rango=0, fin_rango=500)

# Selección múltiple
lenguaje = questi.select("Tu lenguaje favorito:", ["Python", "JavaScript", "Java", "C++"])

# Confirmación
continuar = questi.confirm("¿Deseas continuar?")

if continuar:
    print("¡Continuando con el programa!")
else:
    questi.exit()  # Salida elegante
```

## 📚 Tipos de Validación

### 1. Validación de Texto (`validate_user=1.0`)
```python
# Valida que la entrada no esté vacía (por defecto)
nombre = questi.text("Tu nombre: ")
```

### 2. Validación de Números Enteros

```python
# Rango cerrado [min, max]
edad = questi.text("Edad: ", validate_user=2.0, inicio_rango=0, fin_rango=120)

# Solo mínimo
cantidad = questi.text("Cantidad: ", validate_user=2.1, inicio_rango=1)

# Solo máximo  
intentos = questi.text("Intentos: ", validate_user=2.2, fin_rango=10)
```

### 3. Validación de Números Flotantes

```python
# Rango cerrado para flotantes
precio = questi.text("Precio: ", validate_user=3.0, inicio_rango=0.0, fin_rango=1000.0)

# Solo mínimo para flotantes
descuento = questi.text("Descuento: ", validate_user=3.1, inicio_rango=0.01)

# Solo máximo para flotantes
comision = questi.text("Comisión: ", validate_user=3.2, fin_rango=100.0)
```

### 4. Validadores Personalizados

```python
# Validación de email
email = questi.text("Email: ", validate_user=lambda x: "@" in x and "." in x)

# Validación de contraseña
password = questi.text("Password: ", 
    validate_user=lambda x: len(x) >= 8 and any(c.isdigit() for c in x))

# Sin validación
comentario = questi.text("Comentarios: ", validate_user=None)
```

## 🎯 Ejemplos Prácticos

### Calculadora Simple
```python
from questi import questi

print("=== Calculadora Simple ===")

num1 = float(questi.text("Primer número: ", validate_user=3.0))
operacion = questi.select("Operación:", ["+", "-", "*", "/"])
num2 = float(questi.text("Segundo número: ", validate_user=3.0))

if operacion == "+":
    resultado = num1 + num2
elif operacion == "-":
    resultado = num1 - num2
elif operacion == "*":
    resultado = num1 * num2
elif operacion == "/":
    if num2 != 0:
        resultado = num1 / num2
    else:
        print("Error: División por cero")
        questi.exit()

print(f"Resultado: {resultado}")

if questi.confirm("¿Realizar otra operación?"):
    print("¡Reinicia el programa!")
else:
    questi.exit()
```

### Sistema de Login
```python
from questi import questi

print("=== Sistema de Login ===")

usuario = questi.text("Usuario: ")
password = questi.text("Contraseña: ", 
    validate_user=lambda x: len(x) >= 6)

# Simular validación
if usuario == "admin" and password == "123456":
    print("¡Login exitoso!")
    
    accion = questi.select("¿Qué deseas hacer?", [
        "Ver perfil",
        "Configuraciones", 
        "Cerrar sesión"
    ])
    
    print(f"Seleccionaste: {accion}")
else:
    print("Credenciales incorrectas")
    
questi.exit()
```

## 🛠️ Características Avanzadas

### Mensajes de Despedida Personalizados
```python
# En tu archivo principal, agrega mensajes personalizados
questi.modulo_mensajes["mi_programa.py"] = "¡Gracias por usar Mi Programa!"
```

### Manejo de Cancelaciones
Tutti maneja automáticamente cuando el usuario presiona `Ctrl+C` o `ESC`, mostrando un mensaje de despedida apropiado y terminando el programa de forma elegante.

## 📋 Métodos Disponibles

| Método | Descripción | Retorna |
|--------|-------------|---------|
| `text(mensaje, validate_user, inicio_rango, fin_rango)` | Solicita entrada de texto con validación | `str` |
| `select(mensaje, opciones)` | Muestra menú de selección | `str` |
| `confirm(mensaje)` | Pregunta de confirmación sí/no | `bool` |
| `exit()` | Termina el programa elegantemente | `None` |

## 🔧 Códigos de Validación

| Código | Tipo | Descripción |
|--------|------|-------------|
| `1.0` | Texto | No vacío (por defecto) |
| `2.0` | Entero | Rango [inicio_rango, fin_rango] |
| `2.1` | Entero | Mínimo inicio_rango |
| `2.2` | Entero | Máximo fin_rango |
| `3.0` | Flotante | Rango [inicio_rango, fin_rango] |
| `3.1` | Flotante | Mínimo inicio_rango |
| `3.2` | Flotante | Máximo fin_rango |
| `callable` | Personalizado | Función que retorna bool |
| `None` | Sin validación | Acepta cualquier entrada |

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar Questi-Python:

1. Haz fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Julian7568** - Estudiante de bachillerato apasionado por Python y la programación.

- GitHub: [@Julian7568](https://github.com/Julian7568)

## 🙏 Agradecimientos

- [questionary](https://github.com/tmbo/questionary) - La librería base que hace posible este wrapper
- La comunidad de Python por su apoyo y recursos educativos

---

⭐ **¡Si te gusta este proyecto, dale una estrella en GitHub!** ⭐
