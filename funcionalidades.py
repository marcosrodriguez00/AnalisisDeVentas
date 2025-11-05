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
        arch = open("ventas_dataset_sin_tildes.csv", mode="r")

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
        lista_categoria,
        lista_id_cliente,
        lista_cliente,
        lista_cantidad,
        lista_precio,
        lista_region,
        lista_canal,
        lista_factura
    )        

def crecimientoVentas(eleccion):
    if eleccion == "TODAS":
        (
            lista_fecha,
            lista_id_producto,
            lista_producto,
            lista_categoria,
            lista_id_cliente,
            lista_cliente,
            lista_cantidad,
            lista_precio,
            lista_region,
            lista_canal,
            lista_factura
        ) = cargarDatosCSV()

        # Extraer el año de cada fecha y crear lista_anio

        lista_anio = []
        for i in range(len(lista_fecha)):
            fecha = lista_fecha[i]
            if "-" in fecha:
                anio = fecha.split("-")[0]
            lista_anio.append(anio)

        # Crear lista de productos únicos

        productos_unicos = []
        for i in range(len(lista_categoria)):
            producto_actual = lista_categoria[i]
            repetido = 0
            for j in range(len(productos_unicos)):
                if productos_unicos[j] == producto_actual:
                    repetido = 1
            if repetido == 0:
                productos_unicos.append(producto_actual)

        # Crear lista de años únicos

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

        # Calcular ventas totales por producto en cada año
        # Vamos a tener dos listas paralelas: total_antes y total_despues
        total_antes = []
        total_despues = []

        for i in range(len(productos_unicos)):
            total_antes.append(0)
            total_despues.append(0)

        for i in range(len(lista_producto)):
            prod = lista_categoria[i]
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

        # Calcular crecimiento y armar la matriz
        
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
    else:
        (
        lista_fecha,
        lista_producto,
        lista_cliente,
        lista_cantidad,
        lista_precio,
        lista_region,
        lista_canal,
        lista_factura,
        ) = logica.informeCategorias(eleccion)
        
        # Extraer el año de cada fecha y crear lista_anio

        lista_anio = []
        for i in range(len(lista_fecha)):
            fecha = lista_fecha[i]
            if "-" in fecha:
                anio = fecha.split("-")[0]
            lista_anio.append(anio)

        # Crear lista de productos únicos

        productos_unicos = []
        for i in range(len(lista_producto)):
            producto_actual = lista_producto[i]
            repetido = 0
            for j in range(len(productos_unicos)):
                if productos_unicos[j] == producto_actual:
                    repetido = 1
            if repetido == 0:
                productos_unicos.append(producto_actual)

        # Crear lista de años únicos

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

        # Calcular ventas totales por producto en cada año    
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

        # Calcular crecimiento y armar la matriz

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

        # ORDENAR MATRIZ ALFABÉTICAMENTE POR NOMBRE DE PRODUCTO

        for i in range(len(matriz) - 1):
            for j in range(i + 1, len(matriz)):
                if matriz[i][0] > matriz[j][0]:
                    # intercambiar filas
                    aux = matriz[i]
                    matriz[i] = matriz[j]
                    matriz[j] = aux

    # Imprimir la tabla como tu versión original

    print(f"Comparacion de ventas de entre los años {antes} y {despues}")
    print("-" * 90)
    print("%-30s%-20s%-20s%-26s" % ('Productos', antes, despues, 'Crecimiento%'))
    print("-" * 90)
    for i in range(len(matriz)):
        print("%-30s%-20.2f%-20.2f%-26.2f" % (matriz[i][0], matriz[i][1], matriz[i][2], matriz[i][3]))

