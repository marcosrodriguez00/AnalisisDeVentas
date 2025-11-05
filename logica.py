import os
import sys
import funcionalidades

# -- Helpers main.py -- #

# printea un error en consola #
def error():
    print("ERROR: La opcion no es valida.")
    
# pide un input y verifica que sea valido para el menu principal #
def validarInput(min=0, max=8):
    opcion = -1

    while opcion < min or opcion > max:
        if (min == 0 and max == 0):
            opcion = int(input())
        else: 
            try:
                opcion = int(input(f"Elija una opción ({min}-{max}): "))
                if opcion < min or opcion > max:
                    print(f"⚠️ La opción debe estar entre {min} y {max}.")
            except ValueError:
                print("⚠️ Debe ingresar un número entero.")
                opcion = -1  # fuerza a repetir el ciclo

    return opcion

# -- Helpers funcionalidades.py -- #

# Devuelve el indice del cliente en la lista de acumulados #
def indiceEnLista(acumulados, cliente):
    # Crear una lista con solo los nombres de cliente
    nombres = [fila[0] for fila in acumulados]

    # Revisar si el cliente está en esa lista
    if cliente in nombres:
        return nombres.index(cliente)  # devuelve la posición
    else:
        return -1  # no está

# Función que formatea el més de formato "YYYY-MM" a "NombreMes YYYY"
#    "2024-07" -> "Julio 2024"
def formatear_mes(clave_ym):
    anio = clave_ym[0:4]   # "2024"
    mes_num = clave_ym[5:7] # "07"
    nombres_mes = {
        "01": "Enero",
        "02": "Febrero",
        "03": "Marzo",
        "04": "Abril",
        "05": "Mayo",
        "06": "Junio",
        "07": "Julio",
        "08": "Agosto",
        "09": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre"
    }
    nombre = nombres_mes.get(mes_num, mes_num)
    return f"{nombre} {anio}"

def obtenerCategoriasUnicas():
    """
    Lee el archivo CSV de ventas y devuelve una lista
    con las categorías únicas encontradas.
    """

    categorias_unicas = []

    try:
        arch = open("ventas_dataset_sin_tildes.csv", mode="r")

        primera_linea = True

        for linea in arch:
            linea = linea.strip()
            if linea == "":
                continue

            # saltamos encabezado
            if primera_linea:
                primera_linea = False
                continue

            partes = linea.split(",")

            # evitamos filas incompletas
            if len(partes) < 11:
                continue

            categoria = partes[3].strip()

            # agregamos si no está ya en la lista
            if categoria != "" and categoria not in categorias_unicas:
                categorias_unicas.append(categoria)

        arch.close()

    except FileNotFoundError:
        print("No se encontró el archivo.")
        return []
    except OSError:
        print("No se pudo leer el archivo.")
        return []

    return categorias_unicas

def categoria(dato):
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
    )= cargarDatosCSV()
    
    lista_producto_c = []
    lista_cliente_c = []
    lista_cantidad_c = []
    lista_precio_c = []
    lista_region_c = []
    lista_canal_c = []
    lista_factura_c = []
    
    for i in range(len(lista_producto)):
        if dato == lista_categoria[i]:
            lista_fecha_c.append(lista_fecha[i])
            lista_producto_c.append(lista_producto[i])
            lista_cliente_c.append(lista_cliente[i])
            lista_cantidad_c.append(lista_cantidad[i])
            lista_precio_c.append(lista_precio[i])
            lista_region_c.append(lista_region[i])
            lista_canal_c.append(lista_canal[i])
            lista_factura_c.append(lista_facturacion[i])
    return (
        lista_fecha_c,
        lista_producto_c,
        lista_cliente_c,
        lista_cantidad_c,
        lista_precio_c,
        lista_region_c,
        lista_canal_c,
        lista_factura_c,
        )

def informeCategorias(dato):
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
    )= funcionalidades.cargarDatosCSV()
    
    lista_fecha_c = []
    lista_producto_c = []
    lista_cliente_c = []
    lista_cantidad_c = []
    lista_precio_c = []
    lista_region_c = []
    lista_canal_c = []
    lista_factura_c = []
    
    for i in range(len(lista_producto)):
        if dato == lista_categoria[i]:
            lista_fecha_c.append(lista_fecha[i])
            lista_producto_c.append(lista_producto[i])
            lista_cliente_c.append(lista_cliente[i])
            lista_cantidad_c.append(lista_cantidad[i])
            lista_precio_c.append(lista_precio[i])
            lista_region_c.append(lista_region[i])
            lista_canal_c.append(lista_canal[i])
            lista_factura_c.append(lista_factura[i])
    return (
        lista_fecha_c,
        lista_producto_c,
        lista_cliente_c,
        lista_cantidad_c,
        lista_precio_c,
        lista_region_c,
        lista_canal_c,
        lista_factura_c,
        )       

# --- Helpers de categoria (manuales) ---

def _leerCategoriasParalela():
    """
    Devuelve la lista de 'Categoria' alineada al CSV.
    """
    lista_categoria = []
    try:
        arch = open("ventas_dataset_sin_tildes.csv", mode="r")
        primera_linea = True
        for linea in arch:
            linea = linea.strip()
            if linea == "":
                continue
            if primera_linea:
                primera_linea = False
                continue
            partes = linea.split(",")
            if len(partes) < 11:
                continue
            categoria = partes[3]
            lista_categoria.append(categoria)
        arch.close()
    except FileNotFoundError:
        return []
    except OSError:
        return []
    return lista_categoria


def filtrarPorCategoria(nombre):
    """
    Devuelve EXACTAMENTE las 10 listas de cargarDatosCSV(),
    pero filtradas por 'nombre' de categoría. Si nombre == 'TODAS',
    devuelve el dataset completo sin filtrar.
    """
    datos = funcionalidades.cargarDatosCSV()
    if datos is None:
        return None

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

    # Si piden TODAS, devolvemos el formato sin categoria
    if nombre == "TODAS":
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

    # Filtrar por categoria específica y devolver las mismas 10 listas
    lf, lidp, lp, lidc, lc, lq, lpr, lr, lca, lfac = [], [], [], [], [], [], [], [], [], []

    i = 0
    n = len(lista_producto)
    while i < n:
        if lista_categoria[i] == nombre:
            lf.append(lista_fecha[i])
            lidp.append(lista_id_producto[i])
            lp.append(lista_producto[i])
            lidc.append(lista_id_cliente[i])
            lc.append(lista_cliente[i])
            try:
                lq.append(int(lista_cantidad[i]))
            except:
                lq.append(0)
            try:
                lpr.append(float(lista_precio[i]))
            except:
                lpr.append(0.0)
            lr.append(lista_region[i])
            lca.append(lista_canal[i])
            lfac.append(lista_factura[i])
        i += 1

    return (lf, lidp, lp, lidc, lc, lq, lpr, lr, lca, lfac)