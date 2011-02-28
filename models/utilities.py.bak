# coding: utf8

#########################################################################
## APPLICATION DETAILS, COMMON'Z & UTILITIES
#########################################################################

p_help_k=T('%(app)s_help', dict(app=request.application))
p_home_k=T('%(app)s_home', dict(app=request.application))
class AppDetails():
    name = T("'a' cm/dms"), 
    title = T("molhokwai.net - 'a' cm/dms"), 
    keywords = T("blog, weblog, journal, web, log, web2py, pypress, cms, dms, simple, lightweight, straight-forward, direct, programming, programmer"),
    description = T("molhokwai.net - 'a' cm/dms, lightweight, simple, straight & direct")
    themes_base_list = app_themes_base_list
    init_app_config = {
        'pages' : {
            'help_k' : T('%(app)s_help', dict(app=request.application)),
            'home_k' : T('%(app)s_home', dict(app=request.application)),                                
            p_help_k : """
                Dbl Ctrl to access <i>command line</i> <small>(css-ly removed outline makes cursor faintly visible in chrome, but it's there)</small>
                <br/>
                <br/>
                <br/>
                --------------------------------------------------------------------------------------------<br/>
                Add links to pages to access the pages from the command line
                --------------------------------------------------------------------------------------------<br/>
                login <br/>
                logout <br/>
                add <br/>
                edit <br/>
                delete <br/>
                submit <br/>
                pages <br/>
                links <br/>
                root <br/>
                help <br/>
                <br/>
                <br/>
                --------------------------------------------------------------------------------------------<br/>
                idem, translated in available languages
            """,
            p_home_k : """
                <b>Command line interface<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<small>command based human machine interface basic cms</small>...
                <br/>
                <br/>
                Dbl Ctrl to access <i>command line</i> <small>(css-ly removed outline makes cursor faintly visible in chrome, but it's there)</small><br/>
                &nbsp;&nbsp;&nbsp;&nbsp;<small>*<b>eventually</b>, if the page has elligible primary content, search falls back on <img src="http://www.google.com/uds/css/small-logo.png" alt="Google(reg)"> search 
                if no <i>internally found</i> response</small>.<br/>
                --------------------------------------------------------------------------------------------
                <br/>
                <br/>
                login <br/>
                logout <br/>
                add <br/>
                edit <br/>
                delete <br/>
                submit <br/>
                pages <br/>
                links <br/>
                root <br/>
                help <br/>
                <br/>
                <br/>
                --------------------------------------------------------------------------------------------<br/>
                Add links to pages to access them from the command line<br/>
                --------------------------------------------------------------------------------------------<br/>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
                --------------------------------------------------------------------------------------------<br/>
                idem, translated in available languages            
            """,
            'acknowledgements' : """
                <ul>
                  <li><a href="http://www.web2py.org">web2py</a></li>
                  <li><a href="http://code.google.com/appengine">google app engine</a></li>
                  <li><a href="http://python.org">python</a></li>
                  <li><a href="http://jquery.org">jquery</a></li>
                  <li><a href="http://www.google.be/search?sourceid=chrome&amp;ie=UTF-8&amp;q=pypress">pypress</a></li>
                  <li><a href="http://www.google.be/search?sourceid=chrome&amp;ie=UTF-8&amp;q=pypress#sclient=psy&amp;hl=nl&amp;source=hp&amp;q=acknowledgements:everything+up+to+now&amp;aq=f&amp;aqi=&amp;aql=&amp;oq=&amp;gs_rfai=&amp;pbx=1&amp;psj=1&amp;fp=1eb96132f70894e9">...</a> </li>
                </ul>
                <br>
                <p class="text-alignr font-size09em italic width60pc">(if you find there is missing acknowledgedment, an e-mail to <a href="mailto:admin@molhokwai.net" title="[GMCP] Compose a new mail to admin@molhokwai.net" 
                onclick="window.open('https://mail.google.com/mail/?view=cm&amp;fs=1&amp;tf=1&amp;to=admin@molhokwai.net','Compose new message','width=640,height=480');return false" rel="noreferrer">admin@molhokwai.net</a> 
                is more than welcome)"</p>                
            """
        }
    }
app_details=AppDetails()
if app_config and app_config.APP_METAS:
    if len(app_config.APP_METAS)>0: app_details.name=app_config.APP_METAS[0]
    if len(app_config.APP_METAS)>1: app_details.title=app_config.APP_METAS[1]
    if len(app_config.APP_METAS)>2: app_details.keywords=app_config.APP_METAS[2]
    if len(app_config.APP_METAS)>3: app_details.description=app_config.APP_METAS[3]
        
class aConvert():
    def to_int(self, value):
        """Attention: Eventually returns 0 which 'equals' the False ValueError return"""
        try:
            return int(value)
        except ValueError:
            return False
