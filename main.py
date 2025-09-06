import os
import sys
import funcionalidades
import logica

# -- Helpers de UI -- #

# Printea un minimenu para elegir tipo de comparativas #
def imprimirMenuDeComparativas():
    print("-" * 30)
    print("Elija un parámetro para hacer la comparativa:")
    print("1) Producto")
    print("2) Cliente")
    print("3) Región")
    print("0) Volver al menú principal")
    print("-" * 30)

# Menu principal #
def printMainMenu():
    print("====================================")
    print("   📊 Plataforma de Análisis de Ventas")
    print("====================================\n")
    print("Seleccione una opción:\n")
    print("1) Crecimiento de ventas")
    print("2) Productos más vendidos (Top-N)")
    print("3) Clientes más relevantes")
    print("4) Ticket promedio de venta")
    print("5) Ventas por periodo")
    print("6) Comparativa producto / cliente / región")
    print("7) Participación de mercado interno")
    print("8) Tendencia de crecimiento acumulado")
    print("------------------------------------")
    print("0) Salir")
    print("------------------------------------")

# Regreso al meno principal
def salidaMenuInicio():
    print("\n")
    print("Ingrese 0 para volver al menu de principal")
    eleccion_2 = int(input())
    while eleccion_2 != 0:
        logica.error()
        print("Ingrese 0 para volver al menu de principal")
        eleccion_2 = int(input())
    
    if eleccion_2 == 0:
        printMainMenu()
        eleccion_3 = logica.validarInput()
        return eleccion_3

# Regreso al meno de comparativas
def salidaMenuComparativas():
    print("\n")
    print("Ingrese 0 para volver al menu de comparataivas")
    eleccion_2 = int(input())
    while eleccion_2 != 0:
        logica.error()
        print("Ingrese 0 para volver al menu de comparataivas")
        eleccion_2 = int(input())
    print("Volviendo al menu principal")
    print("\n")
    if eleccion_2 == 0:
        imprimirMenuDeComparativas()
        eleccion_3 = logica.validarInput()
        return eleccion_3

def menu():

    printMainMenu()
    eleccion = logica.validarInput()
    
    while eleccion != 0:

        if eleccion == 1:
            funcionalidades.crecimientoVentas()
            eleccion = salidaMenuInicio()
        
        elif eleccion == 2:
            funcionalidades.productosMasVendidos()
            eleccion = salidaMenuInicio()
            
        elif eleccion == 3:
            funcionalidades.clientesMasRelevantes()
            eleccion = salidaMenuInicio()
        
        elif eleccion == 4:
            funcionalidades.ticketPromedioDeVenta()
            eleccion = salidaMenuInicio()
        
        elif eleccion == 5:
            funcionalidades.ventasPorPeriodo()
            eleccion = salidaMenuInicio()
        
        elif eleccion == 6:
            imprimirMenuDeComparativas()
            tipoDeComparativa = logica.validarInput(0, 3)
            if tipoDeComparativa == 1:
                funcionalidades.comparativaProducto()
                tipoDeComparativa = salidaMenuComparativas()
            elif tipoDeComparativa == 2:
                funcionalidades.comparativaCliente()
                tipoDeComparativa = salidaMenuComparativas()
            elif tipoDeComparativa == 3:
                funcionalidades.comparativaRegion()
                tipoDeComparativa = salidaMenuComparativas()
            elif tipoDeComparativa == 0:
                eleccion = salidaMenuInicio()

        elif eleccion == 7:
            funcionalidades.tendenciaDeCrecimiento()
            eleccion = salidaMenuInicio()
        
        elif eleccion == 8:
            funcionalidades.tendenciaDeCrecimiento()
            eleccion = salidaMenuInicio()
            
    if eleccion == 0:
        print("Saliendo del programa... 👋")
        print("\n")
        
# Entry point #

menu()


