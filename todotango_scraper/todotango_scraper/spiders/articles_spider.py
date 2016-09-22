import re
import json
import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    f = open("articles_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        article_url = response.xpath('//meta[@property="og:url"]/@content').extract_first()
        title = response.xpath('//span[@id="main_historia1_lbl_Titulo"]/text()').extract_first()
        content = response.xpath('//span[@id="main_historia1_lbl_Cronica"]/node()').extract()
        authors = response.xpath('//a[contains(@id,"main_historia1_RP_Autores_hl_Autor_")]/@href').extract()

        works_rel = response.xpath('//a[contains(@id,"main_historia1_RP_Temas_hl_Tema_")]/@href').extract()
        artists_rel = response.xpath('//a[contains(@id,"main_historia1_RP_Creadores_hl_Creador_")]/@href').extract()

        return {'article_url': article_url, 'artists_rel':artists_rel,
                'works_rel': works_rel, 'authors': authors, 'content':
                content, 'title': title}
