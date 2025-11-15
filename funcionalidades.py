import logica
import random

# VARIABLES GLOBALES
nombre_archivo = "ventas_dataset_sin_tildes.csv"

def crecimientoVentas(eleccion):    
    # PRIMERA PASADA: encontrar todas las claves y el año mínimo/máximo

    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo.")
        return

    primero = True
    antes = 0
    despues = 0

    # Usamos diccionarios para rapidez y eficiencia
    categorias_dict = {}         # clave: categoría
    productos_dict = {}          # clave: producto dentro de categoría elegida

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue

        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        producto = partes[2]
        categoria = partes[3]

        # Obtener año
        if "-" in fecha:
            parte_anio = fecha.split("-")[0]
            try:
                anio = int(parte_anio)
            except:
                continue
        else:
            continue

        # Año mínimo y máximo
        if antes == 0 and despues == 0:
            antes = anio
            despues = anio
        else:
            if anio < antes:
                antes = anio
            if anio > despues:
                despues = anio

        # Caso "TODAS": recolectamos categorías únicas
        if eleccion == "TODAS":
            if categoria not in categorias_dict:
                categorias_dict[categoria] = True

        # Caso categoría elegida: recolectamos productos únicos
        else:
            if categoria == eleccion:
                if producto not in productos_dict:
                    productos_dict[producto] = True

    arch.close()

   
    # PREPARAR BASE


    if eleccion == "TODAS":
        lista_base = list(categorias_dict.keys())
    else:
        lista_base = list(productos_dict.keys())

    # Preparamos totales por año
    total_antes = []
    total_despues = []

    i = 0
    while i < len(lista_base):
        total_antes.append(0.0)
        total_despues.append(0.0)
        i += 1

  
    # SEGUNDA PASADA: acumular ventas por categoría o producto
   

    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo en segunda pasada.")
        return

    primero = True

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue

        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        producto = partes[2]
        categoria = partes[3]

        # Obtener año
        if "-" in fecha:
            try:
                anio = int(fecha.split("-")[0])
            except:
                continue
        else:
            continue

        # Cantidad y precio
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0

        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        venta = cantidad * precio

        # Qué comparamos
        if eleccion == "TODAS":
            clave = categoria
        else:
            if categoria != eleccion:
                continue
            clave = producto

        # Buscar índice
        ind = -1
        j = 0
        while j < len(lista_base):
            if lista_base[j] == clave:
                ind = j
            j += 1

        if ind == -1:
            continue

        # Acumular
        if anio == antes:
            total_antes[ind] += venta
        if anio == despues:
            total_despues[ind] += venta

    arch.close()

    
    # ARMAR MATRIZ
   

    matriz = []
    i = 0
    while i < len(lista_base):
        nombre = lista_base[i]
        v1 = total_antes[i]
        v2 = total_despues[i]

        if v1 != 0:
            crec = ((v2 - v1) / v1) * 100
        else:
            crec = 0.0

        matriz.append([nombre, v1, v2, crec])
        i += 1

    
    # ORDENAR MATRIZ ALFABÉTICAMENTE
    
    
    i = 0
    while i < len(matriz) - 1:
        j = i + 1
        while j < len(matriz):
            if matriz[i][0] > matriz[j][0]:
                aux = matriz[i]
                matriz[i] = matriz[j]
                matriz[j] = aux
            j += 1
        i += 1

  
    # IMPRIMIR RESULTADOS
   

    if eleccion == "TODAS":
        print(f"\nComparación de ventas por CATEGORÍA entre {antes} y {despues}")
        print("-" * 90)
        print("%-30s%-20s%-20s%-20s" %
              ("Categoría", antes, despues, "Crecimiento %"))
        print("-" * 90)
    else:
        print(f"\nComparación de productos de la categoría '{eleccion}'")
        print("-" * 90)
        print("%-30s%-20s%-20s%-20s" %
              ("Producto", antes, despues, "Crecimiento %"))
        print("-" * 90)

    i = 0
    while i < len(matriz):
        print("%-30s%-20.2f%-20.2f%-20.2f" %
              (matriz[i][0], matriz[i][1], matriz[i][2], matriz[i][3]))
        i += 1



