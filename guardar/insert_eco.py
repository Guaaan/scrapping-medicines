import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests

archivo = 'insertar.eco'


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
f = open('../outputs/Eitems.json')
data = json.load(f)
connection = t.connection
cursor = connection.cursor()  # to access field as dictionary use cursor(as_dict=True)
try:
    for i in data:
        item = f"'{i['cod_farm_ext']}', '{i['sku']}', '{i['fecha_busq']}'"
        # cursor.execute(f"""
        #     INSERT INTO [prm_e_recolector]
        #     (CodEmpr,
        #     CodFarmExt,
        #     FechaBusq,
        #     SkuExt,
        #     DescripcionExt,
        #     PrecioPubl,
        #     PrecioOfer,
        #     CodBarr,
        #     Link,
        #     Marca,
        #     ImgUrl)
        #     VALUES ('ARI','{i['CodFarmExt']}','{i['FechaBusq']}', '{i['sku']}', '{i['nombre']}', '{i['precio_oferta']}', '{i['precio_normal']}', '{i['codId']}', '{i['link']}', '{i['marca']}', '{i['img']}')
        # """)
        CodFarmExt = i['cod_farm_ext']
        sku = i.get('sku', 'N/E')

        FechaBusq = i['fecha_busq']
        SkuExt = i['sku']
        Nombre = i['nombre']
        PrecioPubl = i['precio_normal']

        PrecioOfer = i.get('precio_oferta')
        CodBarr = i.get('codId', None)
        Link = i['link']
        Marca = i.get('marca',None)
        ImgUrl = i.get('img', "")

        cursor.callproc('[prm].[usp_insertar_recoleccion_data_ari]', (
        CodFarmExt,
        sku,
        FechaBusq,
        # "2024-04-01",
        Nombre,
        PrecioPubl,
        PrecioOfer,
        CodBarr,
        Link,
        Marca,
        ImgUrl,
        ImgUrl,
        None
        ))
        

        PrecioOfer = i['precio_oferta']
        # CodBarr = i['codId']
        cod_barr = i.get('cod_id', None)
        Link = i['link']
        Marca = i['marca']
        ImgUrl = i['img']
        category = "null"

        cursor.callproc('usp_insertar_recoleccion_data_ari', (CodFarmExt, sku,
                        FechaBusq, Nombre, PrecioPubl, PrecioOfer, cod_barr, Link, Marca, ImgUrl, category))


    f.close()
    print('done')
    connection.commit()
except Exception as e:
    print('Error mientras se insertaban datos de ecofarmacias en la base de datos')
    print(e.args)
    print(item)
    f = open(
        f"../../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    # f.write(str(Argument))
    # f.write(item)
    # closing the file
    f.close()
    error()
finally:
    termino()
