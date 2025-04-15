from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from urllib.parse import urlparse, parse_qs
import datetime
import re


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


class FarmaciasAhumadaCrawler(CrawlSpider):
    name = 'ahumada'
    custom_settings = {
        'USER_AGENT':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        # 'CLOSESPIDER_PAGECOUNT': 35
    }

    download_delay = 1

    allowed_domains = ['farmaciasahumada.cl']

    start_urls = ['https://www.farmaciasahumada.cl/on/demandware.store/Sites-ahumada-cl-Site/default/Search-UpdateGrid?cgid=medicamentos&start=12&sz=12','https://www.farmaciasahumada.cl/medicamentos',
                  'https://www.farmaciasahumada.cl/bebidas-y-alimentos.html',
                  'https://www.farmaciasahumada.cl/dispositivos-medicos.html', 'https://www.farmaciasahumada.cl/cronicos.html',
                  'https://www.farmaciasahumada.cl/infantil-y-maternidad/lactancia-y-alimentacion.html', 'https://www.farmaciasahumada.cl/nutricion-deportiva.html',
                  'https://www.farmaciasahumada.cl/nutricion-deportiva.html', 'https://www.farmaciasahumada.cl/cuidado-personal.html',
                  'https://www.farmaciasahumada.cl/belleza.html',
                  'https://www.farmaciasahumada.cl/dermocosmetica.html'
                  ]

    rules = (
        # paginación
        Rule(LinkExtractor(
            restrict_css='button.btn.btn-primary.col-8.col-sm-4.more',attrs=['data-url']),follow=True),
        # detalle productos
        Rule(LinkExtractor(restrict_css='a.link'),
             follow=True,
             callback='parse_items'),

    )

    def get_date(self, date):
        fecha_actual = datetime.datetime.today()
        return fecha_actual.strftime('%Y-%m-%d')

    def clean_string(self, texto):
        nuevo_texto = texto.replace('\n', ' ').replace(
            '\r', ' ').replace('\t', ' ').strip()
        return nuevo_texto

    def extract_gtin13(self, json_string):
        pattern = r'"gtin13"\s*:\s*"(\d+)"'
        match = re.search(pattern, json_string)

        if match:
            return match.group(1)
        else:
            return None

    def limpiar_precio(self, price):
        numbers = re.findall(r'\d+', price)
        number_string = ''.join(map(str, numbers))
        return int(number_string)

    def parse_items(self, response):
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
