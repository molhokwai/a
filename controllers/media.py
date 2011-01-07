# This sets the session authorization values
auth_users=db().select(db.auth_user.ALL)
response.auth_users=auth_users

def init_app():
    """Application first run initialization"""
    if request.vars.app_cfg_NAME:
        app_config=db(db.app_config.id>0)
        if len(app_config.select())>0:
            app_config.update(
                NAME=request.vars.app_cfg_NAME,
                GDATA_API_CONSUMER_KEY=request.vars.app_cfg_GDATA_API_CONSUMER_KEY,
                GDATA_API_CONSUMER_KEY=request.vars.app_cfg_GDATA_API_CONSUMER_SECRET
            )
        else:
            db.app_config.insert(
                NAME=request.vars.app_cfg_NAME,
                GDATA_API_CONSUMER_KEY=request.vars.app_cfg_GDATA_API_CONSUMER_KEY,
                GDATA_API_CONSUMER_KEY=request.vars.app_cfg_GDATA_API_CONSUMER_SECRET
            )
    for au in auth_users:
        if au.email=='anonymous@molhokwai.net':response.anon_user=au
    if response.anon_user is None:
        response.anon_user_id=db.auth_user.insert(
                            registration_id='http://anonymous@molhokwai.net',
                            display_name='anonymous',
                            email='anonymous@molhokwai.net',
                            is_anonymous=True
                            )
        response.anon_user=db(db.auth_user.id==response.anon_user_id).select()[0]

    try:
        if not db(db.posts.post_title=='a_home').select():
            db.posts.insert(
                post_type='page',
                post_title='a_home',
                post_text=app_details.init_app_config['pages']['home'],
                show_in_menu=True
                )
        if not db(db.posts.post_title=='a_help').select():
            db.posts.insert(
                post_type='page',
                post_title='a_help',
                post_text=app_details.init_app_config['pages']['help'],
                show_in_menu=True
                )
    except Exception, ex:
        session.flash=T("Error occured: %(err)s ", dict(err=str(ex)))
init_app()        

def get_usr_display_name(usr):
    display_name=usr.preferredUsername
    if display_name is None or display_name=='':
        display_name=usr.first_name
    if display_name is None or display_name=='':
        display_name=usr.last_name
    return display_name

def user_authorization():
    display_name=get_usr_display_name(auth.user)
    if display_name is None or display_name=='':
        if (auth.user.email is None or auth.user.email==''):
            flash_msg="You are logged in. Your provider sent us empty email and username."
            flash_msg+="Click <a href='%(app_admin_url)s'>here</a> to fill in the data or continue as anonymous."
            session.flash=T(flash_msg,dict(app_admin_url=URL(r = request,f='app_admin/auth_user')))
        else:
            display_name=auth.user.email.split('@')[0]
            flash_msg="You are logged in. With display name: %(display_name)s and email: %(email)s."
            flash_msg+="Click <a href='%(app_admin_url)s'>here</a> to modify these data."
            session.flash=T(flash_msg,dict(app_admin_url=URL(r = request,f='app_admin/auth_user'),
                                        display_name=display_name,email=auth.user.email))
    session.authorized=auth.user.is_admin


if (not auth.user is None and not session.user_authorization_done):
    user_authorization()
    session.user_authorization_done=True

if auth.user and (auth.user.display_name is None or auth.user.display_name==''):
    display_name=get_usr_display_name(auth.user)
    if display_name is None or display_name =='':
        display_name='anonymous@molhokwai.net'
    auth.user.display_name=display_name

response.title = app_details.title
response.keywords = app_details.keywords
response.description = app_details.description

# This dynamically adds the pages to the menu
_pages = db(db.posts.post_type == 'page').select(db.posts.ALL)
items = []
menu_items = []
for page in _pages:
    item = [page.post_title, False, '/%(app)s/default/page/%(id)s' % {'app':request.application, 'id':page.id}]
    items.append(item)
    if page.show_in_menu and len(menu_items)<10:
      menu_items.append(item)
response.pages = items
response.menu=menu_items

# page helper
class PageHelper():
    _title=''
    def get_page_by_title(self,item):
        return item.post_title.lower()==self._title

# instance
page_helper=PageHelper()
post_helper=PageHelper()

# This gets the home page, if one created
def home_page():
    """Convention over configuration: Home page is the one with title T('zorglub'),
        The corresponding eventual language translation of 'home'.
        
        TODO: as proprty in a configuration framework (see if pypress4gae offers home/index page
        configuration, and if so eventually switch to it)
    """
    if response.menu:
        page_helper._title='a_home'
        return filter(page_helper.get_page_by_title,_pages)
_home_page=home_page()
response.home_page=_home_page[0] if (_home_page and len(_home_page)>0) else None


# This gets the help page, if one created
def help_page():
    """See home_page"""
    if response.menu:
        page_helper._title='a_help'
        return filter(page_helper.get_page_by_title,_pages)
_help_page=help_page()
response.help_page=_help_page[0] if (_help_page and len(_help_page)>0) else None

