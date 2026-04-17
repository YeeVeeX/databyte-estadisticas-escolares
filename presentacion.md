# Sistema de Estadísticas Escolares

## DataByte — Escuela San Pascualin

**Proyecto Final — Principios de Programación 1**

Gabriel — CENFOTEC

---

## Contexto del Proyecto

La empresa **DataByte** nos contrató para desarrollar una aplicación en Python que permita calcular y mostrar estadísticas de edades para la **Escuela San Pascualin**.

El objetivo: procesar una muestra de alumnos y extraer métricas clave como edad mayor, edad menor, promedio y mediana, con una interfaz que se sienta profesional y empresarial.

---

## Requerimientos del Cliente

- Almacenar **nombre y edad** de los alumnos en un **diccionario**
- Obtener la **edad mayor y menor**
- Calcular el **promedio** con un decimal
- Calcular la **mediana** (par e impar)
- Usar **funciones `def`** para cada operación
- Implementar una **contraseña segura** antes del menú
- **Menú** con validaciones
- Mostrar **fecha y hora** al cargar la aplicación

---

## Solución Entregada: Dos Versiones

**1. Versión Consola** (`proyecto_final.py`)
Versión base con menú de texto en terminal. Cumple 100% de los requerimientos.

**2. Versión GUI** (`proyecto_final_gui.py`)
Interfaz gráfica profesional con tkinter, generador automático de reportes HTML y TXT.

Ambas versiones son 100% Python estándar — **sin instalar nada adicional**.

---

## Arquitectura General

```
proyecto_final/
├── proyecto_final.py          → Versión consola (285 líneas)
├── proyecto_final_gui.py      → Versión GUI (1200+ líneas)
├── README.md                  → Documentación de uso
├── presentacion.md            → Este documento
└── reportes/                  → Salida automática
    ├── reporte_*.html
    └── reporte_*.txt
```

---

## Tecnologías Utilizadas

| Tecnología | Propósito |
|-----------|-----------|
| **Python 3** | Lenguaje base |
| **tkinter + ttk** | Interfaz gráfica (biblioteca estándar) |
| **datetime** | Fecha y hora del sistema |
| **os** | Creación de carpetas y manejo de archivos |
| **webbrowser** | Apertura automática del reporte HTML |
| **random** | Generación de datos de ejemplo |
| **HTML + CSS** | Formato del reporte empresarial |

Cero librerías externas. Todo funciona tal como viene Python instalado.

---

## Estructura del Código: 3 Capas

**1. Capa de Lógica**
Funciones puras que calculan las estadísticas. Son reutilizables en cualquier interfaz.

**2. Capa de Interfaz**
Frames de tkinter que presentan pantallas al usuario.

**3. Capa de Reportes**
Generadores HTML y TXT que persisten los resultados.

Separar responsabilidades permite reutilizar la misma lógica en consola y en GUI sin duplicar código.

---

## Funciones de Lógica — Parte 1

```python
def validar_contrasena(clave):
    checklist = {
        "largo": len(clave) >= 8,
        "mayus": False, "minus": False,
        "numero": False, "simbolo": False,
    }
    for letra in clave:
        if letra.isupper(): checklist["mayus"] = True
        elif letra.islower(): checklist["minus"] = True
        elif letra.isdigit(): checklist["numero"] = True
        elif letra in "!@#$%^&*()": checklist["simbolo"] = True
    # ... valida y devuelve tupla
```

**Por qué así:** iteramos carácter por carácter con métodos de string nativos (`isupper`, `isdigit`), sin regex. Esto es apropiado para el nivel del curso y es fácil de explicar.

---

## Funciones de Lógica — Parte 2

```python
def obtener_edad_mayor(alumnos):
    mayor = -1
    nombre_mayor = ""
    for nombre in alumnos:
        if alumnos[nombre] > mayor:
            mayor = alumnos[nombre]
            nombre_mayor = nombre
    return nombre_mayor, mayor
```

**Concepto clave:** En lugar de usar `max()` built-in, implementamos el algoritmo manualmente. Esto demuestra comprensión de cómo funciona internamente y devuelve **dos datos** (nombre y edad) al mismo tiempo.

---

## Cálculo del Promedio

```python
def calcular_promedio(alumnos):
    suma = 0
    cantidad = 0
    for nombre in alumnos:
        suma += alumnos[nombre]
        cantidad += 1
    promedio = suma / cantidad
    return round(promedio, 1)
```

**Por qué `round(promedio, 1)`:** el cliente pidió explícitamente "un decimal". La función `round()` garantiza el formato exacto requerido.

**Por qué no usar `sum()` ni `len()`:** implementar manualmente enseña el patrón de acumulador, fundamental en programación.

