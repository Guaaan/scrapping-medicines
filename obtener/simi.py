from gc import callbacks
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import datetime


class SimiSpider(scrapy.Spider):
    name = 'drsimi'
    allowed_domains = ['drsimi.cl']
    start_urls = ['https://www.farmaciasahumada.cl/medicamentos',]

    def start_requests(self):
        yield scrapy.Request('https://www.drsimi.cl/medicamento')

    def parse(self, response):
        categs = ['medicamento','suplementos-y-alimentos', 'dispositivos',]
        for categ in categs:
            for products in response.css('div.vtex-search-result-3-x-galleryItem.vtex-search-result-3-x-galleryItem--normal.vtex-search-result-3-x-galleryItem--grid.pa4'):
                yield {

                    'name': products.css('span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body::text').get(),
                    'link': f"https://www.drsimi.cl{products.css('a.vtex-product-summary-2-x-clearLink.h-100.flex.flex-column').attrib['href']}",
                }
            n_pag = 1
            for n_pag in range(1, 50):
                yield (scrapy.Request(f'https://www.drsimi.cl/{categ}?page={n_pag}', callback=self.parse))
                n_pag = n_pag + 1


process = CrawlerProcess(settings={
    'FEED_URI': 'simiLinks.json',
    'FEED_FORMAT': 'json',
})

with open('simiLinks.json', 'w') as f:
    f.write('')
try:
    process.crawl(SimiSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de Ahumada')
    f = open(f"../logs/{datetime.datetime.now()}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()