def productosMasVendidos(categoria="TODAS"):
    # CASO 1 — TODAS LAS CATEGORÍAS → usar diccionario para máxima eficiencia
   

    if categoria == "TODAS":

        try:
            arch = open(nombre_archivo, "r")
        except:
            print("No se pudo abrir el archivo.")
            return

        primero = True

        # Diccionario:
        # producto : [unidades_totales, facturacion_total]
        acumulado = {}

        # ----------- Primera pasada: acumular ventas por producto -----------
        for linea in arch:
            linea = linea.strip()
            if linea == "":
                continue

            if primero:
                primero = False
                continue

            partes = linea.split(",")
            if len(partes) < 11:
                continue

            producto = partes[2]
            if producto is None or producto == "":
                continue

            # Cantidad
            try:
                cantidad = float(partes[6])
            except:
                cantidad = 0.0

            # Precio
            try:
                precio = float(partes[7])
            except:
                precio = 0.0

            facturacion = cantidad * precio

            # ---------------- Diccionario: acceso DIRECTO ----------------
            if producto not in acumulado:
                acumulado[producto] = [0.0, 0.0]

            acumulado[producto][0] += cantidad
            acumulado[producto][1] += facturacion

        arch.close()

        # No hay productos válidos
        if len(acumulado) == 0:
            print("\nNo hay productos válidos para mostrar.")
            return

      
        # Convertir diccionario a lista para ordenar
        
        lista_prod = []
        for prod in acumulado:
            lista_prod.append([prod, acumulado[prod][0], acumulado[prod][1]])

        
        # Crear dos copias: una para unidades y otra para facturación
        
        topUnidades = []
        topFacturacion = []

        i = 0
        while i < len(lista_prod):
            topUnidades.append(lista_prod[i])
            topFacturacion.append(lista_prod[i])
            i += 1

        
        # Ordenar topUnidades por unidades DESC (burbuja)
        
        i = 0
        while i < len(topUnidades) - 1:
            j = i + 1
            while j < len(topUnidades):
                if topUnidades[i][1] < topUnidades[j][1]:
                    aux = topUnidades[i]
                    topUnidades[i] = topUnidades[j]
                    topUnidades[j] = aux
                j += 1
            i += 1

        
        # Ordenar topFacturacion por facturación DESC (burbuja)
        
        i = 0
        while i < len(topFacturacion) - 1:
            j = i + 1
            while j < len(topFacturacion):
                if topFacturacion[i][2] < topFacturacion[j][2]:
                    aux = topFacturacion[i]
                    topFacturacion[i] = topFacturacion[j]
                    topFacturacion[j] = aux
                j += 1
            i += 1

        
        # Determinar límite del Top 5
        
        if len(lista_prod) > 5:
            limite = 5
        else:
            limite = len(lista_prod)

        
        # Imprimir tabla
        
        print("\nTOP 5 PRODUCTOS — TODAS LAS CATEGORÍAS")
        print("-" * 90)
        print("%-5s%-35s%-25s%-20s" % ("#", "Producto", "Unidades Totales", "Facturación Total"))
        print("-" * 90)

        fila = 0
        while fila < limite:
            p_un = topUnidades[fila][0]
            unidades = int(topUnidades[fila][1])
            p_fac = topFacturacion[fila][0]
            fact = topFacturacion[fila][2]

            print("%-5d%-35s%-25d$%-19.2f" %
                  (fila + 1, p_un, unidades, fact))

            fila += 1

        return  # FIN CASO TODAS

    
    # CASO 2 — UNA CATEGORÍA ESPECÍFICA
    

    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo.")
        return

    primero = True

    # Diccionario para acumular SOLO los productos de esa categoría
    acumulado = {}     # producto : [unidades, facturacion]

    # ----------- Recorrer archivo -----------
    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue

        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        producto = partes[2]
        categoria_actual = partes[3]

        # Filtrar categoría
        if categoria_actual != categoria:
            continue

        if producto is None or producto == "":
            continue

        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0

        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        facturacion = cantidad * precio

        # Diccionario → acceso directo
        if producto not in acumulado:
            acumulado[producto] = [0.0, 0.0]

        acumulado[producto][0] += cantidad
        acumulado[producto][1] += facturacion

    arch.close()

    if len(acumulado) == 0:
        print("\nNo hay productos válidos para mostrar.")
        return

   
    # Convertir a lista para ordenar
    
    lista_prod = []
    for p in acumulado:
        lista_prod.append([p, acumulado[p][0], acumulado[p][1]])

    topUnidades = []
    topFacturacion = []

    i = 0
    while i < len(lista_prod):
        topUnidades.append(lista_prod[i])
        topFacturacion.append(lista_prod[i])
        i += 1
    
    # Ordenar
    # Unidades DESC
    i = 0
    while i < len(topUnidades) - 1:
        j = i + 1
        while j < len(topUnidades):
            if topUnidades[i][1] < topUnidades[j][1]:
                aux = topUnidades[i]
                topUnidades[i] = topUnidades[j]
                topUnidades[j] = aux
            j += 1
        i += 1

    # Facturación DESC
    i = 0
    while i < len(topFacturacion) - 1:
        j = i + 1
        while j < len(topFacturacion):
            if topFacturacion[i][2] < topFacturacion[j][2]:
                aux = topFacturacion[i]
                topFacturacion[i] = topFacturacion[j]
                topFacturacion[j] = aux
            j += 1
        i += 1

    # Limitar a Top 5
    if len(lista_prod) > 5:
        limite = 5
    else:
        limite = len(lista_prod)

    
    # Imprimir resultados
    
    print(f"\nTOP 5 PRODUCTOS DE LA CATEGORÍA '{categoria}'")
    print("-" * 90)
    print("%-5s%-35s%-25s%-20s" %
          ("#", "Producto", "Unidades Totales", "Facturación Total"))
    print("-" * 90)

    fila = 0
    while fila < limite:
        p = topUnidades[fila][0]
        unidades = int(topUnidades[fila][1])
        fact = topFacturacion[fila][2]

        print("%-5d%-35s%-25d$%-19.2f" %
              (fila + 1, p, unidades, fact))

        fila += 1

