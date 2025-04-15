import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests

archivo = 'insertar.ahumada'

def envio():
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"

    payload = json.dumps({
    "farmacia": f"Inicio parte 3 insertar en base de datos: {archivo} "
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_notif, headers=headers, data=payload)

def termino():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.termino.ejecucion"

    payload = json.dumps({
    "farmacia": f"Termino parte 3 insertar en base de datos: {archivo}"
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
f = open('../outputs/Aitems.json')
data = json.load(f)
connection = t.connection 
cursor = connection.cursor() # to access field as dictionary use cursor(as_dict=True)
try:
    for i in data:
        item = i
        cod_farm_ext = i['cod_farm_ext']
        sku = i.get('sku', 'N/E')
        fecha_busq = i['fecha_busq']
        sku_ext = i.get('sku', 'N/E')
        nombre = i['nombre']
        precio_publ = i['precio_normal']
        precio_ofer = i.get('precio_oferta', 0)
        precio_club= 0
        cod_barr = i.get('cod_id', None)
        link = i['link']
        marca = i.get('marca', None)
        img_url = "null"
        category = "null"

        cursor.callproc('[prm].[usp_insertar_recoleccion_data_ari]', (
        cod_farm_ext,
        sku,
        fecha_busq,
        nombre,
        precio_publ,
        precio_ofer,
        precio_club,
        cod_barr,
        marca,
        link,
        img_url,
        category
        ))
    f.close()
    print('done')
    connection.commit()
except Exception as Argument:
    print('Error mientras se insertaban datos de Ahumada en la base de datos')
    print(Argument)
    
    print(item)
    # f = open(f"../../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # # writing in the file
    # f.write(str(Argument))
    # f.write(item)
    # # closing the file
    # f.close()   
    error()
finally:
    termino()




