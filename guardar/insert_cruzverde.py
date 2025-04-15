#!/usr/bin/env python3
#esta primera linea sin comentario hace que se pueda ejecutar directamente ne ssh
from os import link
import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests

archivo = 'insertar.Cruz Verde'

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
f = open('../outputs/Citems.json')
data = json.load(f)
connection = t.connection 
cursor = connection.cursor() # to access field as dictionary use cursor(as_dict=True)
try:
    for i in data: 
        cod_farm_ext = i['cod_farm_ext']
        sku = i['sku']
        fecha_busq = i['fecha_busq']
        nombre = i['nombre']
        precio_normal = i['precio_normal']
        precio_oferta = i['precio_oferta']
        precio_club = i['precio_club']
        cod_id = i['cod_id']
        marca = i['marca']
        link = i['link']
        img = "none"
        category = i['category']

        cursor.callproc('[prm].[usp_insertar_recoleccion_data_ari]', (
        cod_farm_ext,
        sku,
        fecha_busq,
        nombre,
        precio_normal,
        precio_oferta,
        precio_club,
        cod_id,
        marca,
        link,
        img,
        category))
    f.close()
    print('done')
    connection.commit()
except Exception as Argument:
    print('Error mientras se insertaban datos de cruz verde en la base de datos')
    print(Argument)
    # f = open(f"../../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # # writing in the file
    # f.write(str(Argument))
    # # closing the file
    # f.close() 
    error()
finally:
    termino()


    