def productosMasVendidos(categoria="TODAS"):
    # CASO 1: TODAS -> Top 5 de todos los productos
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            return

        (lista_fecha,
         lista_id_producto,
         lista_producto,
         lista_categoria,
         lista_id_cliente,
         lista_cliente,
         lista_cantidad,
         lista_precio,
         lista_region,
         lista_canal,
         lista_factura) = datos 

        acumulado = []  # [producto, unidades_totales, fact_total]

        i = 0
        while i < len(lista_producto):
            prod = lista_producto[i]
            if prod is None or prod == "":
                i = i + 1
                continue

            try:
                cantidad = float(lista_cantidad[i])
            except:
                cantidad = 0.0
            try:
                precio = float(lista_precio[i])
            except:
                precio = 0.0

            fact = cantidad * precio

            j = logica.indiceEnLista(acumulado, prod)
            if j != -1:
                acumulado[j][1] = acumulado[j][1] + cantidad
                acumulado[j][2] = acumulado[j][2] + fact
            else:
                acumulado.append([prod, cantidad, fact])

            i = i + 1

        if len(acumulado) == 0:
            print("\nNo hay productos validos para mostrar.")
            return

        topUnidades = sorted(acumulado, key=lambda fila: fila[1], reverse=True)
        topFacturacion = sorted(acumulado, key=lambda fila: fila[2], reverse=True)

        if len(acumulado) > 5:
            limite = 5
        else:
            limite = len(acumulado)

        print("\nTop 5 PRODUCTOS (TODAS las categorias) — Por Unidades / Por Facturacion")
        print("-" * 74)
        print(f"{'#':<3} {'Por Unidades':<32} {'Por Facturacion':<32}")
        print("-" * 74)

        fila = 0
        while fila < limite:
            nombre_u = topUnidades[fila][0]
            unidades = topUnidades[fila][1]
            nombre_f = topFacturacion[fila][0]
            fact     = topFacturacion[fila][2]
            print(f"{fila+1:<3} {nombre_u:<20} ({int(unidades):>3} u)   {nombre_f:<20} ($ {fact:>7.2f})")
            fila = fila + 1

        return  # fin caso TODAS

    # CASO 2: Categoria especifica -> Productos dentro de una categoria especifica
    datos = logica.filtrarPorCategoria(categoria)
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

    acumulado = []  # [producto, unidades, fact]

    i = 0
    while i < len(lista_producto):
        producto = lista_producto[i]
        if producto is None or producto == "":
            i = i + 1
            continue

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
            acumulado[j][1] = acumulado[j][1] + cantidad
            acumulado[j][2] = acumulado[j][2] + fact
        else:
            acumulado.append([producto, cantidad, fact])

        i = i + 1

    if len(acumulado) == 0:
        print("\nNo hay productos validos para mostrar.")
        return

    topUnidades = sorted(acumulado, key=lambda fila: fila[1], reverse=True)
    topFacturacion = sorted(acumulado, key=lambda fila: fila[2], reverse=True)

    if len(acumulado) > 5:
        limite = 5
    else:
        limite = len(acumulado)

    print(f"\nTop 5 Productos en '{categoria}' — Por Unidades / Por Facturacion")
    print("-" * 70)
    print(f"{'#':<3} {'Por Unidades':<32} {'Por Facturacion':<32}")
    print("-" * 70)

    fila = 0
    while fila < limite:
        nombre_u = topUnidades[fila][0]
        unidades = topUnidades[fila][1]
        nombre_f = topFacturacion[fila][0]
        fact     = topFacturacion[fila][2]
        print(f"{fila+1:<3} {nombre_u:<20} ({int(unidades):>3} u)   {nombre_f:<20} ($ {fact:>7.2f})")
        fila = fila + 1

def clientesMasRelevantes(categoria="TODAS"):
    # TODAS: considera todas las ventas
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            return

        (lista_fecha,
         lista_id_producto,
         lista_producto,
         lista_categoria,   
         lista_id_cliente,
         lista_cliente,
         lista_cantidad,
         lista_precio,
         lista_region,
         lista_canal,
         lista_factura) = datos

        # acumulado: [cliente, total_facturado]
        acumulado = []

        i = 0
        while i < len(lista_cliente):
            cli = lista_cliente[i]
            if cli is None or cli == "":
                i = i + 1
                continue

            try:
                cantidad = float(lista_cantidad[i])
            except:
                cantidad = 0.0
            try:
                precio = float(lista_precio[i])
            except:
                precio = 0.0

            total = cantidad * precio

            j = logica.indiceEnLista(acumulado, cli)
            if j != -1:
                acumulado[j][1] = acumulado[j][1] + total
            else:
                acumulado.append([cli, total])

            i = i + 1

        if len(acumulado) == 0:
            print("\nNo hay clientes validos para mostrar.")
            return

        # ordenar desc por facturación
        acumulado.sort(key=lambda fila: fila[1], reverse=True)

        # Top N (ajustá si querés)
        if len(acumulado) > 10:
            limite = 10
        else:
            limite = len(acumulado)

        # total general para participación
        total_general = 0.0
        t = 0
        while t < len(acumulado):
            total_general = total_general + acumulado[t][1]
            t = t + 1

        print("\nClientes mas relevantes (TODAS las categorias):")
        print("-" * 60)
        print(f"{'Cliente':<28}{'Total ($)':>16}{'Participacion':>16}")
        print("-" * 60)

        k = 0
        while k < limite:
            cli = acumulado[k][0]
            tot = acumulado[k][1]
            if total_general > 0:
                part = (tot * 100.0) / total_general
            else:
                part = 0.0
            print(f"{cli:<28}{tot:>16.2f}{part:>15.1f}%")
            k = k + 1

        print("-" * 60)
        print(f"{'TOTAL':<28}{total_general:>16.2f}{'100.0%':>16}")
        return  # <-- importantísimo para no caer en la rama de abajo

    # Categoria especifica: ventas separadas por categoria
    datos = logica.filtrarPorCategoria(categoria)
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
     lista_factura) = datos  # 10 listas

    acumulado = []  # [cliente, total]

    i = 0
    while i < len(lista_cliente):
        cli = lista_cliente[i]
        if cli is None or cli == "":
            i = i + 1
            continue

        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = cantidad * precio

        j = logica.indiceEnLista(acumulado, cli)
        if j != -1:
            acumulado[j][1] = acumulado[j][1] + total
        else:
            acumulado.append([cli, total])

        i = i + 1

    if len(acumulado) == 0:
        print("\nNo hay clientes validos para mostrar en esa categoria.")
        return

    acumulado.sort(key=lambda fila: fila[1], reverse=True)

    # Top N
    if len(acumulado) > 10:
        limite = 10
    else:
        limite = len(acumulado)

    total_general = 0.0
    t = 0
    while t < len(acumulado):
        total_general = total_general + acumulado[t][1]
        t = t + 1

    print(f"\nClientes mas relevantes en '{categoria}' (por facturacion):")
    print("-" * 60)
    print(f"{'Cliente':<28}{'Total ($)':>16}{'Participacion':>16}")
    print("-" * 60)

    k = 0
    while k < limite:
        cli = acumulado[k][0]
        tot = acumulado[k][1]
        if total_general > 0:
            part = (tot * 100.0) / total_general
        else:
            part = 0.0
        print(f"{cli:<28}{tot:>16.2f}{part:>15.1f}%")
        k = k + 1

    print("-" * 60)
    print(f"{'TOTAL':<28}{total_general:>16.2f}{'100.0%':>16}")

