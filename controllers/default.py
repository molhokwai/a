###################################
## CONTROLLER INITIALIZATION
###################################

try:
    exec('from applications.%s.modules import common' % this_app)
    app_objects=Struct(**{'details':app_details,'config':app_config,'log_wrapped':log_wrapped})
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)    
except Exception, ex:
    log_wrapped('Er', ex)


###################################
## CONTROLLER FUNCTIONS
###################################

# The main page
# Shows the home page if one created (see 'home_page' function page with title)
# Otherwise, defaults to showing the first 10 posts
def index():
    if len(request.args)==0:
        if response.home_page:
            redirect(URL(r=request, c='default', f='page', args=[response.home_page.id]))
        else:
            redirect(URL(r=request, c='setup'))
    else:
      if a_convert.to_int(request.args[0]):
          return dict(posts = db(db.posts.id == int(request.args[0])).select())
      else:
          posts=db(db.posts.post_title == request.args[0]).select()
          if not posts:
              posts = response.posts.filter(lambda x: x.post_title.lower().find(request.args[0].lower())>0)
          return dict(posts = posts)
          
      

# The post page
# Shows the entire post, the comments, and the comment form
def post():
    #try: 
    post_id = int(request.args[0])
    post = db(db.posts.id == post_id).select()[0]
    
    if post and post.auth_requires_login and not auth.user:
        redirect(URL(r = request, f = 'user', args = ['login']))

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
                    post = response.pages.filter(lambda x: x.post_title.lower().find(request.args[0].lower())>0)
                if post: post=post[0]
                
            if post and post.auth_requires_login and not auth.user:
                redirect(URL(r = request, f = 'user', args = ['login']))
                
            
            nake=(request.args[len(request.args)-1]=='nake'
                 or post.post_text.find('<!-- nake page -->')>=0)
        
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
    return dict(manage_title=T("pages"))

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
                                                    'post_category', 'is_translated', 'auth_requires_login'], 
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
    # p_a_c_i_o_val : page attr. content is orginal value
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
                                                            'post_category', 'is_translated', 'auth_requires_login'], 
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

        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
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
    log_wrapped('1', 1)
    if request.args[0] in ['posts_app', 'links_app']:
        log_wrapped('2', 2)
        instance=db.posts if request.args[0]=='posts_app' else db.links
        _ids=request.args[1].split(',')
        log_wrapped('_ids', _ids)
        for i in range(len(_ids)):
            try:
                db(instance.id == int(_ids[i])).update(application=request.application)
            except Exception, ex:
                pass
        session.flash=T('%(inst)s application updated.', dict(inst=str(instance)))
    
    redirect(URL(r = request,f = 'index'))
