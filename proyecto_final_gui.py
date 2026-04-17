# -*- coding: utf-8 -*-
# Proyecto Final - Principios de Programacion 1
# Empresa: DataByte
# Escuela: San Pascualin
# Version: GUI con tkinter + generador de reportes HTML/TXT

import os
import random
import webbrowser
from datetime import datetime
from tkinter import Tk, Toplevel, StringVar, IntVar, Frame, Label, Entry, Button, Spinbox, messagebox
from tkinter import ttk


# ----------------- Variables globales de la aplicacion -----------------

alumnos = {}            # diccionario nombre -> edad
clave_guardada = ""     # contraseña registrada
intentos_restantes = 3  # intentos de login
tamano_muestra = 0      # n alumnos a ingresar
hora_inicio_sesion = "" # para mostrar en el status bar

# Paleta de colores corporativos
COLOR_PRIMARIO = "#1e3a5f"
COLOR_ACENTO = "#4a90e2"
COLOR_FONDO = "#f5f7fa"
COLOR_TEXTO = "#2c3e50"
COLOR_EXITO = "#27ae60"
COLOR_ERROR = "#e74c3c"
COLOR_BLANCO = "#ffffff"


# ----------------- Funciones de logica (reutilizadas de version consola) -----------------

def validar_contrasena(clave):
    # Devuelve tupla (valida, mensaje, checklist_dict)
    checklist = {
        "largo": len(clave) >= 8,
        "mayus": False,
        "minus": False,
        "numero": False,
        "simbolo": False,
    }
    simbolos = "!@#$%^&*()_-+=[]{};:,.<>?/|"

    for letra in clave:
        if letra.isupper():
            checklist["mayus"] = True
        elif letra.islower():
            checklist["minus"] = True
        elif letra.isdigit():
            checklist["numero"] = True
        elif letra in simbolos:
            checklist["simbolo"] = True

    if not checklist["largo"]:
        return False, "Debe tener al menos 8 caracteres", checklist
    if not checklist["mayus"]:
        return False, "Debe tener al menos una mayúscula", checklist
    if not checklist["minus"]:
        return False, "Debe tener al menos una minúscula", checklist
    if not checklist["numero"]:
        return False, "Debe tener al menos un número", checklist
    if not checklist["simbolo"]:
        return False, "Debe tener al menos un símbolo especial", checklist

    return True, "Contraseña válida", checklist


def obtener_edad_mayor(dic):
    mayor = -1
    nombre_mayor = ""
    for nombre in dic:
        if dic[nombre] > mayor:
            mayor = dic[nombre]
            nombre_mayor = nombre
    return nombre_mayor, mayor


def obtener_edad_menor(dic):
    menor = 999
    nombre_menor = ""
    for nombre in dic:
        if dic[nombre] < menor:
            menor = dic[nombre]
            nombre_menor = nombre
    return nombre_menor, menor


def calcular_promedio(dic):
    suma = 0
    cantidad = 0
    for nombre in dic:
        suma += dic[nombre]
        cantidad += 1
    promedio = suma / cantidad
    return round(promedio, 1)


def calcular_mediana(dic):
    edades = []
    for nombre in dic:
        edades.append(dic[nombre])
    edades.sort()

    cantidad = len(edades)
    mitad = cantidad // 2

    if cantidad % 2 == 1:
        return edades[mitad]
    else:
        return (edades[mitad - 1] + edades[mitad]) / 2


# ----------------- Configuracion de la ventana principal -----------------

ventana = Tk()
ventana.title("DataByte - Sistema de Estadísticas Escolares")
ventana.geometry("850x600")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

# Estilos ttk
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure("TFrame", background=COLOR_FONDO)
estilo.configure("Header.TFrame", background=COLOR_PRIMARIO)
estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                 font=("Segoe UI", 10))
estilo.configure("Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_PRIMARIO,
                 font=("Segoe UI", 20, "bold"))
estilo.configure("Subtitulo.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                 font=("Segoe UI", 12))
estilo.configure("Header.TLabel", background=COLOR_PRIMARIO, foreground=COLOR_BLANCO,
                 font=("Segoe UI", 11, "bold"))
estilo.configure("HeaderTitulo.TLabel", background=COLOR_PRIMARIO, foreground=COLOR_BLANCO,
                 font=("Segoe UI", 16, "bold"))
estilo.configure("Exito.TLabel", background=COLOR_FONDO, foreground=COLOR_EXITO,
                 font=("Segoe UI", 9))
estilo.configure("Error.TLabel", background=COLOR_FONDO, foreground=COLOR_ERROR,
                 font=("Segoe UI", 9))
estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=8)
estilo.configure("Nav.TButton", font=("Segoe UI", 10), padding=10, anchor="w")
estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                 background=COLOR_PRIMARIO, foreground=COLOR_BLANCO)

# Diccionario de frames y frame actual
frames = {}
frame_actual = None


def mostrar_frame(nombre):
    # Oculta todos los frames y muestra solo el solicitado
    global frame_actual
    for key in frames:
        frames[key].pack_forget()
    frames[nombre].pack(fill="both", expand=True)
    frame_actual = nombre


# ----------------- FRAME 1: Bienvenida -----------------

frame_bienvenida = ttk.Frame(ventana, style="TFrame")
frames["bienvenida"] = frame_bienvenida

# Contenedor centrado
cont_bienvenida = ttk.Frame(frame_bienvenida, style="TFrame")
cont_bienvenida.place(relx=0.5, rely=0.5, anchor="center")