def ticketPromedioDeVenta(categoria="TODAS"):
    # CASO 1: TODAS -> ticket de todas las ventas
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            return

        (lista_fecha,
         lista_id_producto,
         lista_producto,
         lista_categoria,
         lista_id_cliente,
         lista_cliente,
         lista_cantidad,
         lista_precio,
         lista_region,
         lista_canal,
         lista_factura) = datos

        total_facturacion = 0.0
        cantidad_ventas = 0

        i = 0
        while i < len(lista_cantidad):
            try:
                cantidad = float(lista_cantidad[i])
            except:
                cantidad = 0.0
            try:
                precio = float(lista_precio[i])
            except:
                precio = 0.0

            if cantidad > 0 and precio > 0:
                total_facturacion = total_facturacion + (cantidad * precio)
                cantidad_ventas = cantidad_ventas + 1

            i = i + 1

        print("\n========= TICKET PROMEDIO (TODAS LAS VENTAS) =========")
        if cantidad_ventas == 0:
            print("No hay ventas validas en el archivo.")
            return

        ticket_promedio = total_facturacion / cantidad_ventas
        print(f"Ventas procesadas: {cantidad_ventas}")
        print(f"Facturacion total: ${total_facturacion:,.2f}")
        print(f"Ticket promedio:  ${ticket_promedio:,.2f}")
        print("===========================================")
        return  # fin caso TODAS

    # CASO 2: Categoria especifica
    datos = logica.filtrarPorCategoria(categoria)
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

    i = 0
    while i < len(lista_cantidad):
        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        if cantidad > 0 and precio > 0:
            total_facturacion = total_facturacion + (cantidad * precio)
            cantidad_ventas = cantidad_ventas + 1

        i = i + 1

    print(f"\n========= TICKET PROMEDIO (VENTAS DE {categoria}) =========")
    if cantidad_ventas == 0:
        print("No hay ventas validas en esa categoria.")
        return

    ticket_promedio = total_facturacion / cantidad_ventas
    print(f"Ventas procesadas: {cantidad_ventas}")
    print(f"Facturacion total: ${total_facturacion:,.2f}")
    print(f"Ticket promedio:  ${ticket_promedio:,.2f}")
    print("==============================================")
   
