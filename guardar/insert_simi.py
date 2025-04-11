import pyodbc
import pymssql
import connect as t
import json
import logging
import datetime
import requests

# Lista de archivos JSON a procesar
archivos = [
    'bioequivalentes.json',
    'dispositivos.json',
    'medicamento.json',
    'salud_femenina.json',
    'suplementos.json'
]

def envio(archivo):
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"
    payload = json.dumps({"farmacia": f"Inicio parte 3 insertar en base de datos: {archivo}"})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url_notif, headers=headers, data=payload)

def termino(archivo):
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.termino.ejecucion"
    payload = json.dumps({"farmacia": f"Termino parte 3 insertar en base de datos: {archivo}"})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    
def error(archivo):
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.error.ejecucion"
    payload = json.dumps({
        "archivo": f"insert_{archivo}.py",
        "log": f"{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

# Conexión a la base de datos
connection = t.connection 
cursor = connection.cursor() # Para acceder a los campos como diccionario usar cursor(as_dict=True)

for archivo in archivos:
    try:
        envio(archivo)
        with open(f'../outputs/{archivo}') as f:
            data = json.load(f)

        for i in data:
            cod_farm_ext = i['cod_farm_ext']
            sku = i['sku']
            fecha_busq = i['fecha_busq']
            nombre = i['nombre']
            precio_publ = i['precio_normal']
            precio_ofer = i['precio_oferta']
            precio_desc = 0
            cod_barr = "None"
            link = i['link']
            marca = i.get('marca', None)
            img_url = i.get('img', None)
            categoria = i.get('category', "None")

            cursor.callproc('[prm].[usp_insertar_recoleccion_data_ari]', (
                cod_farm_ext,
                sku,
                fecha_busq,
                nombre,
                precio_publ,
                precio_ofer,
                precio_desc,
                cod_barr,
                marca,
                link,
                img_url,
                categoria
            ))
            print("done", cod_farm_ext, sku, fecha_busq)
        
        connection.commit()
        print(f'{archivo} procesado exitosamente')

    except Exception as e:
        print(f'Error mientras se insertaban datos de {archivo} en la base de datos')
        print(str(e))
        error(archivo)
    
    finally:
        termino(archivo)
