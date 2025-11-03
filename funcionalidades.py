import logica
import random

def cargarDatosCSV():
    """
    Lee un archivo CSV de ventas.
    Devuelve listas paralelas con cada columna.
    """

    # Vamos a guardar los datos en listas paralelas
    lista_fecha = []
    lista_id_producto = []
    lista_producto = []
    lista_categoria = [] 
    lista_id_cliente = []
    lista_cliente = []
    lista_cantidad = []
    lista_precio = []
    lista_region = []
    lista_canal = []
    lista_factura = []

    try:
        # Abrimos el archivo
        arch = open("ventas_dataset_extendido.csv", mode="r")

        # Variable auxiliar para saber si estamos parados en la primera línea (encabezados)
        primera_linea = True

        # Recorremos el archivo línea por línea
        for linea in arch:
            # Eliminamos salto de línea y espacios
            linea = linea.strip()

            # Si está vacía, la saltamos
            if linea == "":
                continue

            # Saltamos la linea de encabezados si aparece
            if primera_linea:
                primera_linea = False
                continue

            # Dividimos por coma
            partes = linea.split(",")

            # Evitamos filas incompletas (ventas donde falten datos)
            if len(partes) < 11:
                continue

            # Asignamos campos (formato fijo de 11 columnas)
            fecha = partes[0]
            id_prod = partes[1]
            producto = partes[2]
            categoria = partes[3]
            id_cli = partes[4]
            cliente = partes[5]

            try:
                cantidad = int(partes[6])
            except ValueError:
                cantidad = 0

            try:
                precio = float(partes[7])
            except ValueError:
                precio = 0.0

            region = partes[8]
            canal = partes[9]
            IDfactura = partes[10]

            # Guardamos en las listas
            lista_fecha.append(fecha)
            lista_id_producto.append(id_prod)
            lista_producto.append(producto)
            lista_categoria.append(categoria)
            lista_id_cliente.append(id_cli)
            lista_cliente.append(cliente)
            lista_cantidad.append(cantidad)
            lista_precio.append(precio)
            lista_region.append(region)
            lista_canal.append(canal)
            lista_factura.append(IDfactura)

        arch.close()
        
    except FileNotFoundError:
        print("No se encontró el archivo.")
        return None
    except OSError:
        print("No se pudo leer el archivo.")
        return None

    # Devolvemos todas las listas juntas
    return (
        lista_fecha,
        lista_id_producto,
        lista_producto,
        lista_id_cliente,
        lista_cliente,
        lista_cantidad,
        lista_precio,
        lista_region,
        lista_canal,
        lista_factura
    )        

