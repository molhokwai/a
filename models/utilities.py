# coding: utf8
from types import *

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
    themes_list = app_themes_list
    theme_sep_token = app_theme_sep_token
    login_mechanism = app_config.APP_SECURITY_DETAILS if app_config and app_config.APP_SECURITY_DETAILS else 'usr_psw'
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

# service (for CSV, XML, JSON, XMLRPC, JSONRPC, AMF)
from gluon.tools import Service
service = Service(globals())

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

class obj_walk:
    @staticmethod
    def to_value(_obj, keys_indexes):
        """Example of Pattern: 
            {
             'a':
                [{'x' : []}, {'y' : ''}, {'z' : {}}...]
           }
        """
        _val = _obj
        for i in range(len(keys_indexes)):
            if ((type(keys_indexes[i]) == IntType and type(_val) == ListType)
              or type(_val) == DictType):
                    _val = _val[keys_indexes[i]]
            else:
                _val = None
        return _val
        
class dict_walk:
    @staticmethod
    def to_value(_dict, keys):
        return obj_walk.to_value(_dict, keys)
        
class Utilities():
    obj_walk = obj_walk()
    dict_walk = dict_walk()
    
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

    ## PAGES
    def is_current_page(self, pg_id_name):
        if len(request.args)>0:
            return str(request.args[0]) == str(pg_id_name)

    def get_page_hierarchy(self, pg_id):
        pg = db(db.posts.id == pg_id).select()[0]
        p_list = [pg.post_title]
        if pg.post_parent>0 and pg.post_parent!=pg_id:
            p_list += self.get_page_hierarchy(pg.post_parent)
        return p_list

    def get_link_hierarchy(self, l_id):
        l = db(db.links.id == l_id).select()[0]
        l_list = [l.link_title]
        if l.link_parent>0 and l.link_parent!=l_id:
            l_list += self.get_link_hierarchy(l.link_parent)
        return l_list
        
        
    ## THEMES
    @staticmethod
    def themes_by_what_what_filter(by_what, what, _themes=app_details.themes_list):
        return filter(lambda x: x.find('%s:%s' % (by_what, what))>=0, _themes) 

    @staticmethod
    def theme_by_what_what_filter(what, theme_sstruct):
        l = filter(lambda x: x.find(what)==0, theme_sstruct.split(app_details.theme_sep_token))
        if len(l)>0:
            return l[0].split(':')[1]        

    def get_themes_names(self, themes_list=app_details.themes_list):
        return map(lambda x: utilities.get_from_theme('name', theme_sstruct=x), themes_list)
    
    def get_from_app_themes(self, by_what, what_what):
        return utilities.themes_by_what_what_filter(by_what, what_what)[0]
    
    def get_from_theme(self, what, what_what=None, theme_name=None, theme_sstruct=None):
        # fix for legacy code lost somewhere
        if what_what and what_what.find(':')>0 : what_what = what_what.split(':')[1]
        if theme_name and theme_name.find(':')>0 : theme_name = theme_name.split(':')[1]

        if theme_sstruct is None:
            if not what_what is None:
                theme_sstruct = self.get_from_app_themes(what, what_what)
            elif not theme_name is None:
                theme_sstruct = self.get_from_app_themes('name', theme_name) 
            
        if not theme_sstruct is None:
            return utilities.theme_by_what_what_filter(what, theme_sstruct)
        elif what_what is None and theme_name is None:
            raise(Exception(T("""(models.utilies.py:Utilities.get_from_theme: one of these optional 
                                    parameters is required: theme_sstruct, what_what, theme_name""")))
            
    def get_base_of_theme(self, name):
        if name in self.get_themes_names(themes_list=app_details.themes_base_list):
            return name
        else:
            theme_base = self.get_from_theme('base', theme_name=name)
            return self.get_base_of_theme(theme_base) if theme_base else None

    ## SERVER SIDE OUTPUT
    def replace_serverside_output_values(self, _text, tag_re='\</*aservero\>'):
        b = re.findall(re.compile('<aservero>\w*?</aservero>'), _text)
        for c in b:
            _text = _text.replace(c, eval(re.sub('\</*aservero\>', '', c)))
        return _text

    def posts_replace_serverside_output_values(self, _posts, tag_re='\</*aservero\>'):
        for p in _posts:
            p.post_text = self.replace_serverside_output_values(x.post_text)
        return _posts

    ## REQUEST HANDLING
    def instructions_filter(self, instructions_type_name, module_config):
        return filter(lambda x: x[1]!=x[2] and not self.is_action(x, module_config), instructions_type_name)

    def instruction_type_subject(self, section, module_config):
        """
           Expects the module config list/dict format (see: app_modules_config)
            Returns:
                ['action'|'object'|'data'],section
        """
        for typ in ['action', 'object']:
            d = self.obj_walk.to_value(module_config, ['instruction', 'keywords', typ])
            for key in d:
                if section in d[key]:
                    return typ,key
        return 'data',section

    def is_object(self,instruction_type_name,module_config):
        return instruction_type_name[0] in ('object')
        
    def is_action(self,instruction_type_name,module_config):
        return (instruction_type_name[0] in ('action')
                or instruction_type_name[2] 
                    in self.obj_walk.to_value(module_config, ['instruction', 'keywords', 'action']))
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
        

########################
## Application Objects 
########################
exec('from applications.%s.modules import request_handler' % this_app)
app_objects=Struct(**{'details':app_details, 'config':app_config, 'log_wrapped':log_wrapped, 
                      'utilities':utilities, 'a_convert' : a_convert, 'tentative_app':tentative_app, 
                      'http_referer':http_referer, 'RequestHandler' : request_handler.RequestHandler, 
                      'app_modules_config' : app_modules_config, 
                      'global_site_url' : global_site_url, 'path_info' : path_info, 'full_url' : full_url})


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
