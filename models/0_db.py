#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client    
    # session.connect(request, response, db=MEMDB(Client()))
    
    ### cache in ram
    from gluon.contrib.gae_memcache import MemcacheClient
    from gluon.contrib.memdb import MEMDB
    cache.memcache = MemcacheClient(request)
    cache.ram = cache.disk = cache.memcache
else:                                         # else use a normal relational database
    db=SQLDB("sqlite://db.db")


#################################
## APPLICATION CONFIG
#################################

## Administrators
administrators_emails=['molhokwai@gmail.com', 'herve.mayou@gmail.com', 'herve.m@molhokwai.net', 'herve.mayou@ymail.com', 'herve.mayou@yahoo.com']

## Table app config
app_theme_sep_token = '-:-'
app_themes_base_list = ['name:0%(tsk)ssidebar:a'%dict(tsk=app_theme_sep_token), 'name:1%(tsk)ssidebar:a'%dict(tsk=app_theme_sep_token), 
            'name:cms%(tsk)ssidebar:cms'%dict(tsk=app_theme_sep_token), 'name:ff0000%(tsk)ssidebar:ff0000'%dict(tsk=app_theme_sep_token), 'name:pypress%(tsk)ssidebar:pypress'%dict(tsk=app_theme_sep_token)]
app_modules_config = {
    'request_handling' : {
        'instruction' : {
            'keywords'  : {
                'action' : {
                    'create' : [T('create'), T('add'), T('read'), T('select')],
                    'read' : [T('read'), T('view'), T('show'), T('display'), T('select')],
                    'update' : [T('edit'), T('modify'), T('update'), T('change')],
                    'delete' : [T('delete'), T('remove'), T('suppress')]
                },
                'object' : {
                    'group' : [T('pages'), T('site'), T('site-section')],
                    'page' : [T('page'), T('view'), T('template')],
                    'block' : [T('block'), T('page-section'), T('container')],
                    'element' : [T('element'), T('control')]
                }
            }
        }
    }
}
db.define_table('app_config',
    SQLField('APP_DETAILS',             'list:string', required=True,    default=['<molhokwai.net-a>', '<v001>'],     
            label=T('App details (name, version)')),
    SQLField('APP_SECURITY_DETAILS',             'list:string', required=True,    default=['rpx'],     
            label=T('App security details (login mechanism)')),
    SQLField('RPX_API',                 'list:string', required=True,    default=['<XXXXXXXXXXXXX>', '<websites.molhokwai>'],    
            label=T('Rpx api (key, sub-domain)')),
    SQLField('APP_CURRENT_LANGUAGES',   'list:string', required=True,    default=['en', 'he', 'hi', 'es', 'fr', 'sw'], 
            label=T('Languages')),
    SQLField('APP_METAS',               'list:string', required=True,    default=['<title>', '<web, utility, application, software, cms, dms>', '<description>'],  
            label=T('App Metas (title, keywords, description)')),
    SQLField('APP_THEMES',               'list:string', required=True,    default=app_themes_base_list,
            label=T('Themes')),
    SQLField('MAIL_SETTINGS',           'list:string',                   default=['<sender@gmail.com>', '<smtp.gmail.com:587>', '<username:password>'],
            label=T('Mail settings (sender, server, login)')),           
    SQLField('PICASA_API',              'list:string',                   default=['<username>', '<password>'],
            label=T('Picasa api (username, password)')),
    SQLField('TWITTER_API',              'list:string',                  default=['<username>', '<password>', '<hashes>'],
            label=T('Twitter api (username, password, hashes -csv, filters -csv)')),
    SQLField('BLOGGER_API',              'list:string',                  default=['<username>', '<password>', '<source>'],
            label=T('Blogger api (username, password, source)')),
    SQLField('BLOGGER_BLOGS_THEMES',     'list:string',                  default=['<theme1:blog1,blog2,blog3...>', '<theme2:blog4,blog5...>', '<theme3:blog6...>'],
            label=T('Blogger blogs themes')),
    SQLField('BLOGGER_BLOGS_LANGUAGES',  'list:string',                  default=['<fr:blog3,blog4,blog6...>', '<nl:blog1,blog1...>', '<en:blog5...>'],
            label=T('Blogger blogs languages')),
    SQLField('APP_MODULES_DETAILS',             'text',         required=True,    default=str(app_modules_config),
            label=T('App modules details (request_handling proxy, ...)'))
)

app_themes_list = app_themes_base_list

app_config=db(db.app_config.id>0).select()
if len(app_config)>0:
    app_config=app_config[0]
    if app_config.APP_THEMES and len(app_config.APP_THEMES)>0:
        app_themes_list = app_config.APP_THEMES