def ventasPorPeriodo(categoria="TODAS"):
    # Seleccion de dataset segun categoria
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            return
        (lista_fecha,
         lista_id_producto,
         lista_producto,
         lista_categoria,
         lista_id_cliente,
         lista_cliente,
         lista_cantidad,
         lista_precio,
         lista_region,
         lista_canal,
         lista_factura) = datos
    else:
        datos = logica.filtrarPorCategoria(categoria)
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
         lista_factura) = datos  # 10 listas

    """
    Analiza las ventas en un periodo específico.
    Ve distribución por mes y por trimestre, con % de crecimiento entre el 1.º
    y 4.º trimestre.
    """

    # Extraer años y acumular ventas por mes (sin separar por año)
    lista_anio = []
    ventas_mes = []
    for i in range(12):
        ventas_mes.append(0.0)

    # Crear listas auxiliares para años únicos y sus totales
    anios_unicos = []
    ventas_anio = []

    i = 0
    while i < len(lista_fecha):
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
        else:
            if "/" in fecha:
                partes = fecha.split("/")
                if len(partes) >= 3:
                    anio = partes[2]
                    try:
                        mes_num = int(partes[1])
                    except:
                        mes_num = 0

        lista_anio.append(anio)

        # Acumular ventas por mes
        if mes_num >= 1 and mes_num <= 12:
            ventas_mes[mes_num - 1] = ventas_mes[mes_num - 1] + cant

        # Acumular ventas totales por año
        repetido = 0
        j = 0
        while j < len(anios_unicos):
            if anios_unicos[j] == anio:
                repetido = 1
                ventas_anio[j] = ventas_anio[j] + cant
            j = j + 1
        if repetido == 0 and anio != "0":
            anios_unicos.append(anio)
            ventas_anio.append(cant)

        i = i + 1

    # Buscar año minimo y maximo 
    if len(anios_unicos) > 0:
        anio_menor = int(anios_unicos[0])
        anio_mayor = int(anios_unicos[0])
        i = 0
        while i < len(anios_unicos):
            actual = int(anios_unicos[i])
            if actual < anio_menor:
                anio_menor = actual
            if actual > anio_mayor:
                anio_mayor = actual
            i = i + 1
    else:
        anio_menor = 0
        anio_mayor = 0

    # Cuadro comparativo de trimestres por año
    print("\n")
    if categoria == "TODAS":
        mensaje3 = "Comparativa de Trimestres por Año (TODAS las categorias)"
    else:
        mensaje3 = "Comparativa de Trimestres por Año - Categoria: " + str(categoria)
    cadena3 = mensaje3.center(90, ' ')
    print(cadena3)
    print("-" * 90)
    print("%-10s%-14s%-14s%-14s%-14s%-10s" %
          ("Anio", "Trim 1", "Trim 2", "Trim 3", "Trim 4", "% Crec. Anual"))
    print("-" * 90)

    # Calcular ventas por trimestre en cada año
    i = 0
    while i < len(anios_unicos):
        anio_actual = anios_unicos[i]
        # inicializar totales trimestrales
        trim1 = 0.0
        trim2 = 0.0
        trim3 = 0.0
        trim4 = 0.0

        # recorrer todos los registros y acumular segun el mes
        j = 0
        while j < len(lista_fecha):
            fecha = lista_fecha[j]
            anio_fila = "0"
            mes_num = 0

            if "-" in fecha:              
                partes = fecha.split("-")
                if len(partes) >= 2:
                    anio_fila = partes[0]
                    try:
                        mes_num = int(partes[1])
                    except:
                        mes_num = 0
            else:
                if "/" in fecha:           
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
            j = j + 1

        # calcular crecimiento total del anio (Trim4 vs Trim1)
        crec_anual = 0.0
        if trim1 != 0:
            crec_anual = ((trim4 - trim1) / trim1) * 100.0

        print("%-10s%-14.2f%-14.2f%-14.2f%-14.2f%9.2f" %
              (anio_actual, trim1, trim2, trim3, trim4, crec_anual), "%")

        i = i + 1

