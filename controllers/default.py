###################################
## CONTROLLER INITIALIZATION
###################################

try:
    exec('from applications.%s.modules import common' % (this_app if this_app else 'a'))
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)
except Exception, ex:
    log_wrapped('Error (%s/controllers/default.py:9)' % this_app, ex)

    
###################################
## CONTROLLER FUNCTIONS
###################################

# The rpc service call function
def service_call():
    return service()

# The main page
# Shows the home page if one created (see 'home_page' function page with title)
# Otherwise, defaults to showing the first 10 posts
def index():
    if request.get('env')['http_host'].find('aisca')>=0:
        if len(request.args)==0 or not auth.user:
            redirect(URL(r=request, c='aisca', f='index'))
        
    if len(request.args)==0:
        if response.home_page:
            redirect(URL(r=request, c='default', f='page', args=[response.home_page.id]))
        else:
            redirect(URL(r=request, c='setup'))
    else:
      if a_convert.to_int(request.args[0]):
          return dict(posts = utilities.posts_replace_serverside_output_values(db(db.posts.id == int(request.args[0])).select()))
      else:
          posts=db(db.posts.post_title == request.args[0]).select()
          if not posts:
              posts = filter(lambda x: x.post_title.lower().find(request.args[0].lower())>0,response.posts)
              posts = utilities.posts_replace_serverside_output_values(posts)
          return dict(posts = posts)          
      

# The post page
# Shows the entire post, the comments, and the comment form
def post():
    #try: 
    post_id = int(request.args[0])
    post = db(db.posts.id == post_id).select()[0]
    
    if post: 
        if post.auth_requires_login and not auth.user:
            redirect(URL(r = request, f = 'user', args = ['login']))
            
        post.post_text = utilities.replace_serverside_output_values(post.post_text)

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
                post = db(db.posts.post_title == request.args[0]).select()
                if not post:
                    pg = filter(lambda x: x[0].lower().find(request.args[0].lower())>=0, response.pages)
                    if not pg:
                      # fix for _ replacing space in url
                      pg = filter(lambda x: x[0].lower().find(request.args[0].replace('_', ' ').lower())>=0, response.pages)
                    if pg and len(pg)>0: pg = pg[0]
                    post = db(db.posts.id == int(pg[2].replace('/%s/default/page/' % this_app, ''))).select()
                if post: post = post[0]
                
            if post:
                if post.auth_requires_login and not auth.user:
                    redirect(URL(r = request, f = 'user', args = ['login']))
            
                nake=(request.args[len(request.args)-1]=='nake'
                     or post.post_text.find('<!-- nake page -->')>=0)
            
                post.post_text = utilities.replace_serverside_output_values(post.post_text)
        
            return dict(post = post, nake  = nake)
        else:
            redirect(URL(r = request,f = 'index'))
            
    except Exception, ex: 
        log_wrapped('Error', str(ex))
        session.flash=T("(Caught) Error occured: %(err)s ", dict(err=str(ex)))
        redirect(URL(r = request,f = 'index'))

# The pages page
# Shows links to all pages
def pages():
	area = 'a'
	if len(request.args)>0:
		area = request.args[0]

	_pages = response.pages
	if area != 'all':
		_pages = filter(lambda x:x[3] == area, response.pages)
	return dict(manage_title=T("pages"), pages=_pages)

# The category page
# Shows all the posts in the requested category
def category():
    def fp(p): return p.post_type=='post'
    try:
        cat_name = request.args[0]
        cat = db(db.categories.category_name == cat_name
                    ).select(db.categories.ALL)[0]
        posts=[]
        try:
            posts = db((db.posts.post_type == 'post') &
                       (db.posts.post_category == cat.id) &
                        ((db.posts.application == request.application) | 
                        (db.posts.application == None))
                       ).select(db.posts.ALL) ## , orderby=~db.posts.post_time
        except Exception, ex:
            posts = db((db.posts.post_type == 'post') &
                       (db.posts.post_category == cat.id)
                       ).select(db.posts.ALL) ## , orderby=~db.posts.post_time
        filter(fp,posts)

        response.sidebar_note = T("You are currently browsing the archives for the %(cat_name)s category.",dict(cat_name=cat_name))
        return dict(posts = utilities.posts_replace_serverside_output_values(posts))
    except Exception, ex:
        log_wrapped('Error in /%s/default/category' % this_app, ex)
        redirect(URL(r = request,f = 'index'))

