import re
import json
import scrapy


class LyricSpider(scrapy.Spider):
    name = "lyric"
    f = open("lyric_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        lyric_url = response.url
        title = response.xpath('//h1/font/text()').extract()
        body = response.xpath('//pre/text()').extract()

        return {'lyric_url': lyric_url, 'title':title,
                'body': body}
