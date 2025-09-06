# funcionalidades.py

import logica
import random

def crecimientoVentas():
    """
    Calcular el crecimiento de ventas en un periodo de tiempo.
    Ejemplo: comparar las ventas de este año contra las del año pasado
    y devolver el porcentaje de aumento o disminución.
    """
    maximo = 500
    minimo = 50
    matriz = []
    productos = ["Zapatillas", "Remera", "Short", "Campera"]
    num = random.randint(1, 25)
    antes = 2000 + num -1
    despues = 2000 + num
    for i in range(len(productos)):
        resultados = []
        ventas_antes = random.randint(minimo, maximo)
        ventas_despues = random.randint(minimo, maximo)
        crecimiento = ((ventas_despues - ventas_antes) / ventas_antes) * 100
        resultados =  [productos[i]] +[ventas_antes] + [ventas_despues] + [crecimiento]
        matriz.append(resultados)
    print(f"Comparacion de ventas de entre los años {antes} y {despues}")
    print("-"*50)
    print("%-14s%-10s%-10s%-16s" %('Productos',antes,despues,'Crecimiento%'))
    print("-"*50)
    for i in range(len(productos)):
        print("%-14s%-10d%-10d%-16.2f" %(matriz[i][0],matriz[i][1],matriz[i][2],matriz[i][3]))

def productosMasVendidos():
    """
    Listar los productos más vendidos.
    Puede mostrar un Top-N (ej: Top 5) ordenado por unidades vendidas
    o por facturación total.
    """
    print(">> Listado de productos más vendidos (en construcción)")

def clientesMasRelevantes():
    """
    Identificar los clientes que generan más ventas.
    Ejemplo: mostrar el Top-N de clientes por ingresos.
    """
    
    # Ejemplo de datos: [cliente, cantidad, precio_unitario]
    ventas = [
        ["Deportes SA",        10, 120.5],
        ["Indumentaria Norte", 25, 45.0],
        ["Outlet Sur",          5, 120.5],
        ["Deportes SA",        12, 60.0],
        ["Tiendas Centro",      3, 210.0],
        ["MegaSports",         30, 45.0]
    ]
    
    # Lista acumuladora: [cliente, total]
    acumulados = []
    
    # Recorremos lista de datos #
    for v in ventas:
        cliente = v[0]
        cantidad = v[1]
        precio = v[2]
        total = cantidad * precio

        i = logica.indiceEnLista(acumulados, cliente)

        if i != -1:
            # si existe sumamos al total existente
            acumulados[i][1] = acumulados[i][1] + total
        else:
            # si no existe lo agregamos
            acumulados.append([cliente, total])
            
    # Ordenamos de mayor a menor por el total
    # key → indica qué usar como criterio de ordenación #
    # reverse = True para ordenar de mayor a menor #
    acumulados.sort(key=lambda fila: fila[1], reverse=True)

    # Mostramos los resultados
    print("\nClientes más relevantes (por facturación):")
    print("-" * 36)
    print(f"{'Cliente':<22} {'Total ($)':>12}")
    print("-" * 36)
    for cliente, total in acumulados:
        print(f"{cliente:<22} {total:>12.2f}")

def ticketPromedioDeVenta():
    """
    Calcular el ticket promedio.
    Es decir, el promedio de dinero que se genera por cada venta realizada.
    """
    print(">> Ticket promedio de venta (en construcción)")


def ventasPorPeriodo():
    """
    Analizar las ventas en un periodo específico.
    Ejemplo: ver cómo se distribuyen las ventas por mes o por trimestre.
    """
    print(">> Ventas por periodo (en construcción)")


def comparativaProducto():
    """
    Comparar las ventas entre dos productos distintos.
    Ejemplo: Producto A vs Producto B en cantidad de ventas y facturación.
    """
    print(">> Comparativa de productos (en construcción)")


def comparativaCliente():
    """
    Comparar las ventas entre dos clientes distintos.
    Ejemplo: Cliente X vs Cliente Y en total de compras realizadas.
    """
    print(">> Comparativa de clientes (en construcción)")


def comparativaRegion():
    """
    Comparar las ventas entre dos regiones distintas.
    Ejemplo: Buenos Aires vs Córdoba.
    """
    print(">> Comparativa de regiones (en construcción)")


def tendenciaDeCrecimiento():
    """
    Mostrar la tendencia de crecimiento acumulado de las ventas.
    Ejemplo: ir sumando mes a mes y graficar o listar la evolución.
    """
    print(">> Tendencia de crecimiento acumulado (en construcción)")
