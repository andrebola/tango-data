

month = {'enero':1,'febrero':2,'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
categories = {u'Carteto T\xedpico': 'Group',
            u'Conjunto': 'Group',
            u'Conjunto coral': 'Group',
            u'Conjunto de guitarras': 'Group',
            u'Cuarteto': 'Group',
            u'Cuarteto T\xedpico': 'Group',
            u'Cuarteto de tango': 'Group',
            u'D\xfao de guitarras': 'Group',
            u'D\xfao de piano ': 'Group',
            u'D\xfao de tango': 'Group',
            u'M\xfasicos': 'Group',
            u'Orquesta': 'Orchestra',
            u'Orquesta T\xedpica': 'Orchestra',
            u'Orquesta de cuerdas tensadas ': 'Orchestra',
            u'Quinteto': 'Group',
            u'Quinteto T\xedpico': 'Group',
            u'Tr\xedo': 'Group',
            u'Tr\xedo de guitarras ': 'Group',
            u'Tr\xedo de viol\xedn': 'Group',
            u'Tr\xedo vocal': 'Group'
        }
class Cleaner():
    def __init__(self):
        # Define mapping between Todotango identifiers and our ids
        self.artist_map = {}
        self.artist_identifier = 0
        self.work_map = {}
        self.work_identifier = 0
        self.recording_identifier = 0

        #counter to know how many recordings matched and which didn't
        self.count_same = 0
        self.count_not_same = []

    def clean_artists(self, artists):
        # Load in artists_new cleaned artists with new id generated.
        self.artists = artists
        self.artist_map['http://www.todotango.com/creadores/ficha/116/Carlos-Gardel'] = 1794
        self.artist_map['http://www.todotango.com/Gardel/'] = 1794
        artists_new = []
        for j in artists:
            artist_type = ''
            short_description = j['category']
            external_id= {'todotango': j['artist_url']}
            begin_place = ''
            if j['place_b'] and len(j['place_b']):
                begin_place = j['place_b'][0].strip()
            name = ''
            if j['name']:
                name = j['name']
            alias = []
            if j['real_name']:
                alias.append(j['real_name'])
                ''
            if j['pseudonym']:
                alias.append(j['real_name'])
            if j['dates']:
                dates = j['dates'].replace('(', '').replace(')', '').split(' - ')
                begin_date = None
                if dates[0] and dates[0] != 'n/d':
                    b_date = dates[0].split(' ')

                    if len(b_date)>1 and b_date[0] in month:
                        begin_date = ['', month[b_date[0]], b_date[1]]
                    elif len(b_date)>1 and b_date[1] in month:
                        begin_date = [b_date[0], month[b_date[1]]]
                        if len(b_date) ==3:
                            begin_date.append(b_date[2])
                    else:
                        begin_date = ['', '', b_date[0]]
                end_date = None
                if dates[1] and dates[1] != 'n/d':
                    e_date = dates[1].split(' ')

                    if len(e_date) > 1 and e_date[0] in month:
                        end_date = ['', month[e_date[0]], e_date[1]]
                    elif len(e_date) > 1 and e_date[1] in month:
                        end_date = [e_date[0], month[e_date[1]], e_date[2]]
                    else:
                        end_date = ['', '', e_date[0]]
            if j['category']:
                if j['category'] in categories:
                    artist_type= categories[j['category']]
                else:
                    artist_type = 'Person'
            else:
                artist_type = None
            artists_new.append({'type':artist_type, 'short_description':short_description,
                                'external_id': external_id, 'begin_place': begin_place,
                                'name':name, 'alias': alias,'begin_date':begin_date,
                                'end_date': end_date, 'gender': '', 'id': self.artist_identifier})
            self.artist_map[j['artist_url']] = self.artist_identifier
            self.artist_identifier +=1
        self.artists_new = artists_new
        return artists_new

    def clean_works(self, works):
        # Load in works_new cleaned works with new id generated
        self.works = works
        works_new = []
        for j in works:
            if j['work_url']:
                external_id= {'todotango': j['work_url']}
                composers = j['composers']
                lyricists = j['liricists']
                date=[]
                if j['year']:
                    date = ['','',j['year']]

                last_br = False
                curr_parag = []
                lyrics = []
                for k in j['lyrics']:
                    if k =='<br>':
                        if last_br:
                            lyrics.append(curr_parag)
                            curr_parag = []
                            last_br = False
                        else:
                            last_br = True
                    else:
                        curr_parag.append(k)
                        last_br = False
                if len(curr_parag):
                    lyrics.append(curr_parag)
                work_type = None
                if 'work_type' in j:
                    work_type = j['work_type']
                works_new.append({'title': j['title'], 'id':self.work_identifier,
                                  'external_id': external_id, 'composers': composers,
                                  'lyricists': lyricists, 'date': date, 'lyric': lyrics,
                                  'type': work_type})
                self.work_map[j['work_url']] = self.work_identifier
                self.work_identifier+=1

        for w in works_new:
            composers = []
            for c in w['composers']:
                a_id = None
                if not c in self.artist_map:
                    for a in self.artists_new:  
                        if '/'+c.split('/')[5]+'/' in a['external_id']['todotango']:
                            a_id = a['id']
                else:
                    a_id = self.artist_map[c]
                if a_id:
                    composers.append(a_id)
                else:
                    print w['composers']
            lyricists = []
            for c in w['lyricists']:
                a_id = None
                if not c in self.artist_map:
                    for a in self.artists_new:  
                        if '/'+c.split('/')[5]+'/' in a['external_id']['todotango']:
                            a_id = a['id']
                else:
                    a_id = self.artist_map[c]
                if a_id:
                    lyricists.append(a_id)
                else:
                    print w['lyricists']
            w['lyricists'] = lyricists
            w['composers'] = composers

        self.works_new = works_new
        return works_new

    def clean_recordings(self):
        # Generate recording list, identifing entities from text and merging
        # list on works and artists.

        #Load recordings from artists
        recordings_aux = []
        recordings = []
        for i in self.artists:
            if not i['artist_url'] in self.artist_map:
                print i['artist_url']
            for r in i['recordings']:
                #work_map[r['r_id'][0]]
                #recordings.append(r)
                same = False
                index = 0
                for r2 in recordings_aux:
                    if (len(r2['r_name'])  == len(r['r_name']) and (len(r['r_name']) ==0 or r2['r_name'][0] == r['r_name'][0])) and \
                    (len(r2['r_id']) == len(r['r_id']) and (len(r['r_id']) ==0 or r2['r_id'][0] == r['r_id'][0])) and \
                    (len(r2['r_description']) ==  len(r['r_description']) and (len(r2['r_description']) == 0 or r2['r_description'][0] == r['r_description'][0])) and \
                    (len(r2['r_performer_type']) == len(r['r_performer_type']) and (len(r2['r_performer_type']) == 0 or r2['r_performer_type'][0] == r['r_performer_type'][0])) and \
                    (len(r2['r_performer'])== len(r['r_performer']) and (len(r2['r_performer']) == 0 or r2['r_performer'][0] == r['r_performer'][0])) and \
                    (len(r2['r_type'])== len(r['r_type']) and (len(r2['r_type']) ==0 or r2['r_type'][0] == r['r_type'][0])) and \
                    (len(r2['r_vocal'])== len(r['r_vocal']) and (len(r2['r_vocal']) ==0 or r2['r_vocal'][0] == r['r_vocal'][0])):
                        same = True
                        break
                    else:
                        index +=1
                if not same:
                    if not r['r_id'][0] in self.work_map:
                        for w in self.works_new:  
                            if '/'+r['r_id'][0].split('/')[5]+'/' in w['external_id']['todotango']:
                                w_id = w['id']
                    else:
                        w_id = self.work_map[r['r_id'][0]]
                    performer = None
                    if len(r['r_performer'])>0:
                        performer = r['r_performer'][0]
                    performer_type = None
                    if len(r['r_performer_type'])>0:
                        performer_type = r['r_performer_type'][0]

                    description = None
                    if len(r['r_description'])>0:
                        description = r['r_description'][0]
                    recordings.append({'work': w_id, 'id': self.recording_identifier, 'name': r['r_name'][0],
                                       'performer': performer,'performer_type':performer_type, 
                                       'vocal': r['r_vocal'][0], 'description': description,
                                      'type': r['r_type'], 'artist': [self.artist_map[i['artist_url']]]})
                    recordings_aux.append(r)
                    self.recording_identifier += 1 
                else:
                    if self.artist_map[i['artist_url']] not in recordings[index]['artist']:
                        recordings[index]['artist'].append(self.artist_map[i['artist_url']])

        # Load recordings from works
        aux_works =[]
        recordings2 = []
        for i in self.works:
            for r in i['recordings']:
                recordings2.append({'r_description':r['r_description'], 'r_performer': r['r_performer'],
         'r_performer_type': r['r_performer_type'],
         'r_type': r['r_type'],
         'r_vocal': r['r_vocal'],
         'r_id': [i['work_url']],
          'r_name': [i['title']]})

        for r in recordings2:
            same = False
            for r2 in recordings_aux:
                    if (len(r2['r_name'])  == len(r['r_name']) and (len(r['r_name']) ==0 or r2['r_name'][0] == r['r_name'][0])) and \
                    (len(r2['r_id']) == len(r['r_id']) and (len(r['r_id']) ==0 or r2['r_id'][0] == r['r_id'][0])) and \
                    (len(r2['r_description']) ==  len(r['r_description']) and (len(r2['r_description']) == 0 or r2['r_description'][0] == r['r_description'][0])) and \
                    (len(r2['r_performer_type']) == len(r['r_performer_type']) and (len(r2['r_performer_type']) == 0 or r2['r_performer_type'][0] == r['r_performer_type'][0])) and \
                    (len(r2['r_performer'])== len(r['r_performer']) and (len(r2['r_performer']) == 0 or r2['r_performer'][0] == r['r_performer'][0])) and \
                    (len(r2['r_type'])== len(r['r_type']) and (len(r2['r_type']) ==0 or r2['r_type'][0] == r['r_type'][0])) and \
                    (len(r2['r_vocal'])== len(r['r_vocal']) and (len(r2['r_vocal']) ==0 or r2['r_vocal'][0] == r['r_vocal'][0])):
                        same = True
            if not same :
                performer = None
                if len(r['r_performer'])>0:
                    performer = r['r_performer'][0]
                performer_type = None
                if len(r['r_performer_type'])>0:
                    performer_type = r['r_performer_type'][0]

                description = None
                if len(r['r_description'])>0:
                    description = r['r_description'][0]
                w_id = self.work_map[r['r_id'][0]]
                recordings.append({'work': w_id, 'id': self.recording_identifier, 'name': r['r_name'][0],
                                       'performer': performer,'performer_type':performer_type,
                                       'vocal': r['r_vocal'][0], 'description': description,
                                       'type': r['r_type'], 'artist': []})
                recordings_aux.append(r)
                self.recording_identifier += 1

        # On recordings identified add links to audio files.
        # audio list structure is the same for artists and works
        for i in self.artists:
            self.add_audio(recordings, i['audio'], self.artist_map[i['artist_url']])

        for w in self.works:
            self.add_audio(recordings, w['audio'])

        #Now change text in performer and vocal for reference in artist
        for r in recordings:
            artists_ids = []
            added = []
            for a in r['artist']:
                if self.artists_new[a]['name'] == r['vocal'].replace('Canta ', ''):
                    artists_ids.append({'id': a, 'type': 'vocals'})
                    added.append(a)
                elif self.artists_new[a]['name'] == r['performer']:
                    artists_ids.append({'id': a, 'type': r['performer_type']})
                    added.append(a)
            for a in r['artist']:
                if a not in added:
                    if self.artists_new[a]['name'] in r['vocal'].replace('Canta ', ''):
                        artists_ids.append({'id': a, 'type': 'vocals'})
                        added.append(a)
                    elif self.artists_new[a]['name'] in r['performer']:
                        artists_ids.append({'id': a, 'type': r['performer_type']})
                        added.append(a)
            for a in r['artist']:
                if a not in added:
                    artists_ids.append({'id': a, 'type': None})
            r['artist'] = artists_ids
            del r['vocal']
            del r['performer_type']
            del r['performer']

        self.recordings = recordings
        return recordings

    def add_audio(self, recordings, audio_list, curr_artist=None):
        for a in audio_list:
            index = 0
            same = False
            for r2 in recordings:
                if (r2['name'] == a['titulo']) and \
                (r2['description'] and r2['description'] == a['detalles']) and \
                (((not r2['performer'] and a['formacion'].strip()=='') or r2['performer'] and r2['performer'] in a['formacion'])\
                or r2['performer_type'].strip() == a['formacion'].strip()):
                    same = True 
                    break
                else:
                    index +=1
            if same:
                self.count_same +=1
                if not 'audio' in recordings[index]:
                    recordings[index]['audio'] = {'todotango': []}
                if not a['mp3'] in recordings[index]['audio']['todotango']:
                    recordings[index]['audio']['todotango'].append(a['mp3'])
                if not 'duracion' in recordings[index] or recordings[index]['duracion'] != a['duracion']:
                    recordings[index]['duracion'] = a['duracion']
                if curr_artist != None and curr_artist not in recordings[index]['artist']:
                    recordings[index]['artist'].append(curr_artist)
            else:
                self.count_not_same.append(a)