# This returns all the categories and their post count
cats = db().select(db.categories.ALL)
items = []
for cat in cats:
    count = len(db(
                   (db.posts.post_type == 'post') & 
                   (db.posts.post_category == cat.id)
                   ).select(db.posts.ALL,orderby=~db.posts.post_time))
    if count > 0:
        item = [cat.category_name, count, '/%(app)s/default/category/%(name)s' % {'app':request.application, 'name':cat.category_name}]
        items.append(item)
response.categories = items

# This returns all the links
links = db().select(db.links.ALL)
items = []
for link in links:
    item = [link.link_title, link.link_url, link.id]
    items.append(item)
response.links = items


# Theme
response.themes=['0', '1']
response.theme = '0'
if request.vars.theme:
    response.cookies['theme'] = request.vars.theme
    response.cookies['theme']['expires'] = 365 * 24 * 3600
    response.cookies['theme']['path'] = '/'

if request.vars.theme:
    response.theme = request.vars.theme
elif request.cookies.has_key('theme'):
    response.theme = request.cookies['theme'].value


# from http://code.google.com/apis/picasaweb/docs/1.0/developers_guide_python.html
import gdata.photos.service
import gdata.media
import gdata.geo

# keys & scope
SOURCE='molhokwai.net-cms-v001'
PICASA_USERNAME='molhokwai'
PICASA_USERPASSWORD='jamiroquai8'

def get_gdata_client(gdata_user=session.gdata_user):
    client = gdata.photos.service.PhotosService()
    
    if not session.gdata_user:
        client.email = '%s@gmail.com' % PICASA_USERNAME
        client.password = PICASA_USERPASSWORD
    else:
        client.email = gdata_user['email']
        client.password = gdata_user['password']
    client.source = SOURCE
    client.ProgrammaticLogin()
    return client

def get_albums_feed(client, username=PICASA_USERNAME, limit=100):
    feed = client.GetUserFeed(limit=limit)
    return feed.entry

def get_album_by_id(client, album_id):
    client=get_gdata_client()
    feed = client.GetUserFeed()
    for entry in feed.entry:
        if entry.gphoto_id.text == album_id:
            return entry