def clientesMasRelevantes(categoria="TODAS"):
    """
    Muestra el TOP de clientes más relevantes por facturación.
    - Si categoria == "TODAS": considera todas las ventas.
    - Si se pasa una categoría específica: filtra solo esas ventas.
    """

    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo:", nombre_archivo)
        return

    primera_linea = True

    # diccionario: cliente -> total_facturado
    facturacion_por_cliente = {}

    for linea in arch:
        linea = linea.strip()
        if not linea:
            continue

        # saltar encabezado
        if primera_linea:
            primera_linea = False
            continue

        # Revisar que la venta tenga datos completos
        partes = linea.split(",")
        if len(partes) < 11:
            continue

        # Extraemos categoria y cliente
        cat_actual = partes[3].strip()
        cliente = partes[5].strip()

        if not cliente:
            continue

        # filtro por categoría si no es "TODAS"
        if categoria != "TODAS" and cat_actual != categoria:
            continue

        # Calculamos facturación
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        total = cantidad * precio

        if cliente in facturacion_por_cliente:
            facturacion_por_cliente[cliente] += total
        else:
            facturacion_por_cliente[cliente] = total

    arch.close()

    # Pasamos a lista acumuladora para ordenar: [cliente, total]
    acumulado = []
    for cli, total in facturacion_por_cliente.items():
        acumulado.append([cli, total])

    if len(acumulado) == 0:
        if categoria == "TODAS":
            print("\nNo hay clientes válidos para mostrar.")
        else:
            print("\nNo hay clientes válidos para mostrar en esa categoría.")
        return

    # ordenar desc por facturación
    acumulado.sort(key=lambda fila: fila[1], reverse=True)

    # Top N
    if len(acumulado) > 10:
        limite = 10
    else:
        limite = len(acumulado)

    # total general para participación
    total_general = 0.0
    t = 0
    while t < len(acumulado):
        total_general += acumulado[t][1]
        t += 1

    # Título según categoría
    if categoria == "TODAS":
        print("\nClientes más relevantes (TODAS las categorías):")
    else:
        print(f"\nClientes más relevantes en '{categoria}' (por facturación):")

    print("-" * 60)
    print(f"{'Cliente':<28}{'Total ($)':>16}{'Participación':>16}")
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
        k += 1

    print("-" * 60)
    print(f"{'TOTAL':<28}{total_general:>16.2f}{'100.0%':>16}")


