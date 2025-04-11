from concurrent.futures import process
from datetime import datetime
from os import link
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import requests

links = []
counts = {}
f = open('similinks.json', 'r')
data = json.load(f)
# Itera sobre los elementos del archivo JSON y actualiza los recuentos
for item in data:
    item_key = tuple(item.items())
    if item_key in counts:
        counts[item_key] += 1
    else:
        counts[item_key] = 1
unique_data = [dict(item) for item in counts.keys()]
f.close()
with open(f'similinks.json', 'w') as f:
    json.dump(unique_data, f)
f.close()
f = open('similinks.json', 'r')
for i in data:
    # si el i['link'] esta en links no lo añado
    if i['link'] not in links:
        links.append(i['link'])
f.close()


class DetailedsimiSpider(scrapy.Spider):

    name = 'detailedsimi'
    allowed_domains = ['drsimi.cl']
    start_urls = links
    if start_urls is not []:
        def parse(self, response):
            for product in response.css('section.vtex-store-components-3-x-container.ph3.ph5-m.ph2-xl.mw9.center'):
                name = product.css(
                    'span.vtex-store-components-3-x-productBrand.vtex-store-components-3-x-productBrand--quickview::text').get()
                prec_arr = response.css(
                    'span.vtex-product-price-1-x-currencyInteger::text').getall()
               # Se determina la cantidad de elementos en la sublista actual
                cantidad_strings = len(prec_arr)

                # Se inicializan los precios normal y de descuento
                precio_normal = 0
                precio_descuento = 0

                # Se define un diccionario de funciones para determinar los precios
                # El diccionario utiliza la cantidad de elementos en la sublista como clave
                switcher = {
                    None: (0,0),  # Si no hay elementos, se devuelven 0 para ambos precios
                    4: lambda: (int(prec_arr[0] + prec_arr[1]), int(prec_arr[2] + prec_arr[3])),  # Si hay 4 elementos, se concatenan pares para formar los precios
                    3: lambda: (int(prec_arr[0]) if len(prec_arr[0]) == 3 else int(prec_arr[0] + prec_arr[1]), int(prec_arr[1] + prec_arr[2])),  # Si hay 3 elementos, se concatenan pares si es necesario y se asignan a los precios
                    2: lambda: (int(prec_arr[0]) if len(prec_arr[0]) == 3 else int(prec_arr[0]), int(prec_arr[1]) if len(prec_arr[1]) > 0 else 0),  # Si hay 2 elementos, se concatenan si es necesario y se asignan a los precios
                    1: lambda: (int(prec_arr[0]), 0),  # Si hay 1 elemento, se asigna al precio normal y el descuento es 0
                }
                precio_normal, precio_descuento = switcher.get(cantidad_strings, lambda: (0, 0))()

                if name is not None:
                    yield {
                        'nombre': name,
                        'link': response.url,
                        # int(''.join(response.css('span.vtex-product-price-1-x-currencyInteger::text').getall())),
                        'precio_normal': precio_normal,
                        "precio_oferta": precio_descuento,
                        "CodFarmExt": "D",
                        "sku": response.css('span.vtex-product-identifier-0-x-product-identifier__value::text').get(),
                        "tipoID": "s",
                        'FechaBusq': datetime.now().date(),
                        "codId": "N/E",
                        "marca": "N/E",
                        # TODO: hacer precio oferta de drsimi pero solo puede ser los lunes
                        "precio_club": 0,
                        "img": response.css('img.vtex-store-components-3-x-productImageTag.vtex-store-components-3-x-productImageTag--main').attrib['src'],
                        "category": response.css('a.vtex-breadcrumb-1-x-link.vtex-breadcrumb-1-x-link--3.dib.pv1.link.ph2.c-muted-2.hover-c-link::text').get(),
                    }


process = CrawlerProcess(settings={
    'FEED_URI': '../outputs/simi_items.json',
    'FEED_FORMAT': 'json',
})

with open('../outputs/simi_items.json', 'w') as f:
    f.write('')
try:
    process.crawl(DetailedsimiSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de dr Simi')
    f = open(f"../logs/{datetime.datetime.now()}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()
