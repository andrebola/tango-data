import re
import json
import scrapy


class BiographySpider(scrapy.Spider):
    name = "biographies"
    f = open("en_bio_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        article_url = response.url
        content = response.xpath('//span[@id="main_biografia1_lbl_Biografia"]/node()').extract()
        authors = response.xpath('//a[contains(@id,"main_biografia1_RP_Autores_hl_Autor_")]/@href').extract()

        works_rel = response.xpath('//a[contains(@id,"main_biografia1_RP_Temas_hl_Tema_")]/@href').extract()
        artists_rel = response.xpath('//a[contains(@id,"main_biografia1_RP_Creadores_hl_Creador_")]/@href').extract()

        return {'article_url': article_url, 'artists_rel':artists_rel,
                'works_rel': works_rel, 'authors': authors, 'content':
                content}
