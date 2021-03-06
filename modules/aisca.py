#!/usr/bin/env python 
# coding: utf8 
from types import *
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!


###################################
## CLASSES
###################################    

###################################
## METHODS
###################################

###################################
## CONTROLLER INIT
###################################    
def controller_init(request, response, session, cache, T, db, auth, app_objects):
    app_details = app_objects.details
    app_config = app_objects.config
    log_wrapped = app_objects.log_wrapped
    utilities = app_objects.utilities
    
    is_page_request = request.function in ['index', 'read']
    link_title = None
    link_id = None
    if request.function == 'index':
        link_title = 'a_home'
    if len(request.args)>0 and is_page_request:
        link_title = request.args[0]        
    if link_title:
        link_id = filter(lambda x:x[0]==link_title,response.links)
        if link_id: link_id=link_id[0][2]

    # Navigation & history
    n_hi = None
    if not session.nav_history:
        session.nav_history = []
    if is_page_request:
        if len(session.nav_history)>2:
            session.nav_history = session.nav_history[1:]
        if link_id:
            n_hi = utilities.get_link_hierarchy(link_id)
        else:
            n_hi = [app_objects.path_info]
            
        if not n_hi in session.nav_history:
            session.nav_history.append(n_hi)

    if n_hi: n_hi.reverse()
    if n_hi and len(n_hi)>1 and n_hi[0]!=n_hi[1]:
        lt_f = filter(lambda x:x[0]==n_hi[0],response.links)
        if lt_f: link_title=lt_f[0][0]
    
    # Menu order, Menu items...
    menu_order=app_objects.menu_order
    link_menu_items = map(lambda x:[x[0], x[0].lower() == link_title, x[1]],
                        filter(lambda x:x[0].lower() in menu_order, response.links))

    menu_items = []
    for i in range(len(link_menu_items)):
        if i<len(menu_order):
            _title=menu_order[i]
            item=filter(lambda x: x[0].lower()==str(_title).lower(), link_menu_items)
            if len(item)>0:
                link_menu_items.remove(item[0])
                menu_items.append(item[0])
    response.menu=menu_items
            
    # instances
    page_helper=app_objects.page_helper
    post_helper=app_objects.post_helper
    
    # home page
    _home_page=app_objects.home_page_link(response, page_helper, response.links, request, T, app_objects)
    response.home_page=_home_page[0] if (_home_page and len(_home_page)>0) else None

    # help page
    _help_page=app_objects.help_page_link(response, page_helper, response.links, request, T, app_objects)
    response.help_page=_help_page[0] if (_help_page and len(_help_page)>0) else None

    # theme (refactoring: same in common.py)
    response.theme = 'aisca'
    if request.vars.theme:
        if request.vars.theme.find(app_details.theme_sep_token)>0: 
            response.cookies['theme'] = utilities.get_from_theme('name', theme_sstruct=request.vars.theme)
        else:
            response.cookies['theme'] = request.vars.theme
        response.cookies['theme']['expires'] = 365 * 24 * 3600
        response.cookies['theme']['path'] = '/'
        response.theme = response.cookies['theme'].value
            
    elif request.cookies.has_key('theme'):
        response.theme = request.cookies['theme'].value
        
    return page_helper, post_helper