def comparativaProducto():
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_categoria,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # acumulado: [producto, categoria, unidadesTotales, facturacionTotal]
    acumulado = []

    i = 0
    while i < len(lista_producto):
        prod = lista_producto[i]
        cat = lista_categoria[i]

        # evitar productos vacíos
        if prod is None or prod == "":
            i = i + 1
            continue

        # convertir a números seguros
        try:
            unidades = float(lista_cantidad[i])
        except:
            unidades = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = unidades * precio

        # buscar si ya existe el producto en acumulado
        idx = logica.indiceEnLista(acumulado, prod)
        if idx != -1:
            acumulado[idx][2] = acumulado[idx][2] + unidades
            acumulado[idx][3] = acumulado[idx][3] + total
        else:
            acumulado.append([prod, cat, unidades, total])

        i = i + 1

    cantidadProductos = len(acumulado)
    if cantidadProductos < 1:
        print("\n⚠️ No hay productos para analizar.")
        return

    # SUBMENÚ DE OPCIONES
    print("\nElija tipo de comparativa de productos:")
    print("1) Comparar 2 productos de una categoría")
    print("2) Comparar TODAS las categorías")
    tipo = logica.validarInput(1, 2)

    # OPCIÓN 1: comparar 2 productos de una MISMA categoría
    if tipo == 1:

        # armar lista de categorías únicas
        categorias_unicas = []
        i = 0
        while i < len(acumulado):
            cat_act = acumulado[i][1]
            repetido = 0
            j = 0
            while j < len(categorias_unicas):
                if categorias_unicas[j] == cat_act:
                    repetido = 1
                j = j + 1
            if repetido == 0:
                categorias_unicas.append(cat_act)
            i = i + 1

        if len(categorias_unicas) == 0:
            print("\n⚠️ No hay categorías para analizar.")
            return

        print("\nCategorías disponibles:")
        i = 0
        while i < len(categorias_unicas):
            print(f"{i+1}. {categorias_unicas[i]}")
            i = i + 1

        opcion_cat = logica.validarInput(1, len(categorias_unicas))
        categoria_elegida = categorias_unicas[opcion_cat - 1]

        # filtrar productos de esa categoría
        productos_cat = []
        i = 0
        while i < len(acumulado):
            if acumulado[i][1] == categoria_elegida:
                productos_cat.append(acumulado[i])
            i = i + 1

        cantidadProductosCat = len(productos_cat)
        if cantidadProductosCat < 2:
            print("\n⚠️ No hay suficientes productos en esa categoría para comparar.")
            return

        print(f"\nProductos de la categoría: {categoria_elegida}")
        k = 0
        while k < cantidadProductosCat:
            unidades_mostrar = productos_cat[k][2]
            if unidades_mostrar == int(unidades_mostrar):
                unidades_mostrar = int(unidades_mostrar)
            print(f"{k+1}. {productos_cat[k][0]}  (u: {unidades_mostrar}, $: {productos_cat[k][3]:.2f})")
            k = k + 1

        opcion1 = logica.validarInput(1, cantidadProductosCat)
        opcion2 = logica.validarInput(1, cantidadProductosCat)
        while opcion1 == opcion2:
            print("⚠️ Deben ser productos distintos.")
            opcion2 = logica.validarInput(1, cantidadProductosCat)

        producto1 = productos_cat[opcion1 - 1]
        producto2 = productos_cat[opcion2 - 1]

        totalUnidades = producto1[2] + producto2[2]
        totalFacturacion = producto1[3] + producto2[3]

        if totalUnidades > 0:
            porcentajeUnidades1 = (producto1[2] * 100.0) / totalUnidades
            porcentajeUnidades2 = (producto2[2] * 100.0) / totalUnidades
        else:
            porcentajeUnidades1, porcentajeUnidades2 = 0.0, 0.0

        if totalFacturacion > 0:
            porcentajeFacturacion1 = (producto1[3] * 100.0) / totalFacturacion
            porcentajeFacturacion2 = (producto2[3] * 100.0) / totalFacturacion
        else:
            porcentajeFacturacion1, porcentajeFacturacion2 = 0.0, 0.0

        print("\nComparativa de productos dentro de la categoría:", categoria_elegida)
        print("-" * 80)
        print(f"{'Producto':<25} {'Unidades':>10} {'Facturación ($)':>18} {'U%':>6} {'F%':>6}")
        print("-" * 80)
        print(f"{producto1[0]:<25} {int(producto1[2]):>10} {producto1[3]:>18.2f} {porcentajeUnidades1:>6.1f} {porcentajeFacturacion1:>6.1f}")
        print(f"{producto2[0]:<25} {int(producto2[2]):>10} {producto2[3]:>18.2f} {porcentajeUnidades2:>6.1f} {porcentajeFacturacion2:>6.1f}")
        print("-" * 80)

        if producto1[3] > producto2[3]:
            print(f"{producto1[0]} facturó más que {producto2[0]} (+$ {producto1[3] - producto2[3]:.2f}).")
        elif producto2[3] > producto1[3]:
            print(f"{producto2[0]} facturó más que {producto1[0]} (+$ {producto2[3] - producto1[3]:.2f}).")
        else:
            print("Ambos productos tienen la misma facturación.")

    # OPCIÓN 2: COMPARATIVA DE TODAS LAS CATEGORÍAS
    elif tipo == 2:
        # armar lista de categorías con sus totales [categoria, unidades, facturacion]
        categorias = []
        i = 0
        while i < len(acumulado):
            cat = acumulado[i][1]
            unidades = acumulado[i][2]
            fact = acumulado[i][3]

            # buscar si ya está la categoría
            idx = -1
            j = 0
            while j < len(categorias):
                if categorias[j][0] == cat:
                    idx = j
                j = j + 1

            if idx != -1:
                categorias[idx][1] = categorias[idx][1] + unidades
                categorias[idx][2] = categorias[idx][2] + fact
            else:
                categorias.append([cat, unidades, fact])
            i = i + 1

        if len(categorias) == 0:
            print("\n⚠️ No hay categorías para comparar.")
            return

        # ordenar alfabéticamente las categorías (burbuja)
        i = 0
        while i < len(categorias) - 1:
            j = i + 1
            while j < len(categorias):
                if categorias[i][0] > categorias[j][0]:
                    aux = categorias[i]
                    categorias[i] = categorias[j]
                    categorias[j] = aux
                j = j + 1
            i = i + 1

        # totales globales
        total_u_global = 0.0
        total_f_global = 0.0
        i = 0
        while i < len(categorias):
            total_u_global = total_u_global + categorias[i][1]
            total_f_global = total_f_global + categorias[i][2]
            i = i + 1

        # mostrar cuadro
        print("\nComparativa de TODAS las CATEGORÍAS")
        print("-" * 90)
        print(f"{'Categoría':<25} {'Unidades':>10} {'Facturación ($)':>18} {'U%':>6} {'F%':>6}")
        print("-" * 90)

        i = 0
        while i < len(categorias):
            cat = categorias[i]
            if total_u_global > 0:
                pu = (cat[1] * 100.0) / total_u_global
            else:
                pu = 0.0
            if total_f_global > 0:
                pf = (cat[2] * 100.0) / total_f_global
            else:
                pf = 0.0

            unidades_mostrar = cat[1]
            if unidades_mostrar == int(unidades_mostrar):
                unidades_mostrar = int(unidades_mostrar)

            print(f"{cat[0]:<25} {unidades_mostrar:>10} {cat[2]:>18.2f} {pu:>6.1f} {pf:>6.1f}")
            i = i + 1

        print("-" * 90)
        print(f"Total unidades: {total_u_global:.2f}")
        print(f"Total facturación: {total_f_global:.2f}")

