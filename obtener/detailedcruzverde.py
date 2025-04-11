#!/usr/bin/env python3
from os import sync
from time import sleep
from unicodedata import category
from wsgiref import headers
from playwright.sync_api import sync_playwright
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import re
from http.cookies import SimpleCookie
import time



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=0)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.cruzverde.cl', timeout=0)
    time.sleep(5)
    #page.click('//*[@id="modal"]/section/div/div[4]/div/at-button/button')
    #page.click('//*[@id="modal"]/section/div/div[4]/div/at-button/button', timeout = 0)

    # page.locator('//*[@id="modal"]/section/div/div[4]/div/at-button/button').click(timeout=100000)

    session = context.cookies()
    # print(json. dumps(session))
    auth_cookie = ''
    for cookie in session:

        # print(f"{cookie['name']}={cookie['value']};")
        auth_cookie += f"{cookie['name']}={cookie['value']};"
        if cookie['name'] == "connect.sid":
            cookie_cruzverde = cookie
            sid_connect = cookie_cruzverde['value']
            print('esta es la que es ✅')
            # print(cookie_cruzverde)
        else:
            print('esta no ❌')
            # print(cookie)
            # print("no hay con ese nombre")
            pass
    browser.close()
    print(auth_cookie)

# print(session)
# open cLinks

# f = open('/home/imq/Documentos/Scraper/final/obtener/clinks.json')
f = open('clinks.json')
skus = []
links = []
data = json.load(f)
for i in data:
    links.append(i['link'])
    u = urlparse(i['link'])
    url = u.path.split('/')[-1]
    sku = [int(s) for s in re.findall(r'\d+', url)]
    # print(sku[0])
    skus.append(sku[0])
f.close()
# print(skus)

res = []
payload = {}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'cookie': auth_cookie,
    # 'cookie': '_gcl_aw=GCL.1664128076.CjwKCAjw-L-ZBhB4EiwA76YzOZYb5eY52q5iyGwQkCxLzyHNpER4QG-Zc1W08h5s3TyQdUsb8yMZzhoCYhMQAvD_BwE; _gcl_au=1.1.1889995834.1664128076; _fbp=fb.1.1664128076754.951331012; _gac_UA-149350909-1=1.1664128101.CjwKCAjw-L-ZBhB4EiwA76YzOZYb5eY52q5iyGwQkCxLzyHNpER4QG-Zc1W08h5s3TyQdUsb8yMZzhoCYhMQAvD_BwE; _hjSessionUser_1614665=eyJpZCI6ImRjYmUyMmZhLWI5MjctNTgwYi04M2QxLTZjZmVhMmVmMGMyZiIsImNyZWF0ZWQiOjE2NjQxMjgwNzcwNjMsImV4aXN0aW5nIjp0cnVlfQ==; connect.sid=s%3Acruzverde-40054cde-c460-44f2-8857-6a9bb358219d.TLhGWlWvj%2B3e2VwtqY%2FkTFE9JZ4HCdHZCn%2FZFqbRq6E; _gid=GA1.2.150825137.1665592851; _hjSession_1614665=eyJpZCI6ImM4YThmMWU3LTAxZWYtNGJhNi05N2QyLWFhNDBmMTdmZDdlNSIsImNyZWF0ZWQiOjE2NjU2ODA1MjcxNjksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga=GA1.2.1824631951.1664128076; _ga_GMKXQPNSW5=GS1.1.1665683516.8.0.1665683516.60.0.0',
    # 'cookie': f'_gcl_au=1.1.1664467762.1646156804; __cq_uuid=bcJxl6JlSaapJiFD32s3u8aNvq; _hjSessionUser_1614665=eyJpZCI6IjFjZWMwYzI0LWE0YTUtNTA1OC1hZTRhLTJkNzFlZmY0YjgxOSIsImNyZWF0ZWQiOjE2NDYxNTY4MDQzNDcsImV4aXN0aW5nIjp0cnVlfQ==; _hjMinimizedPolls=752087; _hp2_id.1146126554=%7B%22userId%22%3A%224364183278864526%22%2C%22pageviewId%22%3A%228175275121120164%22%2C%22sessionId%22%3A%222198972342885046%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_48KVT8ZDPQ=GS1.1.1647523993.7.0.1647523993.0; _fbp=fb.1.1648820883224.69637795; _gid=GA1.2.2037710669.1652284065; connect.sid={sid_connect}; _hjSession_1614665=eyJpZCI6IjFhNDM4Y2E0LWNiNDUtNDE0Ny1hNzMwLTUxYWVlMjlhYTM1ZCIsImNyZWF0ZWQiOjE2NTIzODAyNTEzODksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gat_UA-149350909-1=1; _gat=1; _ga_GMKXQPNSW5=GS1.1.1652380250.86.1.1652380363.59; _ga=GA1.1.1939167070.1646156804',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*',
}
#
for sku in skus:
    url = f"https://api.cruzverde.cl/product-service/products/detail/{sku}"
    response = requests.request("GET", url, headers=headers, data=payload)

    # print(data)
    if response.status_code == 2000:
        data = response.json()
        # print(response.text)
        print(data['productData']['prices'])
        # print(response.headers['content-type'])
        print("ok")
    if response.status_code == 200:
        data = response.json()
        p = data['productData']
        try:
            precio_oferta = p['prices']['price-sale-cl']
        except KeyError as ke:
            precio_oferta = 0
            pass
        try:
            precio_club = p['prices']['price-list-cl']
        except KeyError as ke:
            precio_club = 0
            pass
        try:
            category = p['category']
        except KeyError as ke:
            category = 'N/E'
            pass
        try:
            marca = p['brand']
        except KeyError as ke:
            marca = 'N/E'
            pass
        res.append({
            'CodFarmExt': 'C',
            'sku': p['id'],
            'FechaBusq': datetime.now().strftime('%Y-%m-%d'),
            #     # 'TipoID': 's',
            'nombre': p['name'],
            'marca': marca,
            'precio_normal': p['price'],
            'precio_oferta': precio_oferta,
            'precio_club': precio_club,
            'CodId': 'N/E',
            'link': f"https://www.cruzverde.cl/{p['name'].replace(' ','-')}/{p['id']}.html",
            # 'img': p['catalog_image_url'],
            'category': category,
        })
        print(precio_oferta)
        print(precio_club)
        # for p in data['productData']:
        #     res.append(
        # })

    else:
        # print(response.status_code)
        # print(response.text)
        pass
# with open('/home/imq/Documentos/Scraper/final/outputs/Citems.json', 'w') as outfile:
with open('../outputs/Citems.json', 'w') as outfile:
    json.dump(res, outfile)
print('listo 👍')
