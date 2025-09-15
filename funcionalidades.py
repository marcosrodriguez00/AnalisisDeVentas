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
    acumulado = []
    
    # Recorremos lista de datos #
    for v in ventas:
        cliente = v[0]
        cantidad = v[1]
        precio = v[2]
        total = cantidad * precio

        i = logica.indiceEnLista(acumulado, cliente)

        if i != -1:
            # si existe sumamos al total existente
            acumulado[i][1] = acumulado[i][1] + total
        else:
            # si no existe lo agregamos
            acumulado.append([cliente, total])
            
    # Ordenamos de mayor a menor por el total
    # key → indica qué usar como criterio de ordenación #
    # reverse = True para ordenar de mayor a menor #
    acumulado.sort(key=lambda fila: fila[1], reverse=True)

    # Mostramos los resultados
    print("\nClientes más relevantes (por facturación):")
    print("-" * 36)
    print(f"{'Cliente':<22} {'Total ($)':>12}")
    print("-" * 36)
    for cliente, total in acumulado:
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
    cadena = ' VENTAS GENERADAS '
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
    cadena3 = ' TICKET PROMEDIO '
    cadena4 = cadena3.center(30,'=')
    print("\n")
    print(cadena4)
    print(f"Ventas procesadas: {cantVentas}")
    print(f"Facturación total: ${total:,.2f}")
    print(f"Ticket promedio:  ${ticket:,.2f}")
    
    
def ventasPorPeriodo():
    """
    Analizar las ventas en un periodo específico.
    Ejemplo: ver cómo se distribuyen las ventas por mes o por trimestre.
    """
    suma_mes = 0
    lista = []
    mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]    
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
    # Ejemplo de datos: [Producto, cantidad, precio_unitario]
    ventas = [
        ["Zapatillas Running", 10, 120.5],
        ["Remera Deportiva",   25,  45.0],
        ["Zapatillas Running",  5, 120.5],
        ["Short Entrenamiento",12,  60.0],
        ["Campera Rompeviento", 3, 210.0],
        ["Remera Deportiva",   30,  45.0],
    ]

    # Lista acumuladora [Producto, unidadesTotales, facturacionTotal]
    acumulado = []
    
    i = 0
    while i < len(ventas):
        producto = ventas[i][0]
        unidades = ventas[i][1]
        precio = ventas[i][2]
        total = unidades * precio
        
        indice = logica.indiceEnLista(acumulado, producto)
        if indice != -1: # El cliente ya está en la lista acumulada
            acumulado[indice][1] = acumulado[indice][1] + unidades # Acumulamos cantidad de unidades
            acumulado[indice][2] = acumulado[indice][2] + total # Acumulamos facturación total
        else: # Si el cliente no está en la lista
            acumulado.append([producto, unidades, total])
        i += 1
    
    cantidadProductos = len(acumulado)
    
    # Mostrar los productos disponibles
    print("\nProductos disponibles:")
    k = 0
    while k < cantidadProductos:
        print(f"{k+1}. {acumulado[k][0]}")
        k = k + 1

    # Pedimos elecciones del usuario
    opcion1 = logica.validarInput(1, cantidadProductos)
    opcion2 = logica.validarInput(1, cantidadProductos)
    while opcion1 == opcion2:
        print("⚠️ Deben ser distintos.")
        opcion2 = logica.validarInput(1, cantidadProductos)
        
    producto1 = acumulado[opcion1 - 1]
    producto2 = acumulado[opcion2 - 1]
    
    # calculamos porcentajes relativos
    totalUnidades = producto1[1] + producto2[1]
    totalFacturacion = producto1[2] + producto2[2]
    
    if totalUnidades > 0: # Comprobamos que haya unidades vendidas
        porcentajeUnidades1 = (producto1[1] * 100.0) / totalUnidades # Ventas relativas en unidades de producto 1
        porcentajeUnidades2 = (producto2[1] * 100.0) / totalUnidades # y 2
    else:
        porcentajeUnidades1, porcentajeUnidades2 = 0.0, 0.0
        
    if totalFacturacion > 0: # Comprobamos que haya facturación
        porcentajeFacturacion1 = (producto1[2] * 100.0) / totalFacturacion # Ventas relativas en facturación de producto 1
        porcentajeFacturacion2 = (producto2[2] * 100.0) / totalFacturacion # y 2
    else:
        porcentajeFacturacion1, porcentajeFacturacion2 = 0.0, 0.0
        
    # Mostrar tabla comparativa
    print("\nComparativa de productos")
    print("-" * 60)
    print(f"{'Producto':<22} {'Unidades':>10} {'Facturación ($)':>18} {'U%':>6} {'F%':>6}")
    print("-" * 60)
    print(f"{producto1[0]:<22} {producto1[1]:>10} {producto1[2]:>18.2f} {porcentajeUnidades1:>6.1f} {porcentajeFacturacion1:>6.1f}")
    print(f"{producto2[0]:<22} {producto2[1]:>10} {producto2[2]:>18.2f} {porcentajeUnidades2:>6.1f} {porcentajeFacturacion2:>6.1f}")
    print("-" * 60)
    
    if producto1[2] > producto2[2]:
        print(f"{producto1[0]} facturó más que {producto2[0]} (+$ {producto1[2] - producto2[2]:.2f}).")
    elif producto2[2] > producto1[2]:
        print(f"{producto2[0]} facturó más que {producto1[0]} (+$ {producto2[2] - producto1[2]:.2f}).")
    else:
        print("Ambos productos tienen la misma facturación.")
        
