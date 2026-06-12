import os
import sys
import funcionalidades
import logica
#ddddd12133
# -- Helpers de UI -- #

# Printea un minimenu para elegir tipo de comparativas #
def imprimirMenuDeComparativas():
    print("-" * 30)
    print("Elija un parámetro para hacer la comparativa:")
    print("1) Producto")
    print("2) Cliente")
    print("0) Volver al menú principal")
    print("-" * 30)

# Printea un minimenu para elegir categorias #
def imprimirMenuDeCategorias():

    categorias = logica.obtenerCategoriasUnicas()

    if len(categorias) == 0:
        print("No se encontraron categorías en el archivo.")
        return "TODAS"

    print("-" * 30)
    print("Elija una categoría:")
    print("0 - TODAS")

    # Recorremos manualmente la lista
    indice = 1
    for cat in categorias:
        print(str(indice) + " - " + cat)
        indice = indice + 1

    print("-" * 30)

    # Leer selección
    while True:
        print("Ingrese el número de la categoría: ")
        opcion = logica.validarInput(0, len(categorias))

        if opcion == 0:
            return "TODAS"
        elif opcion > 0 and opcion <= len(categorias):
            return categorias[opcion - 1]
    
# Regreso al menu principal
def salidaMenuInicio():
    while True:
        print("\n")
        print("Ingrese 0 para volver al menu principal")

        try:
            eleccion2 = int(input("> "))
            if eleccion2 == 0:
                break  # salgo del while y voy al menú principal
            else:
                # cualquier cosa distinta de 0: muestro error y vuelvo a pedir
                logica.error()
        except ValueError:
            # si escribe letras, vacío, etc.
            logica.error()

    # acá ya sabemos que eligió 0
    printMainMenu()
    eleccion3 = logica.validarInput(0, 8)
    return eleccion3
    
# Menu principal #

def printMainMenu():
    print("=" * 60)
    cadena1 = '📊 Plataforma de Análisis de Ventas'
    cadena2 = cadena1.center(60,' ')
    print(cadena2)
    print("=" * 60)
    print("\n")
    print("Seleccione una opción:\n")
    print("1) Crecimiento de ventas")
    print("2) Productos más vendidos (Top-5)")
    print("3) Clientes más relevantes")
    print("4) Ticket promedio de venta")
    print("5) Ventas por periodo")
    print("6) Comparativa producto / cliente ")
    print("7) Tendencia de crecimiento acumulado")
    print("8) Comparativa por canal de venta")
    print("-" * 60)
    print("0) Salir")
    print("-" * 60)

def menu():

    printMainMenu()
    eleccion = logica.validarInput(0, 8)
    
    while eleccion != 0:

        if eleccion == 1:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.crecimientoVentas(categoria)
                eleccion = salidaMenuInicio()
        
        if eleccion == 2:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.productosMasVendidos(categoria)
                eleccion = salidaMenuInicio()
            
        if eleccion == 3:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.clientesMasRelevantes(categoria)
                eleccion = salidaMenuInicio()
        
        if eleccion == 4:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.ticketPromedioDeVenta(categoria)
                eleccion = salidaMenuInicio()
        
        if eleccion == 5:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.ventasPorPeriodo(categoria)
                eleccion = salidaMenuInicio()
            
        while eleccion == 6:
            imprimirMenuDeComparativas()
            tipoDeComparativa = logica.validarInput(0, 2)
            if tipoDeComparativa == 1:
                funcionalidades.comparativaProducto()
                eleccion = salidaMenuInicio()
                
            elif tipoDeComparativa == 2:
                funcionalidades.comparativaCliente()
                eleccion = salidaMenuInicio()
                
            elif tipoDeComparativa == 0:
                printMainMenu()
                eleccion = logica.validarInput(0, 9)
                
        if eleccion == 7:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.tendenciaDeCrecimiento(categoria)
                eleccion = salidaMenuInicio()
        
        if eleccion == 8:
            categoria = imprimirMenuDeCategorias()
            if categoria:
                funcionalidades.comparativaCanal(categoria)
                eleccion = salidaMenuInicio()    
            
    if eleccion == 0:
        print("Saliendo del programa... 👋")
        print("\n")

# Entry point #

menu()