@auth.requires_login()
def add():
    try:
        area = request.args[0]

        if area == "post":
            db.posts.post_type.default = 'post'
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 'application', 
                                                    'post_category', 'is_translated', 'auth_requires_login',
                                                    'post_attributes_json'], 
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
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 'application',
                                                    'post_parent', 'show_in_menu', 'is_translated'], 
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
    # p_a_c_i_o_val : page attr. content is orginal value
    p_a_c_i_o_val=None
    try:
        area = request.args[0]        
        if a_convert.to_int(request.args[1]):
            id = int(request.args[1])
        else:
            id = db(db.posts.post_title == request.args[1]).select()[0].id
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
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'application', 'post_text_TCode', 
                                                            'post_category', 'is_translated', 'auth_requires_login',
                                                            'post_attributes_json'], 
                                                            deletable=True, labels = post_labels)
        edit_form.append(INPUT(_type='checkbox', _name='post_attributes_content_is_original', 
                                                _id='post_attributes_content_is_original', value=p_a_c_i_o_val))
        edit_title = T("Edit Post")
    
        if edit_form.accepts(request.vars, session):
            if request.vars.delete_this_record=='on':
                session.flash = T("Post deleted.")
                redirect(URL(r = request,f = 'index/posts'))
            else:    
                from gluon.contrib import simplejson
                _json=simplejson.loads(request.vars.post_attributes_json)
                db(db.posts.id==id).update(post_attributes_json=simplejson.dumps(_json))
                session.flash = T("Post updated.")
                redirect(URL(r = request,f = 'post/%s' %id))

    elif area == 'page':
        this_item = db(db.posts.id == id).select()[0]
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'application', 'post_text_TCode', 
                                                            'post_parent', 'is_translated', 'show_in_menu'], 
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
                    from gluon.contrib import simplejson
                    _json=simplejson.loads(request.vars.post_attributes_json)
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
        
    if area == 'page':
        redirect(URL(r = request, f='pages'))
    
    elif area == 'post':
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
                    redirect(URL(r = request, f = 'manage', args=['post']))
                else:
                    session.flash=T("(Caught) Error occured")
                    
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.posts.id == id).delete()
                session.flash = T("Post deleted")
                redirect(URL(r = request, f = 'index'))
        else:
            edit_form = ''

        return dict(rows = rows, manage_title = manage_title, manage_text='', edit_form = edit_form, area = area)
    
    elif area == 'link':
        rows = db().select(db.links.ALL)
        manage_title = T('Manage Links')

        if command == 'add':
            edit_form = SQLFORM(db.links, labels = link_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = T("Link added")
                redirect(URL(r = request, f = 'manage', args=['link']))
            else:
                session.flash=T("(Caught) Error occured")
       
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_link = db(db.links.id == id).select()[0]
                edit_form = SQLFORM(db.links, this_link)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = T("Link updated")
                    redirect(URL(r = request, f = 'manage', args=['link']))
                else:
                    session.flash=T("(Caught) Error occured")
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.links.id == id).delete()
                session.flash = T("Link deleted")
                redirect(URL(r = request, f = 'manage/link'))
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, manage_text='', edit_form = edit_form, area = area)
    
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
                    redirect(URL(r = request, f = 'manage', args=['category']))
                else:
                    session.flash=T("(Caught) Error occured")
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.categories.id == id).delete()
                session.flash = T("Category deleted")
                redirect(URL(r = request, f = 'manage/category'))
        
        else:
            edit_form = ''

        return dict(rows = rows, manage_title = manage_title, manage_text='', edit_form = edit_form, area = area)        
    
    elif area == 'theme':
        record = None
        form = ''
        manage_title = T('Manage Child Theme')
        manage_text = T('The theme inherits styles from the parent theme chosen, and sets its specific by hot linking to the stylesheet url given, overwriting parent\' style, and/or creating new ones.')
        
        if len(request.args)>1:
            name = request.args[1]
            theme = utilities.get_from_app_themes(name)
            if theme:
                if  theme.find(utilities.theme_sep_token)>0:
                    db.app_themes.id.default = -10
                    db.app_themes.theme_name.default = name
                    db.app_themes.theme_base.default = utilities.get_from_theme('base', name=None, theme=theme)
                    db.app_themes.theme_stylesheet_url.default = utilities.get_from_theme('stylesheet', name=None, theme=theme)
                else:
                    response.flash = T('Base themes are not editable')
            else:
                response.flash = T('Theme not found')

        db.app_themes.theme_editor.default = auth.user.email

        form = SQLFORM(db.app_themes, deletable=True)
        if form.accepts(request.vars, session, dbio = False):
            def get_theme(f_v):
                return ('%(name)s%(token)s%(base)s%(token)s%(stylesheet)s%(token)s%(author)s' % 
                        dict(
                           name=f_v.theme_name,base=f_v.theme_base,
                           stylesheet=f_v.theme_stylesheet_url,
                           author=auth.user.email,token=utilities.theme_sep_token)
                )
            theme = None
            error = False
            for i in range(len(app_config.APP_THEMES)):
                t = utilities.get_from_theme('name', theme=app_config.APP_THEMES[i])
                if t == form.vars.theme_name:
                    if (utilities.get_from_theme('author', theme=app_config.APP_THEMES[i]) !=auth.user.email
                        and utilities.get_from_theme('stylesheet', theme=app_config.APP_THEMES[i]) !=form.vars.theme_stylesheet_url):
                        response.flash = T('This theme name is already in use.')
                        error = True
                    else:
                        app_config.APP_THEMES[i] = get_theme(form.vars)
                        theme = t
                        
            if not theme and not error:
                theme = get_theme(form.vars)
                app_config.APP_THEMES.append(theme)
                
            if theme:
                db(db.app_config.id == app_config.id).update(APP_THEMES = app_config.APP_THEMES)
                session.flash = T('Theme saved. Click here to test it: %(url)s', 
                                dict(url=A(T('test %s' % form.vars.theme_name), 
                                _href=URL(r = request, args=request.args, vars=dict(theme=form.vars.theme_name))))
                                )
                redirect(URL(r = request, args = [request.args[0], form.vars.theme_name]))
    
        return dict(edit_form = form, manage_title=manage_title, manage_text=manage_text)
        
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