def comparativaCliente():
    """
    Comparar las ventas entre dos clientes distintos.
    Ejemplo: Cliente X vs Cliente Y en total de compras realizadas.
    """
    # Ejemplo de datos: [cliente, cantidad, precio_unitario]
    ventas = [
        ["Deportes SA",        10, 120.5],
        ["Indumentaria Norte", 25,  45.0],
        ["Outlet Sur",          5, 120.5],
        ["Deportes SA",        12,  60.0],
        ["Tiendas Centro",      3, 210.0],
        ["MegaSports",         30,  45.0],
    ]

    # Lista acumuladora [cliente, facturación_total]
    acumulado = []
    
    i = 0
    while i < len(ventas):
        cliente = ventas[i][0]
        cantidad = ventas[i][1]
        precio = ventas[i][2]
        total = cantidad * precio
        
        indice = logica.indiceEnLista(acumulado, cliente)
        if indice != -1: # Si está en la lista
            acumulado[indice][1] = acumulado[indice][1] + total # Entonces sumamos al contado de ese cliente
        else: # Si no está agregamos el cliente a la lista acumulada
            acumulado.append([cliente, total])
        
        i += 1
    
    cantidadClientes = len(acumulado) # Variable con la cantidad de clientes en la lista
    
    # Ahora que tenemos la lista completa, mostramos los clientes
    print("\nClientes disponibles:")
    k = 0
    while k < cantidadClientes:
        print(f"{k+1}. {acumulado[k][0]}")
        k = k + 1

    # Pedimos elegir dos clientes para comparar
    opcion1 = logica.validarInput(1, cantidadClientes)
    opcion2 = logica.validarInput(1, cantidadClientes)
    
    # Verificamos las elecciones
    while opcion1 == opcion2:
        print("⚠️ Deben ser distintos.")
        opcion2 = logica.validarInput(1, cantidadClientes)
    
    # Separamos los clientes elegidos
    cliente1 = acumulado[opcion1 - 1]
    cliente2 = acumulado[opcion2 - 1]
    
    # Calculamos la comparación
    totalPar = cliente1[1] + cliente2[1] # Calcula el total de facturación ambos clientes
    if totalPar > 0: # Calcula el porcentaje relativo de cada cliente
        p1 = (cliente1[1] * 100.0) / totalPar 
        p2 = (cliente2[1] * 100.0) / totalPar
    else: # Caso en que ambos clientes hayan vendido 0
        p1 = 0.0
        p2 = 0.0
    
    diferencia = cliente1[1] - cliente2[1]
    
    # Imprimimos la tabla de salida
    print("\nComparativa de clientes (por facturación total)")
    print("-" * 52)
    print(f"{'Cliente':<24} {'Total ($)':>12} {'Participación':>14}")
    print("-" * 52)
    print(f"{cliente1[0]:<24} {cliente1[1]:>12.2f} {p1:>12.1f}%")
    print(f"{cliente2[0]:<24} {cliente2[1]:>12.2f} {p2:>12.1f}%")
    print("-" * 52)
    if diferencia > 0:
        print(f"{cliente1[0]} supera a {cliente2[0]} por $ {diferencia:.2f}.")
    elif diferencia < 0:
        print(f"{cliente2[0]} supera a {cliente1[0]} por $ {abs(diferencia):.2f}.")
    else:
        print("Ambos tienen la misma facturación.")
        
        
def comparativaRegion():
    """
    Comparar las ventas entre dos regiones distintas.
    Ejemplo: Buenos Aires vs Córdoba.
    """
    productos = ["Zapatillas", "Remera", "Short", "Campera"]
    regiones = ["Buenos Aires", "Cordoba"]

    matriz = []  # [producto, ventas_BA, ventas_CBA]

    # Generar ventas aleatorias para cada producto y región
    for prod in productos:
        ventas_ba = random.randint(100, 500)
        ventas_cba = random.randint(100, 500)
        matriz.append([prod, ventas_ba, ventas_cba])

    # Mostrar resultados
    print("\nComparativa de ventas entre regiones:")
    print("-" * 45)
    print(f"{'Producto':<15}{regiones[0]:<12}{regiones[1]:<12}{'Mayor'}")
    print("-" * 45)

    total_ba = 0
    total_cba = 0

    for fila in matriz:
        prod = fila[0]
        ba = fila[1]
        cba = fila[2]

        # Sumar totales por región
        total_ba += ba
        total_cba += cba

        # Ver cuál región vendió más para este producto
        if ba > cba:
            mayor = regiones[0]
        elif cba > ba:
            mayor = regiones[1]
        else:
            mayor = "Empate"

        print(f"{prod:<15}{ba:<12}{cba:<12}{mayor}")

    print("-" * 45)
    print(f"{'TOTAL':<15}{total_ba:<12}{total_cba:<12}", end="")

    if total_ba > total_cba:
        print(f"Gana {regiones[0]}")
    elif total_cba > total_ba:
        print(f"Gana {regiones[1]}")
    else:
        print("Empate")

def tendenciaDeCrecimiento():
     """
    Mostrar la tendencia de crecimiento de las ventas mes a mes en porcentaje
    respecto al total anual (sin acumulado).
    """

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    ventas_mensuales = []

    # Generar ventas aleatorias entre 100 y 500
    for mes in meses:
        ventas = random.randint(100, 500)
        ventas_mensuales.append([mes, ventas])

    # Calcular total anual
    total = sum(v[1] for v in ventas_mensuales)

    # Mostrar resultados en tabla
    print("\nPorcentaje de ventas por mes (respecto al total anual):")
    print("-" * 50)
    print(f"{'Mes':<12}{'Ventas':<12}{'Porcentaje'}")
    print("-" * 50)

    for mes, ventas in ventas_mensuales:
        porcentaje = (ventas / total) * 100