def ticketPromedioDeVenta(categoria="TODAS"):
    # Abrimos el archivo
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo.")
        return

    # Inicializamos variables
    primero = True
    total_facturacion = 0.0
    cantidad_ventas = 0

    # Recorremos archivo
    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue
        
        # Se salta la primera linea
        if primero:
            primero = False
            continue

        # Separa los atributos de la venta y revisa que esten completos
        partes = linea.split(",")
        if len(partes) < 11:
            continue

        # Extrae la categoria del producto vendido
        cat_actual = partes[3]

        # filtro por categoría si corresponde
        if categoria != "TODAS" and cat_actual != categoria:
            continue

        # Extrae cantidad y precio
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        # Si la cantidad y el precio son mayores que 0, suma al total
        if cantidad > 0 and precio > 0:
            total_facturacion = total_facturacion + (cantidad * precio)
            cantidad_ventas = cantidad_ventas + 1

    arch.close()

    # Imprime el menu
    print(f"\n========= TICKET PROMEDIO (VENTAS DE {categoria}) =========")
    if cantidad_ventas == 0:
        print("No hay ventas validas en esa categoria.")
        return

    # Calcula ticket promedio si hay ventas
    ticket_promedio = total_facturacion / cantidad_ventas
    print(f"Ventas procesadas: {cantidad_ventas}")
    print(f"Facturacion total: ${total_facturacion:,.2f}")
    print(f"Ticket promedio:  ${ticket_promedio:,.2f}")
    print("==============================================")
   
