import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests


archivo = 'insertar.farmex'


def envio():
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"

    payload = json.dumps({
        "farmacia": f"Inicio parte 3 insertar en base de datos: {archivo} "
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url_notif, headers=headers, data=payload)


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
f = open('../outputs/Fitems.json')
data = json.load(f)
connection = t.connection
cursor = connection.cursor()  # to access field as dictionary use cursor(as_dict=True)
try:
    for i in data:
        item = f"'{i['CodFarmExt']}', '{i['sku']}', '{i['FechaBusq']}'"
        # for j in data:
        #     precio_convenio = j['ofertas_convenios']
        #     if precio_convenio != [] and precio_convenio != [{'null': None}]:
        #         print(f'{precio_convenio}')
        #         #retorna el primer valor de precio convenio
        #         precio_convenio = precio_convenio[0]['Precio']
        CodFarmExt = i['CodFarmExt']
        sku = i['sku']
        FechaBusq = i['FechaBusq']
        SkuExt = i['sku']
        Nombre = i['nombre']
        PrecioPubl = i['precio_normal']
        PrecioOfer = i['precio_oferta']
        PrecioDesc = i['precio_club ']
        CodBarr = i['codId']
        Link = i['link']
        Marca = i['marca']
        ImgUrl = i['img']

        cursor.callproc('usp_insertar_recoleccion_data_ari', (CodFarmExt, sku,
                        FechaBusq, Nombre, PrecioPubl, PrecioOfer, PrecioDesc, CodBarr, Marca, Link, ImgUrl))

    f.close()
    print('done')
    connection.commit()
except Exception as Argument:
    print('Error mientras se insertaban datos de farmex en la base de datos')
    print(str(Argument))
    print(item)
    f = open(
        f"../../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    f.write(item)
    # closing the file
    f.close()
    error()
finally:
    termino()
