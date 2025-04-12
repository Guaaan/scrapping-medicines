import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from urllib.parse import urlparse

archivo = 'items farmex'

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
f = open('fLinks.json')
data = json.load(f)
for i in data:
    links.append(i['link'])
f.close()

class FarmexDetSpider(scrapy.Spider):
    name = 'farmex_det'
    allowed_domains = ['farmex.cl']
    start_urls = links

    def parse(self, response):
        for product in response.css('div#body-content'):
            bc_url = response.url
            u = urlparse(bc_url)
            category = u.path.split('/')[3]
            req = requests.get(bc_url)
            soup = BeautifulSoup(req.text, 'html.parser')
            ### si el script falla puede ser porque el indice de 
            ### soup.findall está en una posición equivocada
            script = soup.find_all('script')[2].text
            script_tag = json.loads(script)
            print('este es el sku:'+script_tag['sku'])
            ofertas_convenios = []
            
            try:
                convenios_id = response.css('div.options').attrib['id'].replace('product-action-', '')
            except KeyError:
                convenios_id = '0'
            if convenios_id != '0':
                try:
                    url = "https://ordenes.farmex.cl/ordenes/preciosNegociados_PRD.php?id="+convenios_id

                    respuesta = requests.request("GET", url)
                    #process response as json
                    res_json = respuesta.json()
                    for r in res_json:
                        ofertas_convenios.append({r['campania']: r['precioNegociado']})
                except:
                    ofertas_convenios = []

            yield {
                'CodFarmExt': "F",
                'sku': 'N/E',
                'FechaBusq': datetime.now(),
                'nombre': product.css('h1.page-heading::text').get(),
                'precio_normal': product.css('div.detail-price::text').get().strip().replace('$','').replace('.',''),
                'convenio_id': convenios_id,
                'precio_oferta': 0,
                'precio_club': 0,
                'ofertas_convenios': ofertas_convenios,
                'codId': script_tag['sku'],
                'marca': product.xpath('//*[@id="product-info"]/div/div[6]/ul/li/a//text()').get(),
                'link': response.url,
                'img': script_tag['image'],
                'category': category,
            } 

process = CrawlerProcess({
    'FEED_URI': '../outputs/Fitems.json',
    'FEED_FORMAT': 'json',
})

with open('../outputs/Fitems.json', 'w') as f:
    f.write('')

try:
    process.crawl(FarmexDetSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían articulos de farmex')
    f = open(f"../logs/{datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()  
    error()
    