# Logo/titulo DataByte
ttk.Label(cont_bienvenida, text="DataByte", style="Titulo.TLabel").pack(pady=(0, 5))
ttk.Label(cont_bienvenida, text="Sistema de Estadísticas Escolares",
          style="Subtitulo.TLabel").pack(pady=(0, 5))
ttk.Label(cont_bienvenida, text="Escuela San Pascualin",
          style="Subtitulo.TLabel").pack(pady=(0, 30))

# Reloj en vivo
reloj_var = StringVar()
lbl_reloj = Label(cont_bienvenida, textvariable=reloj_var,
                  bg=COLOR_FONDO, fg=COLOR_ACENTO,
                  font=("Segoe UI", 14, "bold"))
lbl_reloj.pack(pady=(0, 10))

fecha_var = StringVar()
lbl_fecha = Label(cont_bienvenida, textvariable=fecha_var,
                  bg=COLOR_FONDO, fg=COLOR_TEXTO,
                  font=("Segoe UI", 11))
lbl_fecha.pack(pady=(0, 40))


def actualizar_reloj():
    # Se vuelve a llamar cada 1000 ms
    ahora = datetime.now()
    reloj_var.set(ahora.strftime("%H:%M:%S"))
    fecha_var.set(ahora.strftime("%A, %d de %B del %Y"))
    ventana.after(1000, actualizar_reloj)


def ir_a_password():
    mostrar_frame("password")


btn_iniciar = Button(cont_bienvenida, text="Iniciar sesión",
                     bg=COLOR_ACENTO, fg=COLOR_BLANCO,
                     font=("Segoe UI", 11, "bold"),
                     bd=0, padx=30, pady=10, cursor="hand2",
                     activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
                     command=ir_a_password)
btn_iniciar.pack()

ttk.Label(cont_bienvenida, text="\nDataByte S.A. - Todos los derechos reservados",
          style="TLabel", font=("Segoe UI", 8)).pack(pady=(40, 0))

# ENTER desde la pantalla de bienvenida inicia sesion
ventana.bind("<Return>", lambda evento: ir_a_password() if frame_actual == "bienvenida" else None)


# ----------------- FRAME 2: Contrasena (registro + login) -----------------

frame_password = ttk.Frame(ventana, style="TFrame")
frames["password"] = frame_password

cont_password = ttk.Frame(frame_password, style="TFrame")
cont_password.place(relx=0.5, rely=0.5, anchor="center")

lbl_titulo_pwd = ttk.Label(cont_password, text="Registro de Acceso",
                           style="Titulo.TLabel")
lbl_titulo_pwd.pack(pady=(0, 5))

lbl_subtitulo_pwd = ttk.Label(cont_password,
                              text="Cree una contraseña segura para ingresar al sistema",
                              style="Subtitulo.TLabel")
lbl_subtitulo_pwd.pack(pady=(0, 20))

# Campo contraseña
frame_campo1 = ttk.Frame(cont_password, style="TFrame")
frame_campo1.pack(pady=5, fill="x")
ttk.Label(frame_campo1, text="Contraseña:").pack(anchor="w")
entry_pwd = Entry(frame_campo1, show="*", font=("Segoe UI", 11),
                  width=35, bd=1, relief="solid")
entry_pwd.pack(pady=(2, 0))

# Campo confirmacion
frame_campo2 = ttk.Frame(cont_password, style="TFrame")
frame_campo2.pack(pady=5, fill="x")
ttk.Label(frame_campo2, text="Confirmar contraseña:").pack(anchor="w")
entry_pwd2 = Entry(frame_campo2, show="*", font=("Segoe UI", 11),
                   width=35, bd=1, relief="solid")
entry_pwd2.pack(pady=(2, 0))

# Checklist de requisitos
frame_check = ttk.Frame(cont_password, style="TFrame")
frame_check.pack(pady=15, fill="x")

check_vars = {
    "largo": StringVar(value="x  Mínimo 8 caracteres"),
    "mayus": StringVar(value="x  Al menos una mayúscula"),
    "minus": StringVar(value="x  Al menos una minúscula"),
    "numero": StringVar(value="x  Al menos un número"),
    "simbolo": StringVar(value="x  Al menos un símbolo especial (!@#$%...)"),
}
check_labels = {}

for clave_check in check_vars:
    lbl = Label(frame_check, textvariable=check_vars[clave_check],
                bg=COLOR_FONDO, fg=COLOR_ERROR,
                font=("Segoe UI", 9), anchor="w")
    lbl.pack(anchor="w", pady=1)
    check_labels[clave_check] = lbl

# Mensaje de error/estado
mensaje_pwd = StringVar(value="")
lbl_mensaje_pwd = Label(cont_password, textvariable=mensaje_pwd,
                        bg=COLOR_FONDO, fg=COLOR_ERROR,
                        font=("Segoe UI", 9, "bold"))
lbl_mensaje_pwd.pack(pady=(5, 10))


def actualizar_checklist(evento=None):
    # Se ejecuta cada vez que el usuario teclea
    clave = entry_pwd.get()
    _, _, checklist = validar_contrasena(clave)

    textos = {
        "largo": "Mínimo 8 caracteres",
        "mayus": "Al menos una mayúscula",
        "minus": "Al menos una minúscula",
        "numero": "Al menos un número",
        "simbolo": "Al menos un símbolo especial (!@#$%...)",
    }

    for clave_c in checklist:
        if checklist[clave_c]:
            check_vars[clave_c].set("OK  " + textos[clave_c])
            check_labels[clave_c].configure(fg=COLOR_EXITO)
        else:
            check_vars[clave_c].set("x   " + textos[clave_c])
            check_labels[clave_c].configure(fg=COLOR_ERROR)


entry_pwd.bind("<KeyRelease>", actualizar_checklist)