---

## Cálculo de la Mediana

```python
def calcular_mediana(alumnos):
    edades = []
    for nombre in alumnos:
        edades.append(alumnos[nombre])
    edades.sort()

    cantidad = len(edades)
    mitad = cantidad // 2

    if cantidad % 2 == 1:
        return edades[mitad]             # Caso impar
    else:
        return (edades[mitad - 1] + edades[mitad]) / 2  # Caso par
```

**El truco:** `cantidad % 2 == 1` detecta si hay cantidad impar de elementos. En ese caso tomamos el elemento central directo. En caso par, promediamos los dos centrales.

---

## Ejemplo de Cálculo de Mediana

**Muestra impar (n=5):** `[7, 8, 9, 10, 12]` ordenada
- `mitad = 5 // 2 = 2`
- `edades[2] = 9` → **Mediana: 9**

**Muestra par (n=4):** `[7, 8, 10, 12]` ordenada
- `mitad = 4 // 2 = 2`
- `(edades[1] + edades[2]) / 2 = (8 + 10) / 2 = 9.0` → **Mediana: 9.0**

La diferencia entre `9` (entero) y `9.0` (flotante) es correcta y muestra cómo Python infiere tipos según la operación.

---

## Interfaz Gráfica: Arquitectura

La GUI usa **un sistema de frames intercambiables** dentro de una ventana única:

```python
frames = {}

def mostrar_frame(nombre):
    for key in frames:
        frames[key].pack_forget()
    frames[nombre].pack(fill="both", expand=True)
```

**Concepto:** cada "pantalla" es un `Frame` separado. Cambiar de pantalla es ocultar todos y mostrar solo uno. Este patrón se llama **State Machine UI**.

---

## Las 5 Pantallas

1. **Bienvenida** — Logo + reloj en vivo
2. **Registro de contraseña** — Validación en tiempo real
3. **Configuración** — Tamaño de la muestra
4. **Ingreso de alumnos** — Formulario + tabla en vivo
5. **Dashboard** — Menú lateral + panel dinámico de estadísticas

Cada pantalla tiene un propósito único y valida sus datos antes de avanzar.

---

## Sistema de Estilos Profesional

Definimos una **paleta corporativa** y la aplicamos con `ttk.Style`:

```python
COLOR_PRIMARIO = "#1e3a5f"   # Azul DataByte
COLOR_ACENTO = "#4a90e2"     # Azul claro botones
COLOR_FONDO = "#f5f7fa"      # Gris muy claro
COLOR_EXITO = "#27ae60"      # Verde validaciones
COLOR_ERROR = "#e74c3c"      # Rojo errores

estilo = ttk.Style()
estilo.theme_use("clam")
```

**Decisión clave:** usar el tema `"clam"` de tkinter en lugar del default de Windows. Luce más moderno y uniforme.

---

## Reloj en Vivo

```python
def actualizar_reloj():
    ahora = datetime.now()
    reloj_var.set(ahora.strftime("%H:%M:%S"))
    fecha_var.set(ahora.strftime("%A, %d de %B del %Y"))
    ventana.after(1000, actualizar_reloj)
```

**Concepto clave:** `ventana.after(1000, funcion)` programa la ejecución de `funcion` en 1000ms (1 segundo) **sin bloquear** la interfaz.

Nunca se debe usar `time.sleep()` en GUI — congelaría la pantalla. El `after()` es la forma correcta de hacer tareas periódicas en tkinter.

---

## Validación de Contraseña en Vivo

Cada vez que el usuario teclea una letra, se re-valida la contraseña y se actualiza el checklist visual:

```python
entry_pwd.bind("<KeyRelease>", actualizar_checklist)

def actualizar_checklist(evento=None):
    clave = entry_pwd.get()
    _, _, checklist = validar_contrasena(clave)

    for clave_c in checklist:
        if checklist[clave_c]:
            check_labels[clave_c].configure(fg=COLOR_EXITO)
        else:
            check_labels[clave_c].configure(fg=COLOR_ERROR)
```

El usuario ve en verde los requisitos cumplidos al instante, sin presionar ningún botón.

---

## Seguridad: Intentos Limitados

```python
def intentar_login():
    global intentos_restantes
    ingresado = entry_pwd.get()

    if ingresado == clave_guardada:
        mostrar_frame("muestra")
        return

    intentos_restantes -= 1
    if intentos_restantes <= 0:
        messagebox.showerror("Acceso bloqueado",
                             "Demasiados intentos fallidos.")
        ventana.destroy()
```

**Práctica de seguridad real:** 3 intentos máximo. Al llegar a 0, la aplicación se cierra. Esto simula el comportamiento de sistemas bancarios y empresariales.

