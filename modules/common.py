#!/usr/bin/env python 
# coding: utf8 
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

###################################
## CLASSES
###################################    
# page helper
class PageHelper():
    _title=''
    def get_page_by_title(self,item):
        return item.post_title.lower()==self._title

###################################
## METHODS
###################################
def app_init(request, response, session, cache, T, db, app_objects):
    app_details = app_objects.details
    app_config = app_objects.config
    log_wrapped=app_objects.log_wrapped

    if not response.auth_users:
        response.auth_users=db().select(db.auth_user.ALL)
    
    """Application first run initialization"""
    for au in response.auth_users:
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
        p_home_k=app_details.init_app_config['pages']['home_k']
        p_help_k=app_details.init_app_config['pages']['help_k']
        initial_posts=[
            p_home_k,
            p_help_k,
            'acknowledgements'
        ]
        for i in range(len(initial_posts)):
            post_title=initial_posts[i]            
            if not db(db.posts.post_title==post_title).select():
                post_text=app_details.init_app_config['pages'][post_title]
                db.posts.insert(
                    post_type='page',
                    post_title=post_title,
                    post_text=post_text,
                    show_in_menu=True
                )
        initial_links={
            'media / picasa / gallery'                           : '/%s/media/picasa/gallery' % request.application,
            'manage media / manage picasa albums / manage photos': '/%s/media/picasa/albums' % request.application,
            'setup, application initialization'                  : '/%s/setup' % request.application
        }
        for link_title in initial_links:
            if not db(db.links.link_title==link_title).select():
                link_url=initial_links[link_title]
                db.links.insert(
                    link_title=link_title,
                    link_url=link_url
                    )
    except Exception, ex:
        log_wrapped('Exception', ex)
        session.flash=T("Error occured: %(err)s ", dict(err=str(ex)))

def get_usr_display_name(usr):
    display_name=usr.preferredUsername
    if display_name is None or display_name=='':
        display_name=usr.first_name
    if display_name is None or display_name=='':
        display_name=usr.last_name
    return display_name

def user_authorization(request, response, session, cache, T, db, auth):
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

def home_page(response, page_helper, _pages, request, T):
    """gets the home page, if one created.
        Convention over configuration: Home page is the one with title T('%s_home' % request.application),
        The corresponding eventual language translation of 'home'.
        
        TODO: as proprty in a configuration framework (see if pypress4gae offers home/index page
        configuration, and if so eventually switch to it)
    """
    if response.menu:
        page_helper._title=T('%s_home' % request.application)
        return filter(page_helper.get_page_by_title,_pages)

def help_page(response, page_helper, _pages, request, T):
    """Gets the help page, if one created
        See home_page
    """
    if response.menu:
        page_helper._title=T('%s_help' % request.application)
        return filter(page_helper.get_page_by_title,_pages)


###################################
## CONTROLLER INIT
###################################    
def controller_init(request, response, session, cache, T, db, auth, app_objects):
    app_details = app_objects.details
    app_config = app_objects.config
    log_wrapped = app_objects.log_wrapped

    if not response.auth_users:
        response.auth_users=db().select(db.auth_user.ALL)
    
    # This sets the session authorization values
    if (not auth.user is None and not session.user_authorization_done):
        user_authorization(request, response, session, cache, T, db, auth)
        session.user_authorization_done=True
    
    if auth.user and (auth.user.display_name is None or auth.user.display_name==''):
        display_name=get_usr_display_name(auth.user)
        if display_name is None or display_name =='':
            display_name='anonymous@molhokwai.net'
        auth.user.display_name=display_name
    
    response.title = app_details.title
    response.keywords = app_details.keywords
    response.description = app_details.description

    # All posts
    response.posts = db().select(db.posts.ALL)
    
    # This dynamically adds the pages to the menu
    _pages = []
    try:
        _pages = db((db.posts.post_type == 'page') &
                    ((db.posts.application == request.application) | 
                    (db.posts.application == None))
                    ).select(db.posts.ALL)
    except Exception, ex:
        _pages = db(db.posts.post_type == 'page').select(db.posts.ALL)
        
    items=[]
    menu_items = []
    for page in _pages:
        item = [page.post_title, False, '/%(app)s/default/page/%(id)s' % {'app':request.application, 'id':page.id}]
        items.append(item)
        if page.show_in_menu and len(menu_items)<10:
          menu_items.append(item)
    response.pages = items
    
    # Menu order, Menu items...
    menu_order=[ T('Home'), T('Mission'), T('Vision'), T('Community'), T('Work') , T('Books') ]
    
    page_menu_items=[]
    for i in range(len(menu_items)):
        if i<len(menu_order):
            _title=menu_order[i]
            item=filter(lambda x: x[0].lower()==str(_title).lower(), menu_items)
            if len(item)>0:
                menu_items.remove(item[0])
                page_menu_items.append(item[0])
    response.menu=page_menu_items
            
    # instance
    page_helper=PageHelper()
    post_helper=PageHelper()
    
    # home page
    _home_page=home_page(response, page_helper, _pages, request, T)
    response.home_page=_home_page[0] if (_home_page and len(_home_page)>0) else None

    # help page
    _help_page=help_page(response, page_helper, _pages, request, T)
    response.help_page=_help_page[0] if (_help_page and len(_help_page)>0) else None
        
    # This returns all the categories and their post count
    cats = db().select(db.categories.ALL)
    items = []
    for cat in cats:
        count = 0
        try:
            count = len(db(
                           (db.posts.post_type == 'post') & 
                           (db.posts.post_category == cat.id) &
                           ((db.posts.application == request.application) | 
                           (db.posts.application == None))
                           ).select(db.posts.ALL)) #,orderby=~db.posts.post_time
        except Exception, ex:
            count = len(db(
                           (db.posts.post_type == 'post') & 
                           (db.posts.post_category == cat.id)
                           ).select(db.posts.ALL)) #,orderby=~db.posts.post_time
        if count > 0:
            item = [cat.category_name, count, '/%(app)s/default/category/%(name)s' % {'app':request.application, 'name':cat.category_name}]
            items.append(item)
    response.categories = items
    
    # This returns all the links
    links = []
    try :
        links = db(((db.links.application == request.application) | 
                    (db.links.application == None))
                  ).select(db.links.ALL)
    except:
        links = db().select(db.links.ALL)
    items = []
    for link in links:
        item = [link.link_title, link.link_url, link.id]
        items.append(item)
    response.links = items
    
    # Theme
    response.themes=['0', '1','cms']
    if app_config and app_config.APP_THEMES:
        response.themes=app_config.APP_THEMES
        
    if request.vars.theme:
        response.cookies['theme'] = request.vars.theme
        response.cookies['theme']['expires'] = 365 * 24 * 3600
        response.cookies['theme']['path'] = '/'
    
    response.theme = '0'
    if request.application in response.themes:
        response.theme = request.application

    if request.vars.theme:
        response.theme = request.vars.theme
    elif request.cookies.has_key('theme'):
        response.theme = request.cookies['theme'].value

    return page_helper, post_helper
