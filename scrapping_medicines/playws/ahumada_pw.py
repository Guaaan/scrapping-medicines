#!/usr/bin/env python3
from os import sync
from unicodedata import category
from wsgiref import headers
from playwright.sync_api import sync_playwright
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import re

with sync_playwright() as p:
    name = 'cruz_verde'
    browser = p.chromium.launch(headless=True, slow_mo=0)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.farmaciasahumada.cl/medicamentos')
     # Hacer clic en el body
    page.click('body')
    session = context.cookies()
    for cookie in session:
        if cookie['name'] == "connect.sid":
            cookie_cruzverde = cookie
            print(cookie_cruzverde)
            sid_connect = cookie_cruzverde['value']
        else:
            pass
    browser.close()

# print(session)
# open cLinks

f = open('clinks.json')
# f = open('/home/imq/Documentos/Scraper/final/obtener/clinks.json')
products_data = []
links=[]
data = json.load(f)
for i in data:
    products_data.append({"sku": i['sku'], 
                      "cod_barra": i['cod_barra']})
    # u = urlparse(i['sku'])
    # url = u.path.split('/')[-1]
    # sku = [int(s) for s in re.findall(r'\d+', url)]
    #print(sku[0])
    # products_data.append(sku[0])
f.close()

res = []
payload = {}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'cookie': f'_gcl_au=1.1.1664467762.1646156804; __cqx_uuid=bcJxl6JlSaapJiFD32s3u8aNvq; _hjSessionUser_1614665=eyJpZCI6IjFjZWMwYzI0LWE0YTUtNTA1OC1hZTRhLTJkNzFlZmY0YjgxOSIsImNyZWF0ZWQiOjE2NDYxNTY4MDQzNDcsImV4aXN0aW5nIjp0cnVlfQ==; _hjMinimizedPolls=752087; _hp2_id.1146126554=%7B%22userId%22%3A%224364183278864526%22%2C%22pageviewId%22%3A%228175275121120164%22%2C%22sessionId%22%3A%222198972342885046%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_48KVT8ZDPQ=GS1.1.1647523993.7.0.1647523993.0; _fbp=fb.1.1648820883224.69637795; _gid=GA1.2.2037710669.1652284065; connect.sid={sid_connect}; _hjSession_1614665=eyJpZCI6IjFhNDM4Y2E0LWNiNDUtNDE0Ny1hNzMwLTUxYWVlMjlhYTM1ZCIsImNyZWF0ZWQiOjE2NTIzODAyNTEzODksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gat_UA-149350909-1=1; _gat=1; _ga_GMKXQPNSW5=GS1.1.1652380250.86.1.1652380363.59; _ga=GA1.1.1939167070.1646156804',
    #'Accept-Encoding': 'gzip, deflate, br',
    #'Accept': '*/*',
}
        #
for prod in products_data:
    url = f"https://api.cruzverde.cl/product-service/products/detail/{prod['sku']}"
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    # print(data)
    bar_code = prod['cod_barra']
    if response.status_code == 200:
        p = data['productData']
        try:
            precio_oferta = p['prices']['price-sale-cl']
        except KeyError as ke:
            precio_oferta = 0
            pass
        try:
            precio_club = p['prices']['price-club-cl']
        except KeyError as ke:
            precio_club = 0
            pass
        try:
            category = p['category']
        except KeyError as ke:
            category = 'N/E'
            pass
        try:
            price = p['price']
        except KeyError as ke:
            price = 'N/E'
            pass
        try:
            marca = p['brand']
        except KeyError as ke:
            marca = 'N/E'
            pass
        try:
            res.append({
                'cod_farm_ext': 'C',
                'sku': p['id'],
                'fecha_busq': datetime.now().strftime('%Y-%m-%d'),
                #     # 'TipoID': 's',
                'nombre': p['name'],
                'marca': marca,
                'precio_normal': price,
                'precio_list': p['prices'],
                'precio_oferta': precio_oferta,
                'precio_club': precio_club,
                'cod_id': bar_code,
                'link': f"https://www.cruzverde.cl/{p['name'].replace(' ','-')}/{p['id']}.html",
                #'img': p['catalog_image_url'],
                'category': category,
            })
        except Exception as error:
            print(error)
        # print(response.json()) 
        print(price)
        
        # for p in data['productData']:
        #     res.append(
        # })
    else:
        print(response.status_code)
        pass
with open('../outputs/Citems.json', 'w') as outfile:
# with open('/home/imq/Documentos/Scraper/final/outputs/Citems.json', 'w') as outfile:
    json.dump(res, outfile)
print('listo 👍')