else:
    app_config = None

db.define_table('app_themes',
    SQLField('theme_name', 'string', required=True, label=T('Theme name')),
    SQLField('theme_base', 'string', required=True, label=T('Based on')),
    SQLField('theme_stylesheet_url', 'string', required=True, label=T('Stylesheet url')),
    SQLField('theme_editor', 'string', required=True, writable=False, label=T('Author/editor'))
)
db.app_themes.theme_name.requires = IS_ALPHANUMERIC()
db.app_themes.theme_stylesheet_url.requires = IS_URL()
db.app_themes.theme_base.requires = IS_IN_SET(app_themes_list)

#########################################################################
## Global convenience variables
#########################################################################
refresh_page = False

protocol = 'http'
if request.get('env')['server_protocol'][:5] == 'HTTPS': protocol='https'
global_site_url = '%s://%s' % (protocol,request.get('env')['http_host'])
path_info = request.get('env')['path_info']
full_url = '%s%s' % (global_site_url, path_info)
http_referer = None

this_app = path_info.split('/')[1]
this_app_url= global_site_url + '/%s' % this_app
tentative_app = session.tentative_app
if 'http_referer' in request.get('env'):
    import re
    http_referer = request.get('env')['http_referer']
    m = re.match('%s.*'%global_site_url, http_referer)
    if m:
        session.tentative_app = http_referer.replace(global_site_url, '').split('/')[1]
if session.tentative_app:
    if tentative_app != session.tentative_app:
        try: cache.ram.flush_all()
        except Exception, ex: pass
        refresh_page = True
    else:
        tentative_app = session.tentative_app
elif not tentative_app:
    tentative_app = this_app



#########################################################################
## Authentication / Authorization
#########################################################################
from gluon.tools import *
auth=Auth(globals(),db)              # authentication/authorization
crud=Crud(globals(),db)              # for CRUD helpers using auth
service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc

mail=Mail()                                                   # mailer
if app_config and app_config.MAIL_SETTINGS:
    mail.settings.server=app_config.MAIL_SETTINGS[0]     # your SMTP server
    mail.settings.sender=app_config.MAIL_SETTINGS[1]     # your email
    mail.settings.login=app_config.MAIL_SETTINGS[2]       # your credentials or None
else:
    if request.env.web2py_runtime_gae:            # if running on Google App Engine
        mail.settings.server='gae'     # your SMTP server
        mail.settings.login=None       # your credentials or None
    else:   
        mail.settings.server='smtp.gmail.com:587'     # your SMTP server
        mail.settings.login='xxxxxxxxxxxxx'       # your credentials or None
        mail.settings.sender='molhokwai@gmail.com'    # your email

