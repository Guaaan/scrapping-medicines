from concurrent.futures import process
from datetime import datetime
from os import link
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import requests
from bs4 import BeautifulSoup


archivo = 'Articulos Ahumada'


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
    


links = []
f = open('aLinks.json')
data = json.load(f)
for i in data:
    links.append(i['link'])
f.close()
class DetailedahumadaSpider(scrapy.Spider):
    
    
    name = 'detailedahumada'
    allowed_domains = ['farmaciasahumada.cl']
    start_urls = links
    if start_urls is not []:
        def parse(self, response):
            for product in response.css('div.column.main'): #('div.product-info-main')
                bc_url = response.url
                req = requests.get(bc_url)
                soup = BeautifulSoup(req.text, 'html.parser')
                #este indice puede variar dependiendo de si el tag script donde se encuentra el codigo de barra ha sido movido por procesos internos de la página de ahumada
                script = soup.find_all('script')[12].text
                barcode = json.loads(script)
                yield {
                    'CodFarmExt': "A",
                    'codId': barcode['gtin13'],
                    'FechaBusq': datetime.now(),
                    'tipoID': 'c',
                    'nombre': product.css('span.base::text').get().replace("'", ""),
                    'precio_oferta': int(product.css('span.price::text').getall()[0].replace('.', '').replace('$', '').replace(' ', '')),
                    'precio_normal': int(product.css('span.price::text').getall()[-1].replace('.', '').replace('$', '').replace(' ', '')),
                    'sku': product.css('div.value::text').get(),
                    'marca': product.css('h3.product-brand::text').get().strip().replace("'", ""),
                    'link': response.url,
                    'img':  product.css('img.gallery-placeholder__image').attrib['src'],
                    'category': 'null'
                }
            
process = CrawlerProcess(settings = {
    'FEED_URI': '../outputs/Aitems.json',
    'FEED_FORMAT': 'json',
})

with open('../outputs/Aitems.json', 'w') as f:
    f.write('')
try:
    process.crawl(DetailedahumadaSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían articulos de Ahumada')
    f = open(f"../logs/{datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()  
    error()
    