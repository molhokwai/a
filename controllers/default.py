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
if request.vars.theme:
    response.cookies['theme'] = request.vars.theme
    response.cookies['theme']['expires'] = 365 * 24 * 3600
    response.cookies['theme']['path'] = '/'

response.theme = '0'
if request.vars.theme:
    response.theme = request.vars.theme
elif request.cookies.has_key('theme'):
    response.theme = request.cookies['theme'].value

# The main page
# Shows the home page if one created (see 'home_page' function page with title)
# Otherwise, defaults to showing the first 10 posts
def index():
    if len(request.args)==0:
        if response.home_page:
            redirect(URL(r = request,c='default',f = 'page/%i' % response.home_page.id))
    else:
      return dict(posts = app_details.start_page_html)

# The post page
# Shows the entire post, the comments, and the comment form
def post():
    #try: 
    post_id = int(request.args[0])
    post = db(db.posts.id == post_id).select()[0]
    comments = db(db.comments.post_id == post_id).select(db.comments.ALL)
    comment_count = len(db(db.comments.post_id == post_id).select(db.comments.ALL))
    db.comments.post_id.default = post_id
    comment_form = SQLFORM(db.comments, fields = ['comment_author', 'comment_author_email', 'comment_author_website', 'comment_text'], labels = comment_labels)
        
    if comment_form.accepts(request.vars, session):
        session.flash = T("Comment added.")
        redirect(URL(r = request,f = 'post/%i' % post_id ))

    return dict(post = post, comments = comments, comment_form = comment_form, comment_count = comment_count)
    #except: 
    #    redirect(URL(r = request,f = 'index'))

# The page page
# Shows the entire page. Does not show comments or the comment form
def page():
    try:
        if len(request.args)>0:
            post=''
            if a_convert.to_int(request.args[0]):
                post = db(db.posts.id == int(request.args[0])).select()[0]
            else:
                post = db(db.posts.post_title == request.args[0]).select()[0]
                        
            nake=(request.args[len(request.args)-1]=='nake'
                 or post.post_text.find('<!-- nake page -->')>=0)
        
            return dict(post = post, nake  = nake)
        else:
            redirect(URL(r = request,f = 'index'))
    except Exception, ex: 
        session.flash=T("(Caught) Error occured: %(err)s ", dict(err=str(ex)))
        redirect(URL(r = request,f = 'index'))

# The pages page
# Shows links to all pages
def pages():
    return dict(manage_title=T("pages"))

# The category page
# Shows all the posts in the requested category
def category():
    def fp(p): return p.post_type=='post'
    try:
        cat_name = request.args[0]
        cat = db(db.categories.category_name == cat_name
                    ).select(db.categories.ALL)[0]
        posts = db((db.posts.post_type == 'post') &
                   (db.posts.post_category == cat.id)
                   ).select(db.posts.ALL) ## , orderby=~db.posts.post_time
        filter(fp,posts)

        response.sidebar_note = T("You are currently browsing the archives for the %(cat_name)s category.",dict(cat_name=cat_name))
        return dict(posts = posts)
    except:
        redirect(URL(r = request,f = 'index'))

