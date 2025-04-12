from concurrent.futures import process
from unicodedata import category
import scrapy
import json
from scrapy.crawler import CrawlerProcess
import requests
from datetime import datetime

archivo = 'items eco'


def error():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.error.ejecucion"

    payload = json.dumps({
    "archivo": f"{archivo}.py",
    "log": f"{datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)



f = open('elinks.json')
links = []
data = json.load(f)
for i in data:
    links.append(i['link'])
f.close()

class EcoDetSpider(scrapy.Spider):
    name = 'eco_det'
    allowed_domains = ['ecofarmacias.cl']
    start_urls = links

    def parse(self, response):
        for product in response.css('div#left-area'):
            category = response.xpath('//*[@id="left-area"]/nav/a[3]/text()').get().replace('\u00e1', 'a').replace('\u00c1','a').replace('\u00f3','o').replace('\u00ed','i')
            tag_codigo = product.css('span.sku::text').get()
            codigo = 0
            if tag_codigo is not None:
                codigo = product.css('span.sku::text').get()
            elif tag_codigo is None:
                codigo = 'N/E' + str(i + 1)
            yield {
                'CodFarmExt': "E",
                'codId': codigo,
                'FechaBusq': datetime.now(),
                'nombre': product.css('h1.product_title.entry-title::text').get(),
                'precio_normal': product.css('bdi::text').get(),
                'precio_oferta': 0,
                'precio_club ': 0,
                'sku': product.css('button.single_add_to_cart_button.button.alt').attrib['value'],
                'marca': 'N/E',
                'link': response.url,
                'img': product.css('img.wp-post-image').attrib['src'],
                'category': category,
            } 

process = CrawlerProcess({
    'FEED_URI': '../outputs/Eitems.json',
    'FEED_FORMAT': 'json',
})

with open('../outputs/Eitems.json', 'w') as f:
    f.write('')

try:
    process.crawl(EcoDetSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían articulos de Ecofarmacias')
    f = open(f"../logs/{datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()  
    error()
    