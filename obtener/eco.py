import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from datetime import datetime
import json

archivo = 'links eco'

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
#envio()

class EcoSpider(scrapy.Spider):
    name = 'eco'
    allowed_domains = ['ecofarmacias.cl']
    start_urls = ['https://www.ecofarmacias.cl/categoria-producto/medicamentos/', 
    'https://www.ecofarmacias.cl/categoria-producto/suplementos-alimenticios/', 
    'https://www.ecofarmacias.cl/categoria-producto/cuidado-personal/',
    'https://www.ecofarmacias.cl/categoria-producto/veterinaria/',
    'https://www.ecofarmacias.cl/categoria-producto/marcas-destacadas/',
    'https://www.ecofarmacias.cl/categoria-producto/covid-19/']

    # def start_requests(self):
    #         yield scrapy.Request('https://www.ecofarmacias.cl/categoria-producto/medicamentos/')

    def parse(self, response):
        for product in response.css('li.product'):
            yield {
                'link': product.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href'],
                # 'name': product.css('h2.woocommerce-loop-product__title').get(),
            }
        
        next_page = response.css('a.next.page-numbers').attrib['href']
        # print('next page: ', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess(settings = {
    'FEED_URI': 'eLinks.json',
    'FEED_FORMAT': 'json',
})

with open('eLinks.json', 'w') as f:
    f.write('')
try:
    process.crawl(EcoSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de Eco')
    f = open(f"../logs/{datetime.datetime.now()}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()