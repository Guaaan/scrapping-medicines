from concurrent.futures import process
from datetime import datetime
from os import link
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import requests
from bs4 import BeautifulSoup
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from urllib.parse import urlparse, parse_qs
import datetime
import re


archivo = 'Articulos Ahumada'

class Articulo(Item):
    link = Field(output_processor=TakeFirst(), default=None)
    cod_farm_ext = Field(output_processor=TakeFirst(), default='A')
    cod_id = Field(output_processor=TakeFirst(), default=None)
    fecha_busq = Field(output_processor=TakeFirst(), default=None)
    tipo_id = Field(output_processor=TakeFirst(), default='c')
    nombre = Field(output_processor=TakeFirst())
    precio_oferta = Field(output_processor=TakeFirst(), default=0)
    precio_normal = Field(output_processor=TakeFirst(), default=0)
    all_prices = Field(default=0)
    sku = Field(output_processor=TakeFirst())
    marca = Field(output_processor=TakeFirst())
    img = Field(output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst(), default=None)


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
    

# envio()

links = []
f = open('../outputs/ahumada_links.json')
data = json.load(f)
for i in data:
    links.append(i['link'])
f.close()
class DetailedahumadaSpider(scrapy.Spider):
    
    
    name = 'detailedahumada'
    allowed_domains = ['farmaciasahumada.cl']
    start_urls = links
#     print(start_urls)
      
    if start_urls is not []:
      def parse(self, response):
        item = ItemLoader(item=Articulo(), response=response)
        product = response.css('div.product-details-section')
        
        offer_price = product.xpath('.//span[@class="sales"]/span/text()').get()
        normal_price = product.xpath('.//del[@class="text-decoration-none"]/span/span/@content').get()

        if normal_price:
            item.add_value("precio_normal", normal_price, MapCompose(self.limpiar_precio))
            item.add_value("precio_oferta", offer_price, MapCompose(self.limpiar_precio))
        else: 
            item.add_value("precio_normal", offer_price, MapCompose(self.limpiar_precio))
            
        item.add_value('cod_farm_ext', "A")
        item.add_xpath("cod_id", "//script[13]/text()", MapCompose(self.extract_gtin13))
        item.add_value('fecha_busq', "123", MapCompose(self.get_date))
        item.add_value('tipo_id', "c")
        item.add_css("nombre", "h1.product-name::text", MapCompose(self.clean_string))
        img = response.css('img.d-block.img-fluid.js-swiper-slide.mx-auto').attrib['src']
        # item.add_css("sku", "div.value::text")
        item.add_css("marca", "h3.manufacturer-name::text", MapCompose(self.clean_string))
        item.add_value('link', response.url)

        item.add_value("img", img)

        yield item.load_item()
      #   def parse(self, response):
      #       for product in response.css('div.column.main'): #('div.product-info-main')
      #           bc_url = response.url
      #           req = requests.get(bc_url)
      #           soup = BeautifulSoup(req.text, 'html.parser')
      #           #este indice puede variar dependiendo de si el tag script donde se encuentra el codigo de barra ha sido movido por procesos internos de la página de ahumada
      #           script = soup.find_all('script')[12].text
      #           barcode = json.loads(script)
      #           yield {
      #               'CodFarmExt': "A",
      #               'codId': barcode['gtin13'],
      #               'FechaBusq': datetime.now(),
      #               'tipoID': 'c',
      #               'nombre': product.css('span.base::text').get().replace("'", ""),
      #               'precio_oferta': int(product.css('span.price::text').getall()[0].replace('.', '').replace('$', '').replace(' ', '')),
      #               'precio_normal': int(product.css('span.price::text').getall()[-1].replace('.', '').replace('$', '').replace(' ', '')),
      #               'sku': product.css('div.value::text').get(),
      #               'marca': product.css('h3.product-brand::text').get().strip().replace("'", ""),
      #               'link': response.url,
      #               'img':  product.css('img.gallery-placeholder__image').attrib['src'],
      #               'category': 'null'
      #           }
            
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
    