def ventasPorPeriodo(eleccion="TODAS"):

    # ==========================================================================
    # PRIMERA PASADA: recolectar AÑOS (base)
    # ==========================================================================
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo.")
        return

    primero = True
    anios_dict = {}   # año -> True

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue
        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        categoria = partes[3]

        # Obtener año y mes del formato YYYY-MM-...
        if "-" not in fecha:
            continue
        pedazos = fecha.split("-")
        if len(pedazos) < 2:
            continue
        try:
            anio = int(pedazos[0])
            mes = int(pedazos[1])
        except:
            continue

        # Filtro por categoría (si corresponde)
        if eleccion != "TODAS" and categoria != eleccion:
            continue

        # Registrar año
        if anio not in anios_dict:
            anios_dict[anio] = True

    arch.close()

    # Base de años (lista) y orden ascendente (burbuja)
    lista_anios = list(anios_dict.keys())
    if len(lista_anios) == 0:
        print("\nNo hay datos para mostrar en el periodo seleccionado.")
        return

    i = 0
    while i < len(lista_anios) - 1:
        j = i + 1
        while j < len(lista_anios):
            if lista_anios[i] > lista_anios[j]:
                aux = lista_anios[i]
                lista_anios[i] = lista_anios[j]
                lista_anios[j] = aux
            j += 1
        i += 1

    # Acumuladores por año (arrays paralelos): T1..T4
    t1 = [0.0] * len(lista_anios)
    t2 = [0.0] * len(lista_anios)
    t3 = [0.0] * len(lista_anios)
    t4 = [0.0] * len(lista_anios)

    # ==========================================================================
    # SEGUNDA PASADA: acumular ventas por AÑO y TRIMESTRE
    # ==========================================================================
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo en segunda pasada.")
        return

    primero = True

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue
        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        categoria = partes[3]

        if "-" not in fecha:
            continue
        pedazos = fecha.split("-")
        if len(pedazos) < 2:
            continue
        try:
            anio = int(pedazos[0])
            mes = int(pedazos[1])
        except:
            continue

        if eleccion != "TODAS" and categoria != eleccion:
            continue

        # cantidad * precio (defensivo)
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        venta = cantidad * precio
        if venta <= 0:
            continue

        # Buscar índice de año en lista_anios
        ind = -1
        j = 0
        while j < len(lista_anios):
            if lista_anios[j] == anio:
                ind = j
            j += 1
        if ind == -1:
            continue

        # Acumular por trimestre
        if 1 <= mes <= 3:
            t1[ind] += venta
        elif 4 <= mes <= 6:
            t2[ind] += venta
        elif 7 <= mes <= 9:
            t3[ind] += venta
        elif 10 <= mes <= 12:
            t4[ind] += venta

    arch.close()

    # ==========================================================================
    # MATRIZ: [Año, T1, T2, T3, T4, Crec% (T1->T4)]
    # ==========================================================================
    matriz = []
    i = 0
    while i < len(lista_anios):
        anio = lista_anios[i]
        v1 = t1[i]; v2 = t2[i]; v3 = t3[i]; v4 = t4[i]
        crec = ((v4 - v1) / v1) * 100.0 if v1 != 0 else 0.0
        matriz.append([anio, v1, v2, v3, v4, crec])
        i += 1

    # ==========================================================================
    # SALIDA
    # ==========================================================================
    titulo = "Comparativa Trimestral (todas las categorías)" if eleccion == "TODAS" \
             else f"Comparativa Trimestral - Categoría: {eleccion}"
    print("\n" + titulo)
    print("-" * 100)
    print("%-8s%-18s%-18s%-18s%-18s%-18s" %
          ("Año", "Trim 1", "Trim 2", "Trim 3", "Trim 4", "Crec. T1→T4 %"))
    print("-" * 100)

    i = 0
    while i < len(matriz):
        fila = matriz[i]
        print("%-8d%-18.2f%-18.2f%-18.2f%-18.2f%-18.2f" %
              (fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]))
        i += 1