def crecimientoVentas():
    (
        lista_fecha,
        lista_id_producto,
        lista_producto,
        lista_id_cliente,
        lista_cliente,
        lista_cantidad,
        lista_precio,
        lista_region,
        lista_canal,
        lista_factura
        
    )= cargarDatosCSV()
    
    # ---------------------------------------------------------
    # Extraer el año de cada fecha y crear lista_anio
    # ---------------------------------------------------------
    lista_anio = []
    for i in range(len(lista_fecha)):
        fecha = lista_fecha[i]
        if "-" in fecha:
            anio = fecha.split("-")[0]
        lista_anio.append(anio)

    # ---------------------------------------------------------
    # Crear lista de productos únicos
    # ---------------------------------------------------------
    productos_unicos = []
    for i in range(len(lista_producto)):
        producto_actual = lista_producto[i]
        repetido = 0
        for j in range(len(productos_unicos)):
            if productos_unicos[j] == producto_actual:
                repetido = 1
        if repetido == 0:
            productos_unicos.append(producto_actual)

    # ---------------------------------------------------------
    # Crear lista de años únicos
    # ---------------------------------------------------------
    anios_unicos = []
    for i in range(len(lista_anio)):
        anio_actual = lista_anio[i]
        if anio_actual != "0":
            repetido = 0
            for j in range(len(anios_unicos)):
                if anios_unicos[j] == anio_actual:
                    repetido = 1
            if repetido == 0:
                anios_unicos.append(anio_actual)

    # Si hay al menos un año, buscar el mínimo y máximo manualmente
    if len(anios_unicos) > 0:
        antes = int(anios_unicos[0])
        despues = int(anios_unicos[0])
        for i in range(len(anios_unicos)):
            actual = int(anios_unicos[i])
            if actual < antes:
                antes = actual
            if actual > despues:
                despues = actual
    else:
        antes = 0
        despues = 0

    # ---------------------------------------------------------
    # Calcular ventas totales por producto en cada año
    # ---------------------------------------------------------
    # Vamos a tener dos listas paralelas: total_antes y total_despues
    total_antes = []
    total_despues = []

    for i in range(len(productos_unicos)):
        total_antes.append(0)
        total_despues.append(0)

    for i in range(len(lista_producto)):
        prod = lista_producto[i]
        anio = lista_anio[i]
        try:
            venta = float(lista_cantidad[i]) * float(lista_precio[i])
        except:
            venta = 0.0

        for j in range(len(productos_unicos)):
            if prod == productos_unicos[j]:
                if anio == str(antes):
                    total_antes[j] = total_antes[j] + venta
                if anio == str(despues):
                    total_despues[j] = total_despues[j] + venta

    # ---------------------------------------------------------
    # Calcular crecimiento y armar la matriz
    # ---------------------------------------------------------
    matriz = []
    for i in range(len(productos_unicos)):
        resultados = []
        prod = productos_unicos[i]
        v_antes = total_antes[i]
        v_desp = total_despues[i]
        if v_antes != 0:
            crecimiento = ((v_desp - v_antes) / v_antes) * 100
        else:
            crecimiento = 0.0
        resultados = [prod, v_antes, v_desp, crecimiento]
        matriz.append(resultados)
        
    # ---------------------------------------------------------
    # Imprimir la tabla como tu versión original
    # ---------------------------------------------------------
    print(f"Comparacion de ventas de entre los años {antes} y {despues}")
    print("-" * 90)
    print("%-30s%-20s%-20s%-26s" % ('Productos', antes, despues, 'Crecimiento%'))
    print("-" * 90)
    for i in range(len(matriz)):
        print("%-30s%-20.2f%-20.2f%-26.2f" % (matriz[i][0], matriz[i][1], matriz[i][2], matriz[i][3]))

def productosMasVendidos():
   
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # acumulado: [producto, unidades_totales, facturacion_total]
    acumulado = []

    i = 0
    while i < len(lista_producto):
        producto = lista_producto[i]
        # Evitamos filas sin nombre de producto
        if producto is None or producto == "":
            i = i + 1
            continue

        # numéricos seguros
        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        fact = cantidad * precio

        j = logica.indiceEnLista(acumulado, producto)
        if j != -1:
            # ya existe → acumular
            acumulado[j][1] = acumulado[j][1] + cantidad
            acumulado[j][2] = acumulado[j][2] + fact
        else:
            # nuevo producto
            acumulado.append([producto, cantidad, fact])

        i = i + 1

    # Si no hay productos válidos
    if len(acumulado) == 0:
        print("\nNo hay productos válidos para mostrar.")
        return

    # Top por Unidades y por Facturación (de mayor a menor)
    topUnidades = sorted(acumulado, key=lambda fila: fila[1], reverse=True)
    topFacturacion = sorted(acumulado, key=lambda fila: fila[2], reverse=True)

    # Límite (Top 5 o menos si hay menos productos)
    if len(acumulado) > 5:
        limite = 5
    else:
        limite = len(acumulado)

    # Imprimir la tabla (mismo formato que tu versión)
    print("\nTop 5 Productos — Por Unidades / Por Facturación")
    print("-" * 70)
    print(f"{'#':<3} {'Por Unidades':<32} {'Por Facturación':<32}")
    print("-" * 70)

    fila = 0
    while fila < limite:
        nombre_u = topUnidades[fila][0]
        unidades = topUnidades[fila][1]
        nombre_f = topFacturacion[fila][0]
        fact     = topFacturacion[fila][2]
        print(f"{fila+1:<3} {nombre_u:<20} ({int(unidades):>3} u)   {nombre_f:<20} ($ {fact:>7.2f})")
        fila = fila + 1

