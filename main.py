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

def menu():

    eleccion = -1
    
    while eleccion != 0:
        printMainMenu()
        eleccion = logica.validarInput()

        if eleccion == 0:
            print("Saliendo del programa... 👋")
        
        elif eleccion == 1:
            funcionalidades.crecimientoVentas()
        
        elif eleccion == 2:
            funcionalidades.productosMasVendidos()
        
        elif eleccion == 3:
            funcionalidades.clientesMasRelevantes()
        
        elif eleccion == 4:
            funcionalidades.ticketPromedioDeVenta()
        
        elif eleccion == 5:
            funcionalidades.ventasPorPeriodo()
        
        elif eleccion == 6:
            imprimirMenuDeComparativas()
            tipoDeComparativa = logica.validarInput(0, 3)
            if tipoDeComparativa == 1:
                funcionalidades.comparativaProducto()
            elif tipoDeComparativa == 2:
                funcionalidades.comparativaCliente()
            elif tipoDeComparativa == 3:
                funcionalidades.comparativaRegion()
            elif tipoDeComparativa == 0:
                print("Volviendo al menu principal")
        
        elif eleccion == 7:
            funcionalidades.tendenciaDeCrecimiento()
        
        elif eleccion == 8:
            funcionalidades.tendenciaDeCrecimiento()

        print("\n")

# Entry point #

menu()
