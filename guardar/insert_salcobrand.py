from tkinter import E
import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests

archivo = 'insertar.salcobrand'

def envio():
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"

    payload = json.dumps({
    "farmacia": f"Inicio parte 2 insertar en base de datos: {archivo} "
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_notif, headers=headers, data=payload)

def termino():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.termino.ejecucion"

    payload = json.dumps({
    "farmacia": f"Termino parte 2 insertar en base de datos: {archivo}"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
def error():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.error.ejecucion"

    payload = json.dumps({
    "archivo": f"insert_{archivo}.py",
    "log": f"{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

envio()
prod = []
f = open('../outputs/Sitems.json')
data = json.load(f)
cantidad = len(data)

connection = t.connection 
cursor = connection.cursor() # to access field as dictionary use cursor(as_dict=True)
registros_insertados = 0  # Variable para contar la cantidad de registros insertados

try:
    for i in data:

    # cursor.execute(f"""
        # INSERT INTO prm_e_recolector (CodEmpr, CodFarmExt, SkuExt, FechaBusq, DescripcionExt, PrecioPubl, PrecioOfer, PrecioDesc, Link, Marca) 
        # VALUES ('ARI', '{i['CodFarmExt']}', '{i['sku']}', '{i['FechaBusq']}', '{i['nombre']}', '{i['precio_normal']}', '{i['precio_oferta']}', '{i['precio_club']}', '{i['link']}', '{i['marca']}')
        # """)
        cod_farm_ext = i['cod_farm_ext']
        sku = i['sku']
        if sku is None:
            sku = "N/E" + str(i)
        fecha_busq = i['fecha_busq']
        nombre = i['nombre']
        precio_normal = i['precio_normal']
        precio_oferta = i['precio_oferta']
        precio_club = i['precio_club']
        cod_barr = i['internal_id']
        link = i['link']
        marca = i['marca']
        img = i['img']
        categoria = i['category']


        cursor.callproc('[prm].[usp_insertar_recoleccion_data_ari]', (
                cod_farm_ext,
                sku,
                fecha_busq,
                nombre,
                precio_normal,
                precio_oferta,
                precio_club,
                cod_barr,
                marca,
                link,
                img,
                categoria
            ))
        registros_insertados += 1  # Incrementa el contador de registros insertados

    f.close()
    print('Done. Se insertaron ' + str(registros_insertados) + ' registros de ' + str(cantidad))
    registros_insertados = 0  # Variable para contar la cantidad de registros insertados
    connection.commit()
except Exception as Argument:
    print('Error mientras se insertaban datos de salcobrand a la base de datos')
    print(str(Argument))
    f = open(f"../../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()
    error()

finally:
    termino()



# cursor.execute("SELECT * FROM products")
# row = cursor.fetchall()
# print(row)

######## INSERT DATA IN TABLE ########
# commit your work to database