def clientesMasRelevantes():
  
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # Lista acumuladora: [cliente, total_facturado]
    acumulado = []

    # Recorremos todos los registros del CSV
    i = 0
    while i < len(lista_cliente):
        cliente = lista_cliente[i]
        # Evitamos filas sin cliente
        if cliente is None or cliente == "":
            i = i + 1
            continue

        # cantidad y precio a números seguros
        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = cantidad * precio

        # Buscamos si el cliente ya está en la lista acumulada
        j = logica.indiceEnLista(acumulado, cliente)
        if j != -1:
            # si existe, sumamos al total existente
            acumulado[j][1] = acumulado[j][1] + total
        else:
            # si no existe, lo agregamos
            acumulado.append([cliente, total])

        i = i + 1

    # Ordenamos de mayor a menor por total facturado (como en tu estilo original)
    acumulado.sort(key=lambda fila: fila[1], reverse=True)

    # Mostramos los resultados
    print("\nClientes más relevantes (por facturación):")
    print("-" * 36)
    print(f"{'Cliente':<22} {'Total ($)':>12}")
    print("-" * 36)

    k = 0
    while k < len(acumulado):
        cliente = acumulado[k][0]
        total = acumulado[k][1]
        print(f"{cliente:<22} {total:>12.2f}")
        k = k + 1

def ticketPromedioDeVenta():
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    total_facturacion = 0.0
    cantidad_ventas = 0

    # Recorremos todas las filas del archivo
    i = 0
    while i < len(lista_cantidad):
        try:
            cantidad = float(lista_cantidad[i])
            precio = float(lista_precio[i])
        except:
            cantidad = 0.0
            precio = 0.0

        if cantidad > 0 and precio > 0:
            total_facturacion = total_facturacion + (cantidad * precio)
            cantidad_ventas = cantidad_ventas + 1

        i = i + 1

    print("\n========= TICKET PROMEDIO =========")

    if cantidad_ventas == 0:
        print("⚠️ No hay ventas válidas en el archivo.")
        return

    ticket_promedio = total_facturacion / cantidad_ventas

    print(f"Ventas procesadas: {cantidad_ventas}")
    print(f"Facturación total: ${total_facturacion:,.2f}")
    print(f"Ticket promedio:  ${ticket_promedio:,.2f}")
    print("===================================")
    