def comparativaProducto():
    """
    Comparativa de productos - usando solo contenidos vistos en la materia
    Python básico, listas, bucles, archivos CSV
    """
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo:", archivo)
        return

    primera_linea = True
    # acumulado: [producto, categoria, unidades_totales, facturacion_total]
    acumulado = []

    # Leer archivo línea por línea
    for linea in arch:
        linea = linea.strip()
        if not linea:
            continue
        if primera_linea:
            primera_linea = False
            continue

        partes = linea.split(",")  # Procesar CSV manualmente
        if len(partes) < 11:
            continue

        producto = partes[2].strip()
        categoria = partes[3].strip()

        if not producto:
            continue

        # Conversión numérica segura
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        facturacion = cantidad * precio

        # Buscar si el producto ya está en acumulado
        encontrado = -1
        i = 0
        while i < len(acumulado):
            if acumulado[i][0] == producto:
                encontrado = i
            i += 1

        if encontrado != -1:
            acumulado[encontrado][2] = acumulado[encontrado][2] + cantidad
            acumulado[encontrado][3] = acumulado[encontrado][3] + facturacion
        else:
            acumulado.append([producto, categoria, cantidad, facturacion])

    arch.close()

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

        # 1) categorías únicas (bucle while manual)
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

        # 3) armar lista de productos de esa categoría
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

        # 4) mostrar productos de esa categoría
        print(f"\nProductos de la categoría: {categoria_elegida}")
        k = 0
        while k < cantidadProductosCat:
            unidades_mostrar = productos_cat[k][2]
            if unidades_mostrar == int(unidades_mostrar):
                unidades_mostrar = int(unidades_mostrar)
            print(f"{k+1}. {productos_cat[k][0]}  (u: {unidades_mostrar}, $: {productos_cat[k][3]:.2f})")
            k = k + 1

        # 5) elegir dos productos
        opcion1 = logica.validarInput(1, cantidadProductosCat)
        opcion2 = logica.validarInput(1, cantidadProductosCat)
        while opcion1 == opcion2:
            print("⚠️ Deben ser productos distintos.")
            opcion2 = logica.validarInput(1, cantidadProductosCat)

        producto1 = productos_cat[opcion1 - 1]
        producto2 = productos_cat[opcion2 - 1]

        # Cálculos manuales
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

        # Mostrar comparativa
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
                    # intercambiar filas
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
    """
    Comparativa de clientes - lectura directa del CSV
    Opción 1: Comparar 2 clientes de una categoría
    Opción 2: Comparar todas las categorías
    """
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo:", nombre_archivo)
        return

    primera_linea = True

    # diccionario: (cliente, categoria) -> facturacion_total
    acumulado_dict = {}

    # Recorremos archivo
    for linea in arch:
        linea = linea.strip()
        if not linea:
            continue
        if primera_linea:
            primera_linea = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        cliente = partes[5].strip()
        categoria = partes[3].strip()

        # evitar filas sin cliente
        if not cliente:
            continue

        # numéricos seguros
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        total = cantidad * precio

        # clave compuesta (cliente, categoria) para el diccionario
        clave = (cliente, categoria)

        # Si la clave ya esta en el diccionario acumulado se agrega si no se crea una nueva fila
        if clave in acumulado_dict:
            acumulado_dict[clave] = acumulado_dict[clave] + total
        else:
            acumulado_dict[clave] = total

    arch.close()

    # acumulado: [cliente, categoria, facturacion_total]
    acumulado = []
    for (cliente, categoria), total in acumulado_dict.items():
        acumulado.append([cliente, categoria, total])

    cantidadClientes = len(acumulado)
    if cantidadClientes < 1:
        print("\n No hay clientes para analizar.")
        return

    # SUBMENÚ: tipo de comparativa
    print("\nElija tipo de comparativa de clientes:")
    print("1) Comparar 2 clientes de una categoría")
    print("2) Comparar TODAS las categorías")
    tipo = logica.validarInput(1, 2)

    # Hasta acá tenemos una lista (acumulado) que tiene al cliente con su categoria y el su total de ventas

    # =========================================================
    # OPCIÓN 1: comparar 2 clientes de una MISMA CATEGORÍA
    # =========================================================
    if tipo == 1:

        # 1) CATEGORÍAS ÚNICAS basadas en lo ya acumulado
        categorias_unicas = sorted(list({fila[1] for fila in acumulado}))

        # 2) MOSTRAR CATEGORÍAS
        print("\nCategorías disponibles:")
        i = 0
        while i < len(categorias_unicas):
            print(f"{i+1}. {categorias_unicas[i]}")
            i = i + 1

        opcion_cat = logica.validarInput(1, len(categorias_unicas))
        categoria_elegida = categorias_unicas[opcion_cat - 1]

        # 3) ARMAR LISTA DE CLIENTES DE ESA CATEGORÍA 
        clientes_cat = []
        i = 0
        while i < len(acumulado):
            if acumulado[i][1] == categoria_elegida:
                clientes_cat.append(acumulado[i])   # [cliente, cat, total]
            i = i + 1

        cantidadClientesCat = len(clientes_cat)
        if cantidadClientesCat < 2:
            print("\n No hay suficientes clientes en esa categoría para comparar.")
            return

        # 4) MOSTRAR CLIENTES DE ESA CATEGORÍA
        print(f"\nClientes que compraron de la categoría: {categoria_elegida}")
        k = 0
        while k < cantidadClientesCat:
            print(f"{k+1}. {clientes_cat[k][0]}  ($ {clientes_cat[k][2]:.2f})")
            k = k + 1

        # 5) elegir dos clientes
        opcion1 = logica.validarInput(1, cantidadClientesCat)
        opcion2 = logica.validarInput(1, cantidadClientesCat)

        while opcion1 == opcion2:
            print("Deben ser distintos.")
            opcion2 = logica.validarInput(1, cantidadClientesCat)

        cliente1 = clientes_cat[opcion1 - 1]
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

    # =========================================================
    # OPCIÓN 2: comparar TODAS las CATEGORÍAS
    # =========================================================
    elif tipo == 2:

        # ARMAR LISTA DE CATEGORÍAS CON TOTALES [categoria, facturacion_total]
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
            print("\n No hay categorías para comparar.")
            return

        # ORDENAR ALFABÉTICAMENTE LAS CATEGORÍAS (BURBUJA)
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

        # TOTAL GLOBAL DE FACTURACIÓN 
        total_global = 0.0
        i = 0
        while i < len(categorias):
            total_global = total_global + categorias[i][1]
            i = i + 1

        # MOSTRAR CUADRO COMPARATIVO DE CATEGORÍAS 
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

            print(f"\n La categoría con mayor facturación fue '{categoria_top}' con $ {mayor_fact:.2f}.")

