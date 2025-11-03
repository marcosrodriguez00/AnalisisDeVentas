import os
import sys

# -- Helpers main.py -- #

# printea un error en consola #
def error():
    print("ERROR: La opcion no es valida.")
    
# pide un input y verifica que sea valido para el menu principal #
def validarInput(min=0, max=8):
    opcion = -1

    while opcion < min or opcion > max:
        if (min == 0 and max == 0):
            opcion = int(input())
        else: 
            try:
                opcion = int(input(f"Elija una opción ({min}-{max}): "))
                if opcion < min or opcion > max:
                    print(f"⚠️ La opción debe estar entre {min} y {max}.")
            except ValueError:
                print("⚠️ Debe ingresar un número entero.")
                opcion = -1  # fuerza a repetir el ciclo

    return opcion

# -- Helpers funcionalidades.py -- #

# Devuelve el indice del cliente en la lista de acumulados #
def indiceEnLista(acumulados, cliente):
    # Crear una lista con solo los nombres de cliente
    nombres = [fila[0] for fila in acumulados]

    # Revisar si el cliente está en esa lista
    if cliente in nombres:
        return nombres.index(cliente)  # devuelve la posición
    else:
        return -1  # no está

# Función que formatea el més de formato "YYYY-MM" a "NombreMes YYYY"
#    "2024-07" -> "Julio 2024"
def formatear_mes(clave_ym):
    anio = clave_ym[0:4]   # "2024"
    mes_num = clave_ym[5:7] # "07"
    nombres_mes = {
        "01": "Enero",
        "02": "Febrero",
        "03": "Marzo",
        "04": "Abril",
        "05": "Mayo",
        "06": "Junio",
        "07": "Julio",
        "08": "Agosto",
        "09": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre"
    }
    nombre = nombres_mes.get(mes_num, mes_num)
    return f"{nombre} {anio}"