import re
import json
import scrapy


class ArtistsSpider(scrapy.Spider):
    name = "artists"
    f = open("artists_urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        artist_url = response.url
        img = response.xpath('//img[@id="main_fichacreador1_encabezado1_img_URLImg"]/@src').extract_first()
        name = response.xpath('//a[@id="main_fichacreador1_encabezado1_hl_NombreApellido"]/text()').extract_first()
        real_name = response.xpath('//span[@id="main_fichacreador1_encabezado1_lbl_NombreCompleto"]/text()').extract_first()
        real_name = real_name.replace('Nombre real: ', '')
        category = response.xpath('//span[@id="main_fichacreador1_encabezado1_lbl_Categoria"]/text()').extract_first()
        dates = response.xpath('//span[@id="main_fichacreador1_encabezado1_lbl_Fechas"]/text()').extract_first()
        place_b = response.xpath('//span[@id="main_fichacreador1_encabezado1_lbl_LugarNacimiento"]/node()').extract()
        if 'Lugar de nacimiento:' in place_b: place_b.remove('Lugar de nacimiento:')
        if '<br>' in place_b: place_b.remove('<br>')
        pseudonym = response.xpath('//span[@id="main_fichacreador1_encabezado1_lbl_Seudonimo"]/text()').extract_first()
        all_compositions=[]
        for c in \
                response.xpath('//a[contains(@id,"main_fichacreador1_DL_Temas_hl_Letra_")]/@href').extract():
            all_compositions.append(c)
        lyrics=[]
        for c in \
                response.xpath('//a[contains(@id,"main_fichacreador1_DL_Letras_hl_Letra_")]/@href').extract():
            lyrics.append(c)
        compositions =[]
        for c in \
                response.xpath('//a[contains(@id,"main_fichacreador1_DL_Partituras_hl_Partitura_")]/@href').extract():
            compositions.append(c)
        pattern = re.compile(r'var audioPlaylist = new Playlist\(".*", (.*?), {.*}\);', re.MULTILINE | re.DOTALL)
        audio2 = response.xpath('//script[contains(., "var audioPlaylist")]/text()').re(pattern)
        audio = []
        if len(audio2):
            audio_items=\
            re.findall(r'{(.*)}', audio2[0])
            for rec in audio_items:
                item = {}
                rec_items = re.findall(r'(id:".*"),(idtema:".*"),(titulo:".*"),(canta:".*"),(detalles:".*"),(duracion:".*"),(formacion:".*"),(oga:".*"),(mp3:".*")', rec)
                for b in rec_items:
                    for a in b:
                        a = a[:len(a)-1]
                        a = a.split(':"')
                        if a[0] in ["id","mp3","oga","titulo","duracion","formacion","detalles"]:
                            item[a[0]] = a[1]
                audio.append(item)

        videos = response.xpath('//iframe[contains(@src,"youtu")]/@src').extract()
        recordings=[]
        for d in\
        response.xpath('//div[@id="discografia"]//div[@class="text-muted"]'):
            prev = d.xpath('.//preceding-sibling::div[1]')
            r_id = prev.xpath('.//a[contains(@id,"main_fichacreador1_RP_Discografia_hl_Tema_")]/@href').extract()
            r_name = prev.xpath('.//a[contains(@id,"main_fichacreador1_RP_Discografia_hl_Tema_")]/text()').extract()
            r_type = prev.xpath('.//span[contains(@id,"main_fichacreador1_RP_Discografia_lbl_RitmoDuracion_")]/text()').extract()
            r_vocal = d.xpath('.//span[contains(@id,"main_fichacreador1_RP_Discografia_lbl_Canta_")]/text()').extract()
            r_performer_type = d.xpath('.//span[contains(@id,"main_fichacreador1_RP_Discografia_lbl_Formacion_")]/text()').extract()
            r_performer = d.xpath('.//span[contains(@id,"main_fichacreador1_RP_Discografia_lbl_Interprete_")]/text()').extract()
            r_description = d.xpath('.//span[contains(@id,"main_fichacreador1_RP_Discografia_lbl_DetallesGrabacion_")]/text()').extract()
            recordings.append({'r_type': r_type, 'r_vocal': r_vocal, 'r_name':
                    r_name, 'r_id': r_id,
                    'r_performer_type': r_performer_type, 'r_performer':
                    r_performer, 'r_description': r_description})

        biography = response.xpath('//a[contains(@id,"main_fichacreador1_Biografias1_DL_Biografias_hl_Biografia_")]/@href').extract()
        articles = response.xpath('//a[contains(@id,"main_fichacreador1_Cronicas1_RP_Cronicas_hl_Cronica_")]/@href').extract()

        return {'artist_url': artist_url, 'img': img, 'name': name, 'real_name':real_name,
                    'category': category, 'dates': dates, 'place_b': place_b,
                    'pseudonym': pseudonym, 'all_compositions':
                    all_compositions, 'lyrics': lyrics, 'audio': audio, 'video': videos,
                    'recordings': recordings, 'compositions': compositions,
                    'biography': biography, 'articles':articles}
