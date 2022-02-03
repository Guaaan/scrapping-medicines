import scrapy
from scrapy.linkextractors import LinkExtractor

class MedicinesSpider(scrapy.Spider):
    name = 'medicine'
    start_urls = ['https://www.farmaciasahumada.cl/medicamentos.html']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            yield {
                'name': products.css('a.product-item-link::text').get().strip(),
                'price': products.css('span.price-wrapper').attrib['data-price-amount'],
                'link': products.css('a.product-item-link').attrib['href'],
                'lab': products.css('p.product-brand-name.truncate::text').get(),
            }

        next_page = response.css('a.action.next').attrib['href']
        print('next page: ', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        