def enter_pwd_registro(evento):
    # ENTER en el primer campo mueve foco al de confirmacion
    entry_pwd2.focus_set()


def enter_pwd2_registro(evento):
    # ENTER en el campo de confirmacion ejecuta el registro
    registrar_contrasena()


def enter_pwd_login(evento):
    # ENTER en el campo de login intenta acceso
    intentar_login()


entry_pwd.bind("<Return>", enter_pwd_registro)
entry_pwd2.bind("<Return>", enter_pwd2_registro)


def registrar_contrasena():
    global clave_guardada, hora_inicio_sesion

    clave = entry_pwd.get()
    confirm = entry_pwd2.get()

    valida, mensaje, _ = validar_contrasena(clave)
    if not valida:
        mensaje_pwd.set("Error: " + mensaje)
        return

    if clave != confirm:
        mensaje_pwd.set("Error: las contraseñas no coinciden")
        return

    # Guardar y pasar a login
    clave_guardada = clave
    hora_inicio_sesion = datetime.now().strftime("%H:%M")

    # Cambiar el frame a modo login
    entry_pwd.delete(0, "end")
    entry_pwd2.delete(0, "end")
    frame_check.pack_forget()
    frame_campo2.pack_forget()
    lbl_titulo_pwd.configure(text="Acceso al Sistema")
    lbl_subtitulo_pwd.configure(text="Ingrese su contraseña para continuar")
    btn_registrar.pack_forget()
    btn_login.pack(pady=10)
    mensaje_pwd.set("")

    # Cambiar el bind de ENTER al modo login
    entry_pwd.unbind("<Return>")
    entry_pwd.bind("<Return>", enter_pwd_login)

    entry_pwd.focus()


def intentar_login():
    global intentos_restantes

    ingresado = entry_pwd.get()
    if ingresado == clave_guardada:
        mostrar_frame("muestra")
        entry_muestra.focus()
        return

    intentos_restantes -= 1
    if intentos_restantes <= 0:
        messagebox.showerror("Acceso bloqueado",
                             "Demasiados intentos fallidos. La aplicación se cerrará.")
        ventana.destroy()
        return

    mensaje_pwd.set("Contraseña incorrecta. Intentos restantes: " +
                    str(intentos_restantes))
    entry_pwd.delete(0, "end")


btn_registrar = Button(cont_password, text="Registrar contraseña",
                       bg=COLOR_ACENTO, fg=COLOR_BLANCO,
                       font=("Segoe UI", 10, "bold"),
                       bd=0, padx=20, pady=8, cursor="hand2",
                       activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
                       command=registrar_contrasena)
btn_registrar.pack(pady=10)

btn_login = Button(cont_password, text="Ingresar",
                   bg=COLOR_EXITO, fg=COLOR_BLANCO,
                   font=("Segoe UI", 10, "bold"),
                   bd=0, padx=30, pady=8, cursor="hand2",
                   activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
                   command=intentar_login)


# ----------------- FRAME 3: Configuracion de muestra -----------------

frame_muestra = ttk.Frame(ventana, style="TFrame")
frames["muestra"] = frame_muestra

cont_muestra = ttk.Frame(frame_muestra, style="TFrame")
cont_muestra.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(cont_muestra, text="Configuración de Muestra",
          style="Titulo.TLabel").pack(pady=(0, 10))
ttk.Label(cont_muestra,
          text="Indique la cantidad de alumnos que serán registrados",
          style="Subtitulo.TLabel").pack(pady=(0, 30))

ttk.Label(cont_muestra, text="Tamaño de la muestra (n):").pack(anchor="w", pady=(0, 3))

entry_muestra = Entry(cont_muestra, font=("Segoe UI", 12),
                      width=20, bd=1, relief="solid", justify="center")
entry_muestra.pack(pady=(0, 5))

mensaje_muestra = StringVar(value="")
lbl_msg_muestra = Label(cont_muestra, textvariable=mensaje_muestra,
                        bg=COLOR_FONDO, fg=COLOR_ERROR,
                        font=("Segoe UI", 9, "bold"))
lbl_msg_muestra.pack(pady=(5, 15))


def confirmar_tamano():
    global tamano_muestra

    valor = entry_muestra.get().strip()
    if not valor.isdigit():
        mensaje_muestra.set("Error: debe ingresar un número entero positivo")
        return

    n = int(valor)
    if n <= 0:
        mensaje_muestra.set("Error: la cantidad debe ser mayor que cero")
        return

    if n > 100:
        mensaje_muestra.set("Error: máximo 100 alumnos por muestra")
        return

    tamano_muestra = n
    mensaje_muestra.set("")
    lbl_progreso_alumnos.configure(text="Alumno 1 de " + str(n))
    mostrar_frame("alumnos")
    entry_nombre.focus()


Button(cont_muestra, text="Continuar",
       bg=COLOR_ACENTO, fg=COLOR_BLANCO,
       font=("Segoe UI", 10, "bold"),
       bd=0, padx=30, pady=8, cursor="hand2",
       activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
       command=confirmar_tamano).pack()

entry_muestra.bind("<Return>", lambda evento: confirmar_tamano())


# ----------------- FRAME 4: Ingreso de alumnos -----------------

frame_alumnos = ttk.Frame(ventana, style="TFrame")
frames["alumnos"] = frame_alumnos

# Header del frame
header_alumnos = ttk.Frame(frame_alumnos, style="Header.TFrame")
header_alumnos.pack(fill="x")

ttk.Label(header_alumnos, text="Registro de Alumnos",
          style="HeaderTitulo.TLabel").pack(side="left", padx=20, pady=12)

