# Proyecto Final - Principios de Programacion 1

**Empresa:** DataByte
**Cliente:** Escuela San Pascualin
**Entrega:** Martes 21 de abril, 2026

## Descripcion

Programa en Python que calcula y muestra estadisticas de edades de una
muestra de alumnos de la escuela San Pascualin.

El proyecto incluye DOS versiones:

1. **`proyecto_final.py`** — version de consola (texto en terminal).
2. **`proyecto_final_gui.py`** — version con interfaz grafica y generador
   de reportes HTML y TXT.

Ambas versiones cumplen los mismos requerimientos. La version GUI añade
una experiencia visual profesional y permite exportar los resultados a
archivos.

## Requerimientos cumplidos

- [x] Almacenar en un diccionario nombre y edad de los alumnos
- [x] Obtener la edad mayor y menor
- [x] Calcular el promedio de edades con un decimal
- [x] Calcular y mostrar la mediana (maneja muestra par e impar)
- [x] Uso de funciones `def` para todas las operaciones
- [x] Contrasena segura antes del menu
- [x] Menu de opciones con validaciones
- [x] Fecha y hora al cargar la aplicacion

**Extras de la version GUI:**

- [x] Interfaz grafica con tkinter (biblioteca estandar)
- [x] Reloj en vivo en la pantalla de bienvenida
- [x] Validacion de contrasena en tiempo real (checklist visual)
- [x] Tabla de alumnos con actualizacion automatica
- [x] Dashboard con cards estilo empresarial
- [x] Generador de reporte HTML con estilos profesionales
- [x] Generador de reporte TXT como respaldo
- [x] Los reportes se guardan con timestamp en carpeta `reportes/`

## Como ejecutar

Version de consola:
```
python proyecto_final.py
```

Version con interfaz grafica:
```
python proyecto_final_gui.py
```

Requiere Python 3.6 o superior. **No necesita librerias externas**
(tkinter viene incluido en la instalacion estandar de Python).

## Flujo de uso (version GUI)

1. **Pantalla de bienvenida** — muestra titulo, logo textual, fecha y
   hora actualizandose en vivo.
2. **Registro de contrasena** — el usuario crea una contrasena segura.
   Los requisitos se marcan en verde en tiempo real conforme se teclea.
3. **Login** — ingresa la contrasena para acceder. Tiene 3 intentos.
4. **Configuracion** — indica el tamano de la muestra (n alumnos).
5. **Ingreso de alumnos** — formulario con campo de nombre y edad
   (spinbox 4-18). La tabla lateral muestra los registros en vivo.
6. **Dashboard principal** — menu lateral con secciones:
   - Resumen general (5 cards con todas las estadisticas)
   - Listado de alumnos
   - Edad mayor y menor
   - Promedio
   - Mediana
   - Generar reporte (HTML, TXT o ambos)
   - Salir
7. **Reporte generado** — se guarda en `reportes/reporte_YYYY-MM-DD_HH-MM-SS.ext`
   y se abre automaticamente (HTML en navegador, TXT en Notepad).

## Como convertir el reporte HTML en PDF

Despues de generar el reporte HTML, desde el navegador presione
**Ctrl+P** y en la ventana de impresion seleccione como destino
"Guardar como PDF". El resultado es un PDF profesional sin necesidad
de instalar librerias externas.

## Estructura de funciones

### Logica (compartida por ambas versiones)

| Funcion | Proposito |
|---------|-----------|
| `validar_contrasena(clave)` | Verifica requisitos de seguridad |
| `obtener_edad_mayor(alumnos)` | Busca la edad maxima |
| `obtener_edad_menor(alumnos)` | Busca la edad minima |
| `calcular_promedio(alumnos)` | Promedio con 1 decimal |
| `calcular_mediana(alumnos)` | Mediana (par/impar) |

### Especificas de la version consola

| Funcion | Proposito |
|---------|-----------|
| `mostrar_fecha_hora()` | Banner con fecha y hora |
| `crear_contrasena()` | Flujo interactivo de registro |
| `autenticar(clave_real)` | Login con 3 intentos |
| `pedir_tamano_muestra()` | Valida n entero positivo |
| `ingresar_alumnos(n)` | Carga diccionario de alumnos |
| `ejecutar_menu(alumnos)` | Bucle del menu principal |

### Especificas de la version GUI

| Funcion | Proposito |
|---------|-----------|
| `mostrar_frame(nombre)` | Navega entre pantallas |
| `actualizar_reloj()` | Refresca fecha/hora cada segundo |
| `actualizar_checklist()` | Validacion visual de contrasena |
| `registrar_contrasena()` | Guarda la contrasena creada |
| `intentar_login()` | Verifica credenciales (3 intentos) |
| `confirmar_tamano()` | Valida el tamano de muestra |
| `agregar_alumno()` | Anade alumno al diccionario y tabla |
| `ver_resumen()`, `ver_alumnos()`, etc. | Cada seccion del dashboard |
| `generar_reporte_html()` | Genera HTML con CSS profesional |
| `generar_reporte_txt()` | Genera reporte en texto plano |
| `guardar_reporte(contenido, ext)` | Guarda con timestamp |
| `abrir_reporte(ruta)` | Abre el reporte generado |
| `dialogo_generar_reporte()` | Modal de seleccion de formato |

## Estructura de archivos

```
proyecto_final/
├── proyecto_final.py           # Version consola
├── proyecto_final_gui.py       # Version GUI
├── README.md                   # Este documento
└── reportes/                   # (se crea al generar el primer reporte)
    ├── reporte_YYYY-MM-DD_HH-MM-SS.html
    └── reporte_YYYY-MM-DD_HH-MM-SS.txt
```

## Ejemplo de salida

Ambas versiones producen el mismo resultado estadistico:

```
Alumnos: Ana=8, Luis=10, Maria=7, Pedro=12, Sofia=9

Edad mayor: 12 anos (Pedro)
Edad menor: 7 anos (Maria)
Promedio:   9.2 anos
Mediana:    9 anos  (muestra impar, valor central)
```

Con muestra par (4 alumnos), la mediana se calcula como el promedio
de los dos valores centrales.