def ventasPorPeriodo():
    (
    lista_fecha,
    lista_id_producto,
    lista_producto,
    lista_id_cliente,
    lista_cliente,
    lista_cantidad,
    lista_precio,
    lista_region,
    lista_canal,
    lista_factura
    ) = cargarDatosCSV()
    
    """
    Analizar las ventas en un periodo específico usando listas externas.
    Distribución por mes y por trimestre, con % de crecimiento entre el 1.º
    y 3.º mes del trimestre. Estilo imperativo clásico.
    """

    # ---------------------------------------------------------
    # Extraer años de las fechas y acumular ventas por mes y año
    # ---------------------------------------------------------
    lista_anio = []
    ventas_mes = []
    for i in range(12):
        ventas_mes.append(0.0)

    # Crear listas auxiliares para años únicos y sus totales
    anios_unicos = []
    ventas_anio = []

    for i in range(len(lista_fecha)):
        fecha = lista_fecha[i]
        try:
            cant = float(lista_cantidad[i])
        except:
            cant = 0.0

        # Detectar formato de fecha
        mes_num = 0
        anio = "0"
        if "-" in fecha:
            partes = fecha.split("-")  # formato YYYY-MM-DD
            if len(partes) >= 2:
                anio = partes[0]
                try:
                    mes_num = int(partes[1])
                except:
                    mes_num = 0

        lista_anio.append(anio)

        # Acumular ventas por mes (sin separar por año)
        if mes_num >= 1:
            if mes_num <= 12:
                ventas_mes[mes_num - 1] = ventas_mes[mes_num - 1] + cant

        # Acumular ventas totales por año
        repetido = 0
        for j in range(len(anios_unicos)):
            if anios_unicos[j] == anio:
                repetido = 1
                ventas_anio[j] = ventas_anio[j] + cant
        if repetido == 0 and anio != "0":
            anios_unicos.append(anio)
            ventas_anio.append(cant)

    # ---------------------------------------------------------
    # Buscar año mínimo y máximo (sin sorted)
    # ------------------------------------------------------
    if len(anios_unicos) > 0:
        anio_menor = int(anios_unicos[0])
        anio_mayor = int(anios_unicos[0])
        for i in range(len(anios_unicos)):
            actual = int(anios_unicos[i])
            if actual < anio_menor:
                anio_menor = actual
            if actual > anio_mayor:
                anio_mayor = actual
    else:
        anio_menor = 0
        anio_mayor = 0
    # ---------------------------------------------------------
    # Cuadro comparativo de trimestres por año
    # ---------------------------------------------------------
    print("\n")
    mensaje3 = "Comparativa de Trimestres por Año"
    cadena3 = mensaje3.center(90, ' ')
    print(cadena3)
    print("-" * 90)
    print("%-10s%-14s%-14s%-14s%-14s%-10s" %
          ("Año", "Trim 1", "Trim 2", "Trim 3", "Trim 4", "% Crec. Anual"))
    print("-" * 90)

    # Calcular ventas por trimestre en cada año
    for i in range(len(anios_unicos)):
        anio_actual = anios_unicos[i]
        # inicializar totales trimestrales
        trim1 = 0.0
        trim2 = 0.0
        trim3 = 0.0
        trim4 = 0.0

        # recorrer todos los registros y acumular según el mes
        for j in range(len(lista_fecha)):
            fecha = lista_fecha[j]
            anio_fila = "0"
            mes_num = 0

            if "-" in fecha:               # formato YYYY-MM-DD
                partes = fecha.split("-")
                if len(partes) >= 2:
                    anio_fila = partes[0]
                    try:
                        mes_num = int(partes[1])
                    except:
                        mes_num = 0
            else:
                if "/" in fecha:           # formato DD/MM/YYYY
                    partes = fecha.split("/")
                    if len(partes) >= 3:
                        anio_fila = partes[2]
                        try:
                            mes_num = int(partes[1])
                        except:
                            mes_num = 0

            if anio_fila == anio_actual:
                try:
                    venta = float(lista_cantidad[j]) * float(lista_precio[j])
                except:
                    venta = 0.0

                if mes_num >= 1 and mes_num <= 3:
                    trim1 = trim1 + venta
                else:
                    if mes_num >= 4 and mes_num <= 6:
                        trim2 = trim2 + venta
                    else:
                        if mes_num >= 7 and mes_num <= 9:
                            trim3 = trim3 + venta
                        else:
                            if mes_num >= 10 and mes_num <= 12:
                                trim4 = trim4 + venta

        # calcular crecimiento total del año (Trim4 vs Trim1)
        crec_anual = 0.0
        if trim1 != 0:
            crec_anual = ((trim4 - trim1) / trim1) * 100.0

        print("%-10s%-14.2f%-14.2f%-14.2f%-14.2f%9.2f" %
              (anio_actual, trim1, trim2, trim3, trim4, crec_anual), "%")