lbl_progreso_alumnos = Label(header_alumnos, text="Alumno 1 de N",
                             bg=COLOR_PRIMARIO, fg=COLOR_BLANCO,
                             font=("Segoe UI", 11))
lbl_progreso_alumnos.pack(side="right", padx=20, pady=12)

# Zona principal dividida en 2
cont_alumnos = ttk.Frame(frame_alumnos, style="TFrame")
cont_alumnos.pack(fill="both", expand=True, padx=20, pady=15)

# Panel izquierdo: formulario
panel_form = ttk.Frame(cont_alumnos, style="TFrame")
panel_form.pack(side="left", fill="y", padx=(0, 20))

ttk.Label(panel_form, text="Datos del alumno",
          font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

ttk.Label(panel_form, text="Nombre:").pack(anchor="w")
entry_nombre = Entry(panel_form, font=("Segoe UI", 11),
                     width=28, bd=1, relief="solid")
entry_nombre.pack(pady=(2, 10))

ttk.Label(panel_form, text="Edad:").pack(anchor="w")
edad_var = IntVar(value=8)
spin_edad = Spinbox(panel_form, from_=4, to=18, textvariable=edad_var,
                    font=("Segoe UI", 11), width=10, bd=1, relief="solid")
spin_edad.pack(pady=(2, 10), anchor="w")

mensaje_alumno = StringVar(value="")
lbl_msg_alumno = Label(panel_form, textvariable=mensaje_alumno,
                       bg=COLOR_FONDO, fg=COLOR_ERROR,
                       font=("Segoe UI", 9, "bold"),
                       wraplength=250, justify="left")
lbl_msg_alumno.pack(pady=(5, 10), anchor="w")

btn_agregar = Button(panel_form, text="Agregar alumno",
                     bg=COLOR_ACENTO, fg=COLOR_BLANCO,
                     font=("Segoe UI", 10, "bold"),
                     bd=0, padx=15, pady=6, cursor="hand2",
                     activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
                     command=lambda: agregar_alumno())
btn_agregar.pack(pady=(0, 6), anchor="w")

btn_llenar_demo = Button(panel_form, text="Llenar con datos de ejemplo",
                         bg="#95a5a6", fg=COLOR_BLANCO,
                         font=("Segoe UI", 9),
                         bd=0, padx=15, pady=5, cursor="hand2",
                         activebackground=COLOR_TEXTO,
                         activeforeground=COLOR_BLANCO,
                         command=lambda: llenar_datos_demo())
btn_llenar_demo.pack(pady=(0, 10), anchor="w")

btn_continuar_dash = Button(panel_form, text="Continuar al panel principal >",
                            bg=COLOR_EXITO, fg=COLOR_BLANCO,
                            font=("Segoe UI", 10, "bold"),
                            bd=0, padx=15, pady=6, cursor="hand2",
                            activebackground=COLOR_PRIMARIO,
                            activeforeground=COLOR_BLANCO,
                            state="disabled",
                            command=lambda: ir_a_dashboard())

# Panel derecho: tabla
panel_tabla = ttk.Frame(cont_alumnos, style="TFrame")
panel_tabla.pack(side="left", fill="both", expand=True)

ttk.Label(panel_tabla, text="Alumnos registrados",
          font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))

tree_alumnos = ttk.Treeview(panel_tabla, columns=("num", "nombre", "edad"),
                            show="headings", height=15)
tree_alumnos.heading("num", text="#")
tree_alumnos.heading("nombre", text="Nombre")
tree_alumnos.heading("edad", text="Edad")
tree_alumnos.column("num", width=40, anchor="center")
tree_alumnos.column("nombre", width=200)
tree_alumnos.column("edad", width=70, anchor="center")
tree_alumnos.pack(fill="both", expand=True)


def enter_nombre_alumno(evento):
    # ENTER en el campo nombre mueve el foco a la edad
    spin_edad.focus_set()
    spin_edad.selection_range(0, "end")


def enter_edad_alumno(evento):
    # ENTER en la edad agrega el alumno directamente
    agregar_alumno()


entry_nombre.bind("<Return>", enter_nombre_alumno)
spin_edad.bind("<Return>", enter_edad_alumno)


def agregar_alumno():
    nombre = entry_nombre.get().strip()

    if nombre == "":
        mensaje_alumno.set("Error: el nombre no puede estar vacío")
        return

    if nombre in alumnos:
        mensaje_alumno.set("Error: ya existe un alumno con ese nombre")
        return

    try:
        edad = int(edad_var.get())
    except:
        mensaje_alumno.set("Error: la edad no es válida")
        return

    if edad < 4 or edad > 18:
        mensaje_alumno.set("Error: la edad debe estar entre 4 y 18 años")
        return

    # Guardar en diccionario
    alumnos[nombre] = edad
    mensaje_alumno.set("")

    # Actualizar tabla
    num = len(alumnos)
    tree_alumnos.insert("", "end", values=(num, nombre, edad))

    # Limpiar formulario
    entry_nombre.delete(0, "end")
    edad_var.set(8)
    entry_nombre.focus()

    # Actualizar progreso
    if num >= tamano_muestra:
        lbl_progreso_alumnos.configure(text="Completado: " + str(num) + " de " +
                                            str(tamano_muestra))
        btn_agregar.configure(state="disabled")
        btn_llenar_demo.configure(state="disabled")
        btn_continuar_dash.configure(state="normal")
        btn_continuar_dash.pack(pady=(10, 0), anchor="w")
        mensaje_alumno.set("Muestra completada. Continúe al panel principal.")
        lbl_msg_alumno.configure(fg=COLOR_EXITO)
    else:
        lbl_progreso_alumnos.configure(text="Alumno " + str(num + 1) + " de " +
                                            str(tamano_muestra))