def tendenciaDeCrecimiento(eleccion):
    """
    Tendencia ACUMULADA de facturación por mes (YYYY-MM).
    - eleccion = "TODAS": todas las categorías
    - eleccion = <nombre_categoria>: filtra esa categoría
    """

    # ==========================================================================
    # PRIMERA PASADA: recolectar MESES (YYYY-MM) como base
    # ==========================================================================
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo.")
        return

    primero = True
    meses_dict = {}  # "YYYY-MM" -> True

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue
        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        categoria = partes[3]

        if eleccion != "TODAS" and categoria != eleccion:
            continue

        # Normalizar a "YYYY-MM" (soporta "YYYY-MM-..." y "DD/MM/YYYY")
        clave_mes = ""
        if "-" in fecha and len(fecha) >= 7:
            clave_mes = fecha[:7]
        elif "/" in fecha:
            ped = fecha.split("/")
            if len(ped) >= 3:
                try:
                    dd = int(ped[0]); mm = int(ped[1]); aa = int(ped[2])
                    clave_mes = f"{aa:04d}-{mm:02d}"
                except:
                    pass

        if clave_mes != "" and clave_mes not in meses_dict:
            meses_dict[clave_mes] = True

    arch.close()

    meses = list(meses_dict.keys())
    if len(meses) == 0:
        print("\nNo hay datos para mostrar en la tendencia acumulada.")
        return

    # Orden cronológico (burbuja sobre "YYYY-MM")
    i = 0
    while i < len(meses) - 1:
        j = i + 1
        while j < len(meses):
            if meses[i] > meses[j]:
                aux = meses[i]; meses[i] = meses[j]; meses[j] = aux
            j += 1
        i += 1

    # ==========================================================================
    # SEGUNDA PASADA: acumular $ por MES (cantidad*precio)
    # ==========================================================================
    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudo abrir el archivo en segunda pasada.")
        return

    primero = True
    totales_por_mes = {}  # "YYYY-MM" -> total $

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue
        if primero:
            primero = False
            continue

        partes = linea.split(",")
        if len(partes) < 11:
            continue

        fecha = partes[0]
        categoria = partes[3]

        if eleccion != "TODAS" and categoria != eleccion:
            continue

        # Clave de mes
        clave_mes = ""
        if "-" in fecha and len(fecha) >= 7:
            clave_mes = fecha[:7]
        elif "/" in fecha:
            ped = fecha.split("/")
            if len(ped) >= 3:
                try:
                    dd = int(ped[0]); mm = int(ped[1]); aa = int(ped[2])
                    clave_mes = f"{aa:04d}-{mm:02d}"
                except:
                    pass

        if clave_mes == "":
            continue

        # cantidad y precio defensivos
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        venta = cantidad * precio
        if venta <= 0:
            continue

        if clave_mes in totales_por_mes:
            totales_por_mes[clave_mes] += venta
        else:
            totales_por_mes[clave_mes] = venta

    arch.close()

    # ==========================================================================
    # Construir vectores ordenados y ACUMULADO
    # ==========================================================================
    montos_mes = []
    i = 0
    while i < len(meses):
        m = meses[i]
        montos_mes.append(totales_por_mes[m] if m in totales_por_mes else 0.0)
        i += 1

    acumulado = []
    suma = 0.0
    i = 0
    while i < len(montos_mes):
        suma += montos_mes[i]
        acumulado.append(suma)
        i += 1

    # Crecimiento acumulado % vs primer mes con ventas (>0)
    idx_base = -1
    i = 0
    while i < len(acumulado):
        if acumulado[i] > 0:
            idx_base = i
            break
        i += 1

    crec_acum_pct = []
    i = 0
    while i < len(acumulado):
        if idx_base != -1 and acumulado[idx_base] > 0:
            pct = ((acumulado[i] - acumulado[idx_base]) / acumulado[idx_base]) * 100.0
        else:
            pct = 0.0
        crec_acum_pct.append(pct)
        i += 1

    # ==========================================================================
    # SALIDA
    # ==========================================================================
    titulo = "Tendencia de Crecimiento ACUMULADO (todas las categorías)" if eleccion == "TODAS" \
             else f"Tendencia de Crecimiento ACUMULADO - Categoría: {eleccion}"
    print("\n" + titulo)
    print("-" * 96)
    print("%-12s%-20s%-24s%-24s" % ("Mes", "Total Mes ($)", "Acumulado ($)", "Crec. Acum % (vs. base)"))
    print("-" * 96)

    i = 0
    while i < len(meses):
        print("%-12s%-20.2f%-24.2f%-24.2f" %
              (meses[i], montos_mes[i], acumulado[i], crec_acum_pct[i]))
        i += 1


