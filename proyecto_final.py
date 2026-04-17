# -*- coding: utf-8 -*-
# Proyecto Final - Principios de Programacion 1
# Empresa: DataByte
# Escuela: San Pascualin
# Descripcion: Calcula estadisticas de edades de una muestra de alumnos

from datetime import datetime


def mostrar_fecha_hora():
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")
    print("=" * 50)
    print("       DATABYTE - Escuela San Pascualin")
    print("=" * 50)
    print("Fecha de ingreso: " + fecha)
    print("Hora de ingreso:  " + hora)
    print("=" * 50)


def validar_contrasena(clave):
    # Verifica que la contrasena sea segura
    if len(clave) < 8:
        return False, "Debe tener al menos 8 caracteres"

    tiene_mayus = False
    tiene_minus = False
    tiene_numero = False
    tiene_simbolo = False
    simbolos = "!@#$%^&*()_-+=[]{};:,.<>?/|"

    for letra in clave:
        if letra.isupper():
            tiene_mayus = True
        elif letra.islower():
            tiene_minus = True
        elif letra.isdigit():
            tiene_numero = True
        elif letra in simbolos:
            tiene_simbolo = True

    if not tiene_mayus:
        return False, "Debe tener al menos una letra mayúscula"
    if not tiene_minus:
        return False, "Debe tener al menos una letra minúscula"
    if not tiene_numero:
        return False, "Debe tener al menos un número"
    if not tiene_simbolo:
        return False, "Debe tener al menos un símbolo especial"

    return True, "Contraseña válida"


def crear_contrasena():
    print("\n--- Registro de contraseña segura ---")
    print("Requisitos:")
    print(" - Mínimo 8 caracteres")
    print(" - Al menos una mayúscula y una minúscula")
    print(" - Al menos un número")
    print(" - Al menos un símbolo especial (!@#$%...)")

    while True:
        clave = input("\nIngrese una contraseña: ")
        valida, mensaje = validar_contrasena(clave)

        if not valida:
            print("Error: " + mensaje)
            continue

        confirmacion = input("Confirme la contraseña: ")
        if clave != confirmacion:
            print("Error: las contraseñas no coinciden")
            continue

        print("Contraseña creada con éxito")
        return clave


def autenticar(clave_real):
    intentos = 3
    while intentos > 0:
        ingreso = input("\nIngrese su contraseña para acceder: ")
        if ingreso == clave_real:
            print("Acceso concedido\n")
            return True
        intentos -= 1
        if intentos > 0:
            print("Contraseña incorrecta. Intentos restantes: " + str(intentos))

    print("Demasiados intentos fallidos. Aplicación bloqueada.")
    return False


def pedir_tamano_muestra():
    while True:
        entrada = input("Ingrese el tamaño de la muestra (n): ")
        if not entrada.isdigit():
            print("Error: debe ingresar un número entero positivo")
            continue
        n = int(entrada)
        if n <= 0:
            print("Error: el tamaño debe ser mayor que cero")
            continue
        return n


def ingresar_alumnos(n):
    alumnos = {}
    i = 1
    while i <= n:
        print("\nAlumno #" + str(i))
        nombre = input("  Nombre: ").strip()

        if nombre == "":
            print("  Error: el nombre no puede estar vacío")
            continue

        if nombre in alumnos:
            print("  Error: ya existe un alumno con ese nombre")
            continue

        edad_texto = input("  Edad: ").strip()
        if not edad_texto.isdigit():
            print("  Error: la edad debe ser un número entero")
            continue

        edad = int(edad_texto)
        if edad < 4 or edad > 18:
            print("  Error: la edad debe estar entre 4 y 18 años (escuela)")
            continue

        alumnos[nombre] = edad
        i += 1

    return alumnos


def obtener_edad_mayor(alumnos):
    mayor = -1
    nombre_mayor = ""
    for nombre in alumnos:
        if alumnos[nombre] > mayor:
            mayor = alumnos[nombre]
            nombre_mayor = nombre
    return nombre_mayor, mayor