def comparativaProducto():
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # acumulado: [producto, unidadesTotales, facturacionTotal]
    acumulado = []

    i = 0
    while i < len(lista_producto):
        prod = lista_producto[i]
        # evitamos filas sin nombre de producto
        if prod is None or prod == "":
            i = i + 1
            continue

        # numéricos seguros
        try:
            unidades = float(lista_cantidad[i])
        except:
            unidades = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = unidades * precio

        idx = logica.indiceEnLista(acumulado, prod)
        if idx != -1:
            # acumular
            acumulado[idx][1] = acumulado[idx][1] + unidades
            acumulado[idx][2] = acumulado[idx][2] + total
        else:
            # nuevo producto
            acumulado.append([prod, unidades, total])

        i = i + 1

    cantidadProductos = len(acumulado)
    if cantidadProductos < 2:
        print("\n⚠️ No hay suficientes productos distintos para comparar.")
        return

    # Mostrar los productos disponibles
    print("\nProductos disponibles:")
    k = 0
    while k < cantidadProductos:
        # mostramos unidades como entero para que quede prolijo
        unidades_mostrar = int(acumulado[k][1]) if acumulado[k][1] == int(acumulado[k][1]) else acumulado[k][1]
        print(f"{k+1}. {acumulado[k][0]}  (u: {unidades_mostrar}, $: {acumulado[k][2]:.2f})")
        k = k + 1

    # Pedimos elecciones del usuario (mismo helper que ya usás)
    opcion1 = logica.validarInput(1, cantidadProductos)
    opcion2 = logica.validarInput(1, cantidadProductos)
    while opcion1 == opcion2:
        print("⚠️ Deben ser distintos.")
        opcion2 = logica.validarInput(1, cantidadProductos)

    producto1 = acumulado[opcion1 - 1]  # [nombre, unidades, facturacion]
    producto2 = acumulado[opcion2 - 1]

    # porcentajes relativos dentro del par
    totalUnidades = producto1[1] + producto2[1]
    totalFacturacion = producto1[2] + producto2[2]

    if totalUnidades > 0:
        porcentajeUnidades1 = (producto1[1] * 100.0) / totalUnidades
        porcentajeUnidades2 = (producto2[1] * 100.0) / totalUnidades
    else:
        porcentajeUnidades1, porcentajeUnidades2 = 0.0, 0.0

    if totalFacturacion > 0:
        porcentajeFacturacion1 = (producto1[2] * 100.0) / totalFacturacion
        porcentajeFacturacion2 = (producto2[2] * 100.0) / totalFacturacion
    else:
        porcentajeFacturacion1, porcentajeFacturacion2 = 0.0, 0.0

    # Mostrar tabla comparativa (mismo formato base que tu versión)
    print("\nComparativa de productos")
    print("-" * 60)
    print(f"{'Producto':<22} {'Unidades':>10} {'Facturación ($)':>18} {'U%':>6} {'F%':>6}")
    print("-" * 60)
    print(f"{producto1[0]:<22} {int(producto1[1]):>10} {producto1[2]:>18.2f} {porcentajeUnidades1:>6.1f} {porcentajeFacturacion1:>6.1f}")
    print(f"{producto2[0]:<22} {int(producto2[1]):>10} {producto2[2]:>18.2f} {porcentajeUnidades2:>6.1f} {porcentajeFacturacion2:>6.1f}")
    print("-" * 60)

    # Conclusión simple
    if producto1[2] > producto2[2]:
        print(f"{producto1[0]} facturó más que {producto2[0]} (+$ {producto1[2] - producto2[2]:.2f}).")
    elif producto2[2] > producto1[2]:
        print(f"{producto2[0]} facturó más que {producto1[0]} (+$ {producto2[2] - producto1[2]:.2f}).")
    else:
        print("Ambos productos tienen la misma facturación.")
        
def comparativaCliente():
   
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # acumulado: [cliente, facturacion_total]
    acumulado = []

    i = 0
    while i < len(lista_cliente):
        cliente = lista_cliente[i]

        # evitar filas sin cliente
        if cliente is None or cliente == "":
            i = i + 1
            continue

        # numéricos seguros
        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = cantidad * precio

        idx = logica.indiceEnLista(acumulado, cliente)
        if idx != -1:
            acumulado[idx][1] = acumulado[idx][1] + total
        else:
            acumulado.append([cliente, total])

        i = i + 1

    cantidadClientes = len(acumulado)
    if cantidadClientes < 2:
        print("\n⚠️ No hay suficientes clientes distintos para comparar.")
        return

    # Mostrar los clientes disponibles
    print("\nClientes disponibles:")
    k = 0
    while k < cantidadClientes:
        print(f"{k+1}. {acumulado[k][0]}")
        k = k + 1

    # Pedimos elegir dos clientes para comparar
    opcion1 = logica.validarInput(1, cantidadClientes)
    opcion2 = logica.validarInput(1, cantidadClientes)

    # Verificamos que no sean iguales
    while opcion1 == opcion2:
        print("⚠️ Deben ser distintos.")
        opcion2 = logica.validarInput(1, cantidadClientes)

    # Selección
    cliente1 = acumulado[opcion1 - 1]   # [nombre, total]
    cliente2 = acumulado[opcion2 - 1]

    # Cálculo de participaciones
    totalPar = cliente1[1] + cliente2[1]
    if totalPar > 0:
        p1 = (cliente1[1] * 100.0) / totalPar
        p2 = (cliente2[1] * 100.0) / totalPar
    else:
        p1 = 0.0
        p2 = 0.0

    diferencia = cliente1[1] - cliente2[1]

    # Salida
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

