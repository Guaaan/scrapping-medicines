from gc import callbacks
from urllib.parse import urlparse
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import logging
from datetime import datetime
import json

archivo = 'links ahumada'

def envio():
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"

    payload = json.dumps({
    "farmacia": f"Parte 1 recolectando: {archivo}"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_notif, headers=headers, data=payload)

def termino():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.termino.ejecucion"

    payload = json.dumps({
    "farmacia": f"Parte 1 recolectando: {archivo}"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
def error():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.error.ejecucion"

    payload = json.dumps({
    "archivo": f"{archivo}.py",
    "log": f"{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
# envio()
class AhumadaSpider(scrapy.Spider):
    name = 'ahumada'
    allowed_domains = ['farmaciasahumada.cl']
    start_urls = ['https://www.farmaciasahumada.cl/medicamentos.html', 'https://www.farmaciasahumada.cl/bebidas-y-alimentos.html',
     'https://www.farmaciasahumada.cl/dispositivos-medicos.html', 'https://www.farmaciasahumada.cl/cronicos.html',
     'https://www.farmaciasahumada.cl/infantil-y-maternidad/lactancia-y-alimentacion.html', 'https://www.farmaciasahumada.cl/nutricion-deportiva.html', 
     'https://www.farmaciasahumada.cl/nutricion-deportiva.html', 'https://www.farmaciasahumada.cl/cuidado-personal.html',
     'https://www.farmaciasahumada.cl/belleza.html', 'https://www.farmaciasahumada.cl/dermocosmetica.html']

    # def start_requests(self):
    #     yield scrapy.Request('https://www.farmaciasahumada.cl/medicamentos.html')

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            u = urlparse(response.url)
            category = u.path.split('/')[-1]
            yield {
                'link': products.css('a.product-item-link').attrib['href'],
                'name': products.css('a.product-item-link::text').get().strip(),
                # 'category': category.replace('.html', '')
                # 'price': products.css('span.price-wrapper').attrib['data-price-amount'],
                # 'lab': products.css('p.product-brand-name.truncate::text').get(),
            }

        # x = 1
        # for i in range(1, 100):
        #     yield (scrapy.Request(f'https://www.farmaciasahumada.cl/medicamentos.html?p={x}', callback=self.parse))
        #     x = x + 1

        next_page = response.css('a.action.next').attrib['href']
        print('next page: ', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess(settings = {
    'FEED_URI': 'aLinks.json',
    'FEED_FORMAT': 'json',
})

with open('aLinks.json', 'w') as f:
    f.write('')
try:
    process.crawl(AhumadaSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de Ahumada')
    f = open(f"../logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()   
#     error()

# finally:
#     termino()