def comparativaCliente():
   
    datos = cargarDatosCSV()
    if datos is None:
        return

    (lista_fecha,
     lista_id_producto,
     lista_producto,
     lista_categoria,
     lista_id_cliente,
     lista_cliente,
     lista_cantidad,
     lista_precio,
     lista_region,
     lista_canal,
     lista_factura) = datos

    # acumulado: [cliente, categoria, facturacion_total]
    acumulado = []

    i = 0
    while i < len(lista_cliente):
        cliente = lista_cliente[i]
        categoria = lista_categoria[i]

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

        # buscar si el cliente ya está acumulado
        idx = logica.indiceEnLista(acumulado, cliente)   # busca en columna 0
        if idx != -1:
            acumulado[idx][2] = acumulado[idx][2] + total
        else:
            acumulado.append([cliente, categoria, total])

        i = i + 1

    cantidadClientes = len(acumulado)
    if cantidadClientes < 1:
        print("\n⚠️ No hay clientes para analizar.")
        return

    # SUBMENÚ: tipo de comparativa
    print("\nElija tipo de comparativa de clientes:")
    print("1) Comparar 2 clientes de una categoría")
    print("2) Comparar TODAS las categorías")
    tipo = logica.validarInput(1, 2)

    # OPCIÓN 1: comparar 2 clientes de una MISMA CATEGORÍA
    if tipo == 1:

        # 1) categorías únicas
        categorias_unicas = []
        i = 0
        while i < len(acumulado):
            cat_act = acumulado[i][1]
            repetido = 0
            j = 0
            while j < len(categorias_unicas):
                if categorias_unicas[j] == cat_act:
                    repetido = 1
                j = j + 1
            if repetido == 0:
                categorias_unicas.append(cat_act)
            i = i + 1

        if len(categorias_unicas) == 0:
            print("\n⚠️ No hay categorías para analizar.")
            return

        # 2) mostrar categorías
        print("\nCategorías disponibles:")
        i = 0
        while i < len(categorias_unicas):
            print(f"{i+1}. {categorias_unicas[i]}")
            i = i + 1

        opcion_cat = logica.validarInput(1, len(categorias_unicas))
        categoria_elegida = categorias_unicas[opcion_cat - 1]

        # 3) armar lista de clientes de esa categoría
        clientes_cat = []
        i = 0
        while i < len(acumulado):
            if acumulado[i][1] == categoria_elegida:
                clientes_cat.append(acumulado[i])   # [cliente, cat, total]
            i = i + 1

        cantidadClientesCat = len(clientes_cat)
        if cantidadClientesCat < 2:
            print("\n⚠️ No hay suficientes clientes en esa categoría para comparar.")
            return

        # 4) mostrar clientes de esa categoría
        print(f"\nClientes que compraron de la categoría: {categoria_elegida}")
        k = 0
        while k < cantidadClientesCat:
            print(f"{k+1}. {clientes_cat[k][0]}  ($ {clientes_cat[k][2]:.2f})")
            k = k + 1

        # 5) elegir dos clientes
        opcion1 = logica.validarInput(1, cantidadClientesCat)
        opcion2 = logica.validarInput(1, cantidadClientesCat)

        while opcion1 == opcion2:
            print("⚠️ Deben ser distintos.")
            opcion2 = logica.validarInput(1, cantidadClientesCat)

        cliente1 = clientes_cat[opcion1 - 1]   # [nombre, cat, total]
        cliente2 = clientes_cat[opcion2 - 1]

        # Cálculo de participaciones dentro del par
        totalPar = cliente1[2] + cliente2[2]
        if totalPar > 0:
            p1 = (cliente1[2] * 100.0) / totalPar
            p2 = (cliente2[2] * 100.0) / totalPar
        else:
            p1 = 0.0
            p2 = 0.0

        diferencia = cliente1[2] - cliente2[2]

        print("\nComparativa de clientes (por facturación total) en categoría:", categoria_elegida)
        print("-" * 60)
        print(f"{'Cliente':<24} {'Total ($)':>12} {'Participación':>14}")
        print("-" * 60)
        print(f"{cliente1[0]:<24} {cliente1[2]:>12.2f} {p1:>12.1f}%")
        print(f"{cliente2[0]:<24} {cliente2[2]:>12.2f} {p2:>12.1f}%")
        print("-" * 60)

        if diferencia > 0:
            print(f"{cliente1[0]} supera a {cliente2[0]} por $ {diferencia:.2f}.")
        elif diferencia < 0:
            print(f"{cliente2[0]} supera a {cliente1[0]} por $ {abs(diferencia):.2f}.")
        else:
            print("Ambos tienen la misma facturación.")

    # OPCIÓN 2: comparar TODAS las CATEGORÍAS
    elif tipo == 2:

        # armar lista de categorías con totales [categoria, facturacion_total]
        categorias = []
        i = 0
        while i < len(acumulado):
            cat = acumulado[i][1]
            fact = acumulado[i][2]

            idx = -1
            j = 0
            while j < len(categorias):
                if categorias[j][0] == cat:
                    idx = j
                j = j + 1

            if idx != -1:
                categorias[idx][1] = categorias[idx][1] + fact
            else:
                categorias.append([cat, fact])

            i = i + 1

        if len(categorias) == 0:
            print("\n⚠️ No hay categorías para comparar.")
            return

        # ordenar alfabéticamente las categorías (burbuja)
        i = 0
        while i < len(categorias) - 1:
            j = i + 1
            while j < len(categorias):
                if categorias[i][0] > categorias[j][0]:
                    aux = categorias[i]
                    categorias[i] = categorias[j]
                    categorias[j] = aux
                j = j + 1
            i = i + 1

        # total global de facturación
        total_global = 0.0
        i = 0
        while i < len(categorias):
            total_global = total_global + categorias[i][1]
            i = i + 1

        # mostrar cuadro comparativo de categorías
        print("\nComparativa de TODAS las CATEGORÍAS (por facturación total)")
        print("-" * 70)
        print(f"{'Categoría':<25} {'Total ($)':>18} {'Participación':>14}")
        print("-" * 70)

        i = 0
        while i < len(categorias):
            cat = categorias[i]
            if total_global > 0:
                p = (cat[1] * 100.0) / total_global
            else:
                p = 0.0
            print(f"{cat[0]:<25} {cat[1]:>18.2f} {p:>12.1f}%")
            i = i + 1

        print("-" * 70)
        print(f"Total facturación global: $ {total_global:.2f}")

        # Determinar la categoría con mayor facturación
        if len(categorias) > 0:
            mayor_fact = categorias[0][1]
            categoria_top = categorias[0][0]
            i = 1
            while i < len(categorias):
                if categorias[i][1] > mayor_fact:
                    mayor_fact = categorias[i][1]
                    categoria_top = categorias[i][0]
                i = i + 1

            print(f"\n🏆 La categoría con mayor facturación fue '{categoria_top}' con $ {mayor_fact:.2f}.")

