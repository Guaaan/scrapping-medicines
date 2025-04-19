#!/usr/bin/env python3
from os import sync
from unicodedata import category
from wsgiref import headers
from playwright.sync_api import sync_playwright, Playwright
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import time
import re


resultados = []
categories = ['/si?map=specificationFilter_20', '/suplementos-y-alimentos',
              '/138?map=productClusterIds', '/dispositivos','/pronutrition?map=specificationFilter_41','/dr-simi?map=specificationFilter_41','/colageno?map=specificationFilter_41','/medicamento/salud-femenina','/cosmeticos/eternal-secret',]


def guardar_resultados_en_json(resultados, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(resultados, archivo, indent=4)


def run(playwright: Playwright, categ_string):

    def handle_response(response):
        # the endpoint we are insterested in
        try:
            if ("v1?workspace=master" in response.url):
                #     print(response.json()['data']['productSearch']['products'])
                productos = response.json(
                )['data']['productSearch']['products']
                if (productos):
                    for item in productos:
                        # print(item)
                        producto = {
                            "link": f"https://www.drsimi.cl{item['link']}",
                            "cod_farm_ext": "D",
                            "cod_id": item['productId'],
                            "fecha_busq": datetime.now().strftime('%Y-%m-%d'),
                            "tipo_id": "sku",
                            "nombre": item['productName'],
                            "precio_oferta": item['priceRange']['sellingPrice']['lowPrice'],
                            "precio_normal": item['priceRange']['sellingPrice']['highPrice'],
                            # "all_prices": item.
                            "sku": item['cacheId'],
                            "marca": item['brand']
                        }
                        # "img": item.
                        # "category": item.
                        print(producto)
                        resultados.append(producto)
        except Exception as e:
            # print(e)
            pass

        # ...
    browser = p.chromium.launch(headless=True, slow_mo=1)
    context = browser.new_context()
    page = context.new_page()
#     page.on("request", lambda request: print(
#         ">>", request.method, request.url))
#     page.on("response", lambda response: print(
#         "<<", response.status, response.url))
    page.on("response", handle_response)
    page.goto(f"https://www.drsimi.cl{categ_string}")

    # Hacer clic en el body
#     page.click('body')
    page.wait_for_load_state("networkidle")
    page.wait_for_selector('//*[@id="gallery-layout-container"]')
    try:
        page.get_by_text("Mostrar más").click()
        for x in range(50):
            page.on("response", handle_response)
            page.get_by_text("Mostrar más").click()
            time.sleep(1)
    except Exception as e:
        page.on("response", handle_response)
        
        pass
    #     browser.close()
    # Esperar al elemento específico //*[@id="modal"]/section/div/div[4]/div/at-button/button

    browser.close()
    time.sleep(5)
    


with sync_playwright() as p:
    for categ in categories:
        run(p, categ)

    guardar_resultados_en_json(resultados, 'resultado.json')