a_convert=aConvert()

# session manager
class SessionManager():
    @property
    def default_page(self):
        return '/%s/company/index' % this_app

    def company_id(self,value=None):
        if not value is None:
            session.company_id=value
        if session.company_id:
            args={ 'icon_url' : db(db.companies.id==session.company_id).select()[0].icon_url }
            company=Struct(**args)
        return session.company_id
        
    def user_is_in_company(self, company_id=None):
        ## TODO: method in company management class, and this session_manager calling it...
        if company_id is None:
            company_id=self.company_id()
        if not auth.user: 
            return False
        else:
            res=db(db.companies.user==auth.user.id).select()
            return len(res)>0
# instance
session_manager=SessionManager()

# common
class Common():
    """def get_small_icon_url(self, icon_url):
        _segs=icon_url.split('.')
        _ext=_segs[len(_segs)-1]
        return icon_url.replace('.%s' % _ext,'_small.%s' % _ext) 
    """    
    def get_shortened_text(self, _text, _max):
        if len(_text)>_max:
            return '%s...' % _text[:(_max-3)]
        else:
            return _text
                            
    def redirect(self, url):
        """in case of redirection to an inner frame"""
        inner_frames_args=['page-box', 'side-box', 'frame-box', 'is_iframe']
        for ifa in inner_frames_args:
            if url.lower().find(ifa.lower())>0:
                redirect(session_manager.default_page)
                break        
        redirect(url)

    def get_embed(self, provider, media_key, width=425, height=344):
        embed=None
        if provider=='youtube':
            embed='    <object width="%(width)i" height="%(height)i">'
            embed+='      <param name="movie" value="http://www.youtube.com/v/%(media_key)s?fs=1"></param>'
            embed+='      <param name="allowFullScreen" value="true"></param>'
            embed+='      <param name="allowScriptAccess" value="always"></param>'
            embed+='      <embed src="http://www.youtube.com/v/%(media_key)s?fs=1"'
            embed+='      type="application/x-shockwave-flash"'
            embed+='      allowfullscreen="true"'
            embed+='      allowscriptaccess="always"'
            embed+='      width="%(width)i" height="%(height)i">'
            embed+='      </embed>'
            embed+='   </object>'
        return embed % {'width':width, 'height':height, 'media_key':media_key}
        
#instance
common=Common()

# utilities
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

# utilities
class Utilities():
    def reverse_numeric_row_id(self, x, y):return y.id - x.id

    def shorten_and_randomize(self, _list, nr):
        import random
        random.shuffle(_list)
        if len(_list)>nr:
            return _list[:nr]
        else:
            return _list        

    def set_cookie(self, name, value):
        response.cookies[name] = value
        response.cookies[name]['expires'] = 365 * 24 * 3600
        response.cookies[name]['path'] = '/'

    def get_cookie(self, name):
        if request.cookies.has_key(name):
            return request.cookies[name]

    theme_sep_token = '#:#'
    def get_from_app_themes(self, name):
        theme = filter(lambda x: x.split(self.theme_sep_token)[0] == name, app_config.APP_THEMES)
        if theme and len(theme)>0:
            return theme[0]
    
    def get_from_theme(self, what, name=None, theme=None):
        if not name is None:
            theme = self.get_from_app_themes(name)
        whats = {'name':0, 'base':1, 'stylesheet':2, 'author':3}
        return theme.split(self.theme_sep_token)[whats[what]]
    
    def get_base_of_theme(self, name):
        if name in app_details.themes_base_list:
            return name
        else:
            theme_base = self.get_from_theme('base', name=name)
            return self.get_base_of_theme(theme_base)

# instance
utilities=Utilities()

########################
## Print, Log Wrapper
########################

def print_wrapped(_name, _value):
    print '-------| %s : %s' % (repr(_name), repr(_value))

def log_wrapped(_name, _value):
    if request.env.web2py_runtime_gae:
        import logging
        logging.info('-------| %s : %s' % (repr(_name), repr(_value)))
    else:
        print_wrapped(_name, _value)
        
#########################################################################
## from : http://bytes.com/topic/python/answers/592479-regex-url-extracting
#########################################################################
expressions={
  'url_find' : [
"([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]",
"([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?",
"(~/|/|\\./)([-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]|\\\\)+",
"'\\<((mailto:)|)[-A-Za-z0-9\\.]+@[-A-Za-z0-9\\.]+"
  ],
  'rel_url_and_end_tags_find' : ["[0-9]{0,1}/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]"]
}

import re
url_finders = [
re.compile(expressions['url_find'][0]),
re.compile(expressions['url_find'][1]),
re.compile(expressions['url_find'][2]),
re.compile(expressions['url_find'][3]),
]
rel_url_and_end_tags_finders = [
re.compile(expressions['rel_url_and_end_tags_find'][0]),
]