def tendenciaDeCrecimiento(categoria="TODAS"):
    """
    Muestra la participacion (%) de cada mes en la facturacion total
    (global o filtrada por una categoria especifica).

    Para cada mes:
    - suma (Cantidad * Precio_Unitario)
    - calcula que % representa sobre el total
    """

    # Seleccion de dataset segun categoria
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            print("No se pudieron cargar los datos de ventas.")
            return

        lista_fecha      = datos[0]
        lista_producto   = datos[2]
        lista_id_cliente = datos[4]
        lista_cliente    = datos[5]
        lista_cantidad   = datos[6]
        lista_precio     = datos[7]
        lista_region     = datos[8]
        lista_canal      = datos[9]
        lista_factura    = datos[10]
        titulo = "Porcentaje de ventas por mes (TODAS las categorias)"
    else:
        datos = logica.filtrarPorCategoria(categoria)
        if datos is None:
            print("No se pudieron cargar los datos de ventas.")
            return

        lista_fecha      = datos[0]
        lista_id_producto= datos[1]
        lista_producto   = datos[2]
        lista_id_cliente = datos[3]
        lista_cliente    = datos[4]
        lista_cantidad   = datos[5]
        lista_precio     = datos[6]
        lista_region     = datos[7]
        lista_canal      = datos[8]
        lista_factura    = datos[9]
        titulo = "Porcentaje de ventas por mes (Categoria: " + str(categoria) + ")"

    # Acumular facturacion por mes "YYYY-MM"
    facturacion_por_mes = {}  # {"YYYY-MM": total}

    i = 0
    while i < len(lista_fecha):
        fecha_str = lista_fecha[i]

        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio_unit = float(lista_precio[i])
        except:
            precio_unit = 0.0

        total_linea = cantidad * precio_unit

        # Clave de mes (suponemos YYYY-MM-DD)
        clave_mes = ""
        if isinstance(fecha_str, str) and len(fecha_str) >= 7:
            clave_mes = fecha_str[:7]

        if clave_mes != "":
            if clave_mes in facturacion_por_mes:
                facturacion_por_mes[clave_mes] = facturacion_por_mes[clave_mes] + total_linea
            else:
                facturacion_por_mes[clave_mes] = total_linea

        i = i + 1

    # Orden cronologico de meses
    meses_ordenados = sorted(facturacion_por_mes.keys())

    # Total general
    total_anual = 0.0
    j = 0
    while j < len(meses_ordenados):
        mes_clave = meses_ordenados[j]
        total_anual = total_anual + facturacion_por_mes[mes_clave]
        j = j + 1

    if total_anual == 0:
        print("No hay facturacion en los datos.")
        return

    # Tabla final
    print("\n" + titulo)
    print("-" * 70)
    print(f"{'Mes':<20}{'Facturacion ($)':<20}{'Participacion':<15}")
    print("-" * 70)

    k = 0
    while k < len(meses_ordenados):
        mes_clave = meses_ordenados[k]
        fact_mes = facturacion_por_mes[mes_clave]
        porcentaje = (fact_mes * 100.0) / total_anual

        etiqueta = logica.formatear_mes(mes_clave)

        print(f"{etiqueta:<20}{fact_mes:<20.2f}{porcentaje:>10.1f}%")
        k = k + 1

    print("-" * 70)
    print(f"{'TOTAL':<20}{total_anual:<20.2f}{'100.0%':>10}")
    print()