@auth.requires_login()
def add():
    try:
        area = request.args[0]

        if area == "post":
            db.posts.post_type.default = 'post'
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 
                                                    'post_category', 'is_translated'], 
                                                    labels = post_labels)
            page_form.append(INPUT(_type='checkbox', 
                                    _name='post_attributes_content_is_original', 
                                    _id='post_attributes_content_is_original', value=''))
            page_title = T("Add Post")
            
            if page_form.accepts(request.vars, session):
                tcode="post_id_"+str(page_form.vars.id)
                from gluon.contrib import simplejson
                _json=simplejson.loads(request.vars.post_attributes_json)
                _json['content_is']['original']=request.vars.post_attributes_content_is_original=='on'
                pg=db(db.posts.id==page_form.vars.id).update(
                                                post_text_TCode=tcode,
                                                post_attributes_json=simplejson.dumps(_json))
                ## FEATURE REQUEST: to add the translation code if not existing
                T(tcode)
                session.flash = T("Post added.")
                redirect(URL(r = request,f = 'post/%i' % page_form.vars.id))
        
        elif area == "page":
            db.posts.post_type.default = 'page'
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 
                                                    'show_in_menu', 'is_translated'], 
                                                    labels = post_labels)
            page_form.append(INPUT(_type='checkbox', _name='post_attributes_content_is_original', 
                                                    _id='post_attributes_content_is_original', value=''))
            page_title = T("Add Page")
            
            if page_form.accepts(request.vars, session):
                tcode="page_id_"+str(page_form.vars.id)
                from gluon.contrib import simplejson
                _json=simplejson.loads(request.vars.post_attributes_json)
                _json['content_is']['original']=request.vars.post_attributes_content_is_original=='on'
                pg=db(db.posts.id==page_form.vars.id).update(
                                                post_text_TCode=tcode,
                                                post_attributes_json=simplejson.dumps(_json)
                                            )
                ## FEATURE REQUEST: to add the translation code if not existing
                T(tcode)
                session.flash = T("Page added.")
                redirect(URL(r = request,f = 'page/%i' % page_form.vars.id))          
                
        else:
            redirect(URL(r = request,f = 'index'))
            
        return dict(page_title = page_title, page_form = page_form)
    except Exception, ex:
        session.flash=T("Error occured: %(err)s ", dict(err=str(ex)))
        redirect(URL(r = request,f = 'index'))

@auth.requires_login()
def edit():
    this_item=None
    area=None
    id=None
    p_a_c_i_o_val=None
    try:
        area = request.args[0]
        id = int(request.args[1])
        this_item = db(db.posts.id == id).select()[0]
    except Exception, ex:
        session.flash=T("Error occured: %(err)s ", dict(err=str(ex)))
        redirect(URL(r = request,f = 'index'))

    try:
        from gluon.contrib import simplejson
        _json=simplejson.loads(this_item.post_attributes_json)
        p_a_c_i_o_val='on' if _json['content_is']['original'] else ''
    except Exception, ex:
        session.flash=T("(Minor) Error occured: %(err)s ", dict(err=str(ex)))
    
    if area == 'post':
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'post_text_TCode', 
                                                            'post_category','is_translated'], 
                                                            deletable=True, labels = post_labels)
        edit_form.append(INPUT(_type='checkbox', _name='post_attributes_content_is_original', 
                                                _id='post_attributes_content_is_original', value=p_a_c_i_o_val))
        edit_title = T("Edit Post")
    
        if edit_form.accepts(request.vars, session):
            if request.vars.delete_this_record=='on':
                session.flash = T("Post deleted.")
                redirect(URL(r = request,f = 'index/posts'))
            else:    
                _json['content_is']['original']=request.vars.post_attributes_content_is_original=='on'
                db(db.posts.id==id).update(post_attributes_json=simplejson.dumps(_json))
                session.flash = T("Post updated.")
                redirect(URL(r = request,f = 'post/%s' %id))

    elif area == 'page':
        this_item = db(db.posts.id == id).select()[0]
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'post_text_TCode', 
                                                            'is_translated', 'show_in_menu'], 
                                                            deletable=True, labels = post_labels)
        edit_form.append(INPUT(_type='checkbox', _name='post_attributes_content_is_original', 
                                                 _id='post_attributes_content_is_original', value=p_a_c_i_o_val))
        edit_title = T("Edit Page")
    
        if edit_form.accepts(request.vars, session):
            if request.vars.delete_this_record=='on':
                session.flash = T("Page deleted.")
                redirect(URL(r = request,f = 'pages'))
            else:
                try:
                    _json['content_is']['original']=request.vars.post_attributes_content_is_original=='on'
                    db(db.posts.id==id).update(post_attributes_json=simplejson.dumps(_json))
                    session.flash = T("Page updated.")
                except Exception, ex:
                    session.flash=T("(Minor) Error occured: %(err)s ", dict(err=str(ex)))
                finally:
                    redirect(URL(r = request,f = 'page/%s' %id))
                        
    else:
        redirect(URL(r = request,f = 'index'))
    
    return dict(edit_form = edit_form, edit_title = edit_title, post=this_item)

        
