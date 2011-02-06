from types import *

###################################
## CONTROLLER INITIALIZATION
###################################    
try:
    exec('from applications.%s.modules import common' % this_app)
    app_objects=Struct(**{'details':app_details,'config':app_config,'log_wrapped':log_wrapped})
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)
except Exception, ex:
    log_wrapped('Er', ex)

# media_photos module
exec('from applications.%s.modules import media_photos' % this_app)

###################################
## CONTROLLER FUNCTIONS
###################################    

# The main page
def index():
    redirect(URL(r=request, f='picasa', args='gallery'))
    return dict(nake=None)

# Picasa
def picasa():
    area = 'gallery'
    if len(request.args)>0:
        area=request.args[0]

    try:
        picasa_manager = media_photos.Manage(app_config)
        if auth.user and auth.user.is_admin:
            if area in ['upload', 'albums', 'add', 'edit', 'delete'] and not session.gdata_user:
                session.redirect_url=URL(r=request, f='picasa', args=[area])
                redirect(URL(r=request, f='picasa', args=['login']))
            else:
                picasa_manager = media_photos.Manage(app_config, gdata_user=None, session=session)
        
            if area == 'login':
                form=FORM(INPUT(_type='email', _name='email', value=auth.user.email),
                            INPUT(_type='password', _name='password'),
                            INPUT(_type='submit', _value=T('submit'))
                )
                if form.accepts(request.vars, session):
                    try:
                        gdata_user={
                            'email' : request.vars.email,
                            'password' : request.vars.password
                        }
                        # programmatic login encapsulated in construction
                        media_photos.Manage(app_config, gdata_user=gdata_user)
                        session.gdata_user=gdata_user
        
                        session.flash = T('Login successfull')
                        if session.redirect_url:
                            redirect(session.redirect_url)
                        else:
                            redirect(URL(r=request, args=['albums']))
                    except Exception, ex:
                        log_wrapped('Error', ex)
                return dict(nake=None, area=area, form=form, item='user')
                
            if area in ['add', 'edit', 'delete', 'upload']:
                # item : album || picture
                item=request.args[1]
    
                if item=='album':
                    if area == 'add':
        
                        form=FORM(DIV(INPUT(_type='text', _name='title'), 
                                        TEXTAREA(_name='summary'),
                                        INPUT(_type='submit', _value=T('submit'))
                                      )
                                )
                        if form.accepts(request.vars, session):
                            if area == 'add':
                                try:
                                    album = picasa_manager.client.InsertAlbum(title=request.vars.title, summary=request.vars.summary)
                                    session.flash = T('Album successfully added')
                                    redirect(URL(r=request, args=['albums']))
                                except Exception, ex:
                                    log_wrapped('Error', ex)
                                    response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
        
                        return dict(nake=None, area=area, form=form, item=item)
        
                    elif area == 'edit':
                        album_id=request.args[2]
                        album_feed=picasa_manager.get_album_by_id(album_id)
                        album_photos=picasa_manager.get_album_photos(
                                            album_id, 
                                            username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                            limit=10
                                            )
        
                        form=FORM(DIV(INPUT(_type='text', _name='title', _value=album_feed.title.text), 
                                        TEXTAREA(_name='summary',  value=album_feed.summary.text),
                                        INPUT(_type='submit', _value=T('submit'))
                                      )
                                )
                        if form.accepts(request.vars, session):
                                try:
                                    album_feed.title.text=request.vars.title
                                    album_feed.summary.text=request.vars.summary
                
                                    updated_album = picasa_manager.client.Put(album_feed, album_feed.GetEditLink().href, converter=gdata.photos.AlbumEntryFromString)
                                    session.flash = T('Album successfully updated')
                                    redirect(URL(r=request, args=['albums']))
                                except Exception, ex:
                                    log_wrapped('Error', ex)
                                    response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
        
                        return dict(nake=None, area=area, form=form, item=item, album=album_photos, album_id=album_id)
        
                    elif area == 'delete':
                        album_id=request.args[2]
                        album_feed=picasa_manager.get_album_by_id(album_id)
                        album_photos=picasa_manager.get_album_photos(
                                          album_id, 
                                          username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                          limit=10
                                          )
        
                        form=FORM(DIV(INPUT(_type='text', _name='title', _value=album_feed.title.text), 
                                        TEXTAREA(_name='summary',  value=album_feed.summary.text),
                                        INPUT(_type='submit', _value=T('delete'))
                                      )
                                )
                        if form.accepts(request.vars, session):
                            try:
                                picasa_manager.client.Delete(album_feed)
                                session.flash = T('Album deleted')
                                redirect(URL(r=request, args=['albums']))
                            except Exception, ex:
                                log_wrapped('Error', ex)
                                response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
        
                        return dict(nake=None, area=area, form=form, item=item, album=album_photos, album_id=album_id)
    
                elif item=='picture':
    
                    if area == 'upload':
                        upload_nr=5
                        album_id=request.args[2]
                        album_url = '/data/feed/api/user/%s/albumid/%s' % (session.gdata_user['email'], album_id)
        
                        form=FORM()
                        for i in range(upload_nr):
                            form.append(DIV(INPUT(_type='file', _name='file_%i' % i), 
                                            INPUT(_type='text', _name='title_%i' % i))
                            )
                        form.append(INPUT(_type='submit', _value=T('submit')))
                        if form.accepts(request.vars, session):
                            import gluon.contenttype as contenttype
                            _exceptions=[]
                            _file_tuples=[]
                            for i in range(upload_nr):
                                _file,filename,filetitle=None,'',''
                                for v in request.post_vars:
                                    if v=='file_%i' % i:
                                        try: 
                                            _file=request.post_vars[v].file
                                            filename=request.post_vars[v].filename
                                        except Exception, ex: log_wrapped('exception', ex)
    
                                    elif v=='title_%i' % i:
                                        filetitle=request.post_vars[v]
    
                                if _file:
                                    if not filetitle:
                                        if filename.find('\\')>0: f_n_s=filename.split('\\')
                                        else: f_n_s=filename.split('/')
                                        filetitle=f_n_s[len(f_n_s)-1]
                                    _file_tuples.append((_file, filename, filetitle))
    
                            for i in range(len(_file_tuples)):
                                try:
                                    photo = picasa_manager.client.InsertPhotoSimple(album_url, _file_tuples[i][2],
                                                                    'Uploaded using the API', _file_tuples[i][0], 
                                                                    content_type=contenttype.contenttype(_file_tuples[i][1]))
                                except Exception, ex:
                                    _exceptions.append(ex)
                                    
                            if len(_exceptions)>0:
                                response.flash=T('There were %i errors during the upload(s): %s' % (len(_exceptions), str(_exceptions)))
                                log_wrapped('exceptions', str(_exceptions))
                            else:
                                redirect(URL(r=request, f='picasa', args=['album', album_id]))
        
                        return dict(nake=None, area=area, form=form, item=item)
    
                    elif area == 'edit':
                        photo_id, album_id=request.args[2], request.args[3]
                        photo=picasa_manager.get_album_photo_by_id(
                                            album_id, photo_id, 
                                            username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                            raw_feed=True
                                            )
                        picasa_manager.initialize_photo_metadata(photo)
        
                        form=FORM(
                                DIV(LABEL(T('title')), INPUT(_type='text', _name='title', _value=photo.title.text)),
                                DIV(LABEL(T('summary')), TEXTAREA(_name='summary', value=photo.summary.text)),
                                DIV(LABEL(T('keywords')), INPUT(_type='text', _name='keywords', _value=photo.media.keywords.text)),
                                DIV(LABEL(XML('&nbsp;')), INPUT(_type='submit', _value=T('submit')))
                            )
                        if form.accepts(request.vars, session):
                            try:
                                photo.title.text = request.vars.title
                                photo.summary.text = request.vars.summary
                                photo.media.keywords.text = request.vars.keywords
                                updated_photo = picasa_manager.client.UpdatePhotoMetadata(photo)
                                
                                session.flash = T('Photo successfully updated')
                                redirect(URL(r=request, args=['edit', 'album', album_id]))
                            except Exception, ex:
                                log_wrapped('Error', ex)
                                response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
    
                        return dict(nake=None, area=area, form=form, item=item, photo=photo)
        
                    elif area == 'delete':                        
                        photo_id, album_id=request.args[2], request.args[3]
                        photo=picasa_manager.get_album_photo_by_id(
                                            album_id, photo_id, 
                                            username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                            raw_feed=True
                                            )
                        form=FORM(
                                DIV(LABEL(T('title')), INPUT(_type='text', _name='title', _value=photo.title.text)),
                                DIV(LABEL(T('summary')), TEXTAREA(_name='summary', value=photo.summary.text)),
                                DIV(LABEL(T('keywords')), INPUT(_type='text', _name='keywords', _value=photo.media.keywords.text)),
                                DIV(LABEL(XML('&nbsp;')), INPUT(_type='submit', _value=T('delete')))
                            )
                        if form.accepts(request.vars, session):
                            try:
                                picasa_manager.client.Delete(photo)
                                session.flash = T('Photo deleted')
                                redirect(URL(r=request, args=['edit', 'album', album_id]))
                            except Exception, ex:
                                log_wrapped('Error', ex)
                                response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
    
                        return dict(nake=None, area=area, form=form, item=item, photo=photo)
    
    
            elif area == 'albums':
                albums_feed=picasa_manager.get_albums_feed()
                
                form=DIV()
                albums=TABLE(TR(TH(T('title')), TH(T('nr of pictures')), TH(), TH(), TH(), TH()))
                for entry in albums_feed:
                    albums.append(TR(
                                        TD(entry.title.text),
                                        TD(entry.numphotos.text),
                                        TD(A(T('view'), _href=URL(r=request, args=['album', entry.gphoto_id.text]))), 
                                        TD( A(T('edit'), _href=URL(r=request, args=['edit', 'album', entry.gphoto_id.text]))),
                                        TD( A(T('delete'), _href=URL(r=request, args=['delete', 'album', entry.gphoto_id.text]))),
                                        TD( A(T('upload to'), _href=URL(r=request, args=['upload', 'picture',  entry.gphoto_id.text]))),
                                    )
                            )
                form.append(A(T('add'), _class='display-block width100pc text-alignr', _href=URL(r=request, args=['add', 'album'])))
                form.append(albums)
                return dict(nake=None, area=area, form=form, item=None)
    
    ## PUBLIC SECTION
        if area == 'gallery':
            recent=picasa_manager.get_recent_photos()
            gallery=picasa_manager.get_album_gallery()
            return dict(nake=None, area=area, item=None, recent=recent, gallery=gallery)
            
        if area == 'album':
            album_id=request.args[1]
            album=picasa_manager.get_album_photos(album_id)
            return dict(nake=None, area=area, item=None, album=album, album_id=album_id)
            
        elif area == 'slideshow':
            album_id=request.args[1]
            album=picasa_manager.get_album_photos(album_id)
            if not session.current_photo or int(session.current_photo)>len(album)-1:
                session.current_photo=0
            photo=album[int(session.current_photo)]
            session.current_photo+=1
            response.refresh='<meta http-equiv="refresh" content="%i;%s" />' % (2, URL(r=request, args=['slideshow', album_id]))
            return dict(nake=True, area=area, item=None, photo=photo, album_id=album_id)
    
    except Exception, ex:
        log_wrapped('Exception', ex)
        if str(ex).lower().find('unknown user')>=0:
            session.flash = T('User is unknown by the Google Photos (Picasa) Service. User must be registered there: %(picasa_link)s', 
                                dict(picasa_link='http://picasaweb.google.com'))
        if str(ex).lower().find('captcha required')>=0:
            session.flash = T('User credentials are unknown to the Google Photos (Picasa) Service. User should be modified by an administrator, in service setup.')
        redirect(URL(r=request, c='default', f='error'))