def comparativaCanal(categoria="TODAS"):
    """
    Compara las ventas totales entre los distintos canales (Online, Tienda, Mayorista).
    Calcula facturacion y participacion porcentual.
    Separa por categoria o toma todos los datos
    """

    try:
        arch = open(nombre_archivo, "r")
    except:
        print("No se pudieron cargar los datos de ventas.")
        return

    primero = True
    facturacion_por_canal = {}  # {'Online': 12345.0, ...}

    for linea in arch:
        linea = linea.strip()
        if linea == "":
            continue

        # saltear encabezado
        if primero:
            primero = False
            continue

        partes = linea.split(",")
        # esperamos al menos 10–11 columnas
        if len(partes) < 10:
            continue

        # Extraemos categoria y canal de la venta
        cat_actual = partes[3]
        canal = partes[9]
    
        # filtro por categoría si corresponde
        if categoria != "TODAS" and cat_actual != categoria:
            continue

        # extraemos cantidad y precio 
        try:
            cantidad = float(partes[6])
        except:
            cantidad = 0.0
        try:
            precio = float(partes[7])
        except:
            precio = 0.0

        total = cantidad * precio

        # acumular por canal en el diccionario
        if canal in facturacion_por_canal:
            facturacion_por_canal[canal] = facturacion_por_canal[canal] + total
        else:
            facturacion_por_canal[canal] = total

    arch.close()

    # Total general
    total_general = 0.0
    for k in facturacion_por_canal:
        total_general = total_general + facturacion_por_canal[k]

    if total_general == 0:
        print("No se registraron ventas.")
        return

    # Ordenar por facturación DESC
    canales_items = []
    for k in facturacion_por_canal:
        canales_items.append([k, facturacion_por_canal[k]])
    canales_items.sort(key=lambda x: x[1], reverse=True)

    # Título según categoría
    if categoria == "TODAS":
        titulo = "Comparativa de ventas por canal (TODAS las categorias)"
    else:
        titulo = "Comparativa de ventas por canal (Categoria: " + str(categoria) + ")"

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