def comparativaCanal(categoria="TODAS"):
    """
    Compara las ventas totales entre los distintos canales (Online, Tienda, Mayorista).
    Calcula facturacion y participacion porcentual.
    Separa por categoria o toma todos los datos
    """

    # Seleccion de dataset segun categoria
    if categoria == "TODAS":
        datos = cargarDatosCSV()
        if datos is None:
            print("No se pudieron cargar los datos de ventas.")
            return

        lista_cantidad = datos[6]
        lista_precio   = datos[7]
        lista_canal    = datos[9]
        titulo = "Comparativa de ventas por canal (TODAS las categorias)"
    else:
        datos = logica.filtrarPorCategoria(categoria)
        if datos is None:
            print("No se pudieron cargar los datos de ventas.")
            return

        lista_cantidad = datos[5]
        lista_precio   = datos[6]
        lista_canal    = datos[8]
        titulo = "Comparativa de ventas por canal (Categoria: " + str(categoria) + ")"

    # Acumular facturacion total por canal
    facturacion_por_canal = {}  # {'Online': 12345.0, ...}

    i = 0
    while i < len(lista_canal):
        canal = lista_canal[i]

        try:
            cantidad = float(lista_cantidad[i])
        except:
            cantidad = 0.0
        try:
            precio = float(lista_precio[i])
        except:
            precio = 0.0

        total = cantidad * precio

        if canal in facturacion_por_canal:
            facturacion_por_canal[canal] = facturacion_por_canal[canal] + total
        else:
            facturacion_por_canal[canal] = total

        i = i + 1

    # Total general (manual) y chequeo
    total_general = 0.0
    for k in facturacion_por_canal:
        total_general = total_general + facturacion_por_canal[k]

    if total_general == 0:
        print("No se registraron ventas.")
        return

    # Ordenar por facturacion desc
    canales_items = []
    for k in facturacion_por_canal:
        canales_items.append([k, facturacion_por_canal[k]])
    canales_items.sort(key=lambda x: x[1], reverse=True)

    # Mostrar resultados
    print("\n" + titulo)
    print("-" * 60)
    print(f"{'Canal':<15}{'Facturacion ($)':>20}{'Participacion':>20}")
    print("-" * 60)

    m = 0
    while m < len(canales_items):
        canal = canales_items[m][0]
        total = canales_items[m][1]
        participacion = (total * 100.0) / total_general
        print(f"{canal:<15}{total:>20.2f}{participacion:>19.1f}%")
        m = m + 1

    print("-" * 60)
    print(f"{'TOTAL':<15}{total_general:>20.2f}{'100.0%':>19}")
    print("-" * 60)

    # Destacar el canal mas fuerte
    canal_top = canales_items[0][0]
    print(f"\n El canal con mayor facturacion es: {canal_top}\n")