@auth.requires_login()
def manage():

    area = None
    if len(request.args)>0:
        area = request.args[0]
    else:
        area = 'post'
    
    try: command = request.args[1]
    except: command = ""
        
    if area == 'post':
        rows = db(db.posts.post_type == 'post').select(db.posts.ALL)
        manage_title = T('Manage Posts')

        if command == 'add':
            edit_form = SQLFORM(db.posts, labels = post_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = T("Post added")
                redirect(URL(r = request, f = 'manage/post'))
            else:
                session.flash = T("Error")
       
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_post = db(db.posts.id == id).select()[0]
                edit_form = SQLFORM(db.posts, this_post)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = T("Post updated")
                    redirect(URL(r = request, f = 'manage/post'))
                else:
                    session.flash = T("Error occured")
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.posts.id == id).delete()
                session.flash = T("Post deleted")
                redirect(URL(r = request, f = 'index'))
        else:
            edit_form = ''

        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    elif area == 'link':
        rows = db().select(db.links.ALL)
        manage_title = T('Manage Links')

        if command == 'add':
            edit_form = SQLFORM(db.links, labels = link_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = T("Link added")
                redirect(URL(r = request, f = 'manage/link'))
            else:
                session.flash = T("Error occured")
       
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_link = db(db.links.id == id).select()[0]
                edit_form = SQLFORM(db.links, this_link)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = T("Link updated")
                    redirect(URL(r = request, f = 'manage/link'))
                else:
                    session.flash = T("Error occured")
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.links.id == id).delete()
                session.flash = T("Link deleted")
                redirect(URL(r = request, f = 'manage/link'))
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    elif area == 'category':
        rows = db().select(db.categories.ALL)
        manage_title = T('Manage Categories')
       
        if command == 'add':
            edit_form = SQLFORM(db.categories, labels = cat_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = T("Category added")
                redirect(URL(r = request, f = 'manage/category'))
        
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_cat = db(db.categories.id == id).select()[0]
                edit_form = SQLFORM(db.categories, this_cat)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = T("Category updated")
                    redirect(URL(r = request, f = 'manage/category'))
                else:
                    session.flash = T("Error occured")
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.categories.id == id).delete()
                session.flash = T("Category deleted")
                redirect(URL(r = request, f = 'manage/category'))
        
        else:
            edit_form = ''

        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)        
    
    else:
        redirect(URL(r = request,f = 'index'))

def error():
    ticket=''
    code=''
    requested_uri=''
    err=''

    try:
        ticket=request.vars.ticket
        if ticket == 'None': ticket=None
        
        code=request.vars.code
        if code == 'None': code=None
        
        requested_uri=request.vars.requested_uri
        if requested_uri == 'None': requested_uri=None
    except Exception, ex:
        err=str(ex)
        session.flash=T("Error occured: %(err)s ", dict(err=str(ex)))
        
    return dict(ticket=ticket, code=code, requested_uri=requested_uri, err=err)
        
def files():
    upload_form=SQLFORM(db.files,labels=file_labels)
    if request.vars.file!=None:
        # TODO: strip_path_and_sanitize()
        upload_form.vars.filename=request.vars.file.filename.lower()
        if upload_form.accepts(request.vars,session):
            response.flash=T('file uploaded')
        
    download_form=FORM(LABEL(T('Enter file name'))
                        ,INPUT(_name="filename", requires=IS_NOT_EMPTY())
                        ,INPUT(_type="submit",_value=T('Submit')))
    if (download_form.accepts(request.vars,session)
        or (request.vars.download and request.vars.filename)):
        _file=db(db.files.filename==request.vars.filename.lower()).select()
        if _file: 
            _file=_file[0]
            redirect(URL(r = request,f = 'download/%s/%s' % (_file.file,_file.filename)))
        else:
            response.flash=T('no file found with the name %(filename)s',
                             dict(filename=request.vars.filename.lower()))
        
    return dict(upload_form=upload_form,download_form=download_form,
                upload_title=T('upload'),download_title=T('download'))