def obtener_edad_menor(alumnos):
    menor = 999
    nombre_menor = ""
    for nombre in alumnos:
        if alumnos[nombre] < menor:
            menor = alumnos[nombre]
            nombre_menor = nombre
    return nombre_menor, menor


def calcular_promedio(alumnos):
    suma = 0
    cantidad = 0
    for nombre in alumnos:
        suma += alumnos[nombre]
        cantidad += 1
    promedio = suma / cantidad
    return round(promedio, 1)


def calcular_mediana(alumnos):
    # Extraer edades y ordenarlas
    edades = []
    for nombre in alumnos:
        edades.append(alumnos[nombre])
    edades.sort()

    cantidad = len(edades)
    mitad = cantidad // 2

    if cantidad % 2 == 1:
        # Cantidad impar: valor central
        mediana = edades[mitad]
    else:
        # Cantidad par: promedio de los dos centrales
        mediana = (edades[mitad - 1] + edades[mitad]) / 2

    return mediana


def mostrar_alumnos(alumnos):
    print("\n--- Listado de alumnos ---")
    print("Nombre               | Edad")
    print("-" * 30)
    for nombre in alumnos:
        print(nombre.ljust(20) + " | " + str(alumnos[nombre]))
    print("Total de alumnos: " + str(len(alumnos)))


def mostrar_mayor_menor(alumnos):
    nombre_max, edad_max = obtener_edad_mayor(alumnos)
    nombre_min, edad_min = obtener_edad_menor(alumnos)
    print("\n--- Edad mayor y menor ---")
    print("Edad mayor: " + str(edad_max) + " años (" + nombre_max + ")")
    print("Edad menor: " + str(edad_min) + " años (" + nombre_min + ")")


def mostrar_promedio(alumnos):
    prom = calcular_promedio(alumnos)
    print("\n--- Promedio de edades ---")
    print("Promedio: " + str(prom) + " años")


def mostrar_mediana(alumnos):
    med = calcular_mediana(alumnos)
    print("\n--- Mediana de edades ---")
    print("Mediana: " + str(med) + " años")


def mostrar_todo(alumnos):
    mostrar_alumnos(alumnos)
    mostrar_mayor_menor(alumnos)
    mostrar_promedio(alumnos)
    mostrar_mediana(alumnos)


def mostrar_menu():
    print("\n" + "=" * 50)
    print("          MENÚ DE OPCIONES")
    print("=" * 50)
    print("1. Ver listado de alumnos")
    print("2. Ver edad mayor y menor")
    print("3. Ver promedio de edades")
    print("4. Ver mediana de edades")
    print("5. Ver todas las estadísticas")
    print("6. Salir")
    print("=" * 50)


def leer_opcion():
    while True:
        opcion = input("Seleccione una opción (1-6): ").strip()
        if not opcion.isdigit():
            print("Error: ingrese un número del 1 al 6")
            continue
        numero = int(opcion)
        if numero < 1 or numero > 6:
            print("Error: la opción debe estar entre 1 y 6")
            continue
        return numero


def ejecutar_menu(alumnos):
    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            mostrar_alumnos(alumnos)
        elif opcion == 2:
            mostrar_mayor_menor(alumnos)
        elif opcion == 3:
            mostrar_promedio(alumnos)
        elif opcion == 4:
            mostrar_mediana(alumnos)
        elif opcion == 5:
            mostrar_todo(alumnos)
        elif opcion == 6:
            print("\nGracias por usar el sistema de DataByte. Hasta pronto!")
            break


def main():
    mostrar_fecha_hora()

    clave = crear_contrasena()

    if not autenticar(clave):
        return

    n = pedir_tamano_muestra()
    alumnos = ingresar_alumnos(n)

    print("\nDatos cargados correctamente.")
    ejecutar_menu(alumnos)


main()