---

## Ingreso de Alumnos con Tabla en Vivo

```python
tree_alumnos = ttk.Treeview(panel_tabla,
                            columns=("num", "nombre", "edad"),
                            show="headings")

def agregar_alumno():
    nombre = entry_nombre.get().strip()
    edad = int(edad_var.get())
    # Validaciones ...
    alumnos[nombre] = edad
    tree_alumnos.insert("", "end",
                       values=(num, nombre, edad))
```

`Treeview` es el widget de tabla de tkinter. Al insertar una fila, aparece instantáneamente sin recargar nada.

---

## Navegación por Teclado (ENTER)

Cada formulario responde a la tecla ENTER para agilizar el uso:

```python
entry_pwd.bind("<Return>", enter_pwd_registro)
entry_muestra.bind("<Return>",
                   lambda e: confirmar_tamano())
entry_nombre.bind("<Return>", enter_nombre_alumno)
spin_edad.bind("<Return>", enter_edad_alumno)
```

**UX empresarial:** el usuario puede completar todos los formularios sin soltar el teclado. ENTER equivale al botón principal de cada pantalla.

---

## Dashboard Dinámico

El dashboard tiene **un panel lateral con botones** y **un panel derecho que cambia** según el botón presionado:

```python
def limpiar_contenido():
    for widget in panel_contenido.winfo_children():
        widget.destroy()

def ver_resumen():
    limpiar_contenido()
    # Construye 5 cards con todas las estadísticas
```

Cada función de sección destruye el contenido anterior y dibuja el nuevo. Patrón clásico de dashboards SPA (single page application).

---

## Cards de Estadísticas

```python
def crear_card(parent, titulo, valor, color):
    card = Frame(parent, bg=COLOR_BLANCO,
                 bd=1, relief="solid")
    Label(card, text=titulo,
          font=("Segoe UI", 10)).pack(pady=(15, 5))
    Label(card, text=valor, fg=color,
          font=("Segoe UI", 22, "bold")).pack(pady=(0, 15))
```

Cada métrica se muestra en una **card** con título pequeño arriba y valor grande abajo — estilo dashboards modernos (Google Analytics, Stripe, etc.).

---

## Generación de Reporte HTML

```python
def generar_reporte_html():
    html = """<!DOCTYPE html>
    <html lang="es">
    <head><style>
      /* CSS inline profesional */
      header { background: linear-gradient(135deg, #1e3a5f, #4a90e2); }
      .card { border-left: 4px solid #4a90e2; }
      table th { background: #1e3a5f; color: white; }
    </style></head>
    <body>...</body>
    </html>"""
    return html
```

El HTML se construye concatenando un **template string** con los datos reales. Se abre en el navegador con `webbrowser.open()`.

---

## Por Qué HTML y no PDF

**Ventajas del HTML:**
- Cero librerías externas (`reportlab`/`fpdf` requieren pip install)
- Look profesional con CSS (gradientes, cards, tablas estilizadas)
- Se convierte a PDF con **Ctrl+P → "Guardar como PDF"** desde el navegador
- Editable si se necesita ajustar antes de imprimir
- Universal: cualquier sistema lo abre

**Bonus:** también generamos un **TXT plano** como respaldo compatible con cualquier editor de texto.

---

## Guardado con Timestamp

```python
def guardar_reporte(contenido, extension):
    ahora = datetime.now()
    nombre = "reporte_" + ahora.strftime(
        "%Y-%m-%d_%H-%M-%S") + "." + extension
    ruta = os.path.join("reportes", nombre)

    archivo = open(ruta, "w", encoding="utf-8")
    archivo.write(contenido)
    archivo.close()
    return ruta
```

Cada reporte tiene nombre único basado en fecha/hora. Nunca se sobrescriben — todos los reportes históricos se conservan automáticamente.

---

## Datos de Ejemplo Automáticos

Para facilitar pruebas con muestras grandes, añadimos un botón que llena automáticamente los alumnos faltantes:

```python
def llenar_datos_demo():
    nombres = ["Ana Rodriguez", "Luis Martinez", ...]
    faltantes = tamano_muestra - len(alumnos)

    for nombre in nombres[:faltantes]:
        edad = random.randint(4, 18)
        alumnos[nombre] = edad
```

Respeta los ya ingresados manualmente y solo completa los que faltan. UX común en software empresarial real.

---

## Flujo Completo de Uso

1. Usuario ve **pantalla de bienvenida** con reloj en vivo
2. Presiona **ENTER** o clic en "Iniciar sesión"
3. Crea una **contraseña segura** (validada en vivo)
4. Accede con la contraseña (3 intentos)
5. Define el **tamaño de la muestra**
6. Ingresa alumnos (manual o con botón demo)
7. Explora estadísticas en el **dashboard**
8. **Genera reporte** HTML/TXT
9. El HTML se abre automáticamente en el navegador
10. Opcional: Ctrl+P → guardar como PDF

