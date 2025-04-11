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
    cod_farm_ext = Field(output_processor=TakeFirst(), default='E')
    cod_id = Field(output_processor=TakeFirst(), default=None)
    fecha_busq = Field(output_processor=TakeFirst(), default=None)
    tipo_id = Field(output_processor=TakeFirst(), default='s')
    nombre = Field(output_processor=TakeFirst())
    precio_oferta = Field(output_processor=TakeFirst(), default=0)
    precio_normal = Field(output_processor=TakeFirst(), default=0)
    all_prices = Field(default=0)
    sku = Field(output_processor=TakeFirst())
    marca = Field(output_processor=TakeFirst())
    img = Field(output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst(), default=None)


class FarmaciasEcoCrawler(CrawlSpider):
    name = 'eco'

    custom_settings = {
        'USER_AGENT':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        # 'CLOSESPIDER_PAGECOUNT': 15
    }

    download_delay = 1
    allowed_domains = ['ecofarmacias.cl']

    start_urls = ['https://www.ecofarmacias.cl/shop/', 'https://www.ecofarmacias.cl/categoria-producto/medicamentos/',
                  'https://www.ecofarmacias.cl/categoria-producto/suplementos-alimenticios/',
                  'https://www.ecofarmacias.cl/categoria-producto/cuidado-personal/',
                  'https://www.ecofarmacias.cl/categoria-producto/veterinaria/',
                  'https://www.ecofarmacias.cl/categoria-producto/marcas-destacadas/',
                  'https://www.ecofarmacias.cl/categoria-producto/covid-19/']

    rules = (
        # paginación
        Rule(LinkExtractor(allow=r'/page/'), follow=True),
        # detalle productos
        Rule(LinkExtractor(allow=r'/producto/'),
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
        # product = response.css('div.product-info-price')
        # prices = product.css('span.price::text').getall()
        # offer_price = product.css('span.price::text').getall()
        # all_prices = product.css('span.price::text').getall()

        # if len(prices) < 2:
        item.add_css("precio_normal", 'bdi::text', MapCompose(self.limpiar_precio))
        #     item.add_value("precio_oferta", 0)
        #     item.add_value("all_prices", all_prices, MapCompose(self.limpiar_precio))
        # else:
        #     item.add_value("precio_normal", prices[1], MapCompose(self.limpiar_precio))
        #     item.add_value("precio_oferta", prices[0], MapCompose(self.limpiar_precio))
        #     item.add_value("all_prices", all_prices, MapCompose(self.limpiar_precio))

        item.add_value('cod_farm_ext', "E")
        # item.add_xpath("cod_id", "//script[13]/text()", MapCompose(self.extract_gtin13))
        item.add_xpath("cod_id", '//span[@class="sku"]/text()')
        # item.add_value('fecha_busq', "123", MapCompose(self.get_date))
        # item.add_value('tipo_id', "c")
        item.add_css("nombre", "h1.product_title.entry-title::text")

        sku = response.css('button.single_add_to_cart_button.button.alt').attrib['value'],
        item.add_value("sku", sku)
        # item.add_css("marca", "h3.product-brand::text", MapCompose(self.clean_string))
        item.add_value('link', response.url)
        img = response.css('img.wp-post-image').attrib['src']
        item.add_value("img", img)

        yield item.load_item()