def social():
    area = 'twitter'
    sub_area=None
    _items=[]
    if request.args[0] == 'twitter' or request.args[0] == 'twitter.json':
        exec('from applications.%s.modules import twitter' % request.application)
        try:
            if len(request.args)>1:
                sub_area = request.args[1]
                if sub_area == 'user':
                    api_config=db(db.app_config.id>0).select()[0].TWITTER_API
                    _username=api_config[0]
                    twitter = twitter.Manager(_username)
                    _items = twitter.get_user_tweets()
                    if type(_items)==DictType and 'error' in _items:
                        _items=[_items['request'], _items['error']]
        except Exception, ex:
            log_wrapped('Error', ex)
            if str(ex).lower().find(str('No JSON object could be decoded').lower())>=0:
                response.flash=T('No tweets for username and/or hash found (error: %(err)s)', dict(err=str(ex)))
            else:
                response.flash=T('Error occured: : %(err)s', dict(err=str(ex)))

    return dict(nake=False, area=area, sub_area=sub_area, items=_items)

def twitter():
    api_config=db(db.app_config.id>0).select()[0].TWITTER_API
    _username = api_config[0]
    _hashes, _filters = api_config[2], api_config[3]
    _filter = '#%s %s' % (' '.join(_filters.split(',')), ' #'.join(_hashes.split(',')))

    exec('from applications.%s.modules import twitter' % request.application)
    twitter = twitter.Manager(_username)
    _items = twitter.search_tweets(_hashes)

    import gluon.contrib.simplejson as simplejson
    return simplejson.dumps(_items)