def llenar_datos_demo():
    # Rellena los alumnos restantes con datos de ejemplo aleatorios
    nombres_demo = [
        "Ana Rodriguez", "Luis Martinez", "Maria Jimenez", "Pedro Solano",
        "Sofia Vargas", "Carlos Mora", "Valeria Castro", "Diego Rojas",
        "Camila Arias", "Andres Leon", "Isabella Ramirez", "Mateo Chaves",
        "Lucia Gonzalez", "Samuel Quesada", "Emma Fernandez", "Gabriel Sanchez",
        "Martina Salas", "Daniel Herrera", "Elena Cordero", "Sebastian Porras",
        "Victoria Alvarado", "Nicolas Monge", "Paula Badilla", "Tomas Araya",
        "Renata Campos", "Javier Umanzor", "Olivia Navarro", "Benjamin Cruz",
        "Amelia Zuniga", "Adrian Obando", "Julieta Madrigal", "Mauricio Gomez",
        "Antonella Brenes", "Santiago Calderon", "Regina Bonilla", "Emilio Ulloa",
        "Fernanda Aguilar", "Ignacio Vega", "Natalia Esquivel", "Rafael Picado",
        "Mia Gutierrez", "Lorenzo Villalobos", "Catalina Segura", "Francisco Barrantes",
        "Constanza Alfaro"
    ]

    faltantes = tamano_muestra - len(alumnos)
    if faltantes <= 0:
        mensaje_alumno.set("La muestra ya está completa")
        return

    # Filtrar nombres disponibles (que no esten ya en el diccionario)
    disponibles = []
    for n in nombres_demo:
        if n not in alumnos:
            disponibles.append(n)

    # Si no alcanzan, generar sufijos
    while len(disponibles) < faltantes:
        disponibles.append("Alumno " + str(len(disponibles) + 1))

    # Agregar los que falten
    agregados = 0
    for nombre in disponibles:
        if agregados >= faltantes:
            break
        if nombre in alumnos:
            continue
        edad = random.randint(4, 18)
        alumnos[nombre] = edad
        num = len(alumnos)
        tree_alumnos.insert("", "end", values=(num, nombre, edad))
        agregados += 1

    # Actualizar estado visual
    total = len(alumnos)
    lbl_progreso_alumnos.configure(text="Completado: " + str(total) +
                                        " de " + str(tamano_muestra))
    btn_agregar.configure(state="disabled")
    btn_llenar_demo.configure(state="disabled")
    btn_continuar_dash.configure(state="normal")
    btn_continuar_dash.pack(pady=(10, 0), anchor="w")
    mensaje_alumno.set("Muestra completada con datos de ejemplo. "
                       "Continúe al panel principal.")
    lbl_msg_alumno.configure(fg=COLOR_EXITO)


def ir_a_dashboard():
    actualizar_dashboard()
    mostrar_frame("dashboard")


# ----------------- FRAME 5: Dashboard principal -----------------

frame_dashboard = ttk.Frame(ventana, style="TFrame")
frames["dashboard"] = frame_dashboard

# Header superior
header_dash = ttk.Frame(frame_dashboard, style="Header.TFrame")
header_dash.pack(fill="x")

ttk.Label(header_dash, text="DataByte",
          style="HeaderTitulo.TLabel").pack(side="left", padx=20, pady=12)

ttk.Label(header_dash, text=" | Panel de Estadísticas",
          style="Header.TLabel").pack(side="left", pady=12)

info_sesion_var = StringVar(value="")
Label(header_dash, textvariable=info_sesion_var,
      bg=COLOR_PRIMARIO, fg=COLOR_BLANCO,
      font=("Segoe UI", 10)).pack(side="right", padx=20, pady=12)

# Cuerpo dividido en lateral + contenido
cuerpo_dash = ttk.Frame(frame_dashboard, style="TFrame")
cuerpo_dash.pack(fill="both", expand=True)

# Lateral izquierdo (navegacion)
lateral = Frame(cuerpo_dash, bg="#e8ecf0", width=200)
lateral.pack(side="left", fill="y")
lateral.pack_propagate(False)

Label(lateral, text="MENÚ", bg="#e8ecf0", fg=COLOR_PRIMARIO,
      font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 5))

# Panel derecho (contenido)
panel_contenido = Frame(cuerpo_dash, bg=COLOR_BLANCO)
panel_contenido.pack(side="left", fill="both", expand=True, padx=15, pady=15)

# Status bar
status_bar = Frame(frame_dashboard, bg=COLOR_PRIMARIO, height=25)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

status_var = StringVar(value="")
Label(status_bar, textvariable=status_var,
      bg=COLOR_PRIMARIO, fg=COLOR_BLANCO,
      font=("Segoe UI", 9)).pack(side="left", padx=15, pady=3)


def limpiar_contenido():
    for widget in panel_contenido.winfo_children():
        widget.destroy()


def actualizar_dashboard():
    info_sesion_var.set("Sesión iniciada a las " + hora_inicio_sesion)
    status_var.set("Total alumnos: " + str(len(alumnos)) +
                   "   |   Muestra: " + str(tamano_muestra) +
                   "   |   " + datetime.now().strftime("%d/%m/%Y"))
    ver_resumen()


def titulo_seccion(texto):
    Label(panel_contenido, text=texto,
          bg=COLOR_BLANCO, fg=COLOR_PRIMARIO,
          font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))


