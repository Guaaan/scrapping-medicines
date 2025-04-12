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
    "log": f"{datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


class FarmexSpider(scrapy.Spider):
    name = 'farmex'
    allowed_domains = ['farmex.cl']
    start_urls = ['https://farmex.cl/collections/accesorios-medicos', 'https://farmex.cl/collections/antibioticos-y-antivirales', 'https://farmex.cl/collections/aspirina', 'https://farmex.cl/collections/cenabast', 'https://farmex.cl/collections/colageno', 'https://farmex.cl/collections/colageno-hidrolizado', 'https://farmex.cl/collections/corazon-circulacion-1', 'https://farmex.cl/collections/cronicos', 'https://farmex.cl/collections/cyber', 'https://farmex.cl/collections/dermatologia-y-antimicoticos', 'https://farmex.cl/collections/desodorante-hipoalergenico-cristal-alumbre', 'https://farmex.cl/collections/diabetes', 'https://farmex.cl/collections/dolor-inflamacion-y-fiebre', 'https://farmex.cl/collections/eutirox', 'https://farmex.cl/collections/exeltis', 'https://farmex.cl/collections/fonasa', 'https://farmex.cl/collections/gastroenterologia-sistema-digestivo', 'https://farmex.cl/collections/gift-card', 'https://farmex.cl/collections/gripe-alergia-y-tos', 'https://farmex.cl/collections/hipertension-corazon', 'https://farmex.cl/collections/hipertension2', 'https://farmex.cl/collections/hormonas', 'https://farmex.cl/collections/ibuprofeno', 'https://farmex.cl/collections/impotencia-sexual-prostata', 'https://farmex.cl/collections/inflamacion-intestinal', 'https://farmex.cl/collections/insumos-dentales', 'https://farmex.cl/collections/juventud-vitalicia-club-viva-de-vida-security', 'https://farmex.cl/collections/kit-navidad', 'https://farmex.cl/collections/laboratorios-bayer', 'https://farmex.cl/collections/leches', 'https://farmex.cl/collections/leches-adultos', 'https://farmex.cl/collections/leches-ninos', 'https://farmex.cl/collections/leches-oferta', 'https://farmex.cl/collections/mascarillas', 'https://farmex.cl/collections/meds1', 'https://farmex.cl/collections/menopausia', 'https://farmex.cl/collections/metlife', 'https://farmex.cl/collections/musa', 'https://farmex.cl/collections/naturales', 'https://farmex.cl/collections/neurobionta', 'https://farmex.cl/collections/nutricion-y-deporte', 'https://farmex.cl/collections/oftalmologia', 'https://farmex.cl/collections/otros', 'https://farmex.cl/collections/perfumeria-y-dermocosmetica', 'https://farmex.cl/collections/probioticos', 'https://farmex.cl/collections/productos-al-vuelo', 'https://farmex.cl/collections/productos-con-envio-a-todo-chile', 'https://farmex.cl/collections/productos-naturales', 'https://farmex.cl/collections/productos-naturales-homeopatia', 'https://farmex.cl/collections/programa-chile-salud', 'https://farmex.cl/collections/promociones', 'https://farmex.cl/collections/regulacion-biologica-homeopatia-compuesta', 'https://farmex.cl/collections/resfrios', 'https://farmex.cl/collections/sistema-nervioso-central', 'https://farmex.cl/collections/sundown-sunvit', 'https://farmex.cl/collections/suplementos-alimenticios-1', 'https://farmex.cl/collections/suscripciones', 'https://farmex.cl/collections/test', 'https://farmex.cl/collections/test-pagefly', 'https://farmex.cl/collections/test-rapido-covid-19', 'https://farmex.cl/collections/todos-menos-productos-al-vuelo', 'https://farmex.cl/collections/tratamiento-peso', 'https://farmex.cl/collections/verano2020', 'https://farmex.cl/collections/vida-sexual', 'https://farmex.cl/collections/vitaminas-y-minerales']

    # def start_requests(self):
    #         yield scrapy.Request('https://www.ecofarmacias.cl/categoria-producto/medicamentos/')

    def parse(self, response):
        for product in response.css('h5.product-name'):
            link = product.css('a').attrib['href']
            if link == "#":
                continue
            yield {
                'link': 'https://farmex.cl/'+link,
                # 'name': product.css('h2.woocommerce-loop-product__title').get(),
            }
        
        next_page = 'https://farmex.cl/'+response.css('a.next').attrib['href']
        # print('next page: ', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess(settings = {
    'FEED_URI': 'fLinks.json',
    'FEED_FORMAT': 'json',
})

with open('fLinks.json', 'w') as f:
    f.write('')
try:
    process.crawl(FarmexSpider)
    process.start()
except Exception as Argument:
    print('Error mientras se obtenían enlaces de farmex')
    f = open(f"../logs/{datetime.now()}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()
#     error()