def get_album_photos(client, album_id, username=PICASA_USERNAME, limit=100, raw_feed=False):
    client=get_gdata_client()
    album_id=album_id
    album_feed = client.GetFeed(
        '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, album_id), limit=limit)
    if raw_feed:
        return album_feed.entry
    else:
        album=[]
        for photo in album_feed.entry:
            album.append(get_photo_details(photo))
        return album

def get_album_photo_by_id(client, album_id, photo_id, username=PICASA_USERNAME, raw_feed=False):
    photos=get_album_photos(client, album_id, username=PICASA_USERNAME, limit=100, raw_feed=raw_feed)
    if raw_feed:
        return filter(lambda x: x.gphoto_id.text==photo_id, photos)[0]
    else:    
        return filter(lambda x: x.id==photo_id, photos)[0]

def initialize_photo_metadata(photo):
    if not photo.media:
        photo.media = gdata.media.Group()
    if not photo.media.keywords:
        photo.media.keywords = gdata.media.Keywords()
    
    if not photo.geo:
        photo.geo = gdata.geo.Where()
    if not photo.geo.Point:
        photo.geo.Point = gdata.geo.Point()
    photo.geo.Point.pos = gdata.geo.Pos(text='%s %s' % ('45', '-45'))

def get_photo_details(photo):
    album_id=photo.albumid.text
    _id=photo.gphoto_id.text
    _title=photo.title.text
    camera = 'unknown'
    if photo.exif.make and photo.exif.model:
      camera = '%s %s' % (photo.exif.make.text, photo.exif.model.text)
    url=photo.content.src
    thumbnail_url=photo.media.thumbnail[0].url
    return Struct(**{'album_id':album_id, 'id':_id, 'title':_title, 
            'camera':camera, 'url': url, 'thumbnail_url':thumbnail_url})
    
def get_album_thumbnail(client, album_id, username=PICASA_USERNAME):
    return get_album_photos(client, album_id, username=username, limit=1)[0]
        
def get_recent_photos(client, username=PICASA_USERNAME):
    photos = client.GetUserFeed(kind='photo', limit='10')
    recent=[]
    for photo in photos.entry:
        recent.append(get_photo_details(photo))
    return recent

def get_album_gallery(client, username=PICASA_USERNAME, limit=100):
    albums_feed=get_albums_feed(client, username=username, limit=limit)
    gallery=[]
    for entry in albums_feed:
        gallery.append(get_album_thumbnail(client, entry.gphoto_id.text))
    return gallery

# The main page
def index():
    redirect(URL(r=request, f='picasa', args='gallery'))
    return dict(nake=None)

# Picasa
def picasa():
    area = 'gallery'
    if len(request.args)>0:
        area=request.args[0]

    if auth.user and auth.user.is_admin:
        if area in ['upload', 'albums', 'add', 'edit', 'delete'] and not session.gdata_user:
            session.redirect_url=URL(r=request, f='picasa', args=[area])
            redirect(URL(r=request, f='picasa', args=['login']))
    
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
                    client = get_gdata_client(gdata_user=gdata_user)
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
            client=get_gdata_client()
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
                                album = client.InsertAlbum(title=request.vars.title, summary=request.vars.summary)
                                session.flash = T('Album successfully added')
                                redirect(URL(r=request, args=['albums']))
                            except Exception, ex:
                                log_wrapped('Error', ex)
                                response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
    
                    return dict(nake=None, area=area, form=form, item=item)
    
                elif area == 'edit':
                    album_id=request.args[2]
                    album_feed=get_album_by_id(client, album_id)
                    album_photos=get_album_photos(client, album_id, 
                                                  session.gdata_user['email'].replace('@gmail.com', ''), limit=10)
    
                    form=FORM(DIV(INPUT(_type='text', _name='title', _value=album_feed.title.text), 
                                    TEXTAREA(_name='summary',  value=album_feed.summary.text),
                                    INPUT(_type='submit', _value=T('submit'))
                                  )
                            )
                    if form.accepts(request.vars, session):
                            try:
                                album_feed.title.text=request.vars.title
                                album_feed.summary.text=request.vars.summary
            
                                updated_album = client.Put(album_feed, album_feed.GetEditLink().href, converter=gdata.photos.AlbumEntryFromString)
                                session.flash = T('Album successfully updated')
                                redirect(URL(r=request, args=['albums']))
                            except Exception, ex:
                                log_wrapped('Error', ex)
                                response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))
    
                    return dict(nake=None, area=area, form=form, item=item, album=album_photos, album_id=album_id)
    
                elif area == 'delete':
                    album_id=request.args[2]
                    album_feed=get_album_by_id(client, album_id)
                    album_photos=get_album_photos(client, album_id, 
                                                  session.gdata_user['email'].replace('@gmail.com', ''), limit=10)
    
                    form=FORM(DIV(INPUT(_type='text', _name='title', _value=album_feed.title.text), 
                                    TEXTAREA(_name='summary',  value=album_feed.summary.text),
                                    INPUT(_type='submit', _value=T('delete'))
                                  )
                            )
                    if form.accepts(request.vars, session):
                        try:
                            client.Delete(album_feed)
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
                                _file_tuples.append((_file, filename, filetitle))

                        for i in range(len(_file_tuples)):
                            try:
                                photo = client.InsertPhotoSimple(album_url, _file_tuples[i][2],
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
                    photo=get_album_photo_by_id(client, album_id, photo_id, 
                                        username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                        raw_feed=True)
                    initialize_photo_metadata(photo)
    
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
                            updated_photo = client.UpdatePhotoMetadata(photo)
                            
                            session.flash = T('Photo successfully updated')
                            redirect(URL(r=request, args=['edit', 'album', album_id]))
                        except Exception, ex:
                            log_wrapped('Error', ex)
                            response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))

                    return dict(nake=None, area=area, form=form, item=item, photo=photo)
    
                elif area == 'delete':                        
                    photo_id, album_id=request.args[2], request.args[3]
                    photo=get_album_photo_by_id(client, album_id, photo_id, 
                                        username=session.gdata_user['email'].replace('@gmail.com', ''), 
                                        raw_feed=True)
                    form=FORM(
                            DIV(LABEL(T('title')), INPUT(_type='text', _name='title', _value=photo.title.text)),
                            DIV(LABEL(T('summary')), TEXTAREA(_name='summary', value=photo.summary.text)),
                            DIV(LABEL(T('keywords')), INPUT(_type='text', _name='keywords', _value=photo.media.keywords.text)),
                            DIV(LABEL(XML('&nbsp;')), INPUT(_type='submit', _value=T('delete')))
                        )
                    if form.accepts(request.vars, session):
                        try:
                            client.Delete(photo)
                            session.flash = T('Photo deleted')
                            redirect(URL(r=request, args=['edit', 'album', album_id]))
                        except Exception, ex:
                            log_wrapped('Error', ex)
                            response.flash = T('An error occured: %(error)s. You can retry or contact the administrator', dict(error=str(ex)))

                    return dict(nake=None, area=area, form=form, item=item, photo=photo)


        elif area == 'albums':
            client=get_gdata_client()
            albums_feed=get_albums_feed(client)
            
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
        client=get_gdata_client()
        recent=get_recent_photos(client)
        gallery=get_album_gallery(client)
        return dict(nake=None, area=area, item=None, recent=recent, gallery=gallery)
        
    if area == 'album':
        client=get_gdata_client()
        album_id=request.args[1]
        album=get_album_photos(client, album_id)
        return dict(nake=None, area=area, item=None, album=album, album_id=album_id)
        
    elif area == 'slideshow':
        client=get_gdata_client()
        album_id=request.args[1]
        album=get_album_photos(client, album_id)
        if not session.current_photo or int(session.current_photo)>len(album)-1:
            session.current_photo=0
        photo=album[int(session.current_photo)]
        session.current_photo+=1
        response.refresh='<meta http-equiv="refresh" content="%i;%s" />' % (2, URL(r=request, args=['slideshow', album_id]))
        return dict(nake=True, area=area, item=None, photo=photo, album_id=album_id)