---

## Decisiones de Diseño

**¿Por qué tkinter y no PyQt?**
tkinter viene incluido en Python. PyQt requiere instalación pesada y licenciamiento.

**¿Por qué variables globales y no clases?**
El curso Principios de Programación 1 enseña paradigma **procedural**. Las clases se introducen en cursos posteriores.

**¿Por qué HTML para reportes?**
Cero dependencias externas. El profesor puede ejecutar el proyecto sin configurar entorno.

---

## Validaciones Implementadas

| Entrada | Validaciones |
|---------|--------------|
| Contraseña | 8+ caracteres, mayús, minús, número, símbolo |
| Confirmación | Debe coincidir con la original |
| Intentos login | Máximo 3, luego se bloquea |
| Tamaño muestra | Entero positivo, máximo 100 |
| Nombre alumno | No vacío, sin duplicados |
| Edad | Rango 4-18 años (edad escolar) |
| Opción menú | Rango 1-6 (consola) |

Todas las validaciones muestran mensajes de error específicos en español.

---

## Cómo Ejecutar el Proyecto

**Prerrequisito:** Python 3.6 o superior instalado.

```bash
# Descargar el proyecto y entrar a la carpeta
cd proyecto_final

# Ejecutar versión consola
python proyecto_final.py

# Ejecutar versión GUI
python proyecto_final_gui.py
```

**Sin instalaciones adicionales.** tkinter viene incluido en Python.

---

## Cómo Replicar el Proyecto

**Paso 1:** Crear archivo `proyecto_final.py` con la lógica base (5 funciones principales).

**Paso 2:** Probar en consola con casos par e impar para validar la mediana.

**Paso 3:** Crear `proyecto_final_gui.py` reutilizando las funciones de lógica.

**Paso 4:** Construir los 5 frames de tkinter uno a la vez, probando cada pantalla antes de pasar a la siguiente.

**Paso 5:** Añadir el generador de reportes HTML y TXT.

**Paso 6:** Testear el flujo completo end-to-end.

---

## Lecciones Aprendidas

**Técnicas:**
- Separar lógica de interfaz permite reutilizar código
- tkinter puede verse moderno con el tema correcto y buena paleta
- `after()` es la forma correcta de hacer tareas periódicas en GUI
- `bind("<Return>", ...)` mejora la UX sin agregar complejidad

**Conceptuales:**
- Los diccionarios son ideales para relacionar datos (nombre → edad)
- La mediana requiere ordenar primero y luego decidir par/impar
- Las validaciones en tiempo real mejoran la experiencia del usuario
- HTML + CSS da mejor resultado visual que muchas librerías PDF

---

## Métricas del Proyecto

- **285 líneas** versión consola
- **1200+ líneas** versión GUI
- **11 funciones** de lógica y estructura
- **5 pantallas** de flujo guiado
- **2 formatos** de reporte (HTML, TXT)
- **7 validaciones** distintas
- **0 librerías** externas
- **100%** de los requerimientos cumplidos

---

## Extras que Superan el Requerimiento

- Interfaz gráfica profesional completa
- Reloj en tiempo real
- Validación de contraseña visual en vivo
- Dashboard con cards empresariales
- Tabla de alumnos en vivo
- Generación automática de reportes HTML/TXT
- Conversión a PDF desde navegador
- Navegación por teclado (ENTER)
- Botón de datos de ejemplo para pruebas rápidas
- Timestamp automático en archivos de reporte

---

## Demostración en Vivo

A continuación se realizará la demostración de la aplicación mostrando:

1. Pantalla de bienvenida con reloj
2. Registro de contraseña con validación visual
3. Login con intentos limitados
4. Ingreso de alumnos (manual + demo)
5. Dashboard con todas las estadísticas
6. Generación de reporte HTML
7. Conversión a PDF desde el navegador

---

## Conclusión

El proyecto cumple **al 100% los requerimientos** del cliente DataByte para la Escuela San Pascualin, y añade una capa profesional de interfaz y reportería que hace la solución **lista para producción**.

El código está diseñado para ser:
- **Legible** (nombres en español, comentarios claros)
- **Mantenible** (funciones pequeñas con una responsabilidad)
- **Portable** (cero dependencias externas)
- **Extensible** (lógica separada de interfaz)

---

## Gracias

**Gabriel** — CENFOTEC

Proyecto Final — Principios de Programación 1
Fecha de entrega: 21 de abril, 2026

¿Preguntas?