def json():
    area=request.args[0]
    return response.json({
        'status' : 1,
        'message' : 'done',
        'result' : {
            'pages' : lambda x: db(db.posts.post_type=='page').select()
        }.get(request.args[0], None)(request.args[0])
    })
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args[0]=='logout':
        session.user_authorization_done=False
    if auth.user and request.vars.next:
        redirect(request.vars.next)
    return dict(form=auth())


@auth.requires_login()
def app_admin():
    area=request.args[0]
    if area=='auth_user':
        form=SQLFORM(db.auth_user,response.anon_user,fields=['display_name','email'])
        if request.post_vars.email:
            auth.user.email=request.vars.email
            
            if (request.vars.email==response.anon_user.email and
                request.vars.display_name==response.anon_user.display_name):
                if form.accepts(request.vars,session):
                    session.flash =T("Update done.")
                    redirect(URL(r = request,f='index'))
                else:
                    db.auth_user.insert(registration_id=auth.user.registration_id,
                                        email=request.vars.email,
                                        display_name=request.vars.display_name)
                    session.flash =T("Data successfully saved.")
                    redirect(URL(r = request,f='index'))
        return dict(form=form,area=area)
    if area=='user':
        if auth.user:
            if auth.user.is_admin:
                _fields=['registration_id','display_name','email','is_admin']
            else:
                _fields=['display_name','email']
                
            form=None
            usr=None
            if len(request.args)>1 and len(request.args[1])>0:
                usr=db(db.auth_user.id==request.args[1]).select()
                if len(usr)>0:usr=usr[0]
                else:
                    session.flash='User not found.'
                    redirect(URL(r=request,f='app_admin/user/'))
                form=SQLFORM(db.auth_user,usr,fields=_fields,deletable=True)
                if form.accepts(request.vars,session):
                    if request.vars.delete_this_record=='on':
                        response.flash=T('User deleted.')
                    else:
                        response.flash=T('User updated.')
                _form_title=T("edit user")
            else:
                form=SQLFORM(db.auth_user,fields=_fields)
                if form.accepts(request.vars,session):
                    session.flash='User created.'
                    redirect(URL(r=request,f='app_admin/user/%(id)i' % form.vars.id))
                _form_title=T("create user")
            return dict(form=form,area=area,form_title=_form_title)
        else:            
            response.flash=T('woooups... not allowed')
            return dict(form='...',area=area,form_title='...')

def download():
    import os
    return response.stream(open(os.path.join(request.folder,'uploads',request.args[0]),'rb'))

@auth.requires_login()
def do_stuff():
    if request.args[0]=='u_tcode_istrans':
        for pg in _pages:
            tcode="page_id_"+str(pg.id)
            is_trans=str(pg.id) in request.vars.ids.split(',')
            upd=db(db.posts.id==pg.id).update(post_text_TCode=tcode,is_translated=is_trans)
        session.flash=T('Translated pages post text T code updated.')
    elif request.args[0]=='u_none_tcode_istrans':
        for pg in _pages:
            tcode="page_id_"+str(pg.id)
            if str(pg.id) in request.vars.ids.split(','):
                upd=db(db.posts.id==pg.id).update(post_text_TCode=None,is_translated=False)
        session.flash=T('Translated pages post text T code updated.')
    elif request.args[0]=='u_auth_user':
        for au in db().select(db.auth_user.ALL):
            upd=db(db.auth_user.id==au.id).update(is_admin=False,is_anonymous=False)
        session.flash=T('Auth user fields updated.')
        
    redirect(URL(r = request,f = 'index'))
