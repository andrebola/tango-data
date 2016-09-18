import facebook
a = facebook.GraphAPI()
a.get_app_access_token('###', '###')
works_urls=[]
for w in works:
    works_urls.append(w['work_url'])
ret = []
for w in works_urls:
    obj = a.get_object(w)
    fid = obj['og_object']['id']
    c = a.get_connections(id=fid, connection_name='comments')
    ret.append({'work_url': w, 'fid': fid, 'num_likes': obj['share']['share_count'], 'comments': c })