def ver_alumnos():
    limpiar_contenido()
    titulo_seccion("Listado de Alumnos")

    tree = ttk.Treeview(panel_contenido, columns=("num", "nombre", "edad"),
                        show="headings", height=18)
    tree.heading("num", text="#")
    tree.heading("nombre", text="Nombre")
    tree.heading("edad", text="Edad")
    tree.column("num", width=50, anchor="center")
    tree.column("nombre", width=300)
    tree.column("edad", width=100, anchor="center")

    i = 1
    for nombre in alumnos:
        tree.insert("", "end", values=(i, nombre, alumnos[nombre]))
        i += 1

    tree.pack(fill="both", expand=True)
    Label(panel_contenido, text="Total de alumnos registrados: " + str(len(alumnos)),
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10, "italic")).pack(anchor="e", pady=(10, 0))


def crear_card(parent, titulo, valor, color):
    # Card estilo dashboard
    card = Frame(parent, bg=COLOR_BLANCO, bd=1, relief="solid",
                 highlightbackground="#dce3eb", highlightthickness=1)
    card.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    Label(card, text=titulo, bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10)).pack(pady=(15, 5), padx=15, anchor="w")
    Label(card, text=valor, bg=COLOR_BLANCO, fg=color,
          font=("Segoe UI", 22, "bold")).pack(pady=(0, 15), padx=15, anchor="w")


def ver_mayor_menor():
    limpiar_contenido()
    titulo_seccion("Edad Mayor y Menor")

    nombre_max, edad_max = obtener_edad_mayor(alumnos)
    nombre_min, edad_min = obtener_edad_menor(alumnos)

    contenedor_cards = Frame(panel_contenido, bg=COLOR_BLANCO)
    contenedor_cards.pack(fill="x", pady=10)

    crear_card(contenedor_cards, "Edad mayor", str(edad_max) + " años", COLOR_ACENTO)
    crear_card(contenedor_cards, "Edad menor", str(edad_min) + " años", COLOR_EXITO)

    Label(panel_contenido,
          text="\nAlumno con la edad mayor: " + nombre_max,
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 11)).pack(anchor="w", pady=5)
    Label(panel_contenido,
          text="Alumno con la edad menor: " + nombre_min,
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 11)).pack(anchor="w", pady=5)


def ver_promedio():
    limpiar_contenido()
    titulo_seccion("Promedio de Edades")

    prom = calcular_promedio(alumnos)

    contenedor = Frame(panel_contenido, bg=COLOR_BLANCO)
    contenedor.pack(fill="x", pady=10)
    crear_card(contenedor, "Promedio (1 decimal)", str(prom) + " años", COLOR_ACENTO)

    Label(panel_contenido,
          text="\nCalculado sobre " + str(len(alumnos)) + " alumnos de la muestra.",
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10, "italic")).pack(anchor="w", pady=10)


def ver_mediana():
    limpiar_contenido()
    titulo_seccion("Mediana de Edades")

    med = calcular_mediana(alumnos)
    cantidad = len(alumnos)

    contenedor = Frame(panel_contenido, bg=COLOR_BLANCO)
    contenedor.pack(fill="x", pady=10)
    crear_card(contenedor, "Mediana", str(med) + " años", COLOR_ACENTO)

    if cantidad % 2 == 1:
        explicacion = ("Muestra impar (n=" + str(cantidad) +
                       "): la mediana es el valor central de la lista ordenada.")
    else:
        explicacion = ("Muestra par (n=" + str(cantidad) +
                       "): la mediana es el promedio de los dos valores centrales.")

    Label(panel_contenido, text="\n" + explicacion,
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10, "italic"),
          wraplength=500, justify="left").pack(anchor="w", pady=10)


def ver_resumen():
    limpiar_contenido()
    titulo_seccion("Resumen Estadístico")

    nombre_max, edad_max = obtener_edad_mayor(alumnos)
    nombre_min, edad_min = obtener_edad_menor(alumnos)
    prom = calcular_promedio(alumnos)
    med = calcular_mediana(alumnos)

    # Fila de 4 cards
    fila = Frame(panel_contenido, bg=COLOR_BLANCO)
    fila.pack(fill="x", pady=10)

    crear_card(fila, "Total alumnos", str(len(alumnos)), COLOR_PRIMARIO)
    crear_card(fila, "Edad mayor", str(edad_max), COLOR_ACENTO)
    crear_card(fila, "Edad menor", str(edad_min), COLOR_EXITO)
    crear_card(fila, "Promedio", str(prom), COLOR_ACENTO)

    fila2 = Frame(panel_contenido, bg=COLOR_BLANCO)
    fila2.pack(fill="x", pady=5)
    crear_card(fila2, "Mediana", str(med), COLOR_PRIMARIO)
    # Espacios vacios para mantener proporciones
    Frame(fila2, bg=COLOR_BLANCO).pack(side="left", fill="both", expand=True, padx=5)
    Frame(fila2, bg=COLOR_BLANCO).pack(side="left", fill="both", expand=True, padx=5)
    Frame(fila2, bg=COLOR_BLANCO).pack(side="left", fill="both", expand=True, padx=5)

    Label(panel_contenido,
          text="\nUtilice el menú lateral para explorar cada estadística en detalle "
               "o generar un reporte completo.",
          bg=COLOR_BLANCO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10, "italic"),
          wraplength=600, justify="left").pack(anchor="w", pady=10)


def salir_app():
    respuesta = messagebox.askyesno("Confirmar salida",
                                    "Desea cerrar la aplicación?")
    if respuesta:
        ventana.destroy()


# Botones del menu lateral (se completan despues de definir la funcion de reporte)
def crear_boton_nav(texto, comando):
    btn = Button(lateral, text=texto, command=comando,
                 bg="#e8ecf0", fg=COLOR_TEXTO,
                 font=("Segoe UI", 10), bd=0,
                 padx=10, pady=10, cursor="hand2",
                 anchor="w", width=22,
                 activebackground=COLOR_ACENTO,
                 activeforeground=COLOR_BLANCO)
    btn.pack(fill="x", padx=5, pady=1)
    return btn


