import re
import json
import scrapy


class WorksSpider(scrapy.Spider):
    name = "works"
    f = open("temas_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        #work_url = response.url
        work_url = response.xpath('//meta[@property="og:url"]/@content').extract_first()
        img = response.xpath('//img[@id="main_Tema1_img_part"]/@src').extract_first()
        title = response.xpath('//span[@id="main_Tema1_lbl_Titulo"]/text()').extract_first()
        work_type = response.xpath('//span[@id="main_Tema1_lbl_Ritmo"]/text()').extract_first()
        year = response.xpath('//span[@id="main_Tema1_lbl_Ano"]/text()').extract_first()
        composers=[]
        for c in \
                response.xpath('//a[contains(@id,"main_Tema1_Tema_Autores1_RP_TemasCreadores_AutoresMusica_hl_Creador_")]/@href').extract():
            composers.append(c)
        liricists=[]
        for c in \
                response.xpath('//a[contains(@id,"main_Tema1_Tema_Autores1_RP_TemasCreadores_AutoresLetra_hl_Creador_")]/@href').extract():
            liricists.append(c)
        scores = response.xpath('//img[contains(@id,"main_Tema1_img_part")]/@src').extract()
        lyrics = response.xpath('//span[@id="main_Tema1_lbl_Letra"]/node()').extract()

        pattern = re.compile(r'var audioPlaylist = new Playlist\(".*", [\[\r\n\t\t   ]?[ ]?(.*?)[\r\n\t        \]\r\n    ]?[ \]]?, {.*}\);', re.MULTILINE | re.DOTALL)
        audio2 = response.xpath('//script[contains(., "var audioPlaylist")]/text()').re(pattern)
        audio = []
        if len(audio2):
            audio_items= audio2[0][1:-1].split('},{')
            for rec in audio_items:
                item = {}
                rec_items = re.findall(r'(id:".*"),(idtema:".*"),(titulo:".*"),(canta:".*"),(detalles:".*"),(duracion:".*"),(formacion:".*"),(oga:".*"),(mp3:".*"),(existeenlistasusuario:".*"),(idusuario:".*")', rec)
                for a in rec_items[0]:
                    a = a[:-1]
                    a = a.split(':"')
                    if a[0] in ["id","mp3","oga","titulo","duracion","formacion","detalles"]:
                        item[a[0]] = a[1]
                audio.append(item)
        videos = response.xpath('//iframe[contains(@src,"youtu")]/@src').extract()
        recordings=[]
        for d in response.xpath('//div[@class="cajita_gris3"]'):
            r_type = d.xpath('.//span[contains(@id,"main_Tema1_RP_Versiones_lbl_RitmoDuracion_")]/text()').extract()
            r_vocal = d.xpath('.//span[contains(@id,"main_Tema1_RP_Versiones_lbl_Canta_")]/text()').extract()
            r_performer_type = d.xpath('.//span[contains(@id,"main_Tema1_RP_Versiones_lbl_Formacion_")]/text()').extract()
            r_performer = d.xpath('.//span[contains(@id,"main_Tema1_RP_Versiones_lbl_Interprete_")]/text()').extract()
            r_description = d.xpath('.//span[contains(@id,"main_Tema1_RP_Versiones_lbl_DetallesGrabacion_")]/text()').extract()
            recordings.append({'r_type': r_type, 'r_vocal': r_vocal,
                'r_performer_type': r_performer_type, 'r_performer':
                r_performer, 'r_description': r_description})

        return {'work_url': work_url, 'img': img, 'title': title, 'work_type': work_type, 'year':
                year, 'composers': composers, 'liricists': liricists, 'scores':
                scores, 'lyrics': lyrics, 'audio': audio, 'video': videos,
                'recordings': recordings}
