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
    print("-"*60)
    print("%-15s%-13s%-13s%-19s" %('Productos',antes,despues,'Crecimiento%'))
    print("-"*60)
    for i in range(len(productos)):
        print("%-15s%-13d%-13d%-19.2f" %(matriz[i][0],matriz[i][1],matriz[i][2],matriz[i][3]))

def productosMasVendidos():
    """
    Listar los productos más vendidos.
    Puede mostrar un Top-5 ordenado por unidades vendidas
    o por facturación total.
    """
    # Datos de ejemplo [producto, cantidad, precio unitario]
    ventas = [
        ["Zapatillas Running", 10, 120.5],
        ["Remera Deportiva",   25,  45.0],
        ["Zapatillas Running",  5, 120.5],
        ["Short Entrenamiento",12,  60.0],
        ["Campera Rompeviento", 3, 210.0],
        ["Remera Deportiva",   30,  45.0],
    ]
    
    # lista acumuladora [producto, unidades_totales, facturacion_total]
    acumulado = []
    
    # Armamos la lista que acumula todas las ventas por producto
    
    i = 0
    while i < len(ventas):
        prod = ventas[i][0]
        cant = ventas[i][1]
        precio = ventas[i][2]
        fact = cant * precio
        
        j = logica.indiceEnLista(acumulado, prod)
        if j != -1:
            # El producto ya existe en la lista asi que lo acumulamos
            acumulado[j][1] = acumulado[j][1] + cant
            acumulado[j][2] = acumulado[j][2] + fact
        else:
            # Si no existe el producto lo agregamos a la lista acumulada
            acumulado.append([prod, cant, fact])
        i = i + 1
                          
    # Construimos listas ordenadas para cada categoria (por unidad y por facturación)
    
    # ordena la lista acumulada de mayor a menor según el valor de la columna de unidades vendidas
    topUnidades = sorted(acumulado, key=lambda fila: fila[1], reverse=True)
    # ordena la lista acumulada de mayor a menor según el valor de la columna de facturación total
    topFacturacion = sorted(acumulado, key=lambda fila: fila[2], reverse=True)
    
    # Imprimir la tabla
    
    print("\nTop 5 Productos — Por Unidades / Por Facturación")
    print("-" * 70)
    print(f"{'#':<3} {'Por Unidades':<32} {'Por Facturación':<32}")
    print("-" * 70)
    
    if len(acumulado) > 5:
        limite = 5
    else:
        limite = len(acumulado)
        
    fila = 0
    while fila < limite:
        nombre_u = topUnidades[fila][0]
        unidades = topUnidades[fila][1]
        nombre_f = topFacturacion[fila][0]
        fact     = topFacturacion[fila][2]
        print(f"{fila+1:<3} {nombre_u:<20} ({unidades:>3} u)   {nombre_f:<20} ($ {fact:>7.2f})")
        fila = fila + 1

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
    Calcula el ticket promedio de un conjunto de ventas simuladas.
    Cada venta = [cantidad, precio_unitario].
    """
    # Creamos una lista de ventas aleatorias (matriz)
    ventas = []
    for i in range(random.randint(5, 12)):   # entre 5 y 12 ventas
        cantidad = random.randint(1, 30)
        precio_unitario = round(random.uniform(20, 300), 2)
        ventas.append([cantidad, precio_unitario])
 
    # Mostramos las ventas generadas
    cadena = 'VENTAS GENERADAS'
    cadena2 = cadena.center(30,'=')
    print("\n")
    print(cadena2)
    for i, fila in enumerate(ventas, start=1):
        print(f"Venta {i}: {fila[0]} unidades x ${fila[1]}")
 
    # Calculamos el ticket promedio
    total = 0.0
    cantVentas = 0
    for fila in ventas:
        if len(fila) != 2:
            continue
        cantidad, precio = fila
        total += cantidad * precio
        cantVentas += 1
 
    if cantVentas == 0:
        print("⚠️ No hay ventas válidas.")
        return
 
    ticket = total / cantVentas
    cadena3 = 'TICKET PROMEDIO'
    cadena4 = cadena3.center(30,'=')
    print("\n")
    print(cadena4)
    print(f"Ventas procesadas: {cantVentas}")
    print(f"Facturación total: ${total:,.2f}")
    print(f"Ticket promedio:  ${ticket:,.2f}")

def ventasPorPeriodo():
    def ventasPorPeriodo():
    """
    Analizar las ventas en un periodo específico.
    Ejemplo: ver cómo se distribuyen las ventas por mes o por trimestre.
    """
    suma_mes = 0
    lista = []
    productos = ["Zapatillas", "Remera", "Short", "Campera"]
    num = random.randint(1, 25)
    mes=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]    
    mensaje = 'Analisis de Ventas por Periodos'
    cadena = mensaje.center(61,' ')
    print(cadena)
    print("-" * 61)
    print("%-16s%-16s%-16s%10s" %('Mes','Cant. x Mes','Cant. x Trimestre','% Crec.'))
    print("-" * 61)
    for i in range(len(mes)):
        print("%-16s" % mes[i], end="")
        cant_ventas = random.randint(10000,50000)
        lista.append(cant_ventas)
        suma_mes = cant_ventas + suma_mes
        if (i+1) % 3 == 0:
            cont = 0
            print("%-16d" % cant_ventas, end="")
            print("%-16d" % suma_mes, end="")
            prom = ((lista[cont+2]-lista[cont])/lista[cont])*100
            print("%10.3f" % prom,"%")
            suma_mes = 0
            lista.clear()
        else:
            print("%-12d" % cant_ventas) 
    print("\n")

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
    