crear_boton_nav("  Resumen general", ver_resumen)
crear_boton_nav("  Listado de alumnos", ver_alumnos)
crear_boton_nav("  Edad mayor y menor", ver_mayor_menor)
crear_boton_nav("  Promedio", ver_promedio)
crear_boton_nav("  Mediana", ver_mediana)


# ----------------- Generacion de reportes -----------------

def generar_reporte_html():
    nombre_max, edad_max = obtener_edad_mayor(alumnos)
    nombre_min, edad_min = obtener_edad_menor(alumnos)
    prom = calcular_promedio(alumnos)
    med = calcular_mediana(alumnos)
    ahora = datetime.now()
    fecha_str = ahora.strftime("%d/%m/%Y %H:%M")

    # Construir las filas de la tabla
    filas_html = ""
    i = 1
    for nombre in alumnos:
        filas_html += ("      <tr><td>" + str(i) + "</td><td>" + nombre +
                       "</td><td>" + str(alumnos[nombre]) + "</td></tr>\n")
        i += 1

    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reporte Estadístico - Escuela San Pascualin</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f5f7fa;
    color: #2c3e50;
    padding: 30px;
  }
  .contenedor {
    max-width: 850px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    overflow: hidden;
  }
  header {
    background: linear-gradient(135deg, #1e3a5f 0%, #4a90e2 100%);
    color: #ffffff;
    padding: 30px 40px;
  }
  header h1 {
    font-size: 28px;
    letter-spacing: 1px;
  }
  header h2 {
    font-size: 16px;
    font-weight: 400;
    margin-top: 5px;
    opacity: 0.9;
  }
  header .meta {
    margin-top: 15px;
    font-size: 12px;
    opacity: 0.85;
  }
  section {
    padding: 30px 40px;
  }
  h3 {
    color: #1e3a5f;
    border-bottom: 2px solid #4a90e2;
    padding-bottom: 8px;
    margin-bottom: 20px;
    font-size: 18px;
  }
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
    margin-bottom: 30px;
  }
  .card {
    background: #f5f7fa;
    border-left: 4px solid #4a90e2;
    padding: 15px 20px;
    border-radius: 4px;
  }
  .card .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #7f8c8d;
    margin-bottom: 6px;
  }
  .card .valor {
    font-size: 24px;
    font-weight: bold;
    color: #1e3a5f;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  table th {
    background: #1e3a5f;
    color: #ffffff;
    text-align: left;
    padding: 12px 15px;
    font-size: 13px;
    letter-spacing: 0.5px;
  }
  table td {
    padding: 10px 15px;
    border-bottom: 1px solid #ecf0f1;
    font-size: 14px;
  }
  table tr:nth-child(even) td {
    background: #f8f9fb;
  }
  table tr:hover td {
    background: #e8f0fa;
  }
  footer {
    background: #ecf0f1;
    padding: 20px 40px;
    text-align: center;
    font-size: 11px;
    color: #7f8c8d;
  }
</style>
</head>
<body>
  <div class="contenedor">
    <header>
      <h1>DataByte</h1>
      <h2>Reporte Estadístico de Edades - Escuela San Pascualin</h2>
      <div class="meta">Generado el """ + fecha_str + """ | Muestra de """ + str(len(alumnos)) + """ alumnos</div>
    </header>

    <section>
      <h3>Resumen Estadístico</h3>
      <div class="cards">
        <div class="card"><div class="label">Total alumnos</div><div class="valor">""" + str(len(alumnos)) + """</div></div>
        <div class="card"><div class="label">Edad mayor</div><div class="valor">""" + str(edad_max) + """</div></div>
        <div class="card"><div class="label">Edad menor</div><div class="valor">""" + str(edad_min) + """</div></div>
        <div class="card"><div class="label">Promedio</div><div class="valor">""" + str(prom) + """</div></div>
        <div class="card"><div class="label">Mediana</div><div class="valor">""" + str(med) + """</div></div>
      </div>

      <h3>Detalles</h3>
      <p style="margin-bottom:10px;font-size:13px;">
        <strong>Alumno con la edad mayor:</strong> """ + nombre_max + """ (""" + str(edad_max) + """ años)<br>
        <strong>Alumno con la edad menor:</strong> """ + nombre_min + """ (""" + str(edad_min) + """ años)
      </p>
    </section>

    <section>
      <h3>Listado Completo de Alumnos</h3>
      <table>
        <thead>
          <tr><th>#</th><th>Nombre</th><th>Edad</th></tr>
        </thead>
        <tbody>
""" + filas_html + """        </tbody>
      </table>
    </section>

    <footer>
      Reporte generado automáticamente por el Sistema DataByte v1.0<br>
      Este documento es confidencial y de uso interno de la Escuela San Pascualin.
    </footer>
  </div>
