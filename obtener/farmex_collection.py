from os import link
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from datetime import datetime
import json

archivo = 'links eco'


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

class FarmexCollectionSpider(scrapy.Spider):
    name = 'farmex'
    allowed_domains = ['farmex.cl']
    start_urls = ['https://farmex.cl/collections/']

    # def start_requests(self):
    #         yield scrapy.Request('https://www.ecofarmacias.cl/categoria-producto/medicamentos/')

    def parse(self, response):
        for product in response.css('div.category.text-center'):
            link = product.css('a.category-name').attrib['href']
            if link == "#":
                continue
            yield {
                'link': 'https://farmex.cl'+link,
                # 'name': product.css('h2.woocommerce-loop-product__title').get(),
            }
        
        next_page = 'https://farmex.cl/'+response.css('a.next').attrib['href']
        # print('next page: ', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess(settings = {
    'FEED_URI': 'fcollections.json',
    'FEED_FORMAT': 'json',
})

with open('fcollections.json', 'w') as f:
    f.write('')
try:
    process.crawl(FarmexCollectionSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de farmex')
    f = open(f"../logs/{datetime.datetime.now()}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()