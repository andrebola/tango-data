import re
import json
import scrapy


class VocabularySpider(scrapy.Spider):
    name = "vocabulary"
    f = open("vocab_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        word_url = response.url
        word = response.xpath('//span[@id="main_lbl_Palabra"]/text()').extract()
        significate = response.xpath('//span[@id="main_lbl_Significado"]/text()').extract()
        works = response.xpath('//a[contains(@id,"main_DL_LetrasConEsteTermino_hl_Tema_")]/@href').extract()

        return {'word_url': word_url, 'word':word,
                'works': works, 'significate': significate}