</body>
</html>
"""
    return html


def generar_reporte_txt():
    nombre_max, edad_max = obtener_edad_mayor(alumnos)
    nombre_min, edad_min = obtener_edad_menor(alumnos)
    prom = calcular_promedio(alumnos)
    med = calcular_mediana(alumnos)
    ahora = datetime.now()
    fecha_str = ahora.strftime("%d/%m/%Y %H:%M")

    linea = "=" * 60
    texto = ""
    texto += linea + "\n"
    texto += "            DATABYTE - REPORTE ESTADÍSTICO\n"
    texto += "            Escuela San Pascualin\n"
    texto += linea + "\n"
    texto += "Generado: " + fecha_str + "\n"
    texto += "Muestra:  " + str(len(alumnos)) + " alumnos\n"
    texto += linea + "\n\n"

    texto += "RESUMEN ESTADÍSTICO\n"
    texto += "-" * 60 + "\n"
    texto += "Total alumnos registrados : " + str(len(alumnos)) + "\n"
    texto += "Edad mayor                : " + str(edad_max) + " años (" + nombre_max + ")\n"
    texto += "Edad menor                : " + str(edad_min) + " años (" + nombre_min + ")\n"
    texto += "Promedio de edades        : " + str(prom) + " años\n"
    texto += "Mediana de edades         : " + str(med) + " años\n\n"

    texto += "LISTADO DE ALUMNOS\n"
    texto += "-" * 60 + "\n"
    texto += "#    Nombre                          Edad\n"
    texto += "-" * 60 + "\n"

    i = 1
    for nombre in alumnos:
        num_str = str(i).ljust(5)
        nom_str = nombre.ljust(32)
        texto += num_str + nom_str + str(alumnos[nombre]) + "\n"
        i += 1

    texto += "\n" + linea + "\n"
    texto += "Fin del reporte - DataByte Sistema v1.0\n"
    texto += linea + "\n"

    return texto


def guardar_reporte(contenido, extension):
    # Crear carpeta reportes si no existe
    try:
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        carpeta_base = os.getcwd()
    carpeta_reportes = os.path.join(carpeta_base, "reportes")
    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)

    # Nombre con timestamp
    ahora = datetime.now()
    nombre_archivo = "reporte_" + ahora.strftime("%Y-%m-%d_%H-%M-%S") + "." + extension
    ruta = os.path.join(carpeta_reportes, nombre_archivo)

    archivo = open(ruta, "w", encoding="utf-8")
    archivo.write(contenido)
    archivo.close()

    return ruta


def abrir_reporte(ruta):
    try:
        if ruta.endswith(".html"):
            webbrowser.open("file:///" + ruta.replace("\\", "/"))
        else:
            os.startfile(ruta)
    except Exception as e:
        messagebox.showwarning("No se pudo abrir",
                               "El reporte se guardó pero no se pudo abrir automáticamente.\n"
                               "Ruta: " + ruta)


def dialogo_generar_reporte():
    # Ventana modal para elegir formato
    dialogo = Toplevel(ventana)
    dialogo.title("Generar Reporte")
    dialogo.geometry("400x310")
    dialogo.configure(bg=COLOR_FONDO)
    dialogo.resizable(False, False)

    Label(dialogo, text="Generar Reporte",
          bg=COLOR_FONDO, fg=COLOR_PRIMARIO,
          font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
    Label(dialogo, text="Seleccione el formato de salida",
          bg=COLOR_FONDO, fg=COLOR_TEXTO,
          font=("Segoe UI", 10)).pack(pady=(0, 20))

    def accion(formato):
        rutas = []
        if formato == "html" or formato == "ambos":
            ruta_html = guardar_reporte(generar_reporte_html(), "html")
            rutas.append(ruta_html)
        if formato == "txt" or formato == "ambos":
            ruta_txt = guardar_reporte(generar_reporte_txt(), "txt")
            rutas.append(ruta_txt)

        dialogo.destroy()

        # Mostrar confirmacion y abrir
        mensaje = "Reporte(s) guardado(s) en:\n\n"
        for r in rutas:
            mensaje += r + "\n"

        messagebox.showinfo("Reporte generado", mensaje)

        # Abrir el HTML si existe (mas visual)
        for r in rutas:
            if r.endswith(".html"):
                abrir_reporte(r)
                return
        # Si no hay HTML, abrir el TXT
        if rutas:
            abrir_reporte(rutas[0])

    Button(dialogo, text="HTML (profesional, abre en navegador)",
           bg=COLOR_ACENTO, fg=COLOR_BLANCO,
           font=("Segoe UI", 10, "bold"),
           bd=0, padx=20, pady=10, cursor="hand2",
           activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
           command=lambda: accion("html")).pack(pady=4, fill="x", padx=40)

    Button(dialogo, text="TXT (texto plano)",
           bg=COLOR_TEXTO, fg=COLOR_BLANCO,
           font=("Segoe UI", 10, "bold"),
           bd=0, padx=20, pady=10, cursor="hand2",
           activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
           command=lambda: accion("txt")).pack(pady=4, fill="x", padx=40)

    Button(dialogo, text="Ambos formatos",
           bg=COLOR_EXITO, fg=COLOR_BLANCO,
           font=("Segoe UI", 10, "bold"),
           bd=0, padx=20, pady=10, cursor="hand2",
           activebackground=COLOR_PRIMARIO, activeforeground=COLOR_BLANCO,
           command=lambda: accion("ambos")).pack(pady=4, fill="x", padx=40)

    Button(dialogo, text="Cancelar",
           bg=COLOR_FONDO, fg=COLOR_TEXTO,
           font=("Segoe UI", 9),
           bd=0, cursor="hand2",
           command=dialogo.destroy).pack(pady=(10, 0))

    dialogo.transient(ventana)
    dialogo.grab_set()
    dialogo.wait_window()


# Botones finales del menu lateral
Frame(lateral, bg="#e8ecf0", height=20).pack()
crear_boton_nav("  Generar reporte", dialogo_generar_reporte)
crear_boton_nav("  Salir", salir_app)


# ----------------- Inicio de la aplicacion -----------------

def iniciar_app():
    actualizar_reloj()
    mostrar_frame("bienvenida")
    ventana.mainloop()


iniciar_app()
