import os
import sys

# Helpers de UI #

# Menu principal #

def print_main_menu():
    print("====================================")
    print("   📊 Plataforma de Análisis de Ventas")
    print("====================================\n")
    print("Seleccione una opción:\n")
    print("1) Crecimiento de ventas")
    print("2) Productos más vendidos (Top-N)")
    print("3) Clientes más relevantes")
    print("4) Ticket promedio de venta")
    print("5) Estacionalidad / Ventas por periodo")
    print("6) Comparativa producto / cliente / región")
    print("7) Participación de mercado interno")
    print("8) Tendencia de crecimiento acumulado")
    print("------------------------------------")
    print("0) Salir")
    print("------------------------------------")

def menu():
    print_main_menu()
    opcion = input("Eliga una opción: ")

    print("Has elegido la opción: " + opcion)
# Entry point #

menu()