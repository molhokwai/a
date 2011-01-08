# coding: utf8

#########################################################################
## APPLICATION DETAILS, COMMON'Z & UTILITIES
#########################################################################

class AppDetails():
    title = T("molhokwai.net - 'a' cm/dms"), 
    keywords = T("blog, weblog, journal, web, log, web2py, pypress, cms, dms, simple, lightweight, straight-forward, direct, programming, programmer"),
    description = T("molhokwai.net - 'a' cm/dms, lightweight, simple, straight & direct")
    init_app_config = {
        'pages' : {
            'help' : """
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
            'home' : """
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
                is more than welcome)</p>                
            """
        }
    }
app_details=AppDetails()
if app_config and app_config.APP_METAS:
    app_details.title=app_config.APP_METAS[0]
    app_details.keywords=app_config.APP_METAS[1]
    app_details.description=app_config.APP_METAS[2]

class aConvert():
    def to_int(self, value):
        """Attention: Eventually returns 0 which 'equals' the False ValueError return"""
        try:
            return int(value)
        except ValueError:
            return False
a_convert=aConvert()

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

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