# auth.settings.hmac_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
auth.settings.hmac_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
if app_config and app_config.APP_SECURITY_DETAILS and app_config.APP_SECURITY_DETAILS[0].lower() == 'rpx':
    auth.settings.table_user = db.define_table('auth_user',
        Field('registration_id', length=512,
              label=T('registration id'),
              requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'auth_user.registration_id')],
              readable=False),
        Field('display_name', length=512,
              label=T('display name'),
              requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'auth_user.display_name')]),
        Field('email', length=512,default='',
              label=T('email'),
              requires = [IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email')]),
            Field('password', label=T('password')),
        Field('is_admin', 'boolean',default=False),
        Field('is_anonymous', 'boolean',default=True),
        Field('registration_key'),
        Field('first_name'),
        Field('last_name')
    )
else:
    auth.settings.table_user = db.define_table('auth_user',
        # this field is here for identical auth_table structure for
        # the different login mechanisms
        Field('registration_id', length=512,
              label=T('registration id'), readable=False, writable=False),
            Field('display_name', length=512,
                      label=T('display name'),
                      requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'auth_user.display_name')]),
            Field('email', length=512,default='',
                      label=T('email'),
                      requires = [IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email')]),
            Field('password', label=T('password')),
            Field('is_admin', 'boolean',default=False,readable=False, writable=False),
            Field('is_anonymous', 'boolean',default=True,readable=False, writable=False),
            Field('registration_key', readable=False, writable=False),
            Field('first_name'),
            Field('last_name')
    )   


auth.define_tables()                 # creates all specified & needed tables


auth.settings.mailer = mail                    # for user email verification
if app_config and app_config.APP_SECURITY_DETAILS and app_config.APP_SECURITY_DETAILS[0].lower() == 'usr_psw':
    auth.settings.registration_requires_verification = False
    auth.settings.registration_requires_approval = False
    auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
    auth.settings.reset_password_requires_verification = True
    auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

## OpenID, Facebook, MySpace, Twitter, Linkedin, etc. registration
protocol='http'
if request.get('env')['server_protocol'][:5]=='HTTPS':protocol='https'

if app_config and app_config.APP_SECURITY_DETAILS and app_config.APP_SECURITY_DETAILS[0].lower() == 'rpx':
    from gluon.contrib.login_methods.rpx_account import RPXAccount
    auth.settings.actions_disabled=['register','change_password','request_reset_password']
    if app_config and app_config.RPX_API:
        auth.settings.login_form = RPXAccount(request, api_key=app_config.RPX_API[0],
            domain=app_config.RPX_API[1],
            url = "%s/default/user/login" % this_app_url)
    else:
        auth.settings.login_form = RPXAccount(request, api_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            domain='websites-molhokwai',
            url = "%s/default/user/login" % this_app_url)

############
## Language
############
current_language='en'
if app_config and app_config.APP_CURRENT_LANGUAGES:
    T.current_languages=app_config.APP_CURRENT_LANGUAGES
    current_language=app_config.APP_CURRENT_LANGUAGES[0]
else:
    T.current_languages=['en','fr']

if request.vars._language:
    session._language=request.vars._language

if session._language:
    current_language = session._language
else:
    if T.http_accept_language:
        current_language=T.http_accept_language
        
if len(current_language)>2:
    current_language = current_language[:2]
T.force('l-l'.replace('l',current_language))

if not session._language:
    session._language = current_language

import datetime

## Table posts
## Fields:
## ------
##    post_text_TCode: To enter a translation code and fill in the translation texts in a way compliant with
##        the built-in translation mechanism (T).
##        ***Only one of the post_text_TCode and the post_text fields is necessary.***
##        The system first checks the *post_text_TCode* field and if not filled in, falls back to the *post_text* field
##    is_translated: if the translation (whether for the post_text, or the post_text_TCode) is done in all the languages 
##        available in the application). To be manually set once the translation in all languages for the post/page is done.
db.define_table('categories',
    SQLField('category_name', required=True))

db.define_table('posts',
    SQLField('post_title', required=True),
    SQLField('post_text', 'text'),
    SQLField('post_text_TCode', 'string',  writable=True),
    SQLField('post_time', 'datetime', default=datetime.datetime.today()),
    SQLField('post_type', required=True),
    SQLField('post_category', required=True, default=-1),
    SQLField('post_parent', required=False, default=-1),
    SQLField('show_in_menu',  'boolean', required=True, default=False),
    SQLField('is_translated', 'boolean', required=True, default=False),
    SQLField('application', 'string', default=request.application),
    SQLField('post_posts', 'list:string'),
    SQLField('auth_requires_login', 'boolean'),
    SQLField('post_attributes_json', 'text', required=True, 
            default="""{
                "content_is" : {
                    "original" : false
                }
            }""")
    )
db.posts.post_type.requires = IS_IN_SET(['post', 'page'])
db.posts.post_category.requires = IS_IN_DB(db, 'categories.id', 'categories.category_name')
db.posts.post_parent.requires = IS_IN_DB(db, 'posts.id', 'posts.post_title')

db.define_table('comments',
    SQLField('post_id', db.posts, required=True),
    SQLField('comment_author'),
    SQLField('comment_author_email', required=True),
    SQLField('comment_author_website'),
    SQLField('comment_text', 'text', required=True),
    SQLField('comment_time', 'datetime', required=True, default=datetime.datetime.today()))

db.define_table('posts_categories',
    SQLField('category', db.categories, required=True),
    SQLField('post', db.posts, required=True))
    
db.define_table('links',
    SQLField('link_title', required=True),
    SQLField('link_parent', required=False, default=-1),
    SQLField('link_url', required=True))
db.links.link_parent.requires = IS_IN_DB(db, 'links.id', 'links.link_title')

db.define_table('files',
    SQLField('file','upload', required=True, autodelete=True),
    SQLField('filename'),
    SQLField('user', required=True, readable=False, writable=False)
)
db.files.filename.requires = IS_NOT_IN_DB(db, 'files.filename')


post_labels = {
    'post_title':'Title',
    'post_text':'Post',
    'post_text_TCode':'Translation code (code & language texts must be set in the translation files)',
    'post_time':'Post Date',
    'post_type':'Type',
    'post_category':'Category',
    'show_in_menu':'Show in menu'
}

comment_labels = {
    'comment_author':'Name',
    'comment_author_email':'Email',
    'comment_author_website':'Website',
    'comment_text':'Comment',
    'post_id':'Post ID'
}

link_labels = {
    'link_title':'Name',
    'link_url':'URL'
}

cat_labels = {
    'category_name':'Name'
}

file_labels = {
    'file':'File',
    'filename':'Enter file name'
}