@auth.requires_login()
def upload():
    """ original code from http://www.google.be/search?sourceid=chrome&ie=UTF-8&q=host2py """
    form=SQLFORM(db.files, fields=['file'])
    if 'file' in request.post_vars:
        form.vars.filename = request.vars.file.filename
        form.vars.user = auth.user.id
    if form.accepts(request.vars): 
        response.flash='File uploaded'
    return dict(form=form)

@auth.requires_login()
def files():
    """ original code from http://www.google.be/search?sourceid=chrome&ie=UTF-8&q=host2py """
    db(db.files.id>0).update(user = auth.user.id)
    if 'del' in request.get_vars:
        db((db.files.user==auth.user.id)&(db.files.id==request.get_vars['del'])).delete()
        session.flash = T('File deleted')
        redirect(URL(r=request,c='default',f='files'))
    elif 'ren' in request.get_vars and request.get_vars['new'] != 'null':
        file = db((db.files.user==auth.user.id)&(db.files.id==request.get_vars['ren'])).select()[0]
        if request.get_vars['new'].find('.') == -1:
            filename = request.get_vars['new'] + '.' + file.filename.split('.').pop()
        else:
            filename = request.get_vars['new']
        db(db.files.id==file.id).update(filename=filename)
        session.flash = T('File updated')
        redirect(URL(r=request,c='default',f='files'))
    files=db(db.files.id>0).select(orderby=db.files.filename)
    return dict(files=files)

def file():
    """ original code from http://www.google.be/search?sourceid=chrome&ie=UTF-8&q=host2py """
    file = db(db.files.filename==request.args[0]).select()
    if len(file) > 0:
        request.args[0] = file[0].file
        return response.download(request,db)
    else:
        return
        
def json():
    area=request.args[0]    
    return response.json({
        'status' : 1,
        'message' : 'done',
        'result' : get_app_objects(area)
    })
    
@service.jsonrpc
def get_app_objects(what):
    return {
        'pages' : lambda x: db(db.posts.post_type=='page').select(),
        'themes' : lambda x: app_config.APP_THEMES
    }.get(what, None)(what)

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
    try:
        if request.args[0]=='logout':
            session.user_authorization_done=False
    
        session._next = request.vars._next
        if auth.user:
            _next = request.vars._next
            if session._next:
                _next = session._next
                del session._next
            if _next:
                redirect(_next)
        return dict(form=auth())
    except Exception, ex:
        log_wrapped('Error (%s/controllers/default/user)' % this_app, ex)
        redirect(URL(r=request, f='user', args=['login']))


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
    if auth.user.is_admin:
        if request.args[0] in ['posts_app', 'links_app']:
            instance=db.posts if request.args[0]=='posts_app' else db.links
            _ids=request.args[1].split(',')
            log_wrapped('_ids', _ids)
            for i in range(len(_ids)):
                try:
                    db(instance.id == int(_ids[i])).update(application=request.application)
                except Exception, ex:
                    pass
            session.flash=T('%(inst)s application updated.', dict(inst=str(instance)))

        elif request.args[0] in ['set_login_mechanism']:
            db(db.app_config.id>0).update(
                    APP_SECURITY_DETAILS = request.vars.APP_SECURITY_DETAILS.split(','),
                    RPX_API = ['b9727a23b1d6ab8d29d112eb0f95ed1368f29c1f' if i==0 else RPX_API[i] for i in range(len(RPX_API))])
            session.flash=T('login mechanism updated.')

        elif request.args[0] in ['update_searchable_entities']:
            searchable_entities = request.vars.searchable_entities.split(',')
            for i in searchable_entities:
                db(db.entities.id==int(i)).update(
                    searchable_through=request.vars.searchable_through.split(','))                    
            session.flash=T('update searchable entities done.')
    else:
        session.flash=T('not admin')

    redirect(URL(r = request,f = 'index'))