def tendenciaDeCrecimiento():
    """
    Muestra la participación (%) de cada mes en la facturación total

    Para cada mes:
    - suma (Cantidad * Precio_Unitario)
    - calcula qué % representa sobre el total anual
    """

    # Leemos los datos de ventas
    datos = cargarDatosCSV()
    if datos is None:
        print("No se pudieron cargar los datos de ventas.")
        return

    # Desempaquetamos lo que nos devolvió cargarDatosCSV()
    lista_fecha         = datos[0]
    lista_producto      = datos[2]
    lista_id_cliente    = datos[3]
    lista_cliente       = datos[4]
    lista_cantidad      = datos[5]
    lista_precio        = datos[6]
    lista_region        = datos[7]
    lista_canal         = datos[8]
    lista_factura       = datos[9]

    # Acumulamos facturación por mes
    facturacion_por_mes = {}  # formato { "YYYY-MM": total_facturacion }

    i = 0
    while i < len(lista_fecha):
        fecha_str = lista_fecha[i]            
        cantidad = lista_cantidad[i]         
        precio_unit = lista_precio[i]        
        total_linea = cantidad * precio_unit  

        # transformamos la fecha a formato mes-año
        # por ejemplo: "2024-07-19"[:7] -> "2024-07"
        clave_mes = fecha_str[:7]

        if clave_mes in facturacion_por_mes:
            facturacion_por_mes[clave_mes] += total_linea
        else:
            facturacion_por_mes[clave_mes] = total_linea

        i += 1

    # Ordenamos los meses cronológicamente, "keys()" se refiere a las claves del objeto, osea en este caso los meses.
    meses_ordenados = sorted(facturacion_por_mes.keys())

    # Calculamos el total general (suma de todos los meses)
    total_anual = 0.0
    j = 0
    while j < len(meses_ordenados):
        mes_clave = meses_ordenados[j]
        total_anual += facturacion_por_mes[mes_clave]
        j += 1

    if total_anual == 0:
        print("⚠️ No hay facturación en los datos.")
        return

    # Imprimimos la tabla final
    print("\nPorcentaje de ventas por mes (respecto al total):")
    print("-" * 70)
    print(f"{'Mes':<20}{'Facturación ($)':<20}{'Participación':<15}")
    print("-" * 70)

    k = 0
    while k < len(meses_ordenados):
        mes_clave = meses_ordenados[k]                
        fact_mes = facturacion_por_mes[mes_clave]     
        porcentaje = (fact_mes / total_anual) * 100.0 
        etiqueta = logica.formatear_mes(mes_clave)          

        print(f"{etiqueta:<20}{fact_mes:<20.2f}{porcentaje:>10.1f}%")
        k += 1

    print("-" * 70)
    print(f"{'TOTAL':<20}{total_anual:<20.2f}{'100.0%':>10}")
    print()

def comparativaCanal():
    """
    Compara las ventas totales entre los distintos canales (Online, Tienda, Mayorista).
    Calcula facturación y participación porcentual.
    """
    # Cargar los datos
    datos = cargarDatosCSV()
    if datos is None:
        print("No se pudieron cargar los datos de ventas.")
        return

    lista_cantidad = datos[5]
    lista_precio = datos[6]
    lista_canal = datos[8]

    # Acumular facturación total por canal
    facturacion_por_canal = {}  # formato: { 'Online': 12345.0, 'Tienda': 9876.0, ... }

    i = 0
    while i < len(lista_canal):
        canal = lista_canal[i]
        total = lista_cantidad[i] * lista_precio[i]

        if canal in facturacion_por_canal:
            facturacion_por_canal[canal] += total
        else:
            facturacion_por_canal[canal] = total
        i += 1

    # Calcular total general y prevenir caso donde no hay ventas
    total_general = sum(facturacion_por_canal.values())
    if total_general == 0:
        print("⚠️ No se registraron ventas.")
        return

    # Ordenar canales por facturación descendente
    canales_ordenados = sorted(facturacion_por_canal.items(), key=lambda x: x[1], reverse=True)

    # Mostrar resultados
    print("\nComparativa de ventas por canal:")
    print("-" * 60)
    print(f"{'Canal':<15}{'Facturación ($)':>20}{'Participación':>20}")
    print("-" * 60)

    for canal, total in canales_ordenados:
        participacion = (total / total_general) * 100
        print(f"{canal:<15}{total:>20.2f}{participacion:>19.1f}%")

    print("-" * 60)
    print(f"{'TOTAL':<15}{total_general:>20.2f}{'100.0%':>19}")
    print("-" * 60)

    # Destacar el canal más fuerte
    canal_top = canales_ordenados[0][0]
    print(f"\n El canal con mayor facturación es: {canal_top}\n")
