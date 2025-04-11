from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from itemloaders.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from urllib.parse import urlparse, parse_qs
import datetime
import json
import re

class Articulo(Item):
    link = Field(output_processor=TakeFirst(), default=None)
    cod_farm_ext = Field(output_processor=TakeFirst(), default='D')
    cod_id = Field(output_processor=TakeFirst(), default=None)
    fecha_busq = Field(output_processor=TakeFirst(), default=None)
    tipo_id = Field(output_processor=TakeFirst(), default='s')
    nombre = Field(output_processor=TakeFirst())
    precio_oferta = Field(output_processor=TakeFirst(),default=0)
    precio_normal = Field(output_processor=TakeFirst(),default=0)
    precio_club = Field(output_processor=TakeFirst(),default=0)
    sku = Field(output_processor=TakeFirst())
    marca = Field(output_processor=TakeFirst())
    img = Field(output_processor=TakeFirst())
    category = Field(output_processor=TakeFirst(), default=None)
    res_sanitaria = Field(output_processor=TakeFirst(), default=None)


class DrSimiCrawler(CrawlSpider):
    name = 'dr_simi'
    custom_settings = {
        'USER_AGENT':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        # 'CLOSESPIDER_PAGECOUNT': 15
    }

    download_delay = 1

    allowed_domains = ['drsimi.cl']

    start_urls = ['https://www.drsimi.cl/medicamento','https://www.drsimi.cl/suplementos-y-alimentos','https://www.drsimi.cl/dispositivos']

    rules = (
        # paginación
        Rule(LinkExtractor(allow=r'\?page='), follow=True),
        # detalle productos
        Rule(LinkExtractor(restrict_css='a.vtex-product-summary-2-x-clearLink.h-100.flex.flex-column'),
             follow=True,
             callback='parse_items'),
    )

    def get_date(self, date):
        fecha_actual = datetime.datetime.today()
        return fecha_actual.strftime('%Y-%m-%d')

    def clean_string(self, texto):
        nuevo_texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
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
    
    def get_low_price(self,cadena_json):
        data = json.loads(cadena_json)
        if 'offers' in data and 'lowPrice' in data['offers']:
            return data['offers']['lowPrice']
        else:
            return None  # O cualquier otro valor que quieras devolver si no se encuentra el precio
    def get_high_price(self,json_string):
        parsed_data = json.loads(json_string)
        
        try:
            high_price = parsed_data["offers"]["offers"][0]["price"]
            return high_price
        except KeyError:
            return None
    def parse_items(self, response):
        item = ItemLoader(item=Articulo(), response=response)
        item.add_css("nombre", 'span.vtex-store-components-3-x-productBrand.vtex-store-components-3-x-productBrand--quickview::text', MapCompose(self.clean_string))
        item.add_value('link', response.url)
        item.add_value('cod_farm_ext', "D")
        item.add_css("sku", "span.vtex-product-identifier-0-x-product-identifier__value::text")
        item.add_value('tipo_id', "s")
        item.add_value('fecha_busq', "123", MapCompose(self.get_date))
        res_sanitaria = response.css("a.vtex-store-components-3-x-imageElementLink").attrib['href']
        item.add_value('res_sanitaria', f"https://farmaciasdeldrsimicl.vteximg.com.br{res_sanitaria}")
        item.add_css('category', "a.vtex-breadcrumb-1-x-link.vtex-breadcrumb-1-x-link--2.dib.pv1.link.ph2.c-muted-2.hover-c-link::text")
        

        item.add_xpath("precio_oferta", '//*[@class="flex flex-column min-vh-100 w-100"]/div/div/script/text()', MapCompose(self.get_low_price))
        # item.add_xpath("precio_normal", '//*[@class="flex flex-column min-vh-100 w-100"]/div/div/script/text()', MapCompose(self.get_high_price))
        item.add_xpath("precio_normal", '//*[@class="flex flex-column min-vh-100 w-100"]/div/div/script/text()', MapCompose(self.get_high_price))


        item.add_xpath("precio_club", './/*[@class="vtex-product-price-1-x-currencyContainer"]//text()', Join(), MapCompose(self.limpiar_precio))
       
        # item.add_css("marca", "h3.product-brand::text", MapCompose(self.clean_string))

        item.add_xpath("img", '//*[@class="vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main"]/@src')

        yield item.load_item()
